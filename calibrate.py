import cv2
import numpy as np
from pyk4a import Config, PyK4A
import pyk4a

def detect_area():
    # Initialize K4A camera
    k4a = PyK4A(
        Config(
            color_resolution=pyk4a.ColorResolution.RES_720P,
            depth_mode=pyk4a.DepthMode.NFOV_UNBINNED,
            synchronized_images_only=True,
        )
    )
    k4a.start()

    # Get a capture from the camera
    capture = k4a.get_capture()
    frame = capture.color[:, :, :3]
    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
    
    # Let the user select an ROI
    cv2.namedWindow("Select Object to Detect")
    cv2.resizeWindow("Select Object to Detect", 640, 480)
    roi = cv2.selectROI("Select Object to Detect", frame)

    # Crop the image to the selected ROI
    img_roi = frame[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]
    # Convert the input image to 8-bit single channel image
    img_roi_gray = cv2.cvtColor(img_roi, cv2.COLOR_BGR2GRAY)
    img_roi_gray = cv2.GaussianBlur(img_roi_gray, (5, 5), 0)

    # Apply a threshold to the image
    ret, thresh = cv2.threshold(img_roi_gray, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    edges = cv2.Canny(img_roi_gray, 100, 200)

    # Find contours in the image
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the contour with the largest area, which should be a rectangle
    max_area = 0
    max_contour = None
    for contour in contours:
        #fit a bounding box to the contour
        x,y,w,h = cv2.boundingRect(contour)
        area = w*h

        # Check if the contour is a rectangle by comparing its aspect ratio
        if area > max_area:
            max_area = area
            max_contour = contour

    # Draw the contour with the largest area on the original image
    contour_offset_x = int(roi[0])
    contour_offset_y = int(roi[1])
    cv2.drawContours(frame, [max_contour + (contour_offset_x, contour_offset_y)], -1, (0, 255, 0), 2)

    # Show the original image with the selected ROI and the contour with the largest area
    cv2.imshow("Select Model", frame)
    cv2.waitKey(0)

    # Release the camera and close all windows
    k4a.stop()
    cv2.destroyAllWindows()

    return max_area
