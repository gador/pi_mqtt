# pi_mqtt

## Summary
Small script to read temperature and other stats of a raspberry pi and publish it to MQTT.

## Requirements
python3
python3-paho-mqtt
python3-configparser
vcgencmd

## example config file layout

[CONFIG]
client = raspberry
host = 192.168.1.12
user = mqtt_client
password = secretpassword
topic = home/raspberrypi/

- host can either be an IP adress or a hostname
- user and password need to be set on the mqtt instance
- topic needs to end with a slash '/'. The measurements will be appended.
  Right now this is: temp, cpu, disk and memory

## License
MIT