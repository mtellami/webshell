from channels.generic.websocket import WebsocketConsumer
from paramiko import SSHClient, AutoAddPolicy
from dotenv import load_dotenv
from json import loads, dumps
from time import sleep
from os import getenv


class SSH:
    def __init__(self, username, password):
        if not username or not password:
            raise Exception('Authentication failed')
        self.client = SSHClient()
        self.client.set_missing_host_key_policy(AutoAddPolicy())
        self.client.connect('localhost', 22, username, password)
        self.channel = self.client.invoke_shell()

    def get_client(self):
        return self.client

    def get_channel(self):
        return self.channel

    def close(self):
        self.channel.close()
        self.client.close()

class Consumer(WebsocketConsumer):
    def connect(self):
        try:
            # connect using username & passoword from the JWT token sent
            load_dotenv()
            self.ssh = SSH(getenv('SSH_USER'), getenv('SSH_PASSWORD'))
            self.accept()
        except Exception:
            print('WebSocket client authentication failed')

    def disconnect(self, close_code):
        if hasattr(self, 'ssh'):
            self.ssh.close()

    def receive(self, text_data=None, bytes_data=None):
        try:
            if not text_data:
                raise Exception('No data sent')
            data = loads(text_data)
            event = data.get('event')
            if not event:
                raise Exception('No event specified')
            if event == 'shellstream':
                command = data.get('command')
                self.stream(command)
        except Exception:
            self.error('invalid payload')

    def stream(self, command):
        try:
            channel = self.ssh.get_channel()
            channel.send(command + '\n')
            sleep(0.1)
            output = ''
            while channel.recv_ready():
                output += channel.recv(1024).decode()
            if channel.closed:
                raise Exception('channel closed')
            self.send(output)
        except Exception:
            self.send('shell stream closed')
            self.close()

    def error(self, message):
        payload = dumps({'error': message})
        self.send(text_data=payload)
