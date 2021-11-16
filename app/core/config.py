import os
from os.path import join, dirname
from dotenv import load_dotenv, find_dotenv

class Settings:
    PROJECT_NAME:str = "Fast API"
    PROJECT_VERSION: str = "1.0.0"

    POSTGRES_USER : str = 'practicasiei'
    POSTGRES_PASSWORD = 'practicasiei'
    POSTGRES_HOST : str = 'db'
    POSTGRES_PORT : str = 5432 
    POSTGRES_DB : str = 'practicasiei'
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

print(os.getenv('POSTGRES_HOST'))
settings = Settings()