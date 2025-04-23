# Use the official Python image as the base image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the Python script and other necessary files to the container
COPY train_model.py .
COPY data/ data/

# Install the required Python packages
RUN pip install --no-cache-dir pandas numpy scikit-learn pickle5

# Run the Python script
CMD ["python", "train_model.py"] 