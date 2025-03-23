import os
from dotenv import load_dotenv

load_dotenv()

TOKEN_TG = os.getenv("TOKEN_TG")
API_KEY = os.getenv("API_KEY")
TOKEN_OPENAI = os.getenv("TOKEN_OPENAI")