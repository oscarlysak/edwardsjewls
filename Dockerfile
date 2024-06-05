# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create a non-root user and switch to it
RUN adduser --disabled-password --gecos '' django
RUN chown -R django /usr/src/app

# Copy and grant executable permissions to the Postgres wait script
COPY wait-for-postgres.py ./
RUN chmod +x wait-for-postgres.py


USER django

# Run the Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
