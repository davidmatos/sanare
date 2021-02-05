#docker build -t sanare-manager:latest .
#docker run -it -p 3000:3000 sanare-manager
FROM ubuntu:18.04

MAINTAINER David R. Matos "david.r.matos@tecnico.ulisboa.pt"

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

RUN cd /usr/local/bin && \
    ln -s /usr/bin/python3 python
    
RUN pip3 install --upgrade pip
# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]