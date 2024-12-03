## Use the official Python image from the Docker Hub
#FROM python:3.11-slim
#
## Set the working directory
#WORKDIR /app
#
## Copy the requirements file into the container
#COPY requirements.txt ./
#
## Install the required packages
#RUN pip install --no-cache-dir -r requirements.txt
#
## Copy the rest of the application code into the container
#COPY . .
#
## Expose the port the app runs on
#EXPOSE 5000
#
## Command to run the application
#CMD ["python3", "app.py"]

FROM python:3.11-slim
WORKDIR /app
#COPY requirements.txt ./
#RUN pip install --no-cache-dir -r requirements.txt
RUN pip install flask
RUN pip install opencv-python
RUN pip install numpy
RUN pip install Pillow
RUN pip install db-sqlite3
RUN apt-get update && apt-get install -y libgl1-mesa-glx
RUN apt-get update && apt-get install -y libglib2.0-0

#EXPOSE 5000  ##
COPY . /app
ENV FLASK_APP=app.py
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
