"""_summary_

Returns:
    _type_: _description_
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """_summary_

    Args:
        BaseSettings (_type_): _description_
    """

    API_PREFIX: str = ""
    DOCS_URL: str = ""

    OPENAPI_URL: str = ""
    ORIGINS: str = "5.34.200.221,37.114.196.41,37.114.196.42,37.114.196.43,37.114.196.45,37.114.196.46,37.114.196.47,37.114.196.48,46.209.118.50,46.209.118.51,46.209.118.52,46.209.118.53,46.209.118.54,46.209.118.55"  # "*"
    ROOT_PATH: str = ""
    SWAGGER_TITLE: str = "Insertions"
    VERSION: str = "0.0.1"

    APPLICATION_ID: str = "d7f48c21-2a19-4bdb-ace8-48928bff0eb5"
    # GRPC_IP: str = "37.32.8.187"
    # GRPC_PORT: int = 9035
    SPLUNK_HOST: str = "37.32.8.187"
    SPLUNK_PORT: int = 5141
    SPLUNK_INDEX: str = "dev"

    DATE_STRING: str = "%Y-%m-%d"
    FASTAPI_DOCS: str = "/docs"
    FASTAPI_REDOC: str = "/redoc"
    MONGO_CONNECTION_STRING: str = "mongodb://37.32.8.187:8081/"
    MONGO_DATABASE: str = "Test"
    FAQ_COLLECTION: str = "FAQ"
    FORBIDDEN_WORDS_COLLECTION: str = "ForbiddenWords"
    SENSITIVE_WORDS_COLLECTION: str = "SensitiveWords"
    PROFESSIONAL_WORDS_COLLECTION: str = "ProfessionalWords"
    TAGS_COLLECTION: str = "Tags"

    TOKEN_URL: str = "/token"
    CLIENT_ID: str = "M2M.RegisterServicePermission"
    CLIENT_SECRET: str = "IDPRegisterServicePermission"
    GRANT_TYPE: str = "client_credentials"
    OPENID_CONFIGURATION_URL: str = (
        "/.well-known/openid-configuration"
    )
    REGISTRATION_URL: str = (
        "/api/service-permossion/register-service-permission"
    )


settings = Settings()
