import os
import sys
import signal
import time
import smbus
import math
import csv
# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

grabar=False
parar=False
t=1

bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
address = 0x68       # This is the address value read via the i2cdetect command
medicion_path="medicion.csv"
fh=open("processid.txt","w")
fh.write(str(os.getpid())) #get current process id and store in file
fh.close()


def read_byte(adr):
    return bus.read_byte_data(address, adr)

def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val

def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def dist(a,b):
    return math.sqrt((a*a)+(b*b))

def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)

def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)

def handUSR1(signum,frame):
    global grabar
    global empezar
    grabar = True
    empezar = True
 
def handUSR2(signum,frame):
    global grabar
    global parar
    grabar = False
    parar = True

signal.signal(signal.SIGUSR1,handUSR1)
signal.signal(signal.SIGUSR2,handUSR2)

while (True):
	if (grabar == True):
		if (empezar == True):
			bus.write_byte_data(address, power_mgmt_1, 0)
			t = 0.001
			empezar=False
			
		with open(medicion_path,'a',newline='') as archivo:
			csvwriter = csv.writer(archivo)
			row = [read_word_2c(0x3b)]
			csvwriter.writerow(row)
			
	elif (parar == True):
		t = 1
		parar = False
	else:
		print ('Esperando')
	time.sleep(t)
    
