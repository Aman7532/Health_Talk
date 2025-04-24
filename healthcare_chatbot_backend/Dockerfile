# Use the official Python image as the base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file or create one if it doesn't exist
COPY requirements.txt* ./
RUN if [ -f requirements.txt ]; then \
    pip install --no-cache-dir numpy==1.24.2 && \
    pip install --no-cache-dir -r requirements.txt; \
    else \
    echo "Creating default requirements.txt"; \
    echo "flask==2.2.3\nnumpy==1.24.2\npandas==1.5.3\nscikit-learn==1.2.2\npython-dotenv==1.0.0\nPyPDF2==3.0.1\nlangchain_text_splitters==0.0.1\nlangchain_google_genai==0.0.2\ngoogle-generativeai==0.3.1\nlangchain_community==0.0.7\nlangchain_core==0.0.12\nlangchain==0.0.276\nfaiss-cpu==1.7.4\nflask-cors==4.0.0\nnltk==3.8.1\ntorch==2.1.0" > requirements.txt && \
    pip install --no-cache-dir numpy==1.24.2 && \
    pip install --no-cache-dir -r requirements.txt; \
    fi

# Download necessary NLTK data
RUN python -m nltk.downloader punkt

# Copy the entire project directory
COPY . .

# Expose the port the app runs on
EXPOSE 3000

# Run the application
CMD ["python", "chatpdf1.py"] 