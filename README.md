# ConfigParser

Check if Python 3.7 is installed

```
hardik@ConfigParser % python -V
Python 3.7.7
```

Sample Config File `config.txt`
```
host = test.com
server_id=55331
server_load_alarm=2.5
user= user
# comment can appear here as well
verbose =true
test_mode = on
debug_mode = off
log_file_path = /tmp/logfile.log
send_notifications = yes
```

Config Parser can be executed in the following way.
```
hardik@ConfigParser % python config_parser.py --file config.txt
INFO:root:
Object Name/Value --> host=test.com
server_id=55331
server_load_alarm=2.5
user=user
verbose=True
test_mode=True
debug_mode=False
log_file_path=/tmp/logfile.log
send_notifications=True

hardik@ConfigParser %
```
