# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code into the container
COPY . .

# Expose the port that the app runs on
EXPOSE 8585

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8585", "--log-level", "info"]
