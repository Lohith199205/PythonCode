from time import sleep
import os,sys
import RPi.GPIO as GPIO
#import paho.mqtt.client as paho
import urllib.request
import urllib.parse as urlparse
import speech_recognition as sr
import pyaudio

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
LED_PIN=11  #define LED pin
LEDPin = 13
LEDPinT = 15
GPIO.setup(LED_PIN,GPIO.OUT)   # Set pin function as output
GPIO.setup(LEDPin,GPIO.OUT)
GPIO.setup(LEDPinT,GPIO.OUT)

def on_connect(self, mosq, obj, rc):
    self.subscribe("led", 0)
    
def on_message(mosq, obj, msg):
    payloadStr = str(msg.payload)[1:]
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload)[1:]+" "+payloadStr)
    if(payloadStr == "1o"):    
        print("LED on 1")     
        GPIO.output(LED_PIN,GPIO.HIGH)  #LED ON
    elif(payloadStr == "1f"):    
        print("LED off 1")
        GPIO.output(LED_PIN,GPIO.LOW)   # LED OFF

    if(payloadStr == "2o"):    
        print("LED on 2")     
        GPIO.output(LED_PIN,GPIO.HIGH)  #LED ON
    elif(payloadStr == "2f"):    
        print("LED off 2")
        GPIO.output(LED_PIN,GPIO.LOW)   # LED OFF
    
    if(payloadStr == "3o"):    
        print("LED on 3")     
        GPIO.output(LED_PIN,GPIO.HIGH)  #LED ON
    elif(payloadStr == "3f"):    
        print("LED off 3")
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

def connect(host='http://google.com'):
    try:
        urllib.request.urlopen(host) #Python 3.x
        return True
    except:
        return False

# test
print( "connected" if connect() else "no internet!" )

while True:
    while rc == 0:
        import time   
        rc = mqttc.loop()
        #time.sleep(0.5)
    print("rc: " + str(rc))
    sleep(1)
    if connect():
        for i,mic_name in enumerate (sr.Microphone.list_microphone_names()):
            print("mic:"+mic_name)
            if "UACDemoV1.0: USB Audio (hw:2,0)" in mic_name:
                print("head phone" + mic_name)
                mic = sr.Microphone(device_index=i, chunk_size=1024, sample_rate=48000)

        pi_ear = sr.Recognizer()
        speech = sr.Microphone()
        while True:
            need_speak = False
            with speech as source:
        # pi_ear.pause_thpi_eareshold=1
                audio = pi_ear.adjust_for_ambient_noise(source, duration=0.5)
                print("\033[0;35mpi: \033[0m I'm listening")
                audio = pi_ear.listen(source)
            try:
        #        you = pi_ear.recognize_google(audio)
                 you = pi_ear.recognize_google(audio, language = 'en-US')
                 print("You said: " + you)
                 if(you == "Spider-Man on" or you == 'Kousalya on' or you == 'Kaushalya on'
                    or you == 'light on' or you =='on light'):    
                    print ("LED on");     
                    GPIO.output(LED_PIN,GPIO.HIGH)  #LED ON
                 elif(you == "Spider-Man of" or you == 'Kaushalya of'
                      or you == 'Kousalya off' or you == 'Kousalya of'
                    or you == 'light off' or you =='of light' or you == 'light of' or you =='off light'):    
                    print ("LED off");
        #         print (payload1=="b'on'");
                    GPIO.output(LED_PIN,GPIO.LOW)   # LED OFF
                    
                 if(you == "fan on"):    
                    print ("fan on");     
                    GPIO.output(LEDPin,GPIO.HIGH)  #LED ON
                 elif(you == "fan off" or you == 'Pan of' or you == 'fan of'):   
                    print ("fan off");
                    #         print (payload1=="b'on'");
                    GPIO.output(LEDPin,GPIO.LOW)   # LED OFF
                 
                 if(you == "tube on"):    
                    print ("LED on tube");     
                    GPIO.output(LEDPinT,GPIO.HIGH)  #LED ON
                 elif(you == "tube off"):   
                    print ("LED off tube");
                    #         print (payload1=="b'on'");
                    GPIO.output(LEDPinT,GPIO.LOW)   # LED OFF
            except:
                you = ""
    else:
        print("no internet")
