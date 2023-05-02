import random
import time

logPath = r"C:\Users\benit\Desktop\qr_codes_test.log"

for i in range(2000):
    value1 = random.randint(10, 500)
    value2 = random.randint(10, 500)
    value3 = random.randint(30, 60)
    newLine = f"QRCODE: Haus_B, (1,1),1 | QRCODE: Baum, (1569, 677), 87.22 | QRCODE: Haus_D, ({value1}, {value2}), {value3} | QRCODE: Haus_D, (1835, 1246), 87.12 | QRCODE: Haus_C, (1296, 1284), 89.24 | 2023-04-21 19:25:39.979248\n"
    
    with open(logPath, 'a') as f:
        f.write(newLine)
        
    time.sleep(0.01)  # wait for 0.1 seconds before next loop iteration
    