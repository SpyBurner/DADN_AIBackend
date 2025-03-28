from flask import Blueprint, jsonify, request
from services.ai_service import AIService  # Import AI service

ai_blueprint = Blueprint("ai", __name__)
ai_service = AIService()  # Initialize AI service

@ai_blueprint.route("/save/<int:shopID>/<int:employeeID>", methods=["POST"])
def save(shopID, employeeID):
    # print(f"Received request to save image for shopId: {shopID}, employeeID: {employeeID}")
    if len(request.files) == 0:
        return jsonify({"error": "Image file is required"}), 400
    
    image_file = request.files["image"]
    
    try:
        # Can return error or success
        result = ai_service.save(shopID, employeeID, image_file)
        # else:
        #     result = ai_service.saveBatch(shopId, employeeID, images)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Server-side error! Please check AI Backend console."}), 500
        
    return jsonify({"message": "Image saved successfully"}), 200

@ai_blueprint.route("/find/<int:shopID>", methods=["POST"])
def find(shopID):
    if len(request.files) == 0:
        return jsonify({"error": "Image file is required"}), 400
    
    image = request.files["image"]
    
    try:
        # Can return error or success
        result = ai_service.find(shopID, image)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Server-side error! Please check AI Backend console."}), 500
        
    return result
