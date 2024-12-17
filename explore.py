from os import listdir
from os.path import isfile, join
import cv2

for f in listdir("GIFS"):
    if isfile(join("GIFS", f)):
        print(f)
        gif = cv2.VideoCapture("GIFS/"+f)
        length = int(gif.get(cv2.CAP_PROP_FRAME_COUNT))
        print(f"{f} length {length}")
        gif.release()

