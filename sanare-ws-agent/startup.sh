iptables -t nat -A POSTROUTING -o ens160 -j MASQUERADE

apt install iptables-persistent

iptables-save > /etc/iptables/rules.v4

echo "/sbin/iptables-restore < /etc/iptables/rules.v4" >> /etc/rc.local

