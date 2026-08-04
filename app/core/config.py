from dotenv import load_dotenv
import os

load_dotenv()


APP_NAME = os.getenv(
    "Application Name",
    "AI Knowledge Platform"
)