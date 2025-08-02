from pydantic import BaseSettings

class Settings(BaseSettings):
    # Настройки приложения
    app_env: str = "development"
    app_secret_key: str = "secret-key"
    app_debug: bool = True
    
    # Настройки БД
    postgres_server: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_db: str = "url_shortener"
    
    # Настройки Redis
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    
    # Rate limiting
    rate_limit: int = 1000
    rate_limit_period: int = 60
    
    # GeoIP
    geoip_path: str = "GeoLite2-City.mmdb"
    
    class Config:
        env_prefix = ""
        case_sensitive = False

settings = Settings()
