import cv2
import numpy as np
from pyzbar.pyzbar import decode
import pyk4a
from pyk4a import Config, PyK4A
import time
from config import camera_config

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
        log_file = open('qr_code_log.txt', 'w')
        log_file.write(f"QR Code Detection Log ({time.strftime('%Y-%m-%d %H:%M:%S')})\n\n")

        while True:
            frame = k4a.get_capture()
            if frame is not None:
                color_image = frame.color
                decoded_objects = decode(color_image)

                if len(decoded_objects) == num_obj:
                    qr_codes = [obj.data.decode("utf-8") for obj in decoded_objects]
                    coords = [(obj.rect.left, obj.rect.top) for obj in decoded_objects]
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
                        print(f"{qr_codes[i]} Angle: {angle} ({coords[i][0]}, {coords[i][1]})")

                    # Write terminal output to log file
                    log_file.write("QR Codes Found: ")
                    for i in range(num_obj):
                        log_file.write(f"{qr_codes[i]} ({coords[i][0]}, {coords[i][1]}) Angle: {angles[i]} ")
                    log_file.write(f"({time.strftime('%Y-%m-%d %H:%M:%S')})\n")

                    print("\nNext Search: ", time.strftime("%Y-%m-%d %H:%M:%S"))

                cv2.imshow("QR Codes", color_image)
                cv2.resizeWindow("QR Codes", (color_image.shape[1], color_image.shape[0]))

            key = cv2.waitKey(1)
            if key == 27 or key == 127: # Quit on Esc or Delete key
                break

        k4a.stop()
        cv2.destroyAllWindows()





#QRCodeDetector.detect_qr_codes(num_obj=5)
