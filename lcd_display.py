#!/usr/bin/python
import time
import paho.mqtt.client as mqtt
import random
import commands
from Adafruit_CharLCD import Adafruit_CharLCD
from time import sleep
from datetime import datetime
import RPi.GPIO as GPIO

 
###############################################
# change this thing ID as required
THING_ID="73dd9ec30f0e11e4ba5c2570ce015a6d"
BROKER_NAME="api.gadgetkeeper.com"
###############################################
 
topic = 'thing.' + THING_ID
broker = BROKER_NAME
client_name = "RaspberryLCD"
 
lcd = Adafruit_CharLCD()
lcd.begin(16, 1)
lcd.clear()


LCD_RS = 26
LCD_E  = 19
LCD_D4 = 13
LCD_D5 = 6
LCD_D6 = 5
LCD_D7 = 11
LED_ON = 15
 
def welcome_msg():
 lcd.message('  Please wait\n')
 sleep(1)
 lcd.message('  Connecting..')
 sleep(2)
 lcd.clear()
 lcd.message('  GadgetKeeper\n')
 sleep(1)
 lcd.message('  Thermometer.')
 sleep(2)
 lcd.clear()
 lcd.message('Waithig for data')
 
def display_info(value):
 lcd.clear()
 lcd.message(datetime.now().strftime('%b %d  %H:%M:%S\n'))
 value = 'Temp:' + str(value) + ' C'
 lcd.message(value)
 
def on_message(mqtt, obj, msg):
  global last_id
  #with open('test.txt', 'wb') as fd:
    #fd.write(msg.payload)
  print 'Request: ' +  msg.payload
  id,jsn,mtd,param = msg.payload.split(',', 3 );
  #print id
  #print jsn
  #print mtd
  #print param
  if mtd:
    mtd1,mtd2 = mtd.split(':',2);
    #mtd3 = mtd2.replace('"', '')
    mtd3 = mtd2.strip('"')
    print 'method -> ' +  mtd3
  if param:
    par1,par2 = param.split('[',2);
    par3 = par2.replace(' ', '')[:-3].upper()
    par4 = par3.strip('"')
    print 'value -> ' + par4
    display_info(par4)
 
welcome_msg()
client = mqtt.client()
client.connect(broker)
client.subscribe(topic,0)
client.on_message = on_message
client.on_connect = on_connect
while True:
   client.loop(15)
   time.sleep(2)
