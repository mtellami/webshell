from channels.generic.websocket import WebsocketConsumer
from os import getenv
import dotenv
import json
import paramiko

dotenv.load_dotenv()

class SSHClient:
    def __init__(self, username, password):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
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
        print('\n\nwebsocket conneted .......\n\n')
        self.accept()
        self.ssh = SSHClient(getenv('SSH_USER'), getenv('SSH_PASSWORD'))

    def disconnect(self, close_code):
        self.ssh.close()

    def receive(self, text_data=None, bytes_data=None):
        try:
            event = json.loads(text_data).get('event')
            if not event:
                raise Exception('No event name')
            if event == 'shell:stream':
                self.stream(bytes_data)
        except Exception as error:
            self.error(error)

    def stream(self, data):
        pass

    def error(self, message):
        self.send(text_data=json.dumps({'error': message}))
