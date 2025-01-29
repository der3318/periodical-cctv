# -*- coding: utf-8 -*-
# dependency: pip install pyinstaller + pip install Pillow (for icon packaging)
# executable: .\Runtime\App\Python\Scripts\pyinstaller.exe --add-data ".\Runtime\App\Python\Lib\site-packages\cv2;cv2" -F -w -i icon.png cctv.py

# standard libs
import configparser
import logging
import os
import sys
import time

# third party libs
import cv2  # pip install opencv-python

# project libs
import ftptls
import utils


def main():

    # config from ini file
    config = configparser.ConfigParser()
    config.read(os.path.join(utils.getUserDocumentsPath(), "cctv.ini"))

    # logging settings
    logging.basicConfig(
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(os.path.join(utils.getUserDocumentsPath(), "cctv.log"), mode="w"),
        ],
        level=logging.DEBUG,
    )

    # worker for repeated task
    while True:
        try:
            # create opencv video capture and mp4 writer
            cap = cv2.VideoCapture(0)
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            mp4 = os.path.join(utils.getUserDocumentsPath(), "cctv.mp4")
            resolution = (config.getint("capture", "width"), config.getint("capture", "height"))
            out = cv2.VideoWriter(mp4, fourcc, config.getfloat("capture", "fps"), resolution)

            # collect frames
            for i in range(config.getint("capture", "frames")):
                if not cap.isOpened():
                    raise Exception("cv.VideoCapture(0)isOpened() returns false. CV2 video capture not available?")
                ret, frame = cap.read()
                if not ret:
                    raise Exception("Can't receive frame. Stream end?")
                frame = cv2.flip(cv2.resize(frame, resolution), 0) if config.getboolean("capture", "flip") else cv2.resize(frame, resolution)
                out.write(frame)
                time.sleep(1.0 / config.getfloat("capture", "fps"))

            # stream cleanup
            cap.release()
            out.release()

            # upload mp4 to ftp tls site
            ip = utils.getPublicIP(config)
            filename = ftptls.uploadTimestampedMP4(config, ip, mp4)
            utils.lineNotify(config, "CCTV {} uploaded successfully".format(filename))

        except Exception as e:
            try:
                utils.lineNotify(config, "Error: {}".format(e))
            except Exception:
                logging.debug("Error: {}".format(e))

        # idle for a while
        time.sleep(config.getint("capture", "idle"))


if __name__ == "__main__":
    main()