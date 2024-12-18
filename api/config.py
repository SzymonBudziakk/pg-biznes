import os
import base64

from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

API_URL = "http://localhost:8080/api"
HEADERS = {
    'Authorization': f'Basic {base64.b64encode(f"{API_KEY}:".encode()).decode()}'
}