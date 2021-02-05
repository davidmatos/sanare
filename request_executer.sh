
#!/bin/sh

mysql --host=127.0.0.1 --port=3306 --user=root --password=somewordpress wordpress -e "select *, convert(argument using utf8) from mysql.general_log where event_time > '2020-11-02 17:30:00.0'"