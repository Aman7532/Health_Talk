FROM node:16-alpine

WORKDIR /app

# Copy the package.json file or create default one if it doesn't exist
COPY package.json* ./
RUN if [ ! -f package.json ]; then \
    echo "Creating default package.json"; \
    echo '{ \
      "name": "healthcare-chatbot-frontend", \
      "version": "1.0.0", \
      "description": "Frontend for Healthcare Chatbot", \
      "main": "index.js", \
      "scripts": { \
        "start": "serve -s public -l 3000" \
      }, \
      "dependencies": { \
        "serve": "^14.0.0" \
      } \
    }' > package.json; \
    fi

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Make sure public directory exists
RUN mkdir -p public

# Expose the port on which the application will run
EXPOSE 3000

# Start the application
CMD ["npm", "start"] 