# -*- coding: utf-8 -*-

# standard libs
import ctypes.wintypes
import urllib.request


# https://stackoverflow.com/a/30924555
def getUserDocumentsPath():
    buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
    ctypes.windll.shell32.SHGetFolderPathW(None, 5, None, 0, buf) # CSIDL_PERSONAL(My Documents)=5 and SHGFP_TYPE_CURRENT=0
    return buf.value


# https://stackoverflow.com/a/41432835
def getPublicIP(config):
    return urllib.request.urlopen(config.get("discoverip", "endpoint")).read().decode("utf-8")


def lineNotify(config, message):
    headers = {"Authorization": "Bearer {}".format(config.get("linenotify", "bearer"))}
    body = {"message": message}
    data = urllib.parse.urlencode(body)
    req = urllib.request.Request(config.get("linenotify", "endpoint"), data = data.encode("utf-8"), method = "POST", headers = headers)
    with urllib.request.urlopen(req) as res:
        return res.read().decode("utf-8")
