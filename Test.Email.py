# Import smtplib for the actual sending function
import smtplib, os

# Import the email modules we'll need
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("matthewvinck@gmail.com", "mattywow0123")

dir_path = os.path.dirname(os.path.realpath(__file__))

f = open(dir_path + '\output.txt', 'r+')
buffer = f.read()
f.close
		
msg = buffer
server.sendmail("matthewvinck@gmail.com", "vinckrm@gmail.com", msg)
server.quit()