from typing import Dict, List, Optional
from pydantic import BaseModel, SecretStr


class TgIdConfig(BaseModel):
    bot: Optional[int]
    admin: Optional[int]
    dev: Optional[int]
    contractor: Optional[int]


class TgUsernameConfig(BaseModel):
    bot: Optional[str]


class SmtpConfig(BaseModel):
    url: str
    port: int


class EmailConfig(BaseModel):
    admin: Optional[str]
    dev: Optional[str]
    contractor: Optional[str]
    smtp: Optional[SmtpConfig]


class ContactInfo(BaseModel):
    tg_id: Optional[TgIdConfig]
    tg_username: Optional[TgUsernameConfig]
    email: Optional[EmailConfig]


class DockerConfig(BaseModel):
    port: int


class SecretConfig(BaseModel):
    api_openai: SecretStr
    token_telegram: SecretStr
    token_payment_provider: SecretStr
    password_smtp: SecretStr


class CoreConfig(BaseModel):
    contact: ContactInfo
    media: str
    persistence: str
    logs: str
    docker: Optional[DockerConfig]
    secret: SecretConfig


class DatabaseSecretConfig(BaseModel):
    password: SecretStr


class DatabaseConfig(BaseModel):
    host: str
    dbname: str
    user: str
    port: int
    secret: Optional[DatabaseSecretConfig]


class ModuleConfig(BaseModel):
    poolingStrategy: str
    vectorizeClassName: bool


class PropertiesConfig(BaseModel):
    name: str
    dataType: List[str]


class ClassConfig(BaseModel):
    class_name: str
    description: str
    properties: List[PropertiesConfig]
    vectorizer: str
    moduleConfig: Dict[str, ModuleConfig]


class VectorDatabaseConfig(BaseModel):
    api_url: str
    sentence_transformer: str
    semantic_threshold: float
    query_limit: int
    classes: Dict[str, ClassConfig]
    filters: Dict[str, List[str]]


class AppConfig(BaseModel):
    deployment: str
    core: CoreConfig
    database: DatabaseConfig
    vector_database: VectorDatabaseConfig
    wiki: Dict[str, Dict]
