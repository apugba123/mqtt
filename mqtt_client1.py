import paho.mqtt.client as mqtt

def on_message(client, userdata,message):
	print message.pyload

client = mqtt.
client()
client.on_connect = on_connect
client.on_message = on_message

def on_connect(client, userdata, flags, code):
	print "connected:" + str(code)
	client.subcribe("test/all")

client.connect("broker.hivemq.com", 1883, 60)

client.loop_forever()
