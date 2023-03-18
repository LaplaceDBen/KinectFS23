from pyk4a import PyK4A, connected_device_count
import numpy as np
import pandas as pd
import cv2

def devices():
    cnt = connected_device_count()
    if not cnt:
        print("No devices available")
        exit()
    print(f"Available devices: {cnt}")
    for device_id in range(cnt):
        device = PyK4A(device_id=device_id)
        device.open()
        print(f"{device_id}: {device.serial}")
        device.close()
        return device_id
    
def detect_objects(image_path, accuracy_threshold, max_size_ratio):
    # ChatGPT
    image = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Threshold the image
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Find contours in the image
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Create a list to store the size, centerpoint, and accuracy of each object
    objects = []

    # Iterate through the contours and append the size, centerpoint, and accuracy to the objects list
    for contour in contours:
        # Get the area of the contour
        area = cv2.contourArea(contour)

        # Skip contours with zero area
        if area == 0:
            continue

        # Get the moments of the contour
        moments = cv2.moments(contour)

        # Calculate the centroid of the contour
        cx = int(moments['m10'] / moments['m00'])
        cy = int(moments['m01'] / moments['m00'])

        # Get the perimeter of the contour
        perimeter = cv2.arcLength(contour, True)

        # Approximate the shape of the contour as a polygon
        approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)

        # Calculate the number of vertices in the polygon
        vertices = len(approx)

        # Calculate the accuracy of the polygon to a square
        accuracy = abs(1 - (area / (perimeter ** 2 / 4)))

        # Check if the object is too large
        height, width = image.shape[:2]
        size_ratio = area / (height * width)
        if size_ratio > max_size_ratio:
            continue

        # Append the size, centerpoint, and accuracy to the objects list
        objects.append([area, (cx, cy), accuracy])

        # Draw the contour and centerpoint if the accuracy is above the threshold
        if accuracy > accuracy_threshold:
            cv2.drawContours(image, [contour], -1, (255, 255, 255), 2)
            cv2.drawMarker(image, (cx, cy), (0, 0, 255), cv2.MARKER_CROSS, 10, 2)
            #add area to contour on image 
            cv2.putText(image, str(area), (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)



    # Create a Pandas dataframe from the objects list
    df = pd.DataFrame(objects, columns=["Size", "Centerpoint", "Accuracy"])

    # Return the dataframe and the image with selected objects drawn on it
    return df, image
