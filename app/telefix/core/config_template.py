from typing import Dict, List, Optional
from pydantic import BaseModel, SecretStr


class TgIdConfig(BaseModel):
    bot: int
    admin: int
    dev: int
    contractor: int


class TgUsernameConfig(BaseModel):
    bot: str


class SmtpConfig(BaseModel):
    url: str
    port: int


class EmailConfig(BaseModel):
    admin: str
    dev: str
    contractor: str
    smtp: SmtpConfig


class ContactInfo(BaseModel):
    tg_id: TgIdConfig
    tg_username: TgUsernameConfig
    email: EmailConfig


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
    secret: DatabaseSecretConfig


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
