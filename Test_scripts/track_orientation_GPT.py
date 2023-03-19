import cv2
import numpy as np

def track_orientation(min_size):
    cap = cv2.VideoCapture(0)

    while True:
        # Capture the video stream
        ret, frame = cap.read()

        # Convert the frame to grayscale and threshold it
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, 127, 255, 0)

        # Find the contours in the thresholded image
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Loop over the contours and draw a minimum bounding box around each one
        for cnt in contours:
            # Get the size of the contour in pixels
            size = cv2.contourArea(cnt)

            # Only track the orientation of objects that are larger than min_size pixels
            if size >= min_size:
                rect = cv2.minAreaRect(cnt)
                box = cv2.boxPoints(rect)
                box = np.int0(box)

                # Draw the contour and the minimum bounding box
                cv2.drawContours(frame,[box],0,(0,0,255),2)

                # Get the orientation angle of the object
                angle = rect[2]

                # Draw the angle on the object
                cv2.putText(frame, str(int(angle)), tuple(box[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Display the video stream with the angle of each object
        cv2.imshow('frame',frame)

        # Exit the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture and close all windows
    cap.release()
    cv2.destroyAllWindows()

# Test the function with a minimum object size of 50 pixels
track_orientation(50)
