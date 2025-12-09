"""
应用配置管理模块
Configuration Management Module
"""

from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional
import os


class Settings(BaseSettings):
    """应用全局配置"""
    
    # ==================== 应用配置 ====================
    APP_NAME: str = "Academic Paper Assistant"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    
    # ==================== 服务器配置 ====================
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 4
    RELOAD: bool = False
    
    # ==================== LLM配置 ====================
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4-turbo-preview"
    OPENAI_TEMPERATURE: float = 0.3
    ANTHROPIC_API_KEY: Optional[str] = None
    
    # ==================== 数据库配置 ====================
    POSTGRES_URL: str = "postgresql://postgres:password@localhost:5432/academic_db"
    POSTGRES_POOL_SIZE: int = 20
    
    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "password"
    
    # ==================== Redis配置 ====================
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None
    REDIS_TTL: int = 3600  # 1小时缓存
    
    # ==================== 向量数据库配置 ====================
    CHROMA_PERSIST_DIR: str = "./data/vector_db"
    EMBEDDING_MODEL: str = "text-embedding-3-large"
    EMBEDDING_DIMENSION: int = 3072
    
    # ==================== 文件存储配置 ====================
    UPLOAD_DIR: str = "./data/uploads"
    MAX_UPLOAD_SIZE: int = 100 * 1024 * 1024  # 100MB
    ALLOWED_EXTENSIONS: list = ["pdf", "txt"]
    
    # ==================== 外部API配置 ====================
    SEMANTIC_SCHOLAR_API_KEY: Optional[str] = None
    SEMANTIC_SCHOLAR_BASE_URL: str = "https://api.semanticscholar.org/graph/v1"
    
    ARXIV_BASE_URL: str = "http://export.arxiv.org/api/query"
    
    MATHPIX_APP_ID: Optional[str] = None
    MATHPIX_APP_KEY: Optional[str] = None
    
    # ==================== 功能开关 ====================
    ENABLE_REDIS_CACHE: bool = True
    ENABLE_RAG: bool = True
    ENABLE_GRAPH_DB: bool = False  # Neo4j暂不启用
    
    # ==================== 任务队列配置 ====================
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"
    
    # ==================== 日志配置 ====================
    LOG_DIR: str = "./logs"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """获取全局配置实例（单例模式）"""
    return Settings()


# 全局配置实例
settings = get_settings()
