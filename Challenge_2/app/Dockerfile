## Use the official Python image from the Docker Hub


FROM python:3.11-slim
WORKDIR /app
#COPY requirements.txt ./
#RUN pip install --no-cache-dir -r requirements.txt
RUN pip install flask
RUN pip install pandas
RUN pip install numpy
RUN pip install Pillow
RUN pip install db-sqlite3
RUN pip install matplotlib
RUN apt-get update && apt-get install -y libgl1-mesa-glx
RUN apt-get update && apt-get install -y libglib2.0-0

#EXPOSE 5000  ##
COPY . /app
ENV FLASK_APP=app.py
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
