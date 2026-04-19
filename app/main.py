import logging
import uuid
from pathlib import Path

import streamlit as st

from app.config import get_settings
from app.graph.workflow import invoke as rag_invoke
from app.ingestion.indexer import Indexer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

st.set_page_config(
    page_title="Gen AI Knowledge Base using RAG",
    page_icon="📚",
    layout="wide",
)

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin"


def _get_indexer() -> Indexer:
    if "indexer" not in st.session_state:
        st.session_state.indexer = Indexer()
    return st.session_state.indexer


def _init_session() -> None:
    if "thread_id" not in st.session_state:
        st.session_state.thread_id = str(uuid.uuid4())
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "is_admin" not in st.session_state:
        st.session_state.is_admin = False


def _render_admin_auth() -> bool:
    st.subheader("Access")
    if st.session_state.is_admin:
        st.success("Logged in as admin")
        if st.button("Log out", key="admin_logout"):
            st.session_state.is_admin = False
            st.rerun()
        return True

    with st.form("admin_login_form"):
        username = st.text_input("Username", key="admin_username")
        password = st.text_input("Password", type="password", key="admin_password")
        submitted = st.form_submit_button("Log in")

    if submitted:
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            st.session_state.is_admin = True
            st.success("Admin login successful")
            st.rerun()
        else:
            st.error("Invalid username or password")

    return False


def _render_sidebar() -> None:
    with st.sidebar:
        st.header("📄 Document Manager")

        is_admin = _render_admin_auth()
        st.divider()

        indexer = _get_indexer()
        indexed_files = indexer.get_indexed_files()

        st.subheader(f"Indexed Files ({len(indexed_files)})")
        with st.container(height=260, border=True):
            if indexed_files:
                for doc_status in indexed_files:
                    st.markdown(
                        f"- 📄 {doc_status.file_name} ({doc_status.chunk_count} chunks)"
                    )
            else:
                st.info("No documents indexed yet.")

        st.divider()

        st.subheader("Upload PDF")
        uploaded_file = st.file_uploader(
            "Choose a PDF file",
            type=["pdf"],
            label_visibility="collapsed",
            disabled=not is_admin,
        )

        if not is_admin:
            st.caption("Read-only mode. Log in as admin to edit documents.")

        if st.button(
            "Index Uploaded PDF",
            disabled=(not is_admin or uploaded_file is None),
        ):
            if uploaded_file is not None:
                settings = get_settings()
                save_dir = Path(settings.KNOWLEDGE_BASE_PATH)
                save_dir.mkdir(parents=True, exist_ok=True)
                save_path = save_dir / uploaded_file.name
                save_path.write_bytes(uploaded_file.getvalue())

                with st.spinner(f"Indexing {uploaded_file.name}..."):
                    result = indexer.add_document(save_path)
                if result.status == "indexed":
                    st.success(
                        f"Indexed {result.file_name} ({result.chunk_count} chunks)"
                    )
                else:
                    st.error(f"Error: {result.message}")
                st.rerun()

        st.divider()

        if st.button("🔄 Re-index All Documents", disabled=not is_admin):
            with st.spinner("Re-indexing all documents..."):
                results = indexer.index_documents()
            indexed_count = sum(1 for r in results if r.status == "indexed")
            total_chunks = sum(r.chunk_count for r in results)
            st.success(f"Indexed {indexed_count} files ({total_chunks} chunks)")
            st.rerun()

        selected_file = st.selectbox(
            "Select file to delete",
            options=[doc.file_name for doc in indexed_files],
            index=None,
            placeholder="Choose a document",
            disabled=(not is_admin or not indexed_files),
        )
        if st.button(
            "🗑️ Delete Selected Document",
            disabled=(not is_admin or not selected_file),
        ):
            result = indexer.delete_document(selected_file)
            st.success(f"Deleted {result.chunk_count} chunks")
            st.rerun()

        st.divider()

        st.subheader("Session")
        st.text(f"Thread: {st.session_state.thread_id[:8]}...")
        if st.button("🧹 Clear Conversation"):
            st.session_state.messages = []
            st.session_state.thread_id = str(uuid.uuid4())
            st.rerun()


def _render_chat() -> None:
    st.title("📚 Gen AI Knowledge Base Assistant")
    st.caption("Ask questions from your indexed documents.")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("sources"):
                with st.expander("📄 Sources"):
                    for src in msg["sources"]:
                        st.markdown(
                            f"- **{src.source_file}** — Page {src.page_number}"
                        )

    if prompt := st.chat_input("Ask a question about your knowledge base..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = rag_invoke(prompt, st.session_state.thread_id)
                    st.markdown(response.answer)
                    if response.sources:
                        with st.expander("📄 Sources"):
                            for src in response.sources:
                                st.markdown(
                                    f"- **{src.source_file}** — Page {src.page_number}"
                                )
                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": response.answer,
                            "sources": response.sources,
                        }
                    )
                except ValueError as e:
                    st.error(str(e))
                except Exception:
                    st.error(
                        "An unexpected error occurred. Please try again."
                    )


def main() -> None:
    _init_session()
    _render_sidebar()
    _render_chat()


if __name__ == "__main__":
    main()
else:
    # Streamlit runs the module directly
    _init_session()
    _render_sidebar()
    _render_chat()
