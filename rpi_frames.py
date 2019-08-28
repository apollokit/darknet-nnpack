# from picamera import PiCamera
from subprocess import Popen, PIPE
import threading
from time import sleep
import os, fcntl
# import cv2
from shutil import copyfile
import argparse
import glob
from os import path

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("--frames_dir", type=str, help="path to the input frames dir")
ap.add_argument("--output_dir", type=str, default="output", help="path to the output frames dir")
args = ap.parse_args()

iframe = 0

# camera = PiCamera()

# camera.resolution = (416, 416)

# camera.capture('frame.jpg')
# sleep(0.1)

yolo_proc = Popen(["./darknet",
                   "detect",
                   "./cfg/yolov3-tiny.cfg",
                   "./yolov3-tiny.weights",
                   "-thresh","0.1"],
                   stdin = PIPE, stdout = PIPE)

fcntl.fcntl(yolo_proc.stdout.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)

iframe = 0

for frame_file in glob.iglob(args.frames_dir+'/image001.jpeg'):
    try:
        stdout = yolo_proc.stdout.read()
        if 'Enter Image Path' in stdout:
            try:
               # im = cv2.imread('predictions.png')
               copyfile('predictions.png', path.join(args.output_dir, f'frame{iframe:03d}.png'))
               iframe += 1 
               # cv2.imshow('yolov3-tiny',im)
               # key = cv2.waitKey(5)
               
            except Exception:
               pass
            # camera.capture('test.jpg')
            yolo_proc.stdin.write(frame_file+'\n')
        if len(stdout.strip()) > 0:
            print('get %s' % stdout)
    except Exception:
        pass
    print(frame_file)
