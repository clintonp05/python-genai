import os
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings,SettingsConfigDict
from typing import List, Optional

class CommonConfig(BaseSettings):
    chunk_strategy: str = Field("fixed", env="CHUNK_STRATEGY")
    embedding_batch_size: int = Field(512, env="EMBEDDING_BATCH_SIZE", gt=0)

    @field_validator('chunk_strategy')
    def validate_chunk_strategy(cls, v):
        if v not in {"fixed", "recursive", "context"}:
            raise ValueError("Invalid chunk strategy")
        return v

def get_env_var(key: str) -> str:
    """
    Get the value of an environment variable.

    Args:
    key (str): The name of the environment variable.

    Returns:
    str: The value of the environment variable.
    """
    return Field(env=key) or os.getenv(key)

class HttpConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_prefix='HTTP_',extra="ignore")
    timeout: str = Field(env="TIMEOUT")
    retry_count: str = Field(env="RETRY_COUNT")
    retry_max: str = Field(env="RETTRY_MAX")
    retry_backoff: str = Field(env="RETRY_BACKOFF")
class AzureOpenAIConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_prefix='AZURE_OPENAI_',extra="ignore")
    endpoint: str = Field(env="ENDPOINT")
    api_key: str = Field(env="API_KEY")
    api_version: str = Field(env="API_VERSION")
    model: str = Field(env="MODEL")

class AzureAISearchConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_prefix='AZURE_AI_SEARCH_',extra="ignore")
    endpoint: str = Field(env="ENDPOINT")
    api_key: str = Field(env="API_KEY")
    index_name: str = Field(env="INDEX_NAME")
    api_version: str = Field(env="API_VERSION")

class ChatbotConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_prefix='CHATBOT_',extra="ignore")
    type : str = Field(env="TYPE")
    temperature: float = Field(0.7, env="TEMPERATURE")
    prompt_template : str = Field(env="PROMPT_TEMPLATE")

class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8',extra="ignore")
    common: CommonConfig = CommonConfig()
    openai: AzureOpenAIConfig = AzureOpenAIConfig()
    ai_search: AzureAISearchConfig = AzureAISearchConfig()
    chatbot: ChatbotConfig = ChatbotConfig()
    http: HttpConfig = HttpConfig()