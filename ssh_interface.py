

import time

class ssh_interface:
    def __init__(self):
        self.is_connected = False
        # self.client = paramiko.SSHClient()
        # self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # self.client.connect(self.host, self.port, self.username, self.password)

    def connect(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        
        #wait 2 seconds
        time.sleep(2)
        
        self.is_connected = True
        
    def disconnect(self):
        self.close()

    def send_command(self, command):
        # stdin, stdout, stderr = self.client.exec_command(command)
        # return stdout.read()
        return "test"

    def close(self):
        # self.client.close()
        self.is_connected = False