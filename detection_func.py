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



class QRCodeDetector_2:
    
    @staticmethod
    def detect_qr_codes(num_obj=5):
        k4a = camera_config
        k4a.start()

        cv2.namedWindow("QR Codes", cv2.WINDOW_NORMAL)
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1

        # Create logger and log file
        logger = logging.getLogger("QR Code Detection Log")
        logger.setLevel(logging.DEBUG)
        log_format = logging.Formatter('%(asctime)s - %(message)s')
        file_handler = logging.FileHandler('logfile.log')
        file_handler.setFormatter(log_format)
        logger.addHandler(file_handler)

        logger.info(f"QR Code Detection Log ({time.strftime('%Y-%m-%d %H:%M:%S')})\n\n")
        
        while True:
            frame = k4a.get_capture()
            if frame is None:
                continue

            color_image = frame.color
            decoded_objects = decode(color_image)

            if len(decoded_objects) != num_obj:
                continue

            qr_codes, coords, angles = [], [], []
            for obj in decoded_objects:
                qr_code = obj.data.decode("utf-8")
                qr_codes.append(qr_code)

                coord = (int(obj.rect.left + obj.rect.width/2), int(obj.rect.top + obj.rect.height/2))
                coords.append(coord)

                rect = cv2.minAreaRect(np.array(obj.polygon, np.int32))
                angle = rect[2]
                angles.append(angle)

                cv2.polylines(
                    color_image,
                    [np.array(obj.polygon, np.int32).reshape((-1, 1, 2))],
                    True,(0, 255, 0),2,)
                
                cv2.putText(
                    color_image,qr_code,(obj.rect.left, obj.rect.top - 30),
                    font,font_scale,(0, 255, 0),2,)
                
                cv2.putText(
                    color_image,f"({coord[0]}, {coord[1]})",(coord[0], coord[1] - 10),font,
                    font_scale,(0, 255, 0),2,)

                logger.info(f"{qr_code} ({coord[0]}, {coord[1]}) Angle: {round(angle, 2)} ")
                print(f"{qr_code} Angle: {round(angle, 2)} ({coord[0]}, {coord[1]})")

            logger.handlers[0].flush()
            print("\nNext Search: ", datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3])

            cv2.imshow("QR Codes", color_image)
            cv2.resizeWindow("QR Codes", (color_image.shape[1], color_image.shape[0]))

            key = cv2.waitKey(1)
            if key in [27, 127]:
                k4a.stop()
                logger.handlers[0].close()
                break

        k4a.stop()
        logger.handlers[0].close()


class QR_Detector_3:
    def __init__(self, num_objects):
        self.logger = logger.Logger()
        self.num_objects = num_objects
    
    def run(self):
        k4a = PyK4A(
            Config(
                color_resolution=pyk4a.ColorResolution.RES_1080P,
                depth_mode=pyk4a.DepthMode.NFOV_UNBINNED,
                synchronized_images_only=True,
            )
        )
        k4a.start()

        while True:
            timestamp = time.time()
            color_image = k4a.get_last_color_image()
            if color_image is not None:
                binary_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
                _, binary_image = cv2.threshold(binary_image, 128, 255, cv2.THRESH_BINARY)
                objects = pyzbar.decode(binary_image)

                if len(objects) == self.num_objects:
                    log_line = f"{timestamp}"
                    for i, obj in enumerate(objects):
                        log_line += f", {obj.data.decode('utf-8')}, {obj.rect}, {obj.angle}"
                    self.logger.log(log_line)

                k4a.release_last_color_image()

    def stop(self):
        self.k4a.stop()
        self.logger.close()








#QRCodeDetector.detect_qr_codes(num_obj=5)
detector = QR_Detector_3(num_objects=5)
detector.stop()

