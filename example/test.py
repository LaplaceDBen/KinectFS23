import cv2
import numpy as np

import pyk4a
from helpers import colorize
from pyk4a import Config, PyK4A

def main():
    k4a = PyK4A(
        Config(
            color_resolution=pyk4a.ColorResolution.OFF,
            depth_mode=pyk4a.DepthMode.NFOV_UNBINNED,
            synchronized_images_only=False,
        )
    )
    k4a.start()

    # getters and setters directly get and set on device
    k4a.whitebalance = 4500
    assert k4a.whitebalance == 4500
    k4a.whitebalance = 4510
    assert k4a.whitebalance == 4510

    while True:
        capture = k4a.get_capture()
        if np.any(capture.depth):
            # Convert depth image to a normalized 8-bit image
            depth_norm = cv2.normalize(capture.depth, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8UC1)

            # Apply a threshold to create a binary image
            _, threshold = cv2.threshold(depth_norm, 100, 255, cv2.THRESH_BINARY)

            # Find contours in the binary image
            contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            closest_depth = float('inf')

            # Loop through each contour
            for contour in contours:
                # Calculate the depth of the object by finding the mean depth value within the contour
                mask = np.zeros_like(capture.depth)
                cv2.drawContours(mask, [contour], 0, 255, -1)
                depth_values = capture.depth[np.where(mask > 0)]
                depth = np.mean(depth_values)

                if depth < closest_depth:
                    closest_depth = depth

            # Write the closest depth in black
            cv2.putText(depth_norm, f"Depth: {closest_depth:.2f} mm", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

            cv2.imshow("k4a", colorize(depth_norm, (None, 5000), cv2.COLORMAP_HSV))
            key = cv2.waitKey(10)
            if key != -1:
                cv2.destroyAllWindows()
                break

    k4a.stop()

if __name__ == "__main__":
    main()
