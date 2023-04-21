import cv2
import numpy as np
from pyzbar.pyzbar import decode
import pyk4a
from pyk4a import Config, PyK4A
import time
from datetime import datetime
from config import camera_config
from numba import jit
import logging
import datetime


class QRCodeDetector:
    
    @staticmethod
    def detect_qr_codes(num_obj=5):
        k4a = camera_config

        k4a.start()

        cv2.namedWindow("QR Codes", cv2.WINDOW_NORMAL)

        # Set font and scale for text and coordinates
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1

        # Open log file and write initial timestamp
        log_file = open('logfile.log', 'w')
        log_file.write(f"QR Code Detection Log ({time.strftime('%Y-%m-%d %H:%M:%S')})\n\n")
        

        while True:
            
            frame = k4a.get_capture()
            if frame is not None:
                color_image = frame.color
                decoded_objects = decode(color_image)

                if len(decoded_objects) == num_obj:
                    qr_codes = [obj.data.decode("utf-8") for obj in decoded_objects]
                    coords = [(int(obj.rect.left + obj.rect.width/2), int(obj.rect.top + obj.rect.height/2)) for obj in decoded_objects]
                    #get angle of qr code
                    
                    angles = []

                    # Draw bounding boxes and write qr code text and coordinates on image
                    for i in range(num_obj):
                        obj = decoded_objects[i]
                        cv2.polylines(
                            color_image,
                            [np.array(obj.polygon, np.int32).reshape((-1, 1, 2))],
                            True,
                            (0, 255, 0),
                            2,
                        )
                        cv2.putText(
                            color_image,
                            qr_codes[i],
                            (obj.rect.left, obj.rect.top - 30),
                            font,
                            font_scale,
                            (0, 255, 0),
                            2,
                        )
                        cv2.putText(
                            color_image,
                            f"({coords[i][0]}, {coords[i][1]})",
                            (coords[i][0], coords[i][1] - 10),
                            font,
                            font_scale,
                            (0, 255, 0),
                            2,
                        )

                        # Get qr code angle and write it in the terminal
                        rect = cv2.minAreaRect(np.array(obj.polygon, np.int32))
                        angle = rect[2]
                        angles.append(angle)
                        #print angle rounded with coordinates

                        print(f"{qr_codes[i]} Angle: {round(angle, 2)} ({coords[i][0]}, {coords[i][1]})")

                        # Write terminal output to log file
                        log_file.write(f"{qr_codes[i]} ({coords[i][0]}, {coords[i][1]}) Angle: {round(angles[i], 2)} ")
                        

                    
                    # Write timestamp to log file
                #og_file.write(f"({datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]})\n")
                log_file.flush()

                print("\nNext Search: ", datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3])

                cv2.imshow("QR Codes", color_image)
                cv2.resizeWindow("QR Codes", (color_image.shape[1], color_image.shape[0]))

            key = cv2.waitKey(1) #wait for 1ms the loop will start again and we will process the next frame
            if key == 27 or key == 127: # Quit on Esc or Delete key
                k4a.stop()
                log_file.close()
                break

        k4a.stop()
        log_file.close()


class QR_Detector_3:
    def __init__(self, num_objects):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler('QR_Detection.log')
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.num_objects = num_objects
        self.k4a = None
        self.log_window = None 

    def start(self):
        self.k4a = pyk4a.PyK4A(
            pyk4a.Config(
                color_resolution=pyk4a.ColorResolution.RES_1080P,
                depth_mode=pyk4a.DepthMode.NFOV_UNBINNED,
                synchronized_images_only=True,
            )
        )
        if not self.k4a.start():
            print("No camera detected")
            self.k4a = None

        while self.k4a:
            timestamp = time.time()
            color_image = self.k4a.get_last_color_image()
            if color_image is not None:
                binary_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
                _, binary_image = cv2.threshold(binary_image, 128, 255, cv2.THRESH_BINARY)
                objects = pyzbar.decode(binary_image)

                if len(objects) == self.num_objects:
                    log_line = f"{timestamp}"
                    for i, obj in enumerate(objects):
                        log_line += f", {obj.data.decode('utf-8')}, {obj.rect}, {obj.angle}"

                    self.logger.info(log_line)

                self.k4a.release_last_color_image()

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()
        if self.k4a is not None:
            self.k4a.stop()
            self.k4a = None
            self.logger.handlers.clear()

    def stop(self):
        self.k4a.stop()
        self.k4a = None
        self.logger.handlers.clear()



class QR_Detector_4:
    def __init__(self, num_objects):
        self.num_objects = num_objects
        
        # Set up logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler('QR_Detection.log')
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def run(self, camera_config,display=False):
        # Start the K4A camera
        k4a = camera_config
        
        # Try to start the camera, log an error and exit if it fails
        if not k4a.start():
            print("No camera detected.")
            self.logger.error("No camera detected.")
            return

        while True:
            timestamp = time.time()
            color_image = k4a.get_capture(convert_to_numpy=True).color
            if color_image is not None:
                binary_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
                _, binary_image = cv2.threshold(binary_image, 128, 255, cv2.THRESH_BINARY)
                objects = pyzbar.decode(binary_image)

                if len(objects) == self.num_objects:
                    log_line = f"{timestamp}"
                    for i, obj in enumerate(objects):
                        log_line += f", {obj.data.decode('utf-8')}, {obj.rect}, {obj.angle}"
                        if display:
                            cv2.putText(color_image, f"{i}: {obj.data.decode('utf-8')}", (obj.rect.left, obj.rect.top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                            cv2.drawContours(color_image, [obj.polygon.astype(int)], 0, (0, 255, 0), 2)
                            cv2.line(color_image, (obj.rect.left, obj.rect.top), (obj.rect.left + obj.rect.width, obj.rect.top + obj.rect.height), (0, 255, 0), 2)
                            cv2.line(color_image, (obj.rect.left + obj.rect.width, obj.rect.top), (obj.rect.left, obj.rect.top + obj.rect.height), (0, 255, 0), 2)

                    self.logger.info(log_line)

                if display:
                    cv2.imshow("QR Detector", color_image)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

                k4a.release_capture()

        cv2.destroyAllWindows()

    def stop(self):
        k4a.stop()
        self.logger.handlers.clear()







'''
QRCodeDetector.detect_qr_codes(num_obj=5)
detector = QR_Detector_3(num_objects=5)
detector.run(display=True)
detector.stop()
'''

