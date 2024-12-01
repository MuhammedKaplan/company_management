# Base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app/

# Expose the application port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "company_management.asgi:application", "--host", "0.0.0.0", "--port", "8000"]