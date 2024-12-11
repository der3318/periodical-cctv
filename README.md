
## 📷 Periodical CCTV

![opencv](https://img.shields.io/badge/opencv--python%20%28pip3%29-4.9.0.80-blue.svg)
![line](https://img.shields.io/badge/line-notify--api.line.me-brightgreen.svg)
[![icon](https://img.shields.io/badge/icon-flaticon%20free%20icon-pink.svg)](https://www.flaticon.com/free-icon/cctv-camera_2642651)
![portable](https://img.shields.io/badge/portable-windows%20x64-yellow.svg)
![license](https://img.shields.io/badge/license-MIT%20%28inherited%29-blueviolet.svg)

Use the laptop's webcam to capture a video periodically, and upload the recorded content to FTPS site with timestamp automatically. The notification or error message will be available in [LINE chatroom (via LINE Notify)](https://notify-bot.line.me/my/).

![Demo.jpg](https://github.com/der3318/periodical-cctv/blob/main/Demo.jpg)


### Configuration & Deployment

Modify the [cctv.ini](https://github.com/der3318/periodical-cctv/blob/main/cctv.ini) configurations and put the INI file under Windows User Document folder (e.g., C:\Users\UserName\Documents\cctv.ini):

```ini
[ftptls]
host = endpoint.hostname.or.ip
user = username
passwd = password
folder = /Path/To/Upload/Destination

[capture]
width = 320
height = 240
flip = false
; 300 frames over 10 fps means a 30s capture
fps = 10.0
frames = 300
; idle 1800s (30m) after every capture
idle = 1800

[discoverip]
endpoint = https://v4.ident.me

[linenotify]
endpoint = https://notify-api.line.me/api/notify
bearer = *******your*******bearer*******token*******
```

Double click cctv.exe to launch the background service (i.e., without console). It will read the above properties and start the capture routine endlessly. To stop the worker, simply kill the process in Windows task manager or other process management utilities.


### Build From Python Scripts

The portable EXE file is built using PyInstaller, optionally requiring Pillow module for icon packaging:

```cmd
python3 -m pip install --upgrade pyinstaller
python3 -m pip install --upgrade Pillow
Path\To\Python\Scripts\pyinstaller.exe --add-data "Path\To\Python\Lib\site-packages\cv2;cv2" -F -w -i icon.png cctv.py
```


### Troubleshooting

🔨 IP Discovery Failure

To distinguish the clip uploader, the tool will look up the machine's external IP address with the help of web API. Here are some alternative endpoints of https://v4.ident.me in case it's broken:

* https://api.ipify.org
* https://checkip.amazonaws.com
* https://ipgrab.io

🔨 Camera Selection

If there're multiple cameras (such as front, rear and peripheral) connected, OpenCV may choose the wrong sensor. A workaround is to disable the non wanted ones in device manager.