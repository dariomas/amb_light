#!/usr/bin/env python
#
# ola_send_dmx.py
# Copyright (C) 2005 Simon Newton

"""Send some DMX data."""

__author__ = 'nomis52@gmail.com (Simon Newton)'

import array
from ola.ClientWrapper import ClientWrapper
import os, sys
import cv2
import numpy as np


def DmxSent(state):
  wrapper.Stop()

universe = 11
data = array.array('B')
for i in range(61):
    data.append(0)

wrapper = ClientWrapper()
client = wrapper.Client()

# read from a cam
cam = cv2.VideoCapture(-1) # 0 is cam ID

# Capture frame-by-frame
ret, f = cam.read()
# _ contains ret. value
# f contains image

if ret == True:
    print "Ret: ", ret

# total width
l = f.shape[1]
# total height
h = f.shape[0]

print " L: ", l
print " H: ", h

# select number of regions
nb = 5

# compute height and width of each region
dh = int(h*0.105) # 5% of total
bandwidth =  int(l/nb) # width

# act continuously

while True:
    # Capture frame-by-frame
    
    # get one image to process
    ret,f = cam.read()

    # for each region
    for k in xrange(nb):
	# create masks
        mask_left = np.zeros((h,l,1), np.uint8)
        #mask_right = np.zeros((h,l,1), np.uint8)

	for i in xrange(dh):
    	    for j in xrange(bandwidth):
		mask_left[int((h-dh)/2)+i][bandwidth*k+j] = 1
		#mask_right[dh*k+i][l-j-1] = 1

	# compute averages
	val_left = cv2.mean(f, mask=mask_left)
	#val_right = cv2.mean(f, mask=mask_right)
	
	#print "NB: ", k, "color L = ", int(val_left[0]), int(val_left[1]), int(val_left[2])
	#print "NB: ", k, "color R = ", val_right
	data[10*k] = 230
	data_R = int(val_left[2])
	data_G = int(val_left[1])
	data_B = int(val_left[0])
	if (data_B > data_G) and (data_B > data_R):
	    data_G = 10
	    data_R = 10
	if (data_G > data_B) and (data_G > data_R):
	    data_B = 10
	    data_R = 10
	if (data_R > data_G) and (data_R > data_B):
	    data_G = 10
	    data_B = 10
	data[(10*k)+1] = data_R 
	data[(10*k)+2] = data_G
	data[(10*k)+3] = data_B 

    #print "+", data
    #send 1 dmx frame with values for channels 1-3
    client.SendDmx(universe, data, DmxSent)

# When everything is done, release the capture
cam.release()
cv2.destroyAllWindows()
wrapper.Run()
