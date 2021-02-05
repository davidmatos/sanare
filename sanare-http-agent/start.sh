service rsyslog restart
python /app/logger.py &
nginx -g 'daemon off;'