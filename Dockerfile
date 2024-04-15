# Use the latest Node.js image from AWS
FROM node:16-alpine as build

# Set the working directory to /app
WORKDIR /app

# Copy the package.json and package-lock.json files to the container
COPY package*.json ./

# Install the dependencies
RUN npm install

# Copy the rest of the application code to the container
COPY . .

# Set the environment variable for React app
ENV NODE_ENV=production

# Use the production build of the React app
RUN npm run build

# Expose the port that the app will listen on
EXPOSE 3000

# Define the command to run when the container starts
CMD ["npm", "start"]