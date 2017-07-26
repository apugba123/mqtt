
import paho.mqtt.client as mqtt



LCD_RS = 26
LCD_E  = 19
LCD_D4 = 13 
LCD_D5 = 6
LCD_D6 = 5
LCD_D7 = 11
LED_ON = 15
         O
def on_message(client, userdata, message):
	print message.payload
	message_type(message)
def message_type(client, userdate, message):
	print message
 
def on_connect(client, userdata, flags, code):
        print "connected:" + str(code)
        client.subscribe("test/apugba123")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("broker.hivemq.com", 1883, 60)
client.loop_forever()

