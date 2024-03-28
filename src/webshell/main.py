import paramiko
import dotenv
import os
import time

dotenv.load_dotenv()

username = os.getenv('SSH_USER')
password = os.getenv('SSH_PASSWORD')

try:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    client.connect(hostname='localhost', username=username, password=password)
    channel = client.invoke_shell()
    time.sleep(0.5)

    commands = [
        'ls',
        'whoami',
        'pwd'
    ]

    for command in commands:
        channel.send(bytes(command + '\n', 'utf-8'))
        time.sleep(0.05)

    output = ''
    while channel.recv_ready():
        output += channel.recv(1024).decode('utf-8')

    print(output)

    client.close()
except Exception as err:
    print(err)
