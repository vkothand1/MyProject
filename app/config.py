from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    OPENAI_API_KEY: str

    KNOWLEDGE_BASE_PATH: str = str(
        Path("/Users/vinothkumarkothandapani/Downloads/AI-RAG-DOCS")
    )
    CHROMA_DB_PATH: str = "./chroma_db"
    MANIFEST_PATH: str = "./vector_index_manifest.json"

    EMBEDDING_MODEL: str = "text-embedding-3-small"
    LLM_MODEL: str = "gpt-4o-mini"
    LLM_TEMPERATURE: float = 0.0

    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200

    TOP_K_RETRIEVAL: int = 10
    TOP_K_RERANK: int = 5
    RELEVANCE_THRESHOLD: float = 0.3

    CHROMA_COLLECTION_NAME: str = "rag_knowledge_base"


def get_settings() -> Settings:
    return Settings()
