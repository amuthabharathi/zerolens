#!/usr/bin/python2

# Author 	: Amutha Bharathi M
# Description	: Test program to interface Wiimote IR CAM module with Raspberry-Pi Zero
 
import smbus
from time import sleep

CAM = smbus.SMBus(1)

IR_CAM_ADDR = 0x58 # found using i2cdetect -y 1 

INIT_SEQ = [0x30, 0x01, 0x30, 0x08, 0x60, 0x90,
	    0x08, 0xC0, 0x1A, 0x40, 0x33, 0x33]

def cam_init():
	print "Initializing IR CAMERA...\n"
	
	# Write 2 bytes at a time for initializing the camera
	for i in range(0,12,2):
		CAM.write_byte_data(IR_CAM_ADDR, INIT_SEQ[i], INIT_SEQ[i+1])
		sleep(0.01)
	print "Initialized."


def get_pos():
	CAM.write_byte(IR_CAM_ADDR, 0x36)
	data = CAM.read_i2c_block_data(IR_CAM_ADDR, 0x36, 16)

	x = [0x00]*4 # initialize 4 x values for 4 IR sources
	y = [0x00]*4 # initialize 4 y values for 4 IR sources
	
	i = 0
	for j in xrange(1,11,3):
		x[i] = data[j] + ((data[j+2]&0x30) << 4)
		y[i] = data[j+1] + ((data[j+2]&0xC0) << 2)
	
#		if x[i] != 1023 and y[i] != 1023 :
#			print i, x[i],y[i]
		i+=1
	
	return x[0],y[0],x[1],y[1] 

#cam_init()

#while True:
#	get_pos()
#	sleep(0.5)
