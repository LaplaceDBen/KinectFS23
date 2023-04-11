import cv2
import numpy as np
from pyk4a import Config, PyK4A
import pyk4a
from

def detect_contour(max_area, max_contour):
    # Initialize K4A camera
    k4a = PyK4A(
        Config(
            color_resolution=pyk4a.ColorResolution.RES_1080P,
            depth_mode=pyk4a.DepthMode.NFOV_UNBINNED,
            synchronized_images_only=True,
        )
    )
    k4a.start()

    while True:
        # Get a capture from the camera
        capture = k4a.get_capture()
        frame = capture.color[:, :, :3]
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

        # Convert the input image to 8-bit single channel image
        img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        img_gray = cv2.GaussianBlur(img_gray, (5, 5), 0)

        # Apply a threshold to the image
        ret, thresh = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

        # Find contours in the image
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Iterate over all contours and compute their similarity to the max_contour
        for contour in contours:
            # Compute the similarity between the current contour and the max_contour
            similarity = cv2.matchShapes(max_contour, contour, cv2.CONTOURS_MATCH_I3, 0)
            # Print the similarity score and draw the contour on the image
            print(f"Contour similarity: {similarity}")
            cv2.drawContours(frame, [contour], -1, (0, 0, 255), 2)

        # Show the image with all the detected contours
        cv2.imshow("Contour detection", frame)

        # Exit the loop if the user presses the 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close all windows
    k4a.stop()
    cv2.destroyAllWindows()

max_area, max_contour = detect_area()
detect_contour(max_area, max_contour)
