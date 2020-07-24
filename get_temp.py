#! /usr/bin/env python3
from subprocess import check_output
from re import findall
import paho.mqtt.client as paho
import configparser
import sys


config = configparser.ConfigParser()
config.read('pi_mqtt.conf')

MQTT_USER = config['DEFAULT']['user']
MQTT_PW = config['DEFAULT']['password']
MQTT_BROKER = config['DEFAULT']['host']
MQTT_TOPIC = config['DEFAULT']['topic']

def get_temp():
    try:
        temp = check_output(["vcgencmd","measure_temp"]).decode("UTF-8")
    except FileNotFoundError:
        print("Please install vcgencmd.")
        sys.exit(1)
    return(findall("\d+\.\d+",temp)[0])


def publish_message(topic, message):

    def on_publish(client,userdata,result):
        print("data published \n")
        pass
    client1 = paho.Client("control1")
    client1.on_publish = on_publish
    client1.username_pw_set(MQTT_USER, MQTT_PW)
    client1.connect(MQTT_BROKER,1883)
    client1.publish(topic, message) 

temp = get_temp()
# temp = 45 for debugging
publish_message(MQTT_TOPIC, temp)