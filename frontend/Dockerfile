# Stage 1: Build the React application
FROM node:20-alpine AS build

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json to install dependencies
COPY . .

# Install project dependencies
RUN npm install

# Build the React application for production
RUN npm run build

# Expose the port
EXPOSE 3000

# Run the app
CMD ["npm", "start"]