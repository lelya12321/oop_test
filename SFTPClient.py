from datetime import datetime
import paramiko
from paramiko import SFTPClient
from pathlib import Path

from paramiko.sftp_attr import SFTPAttributes


class Connection(SFTPClient):

    def get_last_filename(self, path):
        list_ = []
        for i in path.iterdir():
            list_.append(i.stat().st_ctime)
        res = [str(i) for i in path.iterdir() if i.stat().st_ctime == max(list_)]
        return res[0]

    def get(self, remotepath: bytes, localpath: bytes, callback=None) ->bytes:
        return super().get(bytes(remotepath), bytes(localpath))

    def put(self, localpath: bytes, remotepath: bytes, callback=None, confirm=True) ->bytes:
        return super().put(bytes(localpath), bytes(remotepath))

    def remove(self, path: bytes) ->bytes:
        return super().remove(bytes(path))

    def listdir_attr(self, path: bytes, sort=True) ->bytes:
        files = super().listdir_attr(bytes(path))
        if sort == True:
            files.sort(key=lambda f: datetime.fromtimestamp(f.st_mtime).strftime('%Y-%m-%dT%H:%M:%S'))
            return files
        else:
            files.sort(key=lambda f: datetime.fromtimestamp(f.st_mtime).strftime('%Y-%m-%dT%H:%M:%S'), reverse=True)
            return files

    def listdir(self, path: list[SFTPAttributes], sort=True) ->list[SFTPAttributes]:
        return [f.filename for f in self.listdir_attr(path, sort)]

    def close(self):
        self.close()


ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
p = Path('/home/mint/Изображения/')
lp = Path('/home/mint/Изображения/krepkiy_alkogol.jpg')
rp = Path('/home/mint/Документы/krepkiy_alkogol.jpg')
ssh.connect(hostname='127.0.0.1', username='mint', password='1235', look_for_keys=False, allow_agent=False)
ftp = SFTPClient.from_transport(ssh.get_transport())
d = Connection.from_transport(ssh.get_transport())
d.put(lp, rp)
rg = Path('/home/mint/new')
lg = Path('/home/mint/Изображения/new')
d.remove(rg)
d.get(rg, lg)
print(d.listdir_attr(p))
print(d.listdir(p))
print(d.get_last_filename(p))