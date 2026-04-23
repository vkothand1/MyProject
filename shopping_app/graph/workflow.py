from __future__ import annotations

import logging

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph

from shopping_app.agents.assistant import ShoppingAssistant
from shopping_app.agents.purge_review import PurgeReviewAgent
from shopping_app.agents.recommender import ShoppingRecommender
from shopping_app.db import ShoppingRepository
from shopping_app.emailer import send_recommendation_email
from shopping_app.graph.state import ShoppingState

logger = logging.getLogger(__name__)


class ShoppingGraphService:
    def __init__(self) -> None:
        self.repository = ShoppingRepository()
        self.recommender = ShoppingRecommender(self.repository)
        self.assistant = ShoppingAssistant(self.repository)
        self.purge_agent = PurgeReviewAgent(self.repository)
        self._graph = self._build_graph().compile(checkpointer=MemorySaver())

    def _build_graph(self) -> StateGraph:
        graph = StateGraph(ShoppingState)
        graph.add_node("router", self._router_node)
        graph.add_node("recommend", self._recommend_node)
        graph.add_node("add", self._add_node)
        graph.add_node("purge", self._purge_node)
        graph.set_entry_point("router")
        graph.add_conditional_edges(
            "router",
            self._route,
            {"recommend": "recommend", "add": "add", "purge": "purge", "idle": END},
        )
        graph.add_edge("add", END)
        graph.add_edge("purge", END)
        return graph

    @staticmethod
    def _route(state: ShoppingState) -> str:
        return state.get("action", "recommend")

    @staticmethod
    def _router_node(state: ShoppingState) -> dict:
        return {"message": state.get("message", "")}

    def _recommend_node(self, state: ShoppingState) -> dict:
        query = state.get("query", "")
        session_id = state.get("session_id", "")
        try:
            response = self.recommender.recommend(query=query, session_id=session_id)
            email_sent = send_recommendation_email(response.recommendations)
            message = response.message
            if email_sent:
                message = f"{message} Email notification sent to the configured recipient."
            return {"recommendations": response.recommendations, "message": message}
        except Exception as exc:
            logger.exception("Recommendation flow failed")
            return {"recommendations": [], "message": f"Recommendation failed: {exc}"}

    def _add_node(self, state: ShoppingState) -> dict:
        session_id = state.get("session_id", "")
        try:
            statuses = self.assistant.add_selected_items(session_id)
            message = "Selected items moved to the ecommerce platform carts."
            if not statuses:
                message = "No selected items were found to add to cart."
            return {"statuses": statuses, "message": message}
        except Exception as exc:
            logger.exception("Add-to-cart flow failed")
            return {"statuses": [], "message": f"Add-to-cart failed: {exc}"}

    def _purge_node(self, state: ShoppingState) -> dict:
        cutoff_days = state.get("cutoff_days", 60)
        session_id = state.get("session_id", "")
        confirm = state.get("confirm", False)
        try:
            pending_count = self.purge_agent.preview(session_id, cutoff_days)
            if pending_count and not confirm:
                return {
                    "purge_count": pending_count,
                    "message": (
                        f"There are {pending_count} history records older than {cutoff_days} days. "
                        "Human confirmation is required to purge them."
                    ),
                }
            if pending_count and confirm:
                deleted = self.purge_agent.purge(session_id=session_id, cutoff_days=cutoff_days, confirm=True)
                return {"purge_count": deleted, "message": f"Purged {deleted} old history records."}
            return {"purge_count": 0, "message": "No history records require purging."}
        except Exception as exc:
            logger.exception("Purge flow failed")
            return {"purge_count": 0, "message": f"Purge failed: {exc}"}

    def recommend(self, query: str, session_id: str) -> dict:
        return self._graph.invoke(
            {"action": "recommend", "query": query, "session_id": session_id},
            config={"configurable": {"thread_id": session_id}},
        )

    def add_selected(self, session_id: str) -> dict:
        return self._graph.invoke(
            {"action": "add", "session_id": session_id},
            config={"configurable": {"thread_id": session_id}},
        )

    def add_single_item(self, session_id: str, item_id: int) -> dict:
        """Mark a single item as added-to-platform and move it to history."""
        try:
            self.repository.mark_added_to_platform([item_id])
            return {"message": "Item added to the marketplace cart and moved to Added To Platform."}
        except Exception as exc:
            logger.exception("Add single item failed")
            return {"message": f"Failed to add item: {exc}"}

    def purge_history(self, session_id: str, cutoff_days: int = 60, confirm: bool = False) -> dict:
        return self._graph.invoke(
            {
                "action": "purge",
                "session_id": session_id,
                "cutoff_days": cutoff_days,
                "confirm": confirm,
            }
            ,
            config={"configurable": {"thread_id": session_id}},
        )
