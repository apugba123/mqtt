from gpiozero import LCD
from time import sleep
import paho.mqtt.client as mqtt

import RPi.GPIO as GPIO
import time

# Define GPIO to LCD mapping
LCD_RS = 26
LCD_E  = 19
LCD_D4 = 13
LCD_D5 = 6
LCD_D6 = 5
LCD_D7 = 11
LED_ON = 15

# Define some device constants
LCD_WIDTH = 16    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line 

# Timing constants
E_PULSE = 0.00005
E_DELAY = 0.00005

def main():
  # Main program block

  # Initialise display
  lcd_init()

 GPIO.output(LED_ON, False)
  time.sleep(1)
  GPIO.output(LED_ON, True)
  time.sleep(1)

  # Send some centred test
  lcd_byte(LCD_LINE_1, LCD_CMD)
  lcd_string("wELCOME TO TECHLEADS",2)
  lcd_byte(LCD_LINE_2, LCD_CMD)
  lcd_string("KOFORIDUA",2)

  time.sleep(5) # 5 second delay

  # Send some left justified text
  lcd_byte(LCD_LINE_1, LCD_CMD)
  lcd_string("PROJECT LCD",1)
  lcd_byte(LCD_LINE_2, LCD_CMD)
  lcd_string("IOT IN AFRICA",1)

  time.sleep(3) # 3 second delay

  # Send some right justified text
  lcd_byte(LCD_LINE_1, LCD_CMD)
  lcd_string("RPI PROJECT",3)
  lcd_byte(LCD_LINE_2, LCD_CMD)
  lcd_string("ktu.org.gh",3)

  time.sleep(30)

  # Turn off backlight
  GPIO.output(LED_ON, False)

def lcd_init():
  GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
  GPIO.setup(LCD_E, GPIO.OUT)  # E
  GPIO.setup(LCD_RS, GPIO.OUT) # RS
  GPIO.setup(LCD_D4, GPIO.OUT) # DB4
  GPIO.setup(LCD_D5, GPIO.OUT) # DB5
  GPIO.setup(LCD_D6, GPIO.OUT) # DB6
  GPIO.setup(LCD_D7, GPIO.OUT) # DB7
  GPIO.setup(LED_ON, GPIO.OUT) # Backlight enable  
  # Initialise display
  lcd_byte(0x33,LCD_CMD)
  lcd_byte(0x32,LCD_CMD)
  lcd_byte(0x28,LCD_CMD)
  lcd_byte(0x0C,LCD_CMD)
  lcd_byte(0x06,LCD_CMD)
  lcd_byte(0x01,LCD_CMD)

def lcd_string(message,style):
  # Send string to display
  # style=1 Left justified
  # style=2 Centred
  # style=3 Right justified

  if style==1:
    message = message.ljust(LCD_WIDTH," ")
  elif style==2:
    message = message.center(LCD_WIDTH," ")
  elif style==3:
    message = message.rjust(LCD_WIDTH," ")

  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)

def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = data
  # mode = True  for character
  #        False for command

  GPIO.output(LCD_RS, mode) # RS

  # High bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x10==0x10:
    GPIO.output(LCD_D4, True)
  if bits&0x20==0x20:
    GPIO.output(LCD_D5, True)
  if bits&0x04==0x04:
    GPIO.output(LCD_D6, True)
  if bits&0x08==0x08:
    GPIO.output(LCD_D7, True)

  # Toggle 'Enable' pin
  time.sleep(E_DELAY)
  GPIO.output(LCD_E, True)
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)
  time.sleep(E_DELAY)

if __name__ == '__main__':
  main()



           
def on_message(client, userdata, message):
	print message.payload
	message_type(message)

def message_type(message):
	if (message.payload=="Becca"):
		print "==> correct"
		
	else:
		print "==> incorrect "  
def on_connect(client, userdata, flags, code):
        print "connected:" + str(code)
        client.subscribe("test/all")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("broker.hivemq.com", 1883, 60)
client.loop_forever()

