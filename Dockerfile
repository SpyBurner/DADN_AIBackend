FROM python:3.12.9-slim

WORKDIR /AIBackend

COPY ./requirements.txt ./ 
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src ./src
COPY ./.env ./.env

# Set Flask environment variables
ENV FLASK_APP=src/app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8000

# Expose the port
EXPOSE 8000

# Run the application
CMD ["flask", "run", "--debug"]
