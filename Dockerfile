#Use the official Python image
FROM python:3.10-slim

#Set the working directory
WORKDIR /app

#Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#Copy the rest of the application code
COPY . .

#Expose the port Flask runs on
EXPOSE 5000

#Set the command to run the Flask app
CMD ["python", "dotawebapp.py"]
