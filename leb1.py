from time import sleep
import os,sys
import RPi.GPIO as GPIO
import paho.mqtt.client as paho
import urllib.request
import urllib.parse as urlparse

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
LED_PIN=11  #define LED pin
GPIO.setup(LED_PIN,GPIO.OUT)   # Set pin function as output

def on_connect(self, mosq, obj, rc):
        self.subscribe("led", 0)
    
def on_message(mosq, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload)[1:])
    if(msg.payload == "on"):    
        print("LED on")     
        GPIO.output(LED_PIN,GPIO.HIGH)  #LED ON
    else:    
        print("LED off")
        GPIO.output(LED_PIN,GPIO.LOW)   # LED OFF

def on_publish(mosq, obj, mid):
    print("mid: " + str(mid))

    
def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))



mqttc = paho.Client()                        # object declaration
# Assign event callbacks
mqttc.on_message = on_message                          # called as callback
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe


#url_str = os.environ.get('CLOUDMQTT_URL', 'tcp://broker.emqx.io:1883')                  # pass broker addr e.g. "tcp://iot.eclipse.org"
#url_str = os.environ.get('CLOUDMQTT_URL', 'tcp://broker.hivemq.com:1883')
url_str = os.environ.get('CLOUDMQTT_URL', 'tcp://broker.emqx.io:1883') 
url = urlparse.urlparse(url_str)
mqttc.connect(url.hostname, url.port)

rc = 0
while True:
    while rc == 0:
        import time   
        rc = mqttc.loop()
        #time.sleep(0.5)
    print("rc: " + str(rc))
