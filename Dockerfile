# Use lightweight Python image instead of CUDA-heavy PyTorch image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy app files into container
COPY . /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Expose port for FastAPI
EXPOSE 8000

# Install dependencies for downloading from Google Drive
RUN apt-get update && apt-get install -y wget unzip

# Download model.safetensors from Google Drive
RUN wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=15Fizi_XWWUjmsjgLSDyHuMbNw8nQPvGw' -O best_model_bert/model.safetensors

# Run FastAPI app with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
