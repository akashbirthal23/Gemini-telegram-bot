# Select a lean Python base image
FROM python:3.11

# Working directory for your application
WORKDIR /app

# Copy your requirements file
COPY requirements.txt ./

# Install dependencies
RUN pip install -r requirements.txt

# Copy your bot script 
COPY app.py ./
COPY gemini.py ./
COPY resp.py ./

# Define the command to run your bot
CMD [ "python", "app.py" ]  
