from flask import Flask
from controllers.ai_controller import ai_blueprint
from services.ai_service import AIService  # Import AI service

# LOAD ENVIRONMENT VARIABLES
from dotenv import load_dotenv
import os

load_dotenv()
PINECONE_KEY = os.getenv("PINECONE_KEY")
INDEX_HOST = os.getenv("INDEX_HOST")
DECTECTOR_BACKEND = os.getenv("DECTECTOR_BACKEND")

pc = Pinecone(api_key=PINECONE_KEY)
index = pc.Index(host=INDEX_HOST)
# ######

app = Flask(__name__)
ai_service = AIService()  # Initialize AI service ahead of time

app.register_blueprint(ai_blueprint, url_prefix="/ai")

if __name__ == "__main__":
    app.run(debug=True)