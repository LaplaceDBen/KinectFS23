import random
import time
from datetime import datetime
import keyboard

logPath = r"raffi\qr_codes_test2.log"

for i in range(4000):
    value1 = random.randint(50, 300)
    value2 = random.randint(50, 300)
    value3 = random.randint(0, 360)
    value4 = random.randint(-300, -50)
    value5 = random.randint(-300, -50)
    value6 = random.randint(0, 360)
    value7 = random.randint(-300, -50)
    value8 = random.randint(50, 300)
    value9 = random.randint(0, 360)
    value10 = random.randint(50, 300)
    value11 = random.randint(-300, -50)
    value12 = random.randint(0, 360)
    value13 = random.randint(-300, 300)
    value14 = random.randint(-300, 300)
    value15 = random.randint(0, 360)


    newLine = f"QRCODE: Baum, ({value7}, {value8}), {value9} | QRCODE: Haus_B, ({value4}, {value5}), {value6} | QRCODE: Haus_A, ({value1}, {value2}), {value3} | QRCODE: Haus_C, ({value10}, {value11}), {value12} | QRCODE: Haus_D, ({value13}, {value14}), {value15} | 16:49:57.222173\n"
    # newLine = f"QRCODE: Haus_A, ({value1}, {value2}), {value3} | 16:49:57.222173\n"
    # newLine = f"QRCODE: Haus_B, ({value4}, {value5}), {value6} | 16:49:57.222173\n"

    with open(logPath, 'a') as f:
        f.write(newLine)
    
    # current_time = datetime.now().time()
    # print(f'Just wrote a line, current time: {current_time}')

    time.sleep(0.001)  # wait for 0.1 seconds before next loop iteration
    