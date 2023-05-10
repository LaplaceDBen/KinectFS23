import random
import time
from datetime import datetime

logPath = r"raffi\qr_codes_test2.log"

x_pos = 300
y_pos = 300
rotation = 0

newLine = f"QRCODE: Haus_B, ({x_pos}, {y_pos}), {rotation} | 16:49:57.222173\n"

with open(logPath, 'a') as f:
        f.write(newLine)

print(x_pos, y_pos, rotation)

for i in range(300, 39, -4):
    x_pos = i
    rotation += 5
    rotation = rotation%360
    newLine = f"QRCODE: Haus_B, ({x_pos}, {y_pos}), {rotation} | 16:49:57.222173\n"

    with open(logPath, 'a') as f:
        f.write(newLine)
 
    time.sleep(0.01)

print(x_pos, y_pos, rotation)

for i in range(300, 39, -4):
    y_pos = i
    rotation += 5
    rotation = rotation%360
    newLine = f"QRCODE: Haus_B, ({x_pos}, {y_pos}), {rotation} | 16:49:57.222173\n"

    with open(logPath, 'a') as f:
        f.write(newLine)
 
    time.sleep(0.01)

print(x_pos, y_pos, rotation)

for i in range(40, 301, 4):
    x_pos = i
    rotation += 5
    rotation = rotation%360
    newLine = f"QRCODE: Haus_B, ({x_pos}, {y_pos}), {rotation} | 16:49:57.222173\n"

    with open(logPath, 'a') as f:
        f.write(newLine)
 
    time.sleep(0.01)

print(x_pos, y_pos, rotation)

for i in range(40, 301, 4):
    y_pos = i
    rotation += 5
    rotation = rotation%360
    newLine = f"QRCODE: Haus_B, ({x_pos}, {y_pos}), {rotation} | 16:49:57.222173\n"

    with open(logPath, 'a') as f:
        f.write(newLine)
 
    time.sleep(0.01)

print(x_pos, y_pos, rotation)

    