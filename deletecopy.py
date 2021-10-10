import os
import glob

jpg_list = glob.glob("./*.jpg")

for path in jpg_list:
    if "コピー.jpg" in path:
        os.remove(path)