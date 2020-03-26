# Use the official image as a parent image
FROM python:3.7-buster

# Set the working directory
WORKDIR /usr/src/

# Copy the requirements from your host to your current location
COPY requirements.txt .

# Install requirements
RUN pip3 install -r requirements.txt --no-build-isolation 

# Inform Docker that the container is listening on the specified port at runtime.
EXPOSE 8000

# Run the specified command within the container.
CMD [ "python3", "manage.py", "runserver" ]

# Copy the rest of your app's source code from your host to your image filesystem.
COPY . .

RUN python3 manage.py makemigrations
RUN python3 manage.py migrate