# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the FastAPI application files to the container
COPY main.py ./

# Copy the static files to the container
COPY static ./static

# Create a non-root user and switch to it
RUN useradd -m sweet
RUN mkdir -p /home/sweet && echo "Trojan{HasHt@g-PokE-lit3raly-l0caVore-b3ard-m@rF@-kog1-bruH-ar7isan-suCCulenTs}" > /home/sweet/home.txt && chown -R sweet:sweet /home/sweet

# Install FastAPI and Uvicorn
RUN pip install fastapi uvicorn jinja2

# Change ownership of the working directory
RUN chown -R sweet:sweet /app

# Switch to the non-root user
USER sweet

# Expose the port FastAPI will run on
EXPOSE 8000

# Command to run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
