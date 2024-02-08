# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY ./Back_end /usr/src/app

# If you have dependencies listed in a requirements.txt file, uncomment the following line and ensure the file is in the Back_end directory
RUN pip install --no-cache-dir -r requirements.txt

# Run the application
CMD ["python", "movie_routes.py"]
