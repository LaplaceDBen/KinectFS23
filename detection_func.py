import cv2
import numpy as np
from pyzbar.pyzbar import decode
from pyzbar import pyzbar
from config import camera_config
import pyk4a
from pyk4a import Config, PyK4A
import logging
from datetime import datetime


class QRCodeDetector_old:

    @staticmethod
    def detect_qr_codes(num_obj=5):
        k4a = camera_config

        k4a.start()

        cv2.namedWindow("QR Codes", cv2.WINDOW_NORMAL)

        # Set font and scale for text and coordinates
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1

        # Set up logging
        logging.basicConfig(filename='logfile.log', level=logging.INFO, format='%(asctime)s - %(message)s')
        logging.info(f"QR Code Detection Log ({datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})\n\n")

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

                        # Get qr code angle and write it to the log
                        rect = cv2.minAreaRect(np.array(obj.polygon, np.int32))
                        angle = rect[2]
                        angles.append(angle)
                        logging.info(f"{qr_codes[i]} ({coords[i][0]}, {coords[i][1]}) Angle: {round(angles[i], 2)} ")

                    # Write timestamp to the log
                    logging.info(f"({datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]})\n")
                    
                # Display the image with the detected QR codes
                cv2.imshow("QR Codes", color_image)
                cv2.resizeWindow("QR Codes", (color_image.shape[1], color_image.shape[0]))

            key = cv2.waitKey(1) #wait for 1ms the loop will start again and we will process the next frame
            if key == 27 or key == 127: # Quit on Esc or Delete key
                k4a.stop()
                break

        k4a.stop()
        logging.info("QR Code Detection ended\n")




class QRCodeDetector:
    def __init__(self, num_qr_codes, config):
        self.num_qr_codes = num_qr_codes

        # Set up logging
        logging.basicConfig(filename='qr_codes.log', level=logging.INFO, format='%(message)s')

        # Initialize PyK4A
        self.k4a = config
                
        self.k4a.start()

    def detect_qr_codes(self):
        # Capture a frame from the camera
        capture = self.k4a.get_capture()
        if capture.color is not None:
            # Convert the color image to grayscale for QR code detection
            gray = cv2.cvtColor(capture.color, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            

            
            wait = cv2.waitKey(1)
            # Detect QR codes in the grayscale image
            qr_codes = pyzbar.decode(thresh)

            # Check if the required number of QR codes has been found
            
            print(len(qr_codes))
            if len(qr_codes) >= self.num_qr_codes:
                # Write the QR code information to the log file
                qr_codes_info = ''
                for qr_code in qr_codes:
                    qr_code_data = qr_code.data.decode()
                    qr_code_rect = qr_code.rect
                    #center of qr code
                    qr_code_center = (qr_code_rect[0] + qr_code_rect[2] // 2, qr_code_rect[1] + qr_code_rect[3] // 2)
                    qr_code_polygon = qr_code.polygon

                    # Calculate orientation angle using QR code polygon
                    x1, y1 = qr_code_polygon[0]
                    x2, y2 = qr_code_polygon[1]
                    x3, y3 = qr_code_polygon[2]
                    x4, y4 = qr_code_polygon[3]
                    angle = np.rad2deg(np.arctan2(y2-y1, x2-x1))

                    qr_codes_info += f'{qr_code.type}: {qr_code_data}, {qr_code_center}, {angle:.2f} | '
                    cv2.putText(gray, qr_code_data, (qr_code_rect[0], qr_code_rect[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
                    cv2.namedWindow("QR Code Detector", cv2.WINDOW_NORMAL)
                    cv2.resizeWindow("QR Code Detector", 1080,1080)
                    
                    cv2.imshow("QR Code Detector", gray)
                logging.info(f'{qr_codes_info}{datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")}')

        # Release the capture object
        del capture

    def stop(self):
        # Stop the camera capture
        self.k4a.stop()
