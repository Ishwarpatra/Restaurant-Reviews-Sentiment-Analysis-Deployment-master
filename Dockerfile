# --- Stage 1: Build the React Frontend ---
FROM node:18-alpine as build-stage
WORKDIR /app/client
COPY client/package*.json ./
RUN npm install
COPY client/ ./
RUN npm run build

# --- Stage 2: Setup the Python Backend ---
FROM python:3.9-slim

WORKDIR /app

# Install Python Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Backend Code
COPY . .

# Copy the Built Frontend from Stage 1
# We copy 'client/dist' from the previous stage into 'client/dist' here
COPY --from=build-stage /app/client/dist ./client/dist

EXPOSE 5000

# Command to run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]