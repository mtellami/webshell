from channels.generic.websocket import WebsocketConsumer
from .SSHClient import SSHClient
from os import getenv
import dotenv
import json

dotenv.load_dotenv()

class Consumer(WebsocketConsumer):
    def connect(self):
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
