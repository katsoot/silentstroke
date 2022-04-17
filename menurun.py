#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 21:17:11 2022

@author: matthewjinsookim
"""

import sys
import os
from tkinter import *
import sys
import serial
import struct
import time
import threading

#init
StartTime=time.time()

# creates interval function to run after x amount of time
class setInterval :
    def __init__(self,interval,action) :
        self.interval=interval
        self.action=action
        self.stopEvent=threading.Event()
        thread=threading.Thread(target=self.__setInterval)
        thread.start()

    def __setInterval(self) :
        nextTime=time.time()+self.interval
        while not self.stopEvent.wait(nextTime-time.time()) :
            nextTime+=self.interval
            self.action()

    def cancel(self) :
        self.stopEvent.set()

# makes window fullscreen and hides desktop
def end_fullscreen(event):
	root.attributes("-fullscreen", False)

#defining button command
def program_start():


	# add some time 
	for i in range(0,6):
		now = time.time()
		n = 1
		angle = 0
		while n == 1:
			val_byte = sp.read()
			val = int.from_bytes(val_byte, byteorder = 'big', signed=False)
			print(val)
			print(val_byte)
			end = time.time()
			#angle = max(val)
			#end = time.time()
			total = round(end - now)
			if total == 5:
				
				val_array[i] = angle
				angle = 0
				n = 0
			else: 
				if val > angle:	
					angle = val
				


	leg1 = (val_array[0] + val_array[2] + val_array[4])/3
	leg2 = (val_array[1] + val_array[3] + val_array[5])/3

	output_str = "Leg 1: " + str(leg1) + " Leg 2: " + str(leg2)
	
	# update text in Label
	if ((leg1 >= 20) & (leg1 <= 40)):
		label_2.config(text=str(output_str)) 
	else:
		label_2.config(text="Abnormal motor function. The American Heart Association/American Stroke Association \nrecommends visiting your family physician.")

def end_fullscreen():
    root.attributes("-fullscreen", False)


# --- main ---
root = Tk()

# reading OPENMV from USB port

port = '/dev/ttyACM0'
sp = serial.Serial(port, baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, xonxoff=False, rtscts=False, stopbits=serial.STOPBITS_ONE, timeout=None, dsrdtr=True)
sp.setDTR(True)
val_byte = sp.read()
print(val_byte)
val = int.from_bytes(val_byte, byteorder = 'big', signed=False)
#val = val_byte

root.wm_title("Start Up Window")

root.configure(bg="#aec6cf")
root.attributes("-fullscreen", True)

val_array = []
val_array = [0 for i in range(6)] 
angle = 0

n = 0

# init vars
text_update = "Press Collect Measurement"

#label (title)
label_2 = Label(root, text=text_update, 
                font="Helvetica 10 bold", 
                fg="#022851", 
                bg="#FFFFFF")

#Button
btn1 = Button(root, text="Collect Measurement")
btn2 = Button(root, text="Close Screen")

#Configure Layout
label_2.grid(row=1, column=0)
label_2.place(relx=.5, rely=0.2, anchor=CENTER)

btn1.grid(row=2, column=0)
btn1.place(relx=.5, rely=0.5, anchor=CENTER)

btn2.grid(row=3, column=0)
btn2.place(relx=.5, rely=0.6, anchor=CENTER)

#Configuring button commands
btn1.config(command=program_start)
btn2.config(command=end_fullscreen)
    

root.bind("<Escape>", end_fullscreen)
root.mainloop()
