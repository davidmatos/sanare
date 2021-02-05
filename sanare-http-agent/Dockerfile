#docker build -t sanare-http-agent:latest .
#docker run -it -p 8081:80 --network sanare-py_sanare sanare-http-agent
FROM ubuntu:18.04

MAINTAINER David R. Matos "david.r.matos@tecnico.ulisboa.pt"

RUN apt update -y
RUN apt install -y nginx
RUN apt install -y iputils-ping
RUN apt install -y curl
RUN apt install -y python3-pip python3-dev

RUN cd /usr/local/bin && \
    ln -s /usr/bin/python3 python

RUN pip3 install --upgrade pip


COPY . /app
RUN cd app && pip install -r requirements.txt

RUN apt install rsyslog -y

#RUN  echo "no" | apt install -y rsyslog-pgsql



RUN unlink /etc/nginx/sites-enabled/default

#copy configuration
COPY nginx.conf /etc/nginx/nginx.conf


COPY 51-mywebsite.conf /etc/rsyslog.d/51-mywebsite.conf

COPY start.sh start.sh

#RUN ln -s /etc/nginx/nginx.conf /etc/nginx/sites-enabled/reverse-proxy.conf

#RUN nginx -t

#RUN /etc/init.d/nginx restart

#CMD ["nginx", "-g", "daemon off;"]
#CMD ["service", "rsyslog", "restart"]

CMD ["sh", "./start.sh"]
