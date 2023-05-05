import cv2
import numpy as np
from pyzbar.pyzbar import decode
from pyzbar import pyzbar
from config import camera_config
import pyk4a
from pyk4a import Config, PyK4A, ColorControlCommand, ColorControlMode
import logging
from datetime import datetime
import time
import matplotlib.pyplot as plt
from tqdm import tqdm_gui
from config import camera_config
import concurrent.futures
import pandas as pd






class QRCodeDetector:
    def __init__(self, num_qr_codes, t, config, resolution, display=False):
        self.num_qr_codes = num_qr_codes
        self.display = display
        # Set up logging
        logging.basicConfig(filename='qr_codes.log', level=logging.INFO, format='%(message)s')
        self.threashold = t
        # Initialize PyK4A
        self.k4a = config
                
        self.k4a.start()
        
        self.resolution = resolution
        

    def detect_qr_codes(self):
        # Capture a frame from the camera
        while True:
            capture = self.k4a.get_capture()
            if capture.color is not None:
                
                height, width, _ = capture.color.shape

                # Calculate the number of pixels to be clipped on each side
                clip_pixels = int(width * 0.25)

                # Perform cropping
                cropped_image = capture.color[:, clip_pixels:-clip_pixels, :]
                
                gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
                _, thresh = cv2.threshold(gray, self.threashold, 255, cv2.THRESH_TRUNC)
                #thresh2 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 21, 2)

                
                wait = cv2.waitKey(1) #necessary for the camera to work
                # Detect QR codes in the grayscale image
                # Create a thread or process pool
                
                '''
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    # Submit tasks to the pool for parallel execution
                    qr_codes1 = executor.submit(pyzbar.decode, thresh)
                    qr_codes2 = executor.submit(pyzbar.decode, thresh2)
                '''
                qr_codes = pyzbar.decode(thresh)   

                # Retrieve the results from the executed tasks
                #qr_codes1 = qr_codes1.result()
                #qr_codes2 = qr_codes2.result()
                #qr_codes = qr_codes1 if len(qr_codes1) == self.num_qr_codes else qr_codes2
                # Check if the required number of QR codes has been found
                
                print("QR codes with trunc: ", len(qr_codes))
                #print("QR codes with adaptive thresholding: ", len(qr_codes2))
                if len(qr_codes) == self.num_qr_codes:
                    # Write the QR code information to the log file
                    qr_codes_info = ''
                    for qr_code in qr_codes:
                        qr_code_data = qr_code.data.decode()
                        qr_code_rect = qr_code.rect
                        # Center of qr code
                        
                            
                        qr_code_center = ((qr_code_rect[0] + qr_code_rect[2]) // 2, (qr_code_rect[1] + qr_code_rect[3]) // 2)
                        qr_code_polygon = qr_code.polygon
                        orientation = qr_code.orientation
                        factors = {'720p': 1.05, '1080p': 1.05, '2160p': 1.05}
                        factor = factors.get(self.resolution, 1.0)
                        qr_code_center = tuple(int(x * factor) for x in qr_code_center)

                        side = {'DOWN': 0, 'LEFT': 90, 'RIGHT': 180, 'UP': 270}.get(orientation, 0)
                        # Calculate orientation angle using QR code polygon
                        x1, y1 = qr_code_polygon[0]
                        x2, y2 = qr_code_polygon[1]
                        x3, y3 = qr_code_polygon[2]
                        x4, y4 = qr_code_polygon[3]
                        angle = np.rad2deg(np.arctan2(y2-y1, x2-x1)) + side
                        #angle = np.rad2deg(np.arctan2(np.abs(y2-y1), np.abs(x2-x1))) + side # <---- FIX?
                        if self.display:
                            cv2.putText(gray, qr_code_data, (qr_code_rect[0], qr_code_rect[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
                            cv2.namedWindow("QR Code Detector", cv2.WINDOW_NORMAL)
                            cv2.resizeWindow("QR Code Detector", 1080,1080)
                            cv2.imshow("QR Code Detector", thresh)
                    
                        qr_codes_info = ' | '.join([f'{qr_code.type}: {qr_code.data.decode()}, {((qr_code.rect[0] + qr_code.rect[2]) // 2, (qr_code.rect[1] + qr_code.rect[3]) // 2)}, {angle:.2f}' for qr_code in qr_codes]) + ' | '

                    logging.info(f'{qr_codes_info}{datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")}')

            # Release the capture object
            del capture
            del gray
            del thresh


    def stop(self):
        # Stop the camera capture
        self.k4a.stop()
        # Release the camera
        
    def __del__(self):
        self.k4a.stop()





class QRCodeDetector_time:
    def __init__(self, num_qr_codes, config, fast_calibration=False):
        self.num_qr_codes = num_qr_codes
        # Initialize PyK4A
        self.k4a = config
        self.fast_calibration = fast_calibration  
        self.k4a.start()

    def detect_qr_codes_avg(self):
        #thresh_values from 75 to 255
        thresh_values = np.arange(60, 220, 1)
        min_avg_time = float('inf')
        min_std_time = float('inf')
        best_thresh = None
        avg_times = []
        std_times = []
        with tqdm_gui(total=len(thresh_values), desc="Progress",leave=True) as pbar:
            for j in thresh_values:
                print(j)
                times = []
                for i in range(5):
                    start_time = time.time()
                    detected_qr_codes = 0
                    while detected_qr_codes < self.num_qr_codes:
                        # Capture a frame from the camera
                        capture = self.k4a.get_capture()
                        if capture.color is not None:
                            # Convert the color image to grayscale for QR code detection
                            
                            height, width, _ = capture.color.shape

                            # Calculate the number of pixels to be clipped on each side
                            clip_pixels = int(width * 0.25)

                            # Perform cropping
                            cropped_image = capture.color[:, clip_pixels:-clip_pixels, :]
                
                            gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
                            #gray = cv2.cvtColor(capture.color, cv2.COLOR_BGR2GRAY)
                            _, thresh = cv2.threshold(gray, j, 255, cv2.THRESH_TRUNC) 
                            #thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
                            

                            #if a pixel value in the source image is greater than the threshold value, it is set to the threshold value. Otherwise, it remains unchanged.
                            #_, thresh = cv2.threshold(gray, j, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
                            #Otsu’s binarization method is used to automatically determine an optimal threshold value based on the image histogram. Then, THRESH_BINARY is applied using this optimal threshold value. 
                            #This means that if a pixel value in the source image is greater than the threshold value, it is set to the maximum value (in this case 255). 
                            # Otherwise, it is set to 0.
                            
                            wait = cv2.waitKey(1)
                            # Detect QR codes in the grayscale image
                            qr_codes = pyzbar.decode(thresh)
                            detected_qr_codes += len(qr_codes)
                        if time.time() - start_time > 0.5:
                            break
                        end_time = time.time()
                        times.append(end_time - start_time)
                avg_time = np.mean(times)
                std_time = np.std(times)
                avg_times.append(avg_time)
                std_times.append(std_time)
                pbar.update(1)
                
                
                print(f'avg_time: {avg_time:.4f} sec,std: {std_time:.4f} sec')
            
                if avg_time < min_avg_time:
                    min_avg_time = avg_time
                    min_std_time = std_time
                    best_thresh = j
                if self.fast_calibration == True and avg_time > (min_avg_time + min_std_time):
                    self.k4a.stop()
                    pbar.close()
                    plt.close()
                    return best_thresh,  min_avg_time, min_std_time
                    
        
        
        
        pbar.close()
        #force to close the progress bar
        plt.close()
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





class QRCodeDetector_empirical:
    def __init__(self, num_qr_codes, config, fast_calibration=False):
        self.num_qr_codes = num_qr_codes
        self.k4a = config
        self.fast_calibration = fast_calibration
        self.k4a.start()

    def detect_qr_codes_avg(self):
        # Threshold values for different filters
        thresh_values = {
            'Trunc': np.arange(100, 115, 1),
            'Mean_C': np.arange(100, 115, 1),
            'Otsu': np.arange(100, 115, 1),
            'Binary': np.arange(100, 115, 1),
            'Adaptive': np.arange(100, 115, 1)
        }
        
        filters = {
            'Trunc': cv2.THRESH_TRUNC,
            'Mean_C': cv2.ADAPTIVE_THRESH_MEAN_C,
            'Otsu': cv2.THRESH_BINARY | cv2.THRESH_OTSU,
            'Binary': cv2.THRESH_BINARY,
            'Adaptive': cv2.ADAPTIVE_THRESH_MEAN_C
        }
        
        results = {
            'Filter': [],
            'Threshold': [],
            'Average Time (sec)': []
        }
        
        with tqdm_gui(total=len(thresh_values), desc="Progress", leave=True) as pbar:
            for filter_name, thresh_range in thresh_values.items():
                times = []
                for threshold in thresh_range:
                    print(f'Threshold: {threshold} - Filter: {filter_name}')
                    for _ in range(5):
                        start_time = time.time()
                        detected_qr_codes = 0
                        while detected_qr_codes < self.num_qr_codes:
                            capture = self.k4a.get_capture()
                            if capture.color is not None:
                                height, width, _ = capture.color.shape
                                clip_pixels = int(width * 0.25)
                                cropped_image = capture.color[:, clip_pixels:-clip_pixels, :]
                                gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)

                                if filter_name == 'Adaptive':
                                    thresh = cv2.adaptiveThreshold(gray, 255, filters[filter_name], cv2.THRESH_BINARY, 11, 2)
                                else:
                                    _, thresh = cv2.threshold(gray, threshold, 255, filters[filter_name])

                                qr_codes = pyzbar.decode(thresh)
                                detected_qr_codes += len(qr_codes)
                            
                            if time.time() - start_time > 0.5:
                                break
                        end_time = time.time()
                        times.append(end_time - start_time)
                
                avg_time = np.mean(times)
                results['Filter'].extend([filter_name] * len(thresh_range))
                results['Threshold'].extend(thresh_range)
                results['Average Time (sec)'].extend([avg_time] * len(thresh_range))
                pbar.update(1)

                print(f'Avg Time: {avg_time:.4f} sec')
        
        pbar.close()
        plt.close()

        # Convert results to dataframe
        df = pd.DataFrame(results)

        # Save dataframe to CSV
        df.to_csv('threshold_results.csv', index=False)

        self.k4a.stop()

        return df



