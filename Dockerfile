FROM python:3.8-slim

WORKDIR /interface
RUN apt-get update && apt-get install -y fswebcam

COPY . .

# Don't try to install on desktops
RUN if [ uname -m != "x86_64" ]; then pip install RPi.GPIO; fi
RUN mkdir data && data/lapses
EXPOSE 80
CMD ["python", "./main.py"]