# Use the official Python image from Docker Hub
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Copy requirements.txt to the container
COPY requirements.txt /app/

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Expose the port your Django app runs on
EXPOSE 8000

# Run the Django development server
CMD ["python", "manage.py", "runserver", "127.0.0.1:8000"]
