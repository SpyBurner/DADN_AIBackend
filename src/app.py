from flask import Flask
from controllers.ai_controller import ai_blueprint
from services.ai_service import AIService  # Import AI service

# ######

app = Flask(__name__)
ai_service = AIService()  # Initialize AI service ahead of time

app.register_blueprint(ai_blueprint, url_prefix="/ai")

if __name__ == "__main__":
    app.run(debug=True)