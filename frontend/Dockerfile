# Use official Node image
FROM node:20-alpine

WORKDIR /app

# Copy package files first for better caching
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application
COPY . .

# Add type: module to package.json to fix the warning
RUN npm pkg set type="module"

EXPOSE 3000

# Start the development server
CMD ["npm", "run", "dev"]