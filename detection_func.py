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
            _, thresh = cv2.threshold(gray, self.threashold, 255, cv2.THRESH_TRUNC)
            

            
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
        plt.annotate(f'{min_y:.4f} sec', xy=(min_x,min_y), xytext=(min_x+1,min_y+0.1), arrowprops=dict(facecolor='black', arrowstyle='->'))

        # Get the maximum x and y values
        xmax = ax.get_xlim()[1]
        ymax = ax.get_ylim()[1]
        #add legend top left
        plt.legend(['Average Time', 'Average Time - 1 std', 'Average Time + 1 std'], loc='upper right')

        plt.show()
        self.k4a.stop()
        
        return best_thresh,  min_avg_time, min_std_time





class QRCodeDetector_check():
    def __init__(self, num_qr_codes):
        self.num_qr_codes = num_qr_codes
        self.k4a = camera_config
        self.k4a.start()

    def detect_qr_codes(self):
        qr_codes = {}
        attempts = 0
        while len(qr_codes) < self.num_qr_codes:
            frame = self.k4a.get_capture()
            grey = cv2.cvtColor(frame.color, cv2.COLOR_BGR2GRAY)
            if frame is not None:
                color_image = frame.color
                decoded_objects = decode(grey)
                for obj in decoded_objects:
                    qr_codes[obj.data.decode('utf-8')] = obj.type
            attempts += 1
            if attempts >= 100:
                raise Exception(f"Failed to find {self.num_qr_codes} different QR codes after {attempts} attempts")
        
        with open('objects.txt', 'w') as f:
            for key, value in qr_codes.items():
                f.write(f'{key}: {value}\n')
        
        self.k4a.stop()
        return attempts, len(qr_codes)
