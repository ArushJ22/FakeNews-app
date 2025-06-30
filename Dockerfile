# Use lightweight Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy app files into container
COPY . /app

# Install pip dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Install gdown for downloading large Google Drive files
RUN pip install gdown

# Create directory for model
RUN mkdir -p best_model_bert

# Download model.safetensors from Google Drive using gdown (handles large files properly)
RUN gdown --id 15Fizi_XWWUjmsjgLSDyHuMbNw8nQPvGw -O best_model_bert/model.safetensors

# Expose port for FastAPI
EXPOSE 8000

# Run FastAPI app with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
