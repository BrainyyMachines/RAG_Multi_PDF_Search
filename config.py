import os
from dotenv import load_dotenv
load_dotenv()

EURI_API_KEY = os.getenv("EURI_API_KEY")
EURI_CHAT_URL="https://api.euron.one/api/v1/euri/alpha/chat/completions"
EURI_EMBED_URL="https://api.euron.one/api/v1/euri/alpha/embeddings"