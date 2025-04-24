# Use the official Python image as the base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Download necessary NLTK data
RUN python -m nltk.downloader punkt

# Copy the entire project directory
COPY . .

# Expose the port the app runs on
EXPOSE 3000

# Run the application
CMD ["python", "chatpdf1.py"] 