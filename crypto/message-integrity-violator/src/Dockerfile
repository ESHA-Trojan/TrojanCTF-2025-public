# Use an official Python runtime as the base image
FROM python:3.9-slim

RUN apt-get -y update

# Set the working directory in the container
WORKDIR /app

RUN useradd --system runner

RUN pip install waitress
# Copy the requirements file into the container
COPY --chown=runner:runner requirements.txt requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the server code into the container
COPY --chown=runner:runner server.py .

USER runner

# Expose the port the app runs on
EXPOSE 5000

# Command to run the server
CMD ["waitress-serve", "--port", "5000", "--host", "0.0.0.0", "server:app"]