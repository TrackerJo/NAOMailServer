 #Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import smtplib, ssl
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
import time
from email import encoders
import random
from email.message import EmailMessage
import os
from dotenv import load_dotenv, dotenv_values 
# loading variables from .env file
load_dotenv() 

# Import Module
import paramiko
 
# Fill Required Information
HOSTNAME = "192.168.1.22"
USERNAME = "nao"
PASSWORD = "nao"




port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "jovi@clhscadets.com"  # Enter your address
password = os.getenv("PASSWORD")  # Enter your password
emailMSG = None
hostName = "192.168.1.16"
serverPort = 8080
usingRobot = True

class MyServer(BaseHTTPRequestHandler):
    def load_binary(filename):
        with open(filename, 'rb') as file_handle:
            return file_handle.read()
    def send_email(self):
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.send_message(emailMSG)
            # server.sendmail(sender_email, receiver_email, msg.as_string())
        if usingRobot:
            # Delete the file on this computer
            Path("image.jpg").unlink()


        
    def do_GET(self):
        global emailMSG
        self.send_response(200)
        
        self.send_header("Access-Control-Allow-Origin", "http://127.0.0.1:5500")
        
        paths = self.path.split("/")
        
        if paths[1] == "set_content":
            self.send_header("Content-type", "text/html")
            self.end_headers()
            if usingRobot:
               
                ssh_client = paramiko.SSHClient()
                ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh_client.connect(hostname=HOSTNAME, username=USERNAME, password=PASSWORD,allow_agent=False)
                sftp_client = ssh_client.open_sftp()
                path = './recordings/cameras/' 
                sftp_client.chdir(path)

                # transport = paramiko.Transport((HOSTNAME, 22))

                #         #hard-coded
                # transport.connect(username = USERNAME, password = PASSWORD)

                # sftp = paramiko.SFTPClient.from_transport(transport)

                # import sys
                #hard-coded
                localpath = "image.jpg"
                # sftp.put(localpath, path)
                # sftp.chdir(path)
                sftp_client.get('image.jpg', localpath)

                sftp_client.close()
                ssh_client.close()

                # Display the content of downloaded file
            emailMSG = EmailMessage()
            # msg = MIMEMultipart()

            # msg.attach(MIMEText("Subject: {}".format(paths[3].replace("%20", " ")) + paths[4].replace("%20", " ")))
            
            emailMSG['Subject'] = paths[2].replace("%20", " ")
            emailMSG['From'] = sender_email
            emailMSG['Bcc'] = "sstorm@clhscadets.com"
           
            # body = paths[4].replace("%20", " ")
            # body = "Test"
            # print(body)
            # emailMSG.set_content(body)
            emailMSG.set_content(paths[3].replace("%20", " "))
            
            if usingRobot:
                file = open("image.jpg", "rb")
                content = file.read()
                emailMSG.add_attachment(content, maintype='application', subtype='jpg', filename='image.jpg')
            # Open txt file to read and write to file
            emailFile = open("email.txt", "r")

            
            # Read the content of the file
            emailContent = emailFile.read()
            emailFile.close()
            emailFile = open("email.txt", "w")
            # Get first line of file
            emailTo = emailContent.split("\n")[0]
            if emailTo == "":
                self.wfile.write(bytes("need_email", "utf-8"))
                return
            emailMSG['To'] = emailTo
            self.send_email()
            # Clear the file
            emailFile.seek(0)
            emailFile.truncate()
            emailFile.close()
            emailMSG = None
            self.wfile.write(bytes("email_sent", "utf-8"))
        elif paths[1] == "set_email":
            self.send_header("Content-type", "application/json")
            self.end_headers()
            if emailMSG != None:
                emailMSG['To'] = paths[2]
                self.send_email()
                emailMSG = None
                response = "{\"status\": \"email_sent\"}"
                self.wfile.write(bytes(response, "utf-8"))
                return
            emailFile = open("email.txt", "w")
            emailFile.write(paths[2])
            emailFile.close()
            # Send response as JSON
            response = "{\"status\": \"set_email\"}"

            self.wfile.write(bytes(response, "utf-8"))

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
