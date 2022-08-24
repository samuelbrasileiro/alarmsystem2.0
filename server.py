import time
import json
import socket as s
import os
import datetime
from dotenv import load_dotenv

load_dotenv()
email = os.getenv('EMAIL')
password = os.getenv('PASSWORD')

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

socket = s.socket(s.AF_INET, s.SOCK_STREAM)
try:
    socket.bind(('127.0.0.1', 2045))
except s.error:
    print("Failed to bind")
    sys.exit()
socket.listen()
print("Successful binding!")

while True:
    try:
        conn,addr = socket.accept()
        data = conn.recv(4096)
        password = data.decode("utf-8").strip()
        user = fetch_user(password)
        log_user(user)
        if user == None:
          user = "ERROR"
        conn.sendall(bytes(user, "utf-8"))
    except:
      pass
