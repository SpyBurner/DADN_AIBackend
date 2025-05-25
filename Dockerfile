FROM python:3.12.9-slim

WORKDIR /AIBackend

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

COPY ./requirements.txt ./ 
RUN --mount=type=cache,target=/root/.cache/pip pip install --no-cache-dir -r requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip pip install tensorflow[and-cuda]

COPY ./src ./
COPY ./.env ./
COPY ./vgg_face_weights.h5 /root/.deepface/weights/vgg_face_weights.h5

# Set Flask environment variables
ENV FLASK_APP=src/app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8000

# Expose the port
EXPOSE 8000

# Run the application
# CMD ["flask", "run", "--debug"]
