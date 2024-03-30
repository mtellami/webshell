import paramiko

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
