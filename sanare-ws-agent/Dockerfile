#docker build -t sanare-ws-agent:latest .
#docker run --cap-add=NET_ADMIN --cap-add=NET_RAW -it  sanare-ws-agent


FROM ubuntu:18.04
USER root


RUN apt update

RUN apt install -y isc-dhcp-server

RUN apt install -y iptables 

COPY interfaces /etc/network/interfaces

#RUN systemctl restart networking

RUN echo 'INTERFACES="ens192"' >> /etc/default/isc-dhcp-server

COPY dhcpd.conf /etc/dhcp/dhcpd.conf

#RUN service isc-dhcp-server restart

RUN echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf

#RUN iptables -t nat -A POSTROUTING -o ens160 -j MASQUERADE

#RUN apt install iptables-persistent

#RUN iptables-save > /etc/iptables/rules.v4

#RUN echo "/sbin/iptables-restore < /etc/iptables/rules.v4" >> /etc/rc.local



