import cv2
import numpy as np
from pyzbar.pyzbar import decode
from pyzbar import pyzbar
from config import camera_config
import pyk4a
from pyk4a import Config, PyK4A
import logging
from datetime import datetime
import time
import matplotlib.pyplot as plt

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
    def __init__(self, num_qr_codes, t, config):
        self.num_qr_codes = num_qr_codes

        # Set up logging
        logging.basicConfig(filename='qr_codes.log', level=logging.INFO, format='%(message)s')
        self.threashold = t

        # Initialize PyK4A
        self.k4a = config
                
        self.k4a.start()

    def detect_qr_codes(self):
        # Capture a frame from the camera
        capture = self.k4a.get_capture()
        if capture.color is not None:
            # Convert the color image to grayscale for QR code detection
            gray = cv2.cvtColor(capture.color, cv2.COLOR_BGR2GRAY)
            #_, thresh = cv2.threshold(gray, self.threashold, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)slower filter
            _, thresh = cv2.threshold(gray, j, 255, cv2.THRESH_TRUNC)
            

            
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




class QRCodeDetector_time:
    def __init__(self, num_qr_codes):
        self.num_qr_codes = num_qr_codes
        # Initialize PyK4A
        self.k4a = camera_config
                
        self.k4a.start()

    def detect_qr_codes_avg(self):
        thresh_values = [51,53,55,57,59,61,63,65,67,69,71,73,75,77,79,
                         81,83,85,87,89,91,93,95,97,99,101,103,105,107,109,111,113,115,117,119,121,123,125,127,129,131,133,135,137,
                         139,141,143,145,147,149,151,153,155,157,159,161,163,165,167,169,171,173,175,177,179,181,183,185,187,189,191,
                         193,195,197,199,201,203,205,207,209,211,213,215,217,219,221,223,225,227,229,231,233,235,237,239,241,243,245,
                         247,249,251,253,255]
        min_avg_time = float('inf')
        min_std_time = float('inf')
        best_thresh = None
        avg_times = []
        std_times = []
        for j in thresh_values:
            print(j)
            times = []
            for i in range(10):
                start_time = time.time()
                detected_qr_codes = 0
                while detected_qr_codes < self.num_qr_codes:
                    # Capture a frame from the camera
                    capture = self.k4a.get_capture()
                    if capture.color is not None:
                        # Convert the color image to grayscale for QR code detection
                        gray = cv2.cvtColor(capture.color, cv2.COLOR_BGR2GRAY)
                        _, thresh = cv2.threshold(gray, j, 255, cv2.THRESH_TRUNC) 
                        #if a pixel value in the source image is greater than the threshold value, it is set to the threshold value. Otherwise, it remains unchanged.
                        #_, thresh = cv2.threshold(gray, j, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
                        #Otsu’s binarization method is used to automatically determine an optimal threshold value based on the image histogram. Then, THRESH_BINARY is applied using this optimal threshold value. 
                        #This means that if a pixel value in the source image is greater than the threshold value, it is set to the maximum value (in this case 255). 
                        # Otherwise, it is set to 0.
                        
                        wait = cv2.waitKey(1)
                        # Detect QR codes in the grayscale image
                        qr_codes = pyzbar.decode(thresh)
                        detected_qr_codes += len(qr_codes)
                    if time.time() - start_time > 1:
                        break
                end_time = time.time()
                times.append(end_time - start_time)
            avg_time = np.mean(times)
            std_time = np.std(times)
            avg_times.append(avg_time)
            std_times.append(std_time)
            
            
            print(f'avg_time: {avg_time:.4f} sec,std: {std_time:.4f} sec')
            
            if avg_time < min_avg_time:
                min_avg_time = avg_time
                min_std_time = std_time
                best_thresh = j
        
        
        minus_one_std = [avg_time - std_time for avg_time in avg_times]
        plus_one_std = [avg_time + std_time for avg_time in avg_times]
        plt.plot(thresh_values, avg_times, color='red',  linestyle='solid', linewidth=2, markersize=8)
        plt.plot(thresh_values, minus_one_std, '--', color='blue')
        plt.plot(thresh_values, plus_one_std, '--', color='blue')
        plt.fill_between(thresh_values, minus_one_std, plus_one_std, alpha=0.2, color='lightblue')
        #add another line
        plt.xlabel('Threshold Value')
        #add grid
        plt.grid(True)
        plt.ylabel('Average Time (sec)')
        plt.title('Average Time vs Threshold Value- Binarization Method: Trunc')
        ax = plt.gca()
        # Find the minimum y value and its corresponding x value
        min_y = min(avg_times)
        min_x = thresh_values[avg_times.index(min_y)]

        # Add an arrow annotation at the minimum value
        plt.annotate(f'{min_y:.4f} sec', xy=(min_x,min_y), xytext=(min_x+10,min_y+0.1), arrowprops=dict(facecolor='black', arrowstyle='->'))

        # Get the maximum x and y values
        xmax = ax.get_xlim()[1]
        ymax = ax.get_ylim()[1]
        #add legend top left
        plt.legend(['Average Time', 'Average Time - 1 std', 'Average Time + 1 std'], loc='upper right')

        plt.show()
        self.k4a.stop()
        
        return best_thresh,  min_avg_time, min_std_time



