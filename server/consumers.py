from channels.generic.websocket import WebsocketConsumer
from paramiko import SSHClient, AutoAddPolicy
from dotenv import load_dotenv
from json import loads, dumps
from time import sleep
from os import getenv
from jwt import decode


class SSH:
    def __init__(self, username, password):
        if not username or not password:
            raise Exception('Authentication failed: No session credentials')
        try:
            self.client = SSHClient()
            self.client.set_missing_host_key_policy(AutoAddPolicy())
            self.client.connect('localhost', 22, username, password)
            self.channel = self.client.invoke_shell()
        except:
            raise Exception('Failed to connect to ssh server')

    def get_client(self):
        return self.client

    def get_channel(self):
        return self.channel

    def close(self):
        self.channel.close()
        self.client.close()

class Consumer(WebsocketConsumer):
    def connect(self):
        load_dotenv()
        try:
            token = self.scope['query_string'].decode().split('=')[1]
            if not token:
                raise Exception('No access token provided')
            payload = decode(token, getenv('JWT_SECRET_KEY'), algorithms=['HS256'])
            username = payload['username']
            password = payload['password']
            self.ssh = SSH(username, password)
            self.accept()
            sleep(0.5)
            self.send(self.channel())
        except Exception as error:
            print('WebSocket client authentication failed:', error, flush=True)

    def disconnect(self, close_code):
        if hasattr(self, 'ssh'):
            self.ssh.close()

    def receive(self, text_data=None, bytes_data=None):
        try:
            if text_data == None:
                raise Exception('No data sent')
            data = loads(text_data)
            event = data.get('event')
            if not event:
                raise Exception('No event specified')
            if event == 'shellstream':
                command = data.get('command')
                self.stream(command)
        except Exception as error:
            print(error)
            self.error('invalid payload')

    def stream(self, command):
        try:
            channel = self.ssh.get_channel()
            channel.send(command)
            sleep(0.1)
            self.send(self.channel())
        except Exception:
            self.send('shell stream closed')
            self.close()

    def error(self, message):
        payload = dumps({'error': message})
        self.send(text_data=payload)

    def channel(self):
        channel = self.ssh.get_channel()
        output = ''
        while channel.recv_ready():
            output += channel.recv(1024).decode()
        return output
