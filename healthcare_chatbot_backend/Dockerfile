# Use the official Python image as the base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file or create one if it doesn't exist
COPY requirements.txt* ./

# Install Python packages in stages for better dependency resolution
RUN if [ -f requirements.txt ]; then \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir numpy==1.24.2 && \
    pip install --no-cache-dir pandas==1.5.3 scikit-learn==1.2.2 && \
    pip install --no-cache-dir flask==2.2.3 flask-cors==4.0.0 python-dotenv==1.0.0 && \
    pip install --no-cache-dir PyPDF2==3.0.1 && \
    pip install --no-cache-dir nltk==3.8.1 && \
    pip install --no-cache-dir faiss-cpu==1.7.4 && \
    pip install --no-cache-dir google-generativeai==0.3.1 && \
    pip install --no-cache-dir langchain==0.0.276 langchain_core==0.0.12 && \
    pip install --no-cache-dir langchain_text_splitters==0.0.1 && \
    pip install --no-cache-dir langchain_google_genai==0.0.2 && \
    pip install --no-cache-dir langchain_community==0.0.7 && \
    pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu torch==2.1.0; \
    else \
    echo "Creating default requirements.txt"; \
    echo "flask==2.2.3\nnumpy==1.24.2\npandas==1.5.3\nscikit-learn==1.2.2\npython-dotenv==1.0.0\nPyPDF2==3.0.1\nlangchain_text_splitters==0.0.1\nlangchain_google_genai==0.0.2\ngoogle-generativeai==0.3.1\nlangchain_community==0.0.7\nlangchain_core==0.0.12\nlangchain==0.0.276\nfaiss-cpu==1.7.4\nflask-cors==4.0.0\nnltk==3.8.1\ntorch==2.1.0" > requirements.txt && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir numpy==1.24.2 && \
    pip install --no-cache-dir pandas==1.5.3 scikit-learn==1.2.2 && \
    pip install --no-cache-dir flask==2.2.3 flask-cors==4.0.0 python-dotenv==1.0.0 && \
    pip install --no-cache-dir PyPDF2==3.0.1 && \
    pip install --no-cache-dir nltk==3.8.1 && \
    pip install --no-cache-dir faiss-cpu==1.7.4 && \
    pip install --no-cache-dir google-generativeai==0.3.1 && \
    pip install --no-cache-dir langchain==0.0.276 langchain_core==0.0.12 && \
    pip install --no-cache-dir langchain_text_splitters==0.0.1 && \
    pip install --no-cache-dir langchain_google_genai==0.0.2 && \
    pip install --no-cache-dir langchain_community==0.0.7 && \
    pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu torch==2.1.0; \
    fi

# Download necessary NLTK data
RUN python -m nltk.downloader punkt

# Copy the entire project directory
COPY . .

# Expose the port the app runs on
EXPOSE 3000

# Run the application
CMD ["python", "chatpdf1.py"] 