# Use an official Python runtime as the base image
FROM python:3.11.4

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /code

# install dependencies
RUN pip install --upgrade pip
COPY peer_mentoring/requirements.txt /code/
RUN pip install -r requirements.txt


# copy project
COPY . /code/
