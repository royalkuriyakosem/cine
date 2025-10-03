# Use official Node image
FROM node:20-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Install vite in the project (not globally)
RUN npm install vite @vitejs/plugin-react

# Copy the rest of the application
COPY . .

EXPOSE 3000

# Start the development server
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]