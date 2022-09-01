import time
import json
import socket as s
import os
import datetime
import sys
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

def fetch_user(password):
  users_login = open("users_data.txt", "r").read().split('\n')
  users = [user.strip().split(' ') for user in users_login]
  filtered_users = [user[0] for user in users if user[1] == password]
  if len(filtered_users) > 0:
    user = filtered_users[0]
    return user
  else:
    return None

def log_user(user):
  users_log = open("users_log.txt", "a")
  if user == None:
    users_log.write(f"Invalid authentication at {datetime.datetime.now()}\n")
  else:
    users_log.write(f"{user} authenticated at {datetime.datetime.now()}\n")
  users_log.close()

def send_email():
    users_log = open("users_log.txt", "r").read().split('\n')
    failed_logs = users_log[-3:-1]
    msgTo = os.getenv('RECEIVE_EMAIL')
    msgFrom = os.getenv('SEND_EMAIL')
    fromPass = os.getenv('SEND_PASSWORD')
    smtpObj = smtplib.SMTP("smtp.mailtrap.io", 2525)
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login(msgFrom, fromPass)
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Acesso inválido consecutivo"
    msg["From"] = msgFrom
    msg["To"] = msgTo
    text = """\ %s """ % '\n'.join(failed_logs)
    part1 = MIMEText(text,"plain")
    msg.attach(part1)
    smtpObj.sendmail(msgFrom,msgTo,msg.as_string())
    smtpObj.quit()
    print("Email enviado com sucesso!")
    

socket = s.socket(s.AF_INET, s.SOCK_STREAM)
try:
    socket.bind(('192.168.15.11', 2045))
except s.error:
    print("Failed to bind")
    sys.exit()
socket.listen()
print("Successful binding!")

error_count = 0
while True:
    try:
        conn,addr = socket.accept()
        data = conn.recv(4096)
        password = data.decode("utf-8").strip()
        print(password) 
        user = fetch_user(password)
        log_user(user)
        if user == None:
          user = "ERROR"
          error_count += 1
        else:
            error_count = 0
        conn.sendall(bytes(user, "utf-8"))
        print(error_count)
        if error_count == 2:
            send_email()
            error_count = 0
    except:
        pass
