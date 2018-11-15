import os
import sys
import signal
import smbus

import datetime
import time
import math
import numpy as np
# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

start_record    = False
continue_record = False
stop_record     = False

t = 1

bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
address = 0x68       # This is the address value read via the i2cdetect command
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
    global continue_record
    global start_record
    start_record     = True
    continue_record  = True


def handUSR2(signum,frame):
    global continue_record
    global stop_record
    continue_record = False
    stop_record     = True

signal.signal(signal.SIGUSR1,handUSR1)
signal.signal(signal.SIGUSR2,handUSR2)

if __name__ == '__main__':
    while (True):
        if (continue_record == True):
            if (start_record == True):
                bus.write_byte_data(address, power_mgmt_1, 0)
                dataX        = np.empty(0)
                dataY        = np.empty(0)
                dataZ        = np.empty(0)
                t            = 0.001
                start_record = False
                i = 0

            if i < 30000:
                accel_xout_scaled = read_word_2c(0x3b)/16384.0
                accel_yout_scaled = read_word_2c(0x3d)/16384.0
                accel_zout_scaled = read_word_2c(0x3f)/16384.0

                dataX = np.append(dataX,accel_xout_scaled)
                dataY = np.append(dataY,accel_yout_scaled)
                dataZ = np.append(dataZ,accel_zout_scaled)

                i=+1
            else:
                np.savez('measure/'+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),x=dataX,y=dataY,z=dataZ)
                data = np.empty(0)
                print('Dump')

        elif (stop_record == True):
            np.savez('measure/'+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),x=dataX,y=dataY,z=dataZ)
            t = 1
            stop_record = False

        else:
            print ('Esperando')
            time.sleep(t)
