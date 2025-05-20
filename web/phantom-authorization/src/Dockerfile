# Use Ubuntu 22.04 as base image
FROM ubuntu:22.04

# Set working directory
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y curl

RUN curl -sL https://deb.nodesource.com/setup_18.x -o /tmp/nodesource_setup.sh
RUN bash /tmp/nodesource_setup.sh
RUN apt update
RUN apt install nodejs -y

# Copy package files separately for caching
COPY package*.json ./

# Install node modules
ENV NODE_ENV=development
RUN npm install

# Copy remaining project files
COPY . .

# Expose port used by Next.js dev server
EXPOSE 3000

# Start the dev server
CMD ["npm", "run", "dev"]
