import os
from dotenv import load_dotenv
load_dotenv()

PORT = int(os.environ.get('PORT'))
GROQ_API_KEY = str(os.environ.get('GROQ_API_KEY'))
GROQ_CHAT_MODEL = str(os.environ.get('GROQ_CHAT_MODEL'))
DJANGO_SECRET_KEY = str(os.environ.get('DJANGO_SECRET_KEY'))
