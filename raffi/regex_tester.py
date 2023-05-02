import os
import time
import re
# import keyboard

log_path = r"raffi\qr_codes_test.log"

def follow(path):
    with open(path, "r", encoding="utf8") as file:
        file.seek(0, os.SEEK_END)
        while True:
            line = file.readline()
            if not line:
                time.sleep(0.01)
                continue
            yield line

for line in follow(log_path):
    objects = re.findall(r"QRCODE:\s([\w]+),\s\((\d+),\s(\d+)\),\s([\d\.]+)\s\|\s", line)
    for object in objects:
        print(f"Name: {object[0]}, X-Koordinate: {object[1]}, Y-Koordinate: {object[2]}, Rotation: {object[3]}")
        if object[0] == 'Haus_A':
            print('MOVING HOUSE A!\n')
        if object[0] == 'Haus_B':
            print('MOVING HOUSE B!\n')
        if object[0] == 'Baum':
            print('Moving Tree!\n')
    # if keyboard.is_pressed('q'):
    #     break

