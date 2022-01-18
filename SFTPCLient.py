import pathlib
from datetime import datetime
import paramiko
from paramiko import SFTPClient
from pathlib import Path
from typing import Union

from paramiko.sftp_attr import SFTPAttributes


class Connection(SFTPClient):

    def get_last_filename(self, path: Union[bytes, pathlib.Path], sort: bool=True) ->str:
        return self.listdir_attr(path, sort)[0].filename

    def _adjust_cwd(self, path: Union[bytes, pathlib.Path]) ->str:
        return super(Connection, self)._adjust_cwd(bytes(path))

    def listdir_attr(self, path: Union[bytes, pathlib.Path], sort: bool=False) ->list[SFTPAttributes]:
        files = super().listdir_attr(bytes(path))
        if sort == True:
            files.sort(key=lambda f: datetime.fromtimestamp(f.st_mtime).strftime('%Y-%m-%dT%H:%M:%S'), reverse=True)
            return files

        return files

    def listdir(self, path: Union[list[SFTPAttributes]], sort: bool=True) ->list[str]:
        return [f.filename for f in self.listdir_attr(path, sort)]

if __name__ == '__main__':
    Connection

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
p = Path('/home/ubuntu/Изображения/')
lp = Path('/home/ubuntu/Изображения/command')
rp = Path('/home/ubuntu/Документы/command')
ssh.connect(hostname='127.0.0.1', username='ubuntu', password='1235', look_for_keys=False, allow_agent=False)
ftp = SFTPClient.from_transport(ssh.get_transport())
d = Connection.from_transport(ssh.get_transport())
d.put(lp, rp)
# rg = Path('/home/mint/new')
# lg = Path('/home/mint/Изображения/new')
# d.remove(rg)
# d.get(rg, lg)
print(d.listdir_attr(p))
print(d.listdir(p))
print(d.get_last_filename(p))