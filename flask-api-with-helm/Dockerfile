# Pull base image
FROM python:3.11.1

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install pipenv
RUN pip install pipenv

# Copy Pipfile and Pipfile.lock
COPY Pipfile Pipfile.lock /app/

# Install dependencies
RUN pipenv install --system --deploy

# Copy project
COPY app.py /app/

# Run the application
CMD ["python", "app.py"]
