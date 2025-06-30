# Use lightweight Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy all files to the container
COPY . /app

# Install dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install gdown

# Create directory and download model from Google Drive
RUN mkdir -p best_model_bert && \
    gdown --id 15Fizi_XWWUjmsjgLSDyHuMbNw8nQPvGw -O best_model_bert/model.safetensors

# Expose port required by Hugging Face Spaces
EXPOSE 7860

# Start FastAPI app with Uvicorn on correct port
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
