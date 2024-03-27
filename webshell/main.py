import paramiko
import dotenv
import os

dotenv.load_dotenv()

username = os.getenv('SSH_USER')
password = os.getenv('SSH_PASSWORD')

try:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    client.connect(hostname='localhost', username=username, password=password)

    command = 'ls'
    stdin, stdout, stderr = client.exec_command(command)

    print(stdout.read().decode(), end='')

    client.close()
except Exception as err:
    print(err)
