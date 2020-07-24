#! /usr/bin/env python3
from subprocess import check_output
from re import findall
import paho.mqtt.client as paho
import configparser
import psutil
import sys


config = configparser.ConfigParser()
config.read('pi_mqtt.conf')

if config.has_section('CONFIG'):
    MQTT_USER = config['CONFIG']['user']
    MQTT_PW = config['CONFIG']['password']
    MQTT_BROKER = config['CONFIG']['host']
    MQTT_TOPIC = config['CONFIG']['topic']
    MQTT_CLIENT = config['CONFIG']['client']
else:
    print("No 'CONFIG' section in config file supplied or no pi_mqtt.conf file found")
    sys.exit(1)

def get_temp():
    try:
        temp = check_output(["vcgencmd","measure_temp"]).decode("UTF-8")
    except FileNotFoundError:
        print("Please install vcgencmd.")
        sys.exit(1)
    return(findall(r"\d+\.\d+",temp)[0])

def get_disk_usage():
    return str(psutil.disk_usage('/').percent)

def get_memory_usage():
    return str(psutil.virtual_memory().percent)

def get_cpu_usage():
    return str(psutil.cpu_percent(interval=None))

def init_client():
    client = paho.Client(MQTT_CLIENT)
    client.username_pw_set(MQTT_USER, MQTT_PW)
    client.connect(MQTT_BROKER,1883)
    return client

def publish_message(client, topic, message):
    client.publish(topic, message) 

client = init_client()

publish_message(client, MQTT_TOPIC + 'temp', '45')
publish_message(client, MQTT_TOPIC + 'disk', get_disk_usage())
publish_message(client, MQTT_TOPIC + 'memory', get_memory_usage())
publish_message(client, MQTT_TOPIC + 'cpu', get_cpu_usage())