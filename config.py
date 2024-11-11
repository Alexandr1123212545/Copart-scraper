from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    BASE_URL: str
    SALES_LIST: str
    SALES_PAGE: str

    @property
    def db_url_asyncpg(self):
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def db_url_psycopg(self):
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def get_links_site(self):
        return {
            'base_url': self.BASE_URL,
            'sales_list': self.SALES_LIST,
            'sales_page': self.SALES_PAGE
        }

    class Config:
        env_file = ".env"

settings = Settings()