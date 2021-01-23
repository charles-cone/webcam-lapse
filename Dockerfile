FROM python:3.8-slim

WORKDIR /interface
RUN apt-get update && apt-get install -y fswebcam

COPY . .

EXPOSE 8000
CMD ["python", "./main.py"]