# Use an official Python runtime as a base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Add your application's requirements.txt and install dependencies
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt && pip install "psycopg[binary]"

# Add the rest of your application's source code
COPY . /app

# Make port 80 available to the world outside this container
EXPOSE 80

# Run your application when the container launches
CMD ["python", "-m", "script.main"]