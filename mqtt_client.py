import paho.mqtt.client as mqtt
from RPLCD import CharLCD
import time
lcd = CharLCD(cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[33, 31, 29, 23])


def becca(message):
	lcd.write_string(message.payload)
	time.sleep(10)
	lcd.clear()
def on_message(client, userdata, message):
	print message.payload
	becca(message)
	
 
def on_connect(client, userdata, flags, code):
        print "connected:" + str(code)
        client.subscribe("test/motion")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("broker.hivemq.com", 1883, 60)

client.loop_forever()



