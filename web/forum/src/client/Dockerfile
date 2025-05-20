FROM node:18

# Set the working directory inside the container (matches working_dir in compose)
# or /client or /server depending on where used
WORKDIR /client  

# Copy package files and install dependencies
COPY package*.json ./
RUN npm ci --omit=dev

# Copy rest of the app
COPY . .

USER node
ENV NODE_ENV=production

# Expose the port (not strictly needed but good practice)
EXPOSE 3000

# Start the application
CMD ["npm", "start"] 
# note: this isn't a production build, but it's better than nothing
