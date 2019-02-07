import urllib
import re
import json
import sched, time
import smtplib as smtp
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

TIMER = 60
COUNT = 0
URL = "https://www.overkillshop.com/en/"
SEND_EMAIL = True

# Creating an instance with our secrets.json file
with open("secrets.json") as secrets_file:
    secrets = json.load(secrets_file)
    secrets_file.close()

# Email values
MY_ADDRESS = secrets['myEmail']
PASSWORD = secrets['emailSecret']

# Twilio secret variables
AccountSID = secrets['twilioKey']
AuthToken = secrets['twilioSecret']
MyNumber = secrets['myNumber']
TwilioNumber = secrets['twilioNumber']

def searchSite():
	contents = urllib.urlopen(URL).read()
	matches = re.findall('Air Jordan', contents);

	if len(matches) == 0: 
		print 'I did not find anything'
	else:
		print 'My string is in the website ' + str(len(matches)) + ' times'

	global COUNT
	if len(matches) > COUNT:
		COUNT = len(matches)
		if SEND_EMAIL: send_email()
	set_timer(searchSite)

def set_timer(onFire):
	schedule = sched.scheduler(time.time, time.sleep)
	schedule.enter(TIMER, 1, onFire, ())
	schedule.run()

def send_email():
	server   = smtp.SMTP('smtp.gmail.com:587')
	# create a message
	msg      = MIMEMultipart()
	text     = MIMEText(message)
	subject  = URL + 'hit Air Jordan ' + str(COUNT) + ' times'

	# Set up server
	server.ehlo()
	server.starttls()
	server.login(MY_ADDRESS, PASSWORD)
	server.sendmail(MY_ADDRESS, MY_ADDRESS, msg.as_string())
	# Terminate the SMTP session and close the connection
	server.quit()

if __name__ == "__main__":
	searchSite()