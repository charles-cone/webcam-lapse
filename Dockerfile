FROM python:3.8-slim

WORKDIR /interface
RUN apt-get update && apt-get install -y fswebcam

COPY . .
RUN pip install -r requirements.txt

EXPOSE 80
CMD ["python", "./main.py"]