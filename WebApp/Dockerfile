FROM ubuntu:18.04
COPY . /app
WORKDIR /app

RUN /bin/bash -c 'echo Y | apt-get update'
RUN /bin/bash -c 'echo Y | apt-get install python3'
RUN /bin/bash -c 'echo Y | apt-get install python3-pip'
RUN /bin/bash -c 'pip3 install -r requirements.txt'
EXPOSE 5000
CMD python3 ./flask_app.py