# 
# def on_connect(self, mosq, obj, rc):
# self.subscribe("led", 0)
# 
# def on_message(mosq, obj, msg):
# #GPIO.output(LEDPin,GPIO.HIGH)
# print(msg.topic + " /" + str(msg.qos) + " " + str(msg.payload))
# 
# payload1 = str(msg.payload)
# print(str(msg.payload)[-3:]);
# if(str(msg.payload)[-3:] == "nb'"):    
# print ("LED on");     
# GPIO.output(LED_PIN,GPIO.HIGH)  #LED ON
# elif(str(msg.payload)[-3:] == "fb'"):    
# print ("LED off");
# #         print (payload1=="b'on'");
# GPIO.output(LED_PIN,GPIO.LOW)   # LED OFF
# 
# if(str(msg.payload)[-3:] == "ny'"):    
# print ("LED on");     
# GPIO.output(LEDPin,GPIO.HIGH)  #LED ON
# elif(str(msg.payload)[-3:] == "fy'"):   
# print ("LED off");
# #         print (payload1=="b'on'");
# GPIO.output(LEDPin,GPIO.LOW)   # LED OFF
# 
# if(str(msg.payload)[-3:] == "nt'"):    
# print ("LED on tube");     
# GPIO.output(LEDPinT,GPIO.HIGH)  #LED ON
# elif(str(msg.payload)[-3:] == "ft'"):   
# print ("LED off tube");
# #         print (payload1=="b'on'");
# GPIO.output(LEDPinT,GPIO.LOW)   # LED OFF
# 
# 
# def on_publish(mosq, obj, mid):
# print("mid: " + str(mid))
# 
# 
# def on_subscribe(mosq, obj, mid, granted_qos):
# print("Subscribed: " + str(mid) + " " + str(granted_qos))
# 
# 
# 
# mqttc = paho.Client()                        # object declaration
# # Assign event callbacks
# mqttc.on_message = on_message                          # called as callback
# mqttc.on_connect = on_connect
# mqttc.on_publish = on_publish
# mqttc.on_subscribe = on_subscribe
# 
# 
# #url_str = os.environ.get('CLOUDMQTT_URL', 'tcp://broker.emqx.io:1883')                  # pass broker addr e.g. "tcp://iot.eclipse.org"
# #url_str = os.environ.get('CLOUDMQTT_URL', 'tcp://broker.hivemq.com:1883')
# url_str = os.environ.get('CLOUDMQTT_URL', 'tcp://broker.emqx.io:1883') 
# url = urlparse.urlparse(url_str)
# mqttc.connect_async(url.hostname, url.port)
# #print(mqttc.connect(url.hostname, url.port))
# 
# rc = 0
# while True:
# while rc == 0:
# import time   
# rc = mqttc.loop_start()
# #print(rc);
# time.sleep(1)
# #print("rc: " + str(rc))

# 
# if(str(msg.payload)[-3:] == "ny'"):    
# print ("LED on");     
# GPIO.output(LEDPin,GPIO.HIGH)  #LED ON
# elif(str(msg.payload)[-3:] == "fy'"):   
# print ("LED off");
# #         print (payload1=="b'on'");
# GPIO.output(LEDPin,GPIO.LOW)   # LED OFF
# 
# if(str(msg.payload)[-3:] == "nt'"):    
# print ("LED on tube");     
# GPIO.output(LEDPinT,GPIO.HIGH)  #LED ON
# elif(str(msg.payload)[-3:] == "ft'"):   
# print ("LED off tube");
# #         print (payload1=="b'on'");
# GPIO.output(LEDPinT,GPIO.LOW)   # LED OFF






