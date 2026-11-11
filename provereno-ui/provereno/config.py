from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    database_url: str
    github_client_id: str = ""
    github_client_secret: str = ""
    session_secret_key: str = Field(min_length=32)
    allowed_github_orgs: str = ""
    allowed_github_logins: str = ""
    data_dir: str = "./data"

settings = Settings()
