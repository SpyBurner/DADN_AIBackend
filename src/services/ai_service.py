from pinecone import Pinecone
from deepface import DeepFace
import cv2
import numpy as np

# LOAD ENVIRONMENT VARIABLES
from dotenv import load_dotenv
import os

load_dotenv()
PINECONE_KEY = os.getenv("PINECONE_KEY")
INDEX_HOST = os.getenv("INDEX_HOST")

pc = Pinecone(api_key=PINECONE_KEY)
index = pc.Index(host=INDEX_HOST)

# from pillow import Image

pc = Pinecone(api_key=PINECONE_KEY)
index = pc.Index(host=INDEX_HOST)
detector_backend = 'ssd'

class AIService:
    def __init__(self):
        print("Initializing AI Service...")

    def save(self, namespace, id, image_file):
        try:
            # Read the image file as a NumPy array
            file_bytes = np.frombuffer(image_file.read(), np.uint8)
            image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)  # Convert to OpenCV format

            if image is None:
                raise ValueError("Invalid image data")
            
            embedding = DeepFace.represent(img_path=image, detector_backend=detector_backend)
            
            if (len(embedding) == 0):
                raise Exception("No embedding found for image")
            
            embedding_vector = embedding[0]['embedding']
            
            # print(f"Embedding vector: {embedding_vector}")
            
            vectors = [
                {
                    "id": str(id),
                    "values": embedding_vector,
                }
            ]
            
            try:
                index.upsert(namespace=str(namespace), vectors=vectors)
            except Exception as e:
                raise Exception(f"Error saving to Pinecone: {e}")
        except Exception as e:
            raise RuntimeError(str(e))  # Let the controller handle errors
    
        # Save multiple images
        # For later use, if needed
    # def saveBatch(self, namespace, ids, image_files):
    #     pass
    #     try:
    #         multi_file_bytes = [np.frombuffer(image_file.read(), np.uint8) for image_file in image_files]
            
    #         images = [cv2.imdecode(file_bytes, cv2.IMREAD_COLOR) for file_bytes in multi_file_bytes]
        
    #         embeddings = [DeepFace.represent(img_path=image, detector_backend=detector_backend) for image in images]
            
    #         if (len(embedding) == 0):
    #             raise Exception("No embedding found for image")
            
    #         vectors = [embedding[0]['embedding'] for embedding in embeddings]
            
            
            
    #     except Exception as e:
    #         raise RuntimeError(str(e))
        
    
    def find(self, namespace, image_file):
        
        file_bytes = np.frombuffer(image_file.read(), np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        
        if image is None:
            raise ValueError("Invalid image data")
        
        embedding = DeepFace.represent(img_path=image, detector_backend=detector_backend)
        
        embedding_vector = embedding[0]['embedding']
        
        response = index.query(
            namespace=str(namespace),
            vector=embedding_vector,
            top_k=1,
            include_values=True,
            include_id=True,
        )
        
        import pickle
        pickle.dump(response, open("response.pickle", "wb"))
        
        if (response['matches'] == []):
            return {"error": "No match found"}, 404
        
        result = response['matches'][0]
        
        return {
            "employeeID": result['id'],
        }, 200
        