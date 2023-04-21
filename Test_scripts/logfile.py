

import logging
from pyzbar import pyzbar
import cv2
import numpy as np
import pyk4a
from pyk4a import Config, PyK4A





qrcode_detector = QRCodeDetector(num_qr_codes=5)
while True:
    qrcode_detector.detect_qr_codes()
qrcode_detector.stop()


