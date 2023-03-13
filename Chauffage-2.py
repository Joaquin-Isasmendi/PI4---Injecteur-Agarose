import time
import math
import RPi.GPIO as GPIO
from smbus import SMBus
#import Adafruit_CharLCD

# Constantes
bus=SMBus(1)
R1=10000
Tc=0
Vout=0
A=0.001658030667120
B=0.00010997945642
C=2.053557090742E-05
D=-7.443525854199E-07

output_min = 24
output_max = 255
pressure_max = 5
pressure_min = 0

baud_rate = 9600
sensor_read_delay = 5

# Pins
pin_mosfet=11

#Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_mosfet, GPIO.OUT)

# Setup LCD
#lcd=Adafruit_CharLCD(rs=26, en=19, d4=13, d5=6, d6=5, d7=11, cols=16, lines=2)
#lcd.begin(16,2)

ads7830_in=[0x84, 0xc4, 0x94, 0xd4, 0xa4, 0xe4, 0xb4, 0xf4]
def read_ads7830(input):
    bus.write_byte(0x4b,ads7830_in[input])
    return bus.read_byte(0x4b)

def read_temperature():
    # Read the thermistor voltage
    Vout = read_ads7830(0)/255*3.3
    # Calculate thermistor resistance
    R2 = R1 * ( 3.3/ (Vout) - 1.0)
    logR2 = math.log(R2)
    # Calculate temperature in Kelvin
    Tk = (1.0 / (A + B*logR2 + C*math.pow(logR2,2) + D*math.pow(logR2,3)))
    # Convert to Celsius
    Tc = Tk - 273.15 
    return Tc

def control_mosfet(temp):
    if temp <= 35:
        GPIO.output(pin_mosfet,GPIO.HIGH)
    elif temp <= 38 and temp >= 35:
         GPIO.output(pin_mosfet, 20)

    else:
         GPIO.output(pin_mosfet, 0)


def read_pressure():
    # Read the thermistor voltage
    Vout = (read_ads7830(1))
    #print(Vout)
    pressure_value = ((Vout - output_min) *
                      (pressure_max - pressure_min) /
                      (output_max - output_min))
    return pressure_value

while True:
    temp = read_temperature()
    print("temp:",temp)
    #lcd.clear()
    #lcd.message("Temperature: %.2f C" % temp)
    control_mosfet(temp)
    print("pressure:",read_pressure()*70.3)
    
    time.sleep(0.2)