import time
import os

def readFile(path):
    with open(path, "r", encoding="utf8") as file:
        print(file.read())


logPath = r"C:\Users\rapha\OneDrive\Desktop\CDS_FS23\Projektarbeit\GitHub\KinectFS23\raffi\qr_codes_test.log"
# readFile(logPath)


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
    print(line)


# Letzte Zeile printen
# with open(logPath, "r", encoding="utf8") as file:
#     lines = file.readlines()
#     last_line = lines[-1].strip()
#     print(last_line)g