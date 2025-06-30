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

# Run FastAPI app with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
