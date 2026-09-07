from dotenv import load_dotenv
import os

load_dotenv()

APP_NAME = os.getenv("Application Name", "AI Knowledge Platform")
DATABASE_URL = os.getenv("DATABASE_URL")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
EMBEDDING_DIMENSIONS = int(os.getenv("EMBEDDING_DIMENSIONS", 384))

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")
LLM_MODEL = os.getenv("LLM_MODEL", "llama3.2:3b")
CHUNKING_STRATEGY = os.getenv("CHUNKING_STRATEGY", "fixed")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", 60))