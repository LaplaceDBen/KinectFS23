import cv2
import numpy as np

import pyk4a
from pyk4a import Config, PyK4A


def main():
    k4a = PyK4A(
        Config(
            color_resolution=pyk4a.ColorResolution.RES_720P,
            depth_mode=pyk4a.DepthMode.NFOV_UNBINNED,
            synchronized_images_only=True,
        )
    )
    k4a.start()

    # getters and setters directly get and set on device
    k4a.whitebalance = 4500
    assert k4a.whitebalance == 4500
    k4a.whitebalance = 4510
    assert k4a.whitebalance == 4510

#ChatGPTSnipped
    while 1:
        capture = k4a.get_capture()
        if np.any(capture.color):
            # Convert the color image to grayscale
            gray = cv2.cvtColor(capture.color[:, :, :3], cv2.COLOR_BGR2GRAY)

            # Detect edges using Canny
            edges = cv2.Canny(gray, 100, 200)

            # Find contours of objects
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Initialize the output array with the same dimensions and data type as the input image
            result = np.zeros_like(capture.color[:, :, :3])

            # Draw edges and contours on the output array
            cv2.drawContours(result, contours, -1, (0, 255, 0), 2)

            # Convert the output array to RGB and show the result
            result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
            cv2.imshow("k4a", result)

            key = cv2.waitKey(10)
            if key != -1:
                cv2.destroyAllWindows()
                break

    k4a.stop()


if __name__ == "__main__":
    main()
