from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    MONGODB_URL: str = os.getenv("MONGODB_URL")
    MONGODB_DATABASE: str = os.getenv("MONGODB_DATABASE")

settings = Settings()