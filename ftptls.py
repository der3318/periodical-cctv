# -*- coding: utf-8 -*-

# standard libs
import datetime
import ftplib
import ssl
import types


# https://stackoverflow.com/a/50129806
def storbinarynounwrap(self, cmd, fp, blocksize = 8192, callback = None, rest = None):
    self.voidcmd("TYPE I")
    with self.transfercmd(cmd, rest) as conn:
        while True:
            buf = fp.read(blocksize)
            if not buf: break
            conn.sendall(buf)
            if callback: callback(buf)
        if isinstance(conn, ssl.SSLSocket):
            # HACK: Instead of attempting unwrap the connection, pass here
            pass
    return self.voidresp()


def uploadTimestampedMP4(config, ip, mp4):
    filename = "{}-{}.mp4".format(datetime.datetime.now().strftime("%Y%m%d%H%M%S"), ip)
    with ftplib.FTP_TLS(config.get("ftptls", "host")) as ftps:
        ftps.storbinary = types.MethodType(storbinarynounwrap, ftps)
        ftps.login(config.get("ftptls", "user"), config.get("ftptls", "passwd"))
        ftps.prot_p()
        ftps.cwd(config.get("ftptls", "folder"))
        with open(mp4, "rb") as clip:
            ftps.storbinary("STOR {}".format(filename), clip)
    return filename
