import time
import os
import re

logPath = r"C:\Users\rapha\OneDrive\Desktop\CDS_FS23\Projektarbeit\GitHubNew\KinectFS23\raffi\qr_codes_test.log"

def follow(path):
    with open(path, "r", encoding="utf8") as file:
        file.seek(0, os.SEEK_END)
        while True:
            line = file.readline()
            print(line)
            if not line:
                time.sleep(0.1)
                continue
            yield line

for line in follow(logPath):
    objects = re.findall(r"QRCODE:\s([\w]+),\s\((\d+),\s(\d+)\),\s([\d\.]+)\s\|\s", line)
    for obj in objects:
        if obj[0] == 'Haus_A':
            house_A = (int(obj[1]), int(obj[2]), float(obj[3]))
            print('House_A:',house_A)
        elif obj[0] == 'Haus_B':
            house_B = (int(obj[1]), int(obj[2]), float(obj[3]))
            print('House_B:',house_B)
        elif obj[0] == 'Haus_C':
            house_C = (int(obj[1]), int(obj[2]), float(obj[3]))
            print('House_C:',house_C)
        elif obj[0] == 'Haus_D':
            house_D = (int(obj[1]), int(obj[2]), float(obj[3]))
            print('House_D ',house_D)
        elif obj[0] == 'Baum':
            tree = (int(obj[1]), int(obj[2]), float(obj[3]))
            print('Tree: ',tree)
