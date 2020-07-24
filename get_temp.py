#! /usr/bin/env python3
from subprocess import check_output
from re import findall
import paho.mqtt.publish as publish
import configparser
import sys

config = configparser.ConfigParser()
config.read('pi_mqtt.conf')

MQTT_USER = config['DEFAULT']['user']
MQTT_PW = config['DEFAULT']['password']
MQTT_BROKER = config['DEFAULT']['host']
MQTT_TOPIC = config['DEFAULT']['topic']

MQTT_AUTH = {'username':MQTT_USER, 'password':MQTT_PW}

def get_temp():
    try:
        temp = check_output(["vcgencmd","measure_temp"]).decode("UTF-8")
    except FileNotFoundError:
        print("Please install vcgencmd.")
        sys.exit(1)
    return(findall("\d+\.\d+",temp)[0])


def publish_message(topic, message):
    publish.single(topic, message, hostname=MQTT_BROKER, auth=MQTT_AUTH)

temp = get_temp()
publish_message(MQTT_TOPIC, temp)