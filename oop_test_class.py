import os.path
import time

import paramiko

class Connection:

    def __init__(self, ip, username, password):
        self.ip = ip
        self.username = username
        self.password = password
        self.ssh = None
        self.sftp_client = None

    def connect(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(self.ip, username=self.username, password=self.password)
        self.sftp_client = self.ssh.open_sftp()

    def send_command(self, some_command):
        stdin, stdout, stderr = self.ssh.exec_command(some_command)
        print(stdout.read().decode())


    def get(self, localfile, remotefile):
        self.sftp_client.get(localfile, remotefile)

    def put(self, localfile, remotefile):
        self.sftp_client.put(localfile, remotefile)

    def sleep(self, second):
        time.sleep(second)

    def remove(self, file_for_remove):
        self.sftp_client.remove(file_for_remove)

    def latest_file(self, path_):
        files_for_time = []
        self.path_ = path_
        for root, dirs, files in os.walk(path_):
            for file in files:
                files_for_time.append(os.path.join(root, file))

        latest_file = max(files_for_time, key=os.path.getctime)
        print(latest_file)

    def close(self):
        self.ssh.close()

d = Connection(ip='127.0.0.1', username='mint', password='1235')
d.connect()
d.send_command('hostname')
d.get('/home/mint/document.pdf', '/home/mint/Изображения/document.pdf')
d.put('/home/mint/krepkiy_alkogol.jpg', '/home/mint/Изображения/krepkiy_alkogol.jpg')
d.sleep(10)
d.remove('/home/mint/Изображения/document.pdf')
d.latest_file('/home/mint/Изображения/')


