from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class Marketplace(str, Enum):
    AMAZON = "amazon"
    WALMART = "walmart"
    COSTCO = "costco"
    TARGET = "target"


class ItemStatus(str, Enum):
    RECOMMENDED = "recommended"
    SELECTED = "selected"
    REJECTED = "rejected"
    ADDED_TO_PLATFORM = "added_to_platform"
    PURGE_PENDING = "purge_pending"


class ProductCandidate(BaseModel):
    platform: Marketplace
    title: str
    url: str
    item_price: float
    shipping_cost: float = 0.0
    total_cost: float = 0.0
    description: str = ""
    source_query: str = ""
    list_date: datetime = Field(default_factory=datetime.utcnow)
    platform_added_date: datetime | None = None
    score: float = 0.0
    notes: str = ""
    price_verified: bool = False


class RecommendationRequest(BaseModel):
    query: str = Field(min_length=3, max_length=1000)
    session_id: str


class RecommendationResponse(BaseModel):
    query: str
    recommendations: list[ProductCandidate] = Field(default_factory=list)
    message: str = ""


class CartAction(BaseModel):
    item_ids: list[int] = Field(default_factory=list)
    session_id: str


class PurgeRequest(BaseModel):
    session_id: str
    cutoff_days: int = 60
    confirm: bool = False


class PurgeResult(BaseModel):
    pending_confirmation: bool = False
    deleted_count: int = 0
    message: str = ""


class LoginConfig(BaseModel):
    platform: Marketplace
    username: str = ""
    password: str = ""
