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
def getPublicIP():
    return urllib.request.urlopen("https://v4.ident.me").read().decode("utf8")