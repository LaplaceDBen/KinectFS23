import cv2
import numpy as np
import time

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

    count = 0
    while True:
        capture = k4a.get_capture()

        if np.any(capture.color):
            # Get the dimensions of the color image
            height, width, _ = capture.color.shape

            # Calculate the number of pixels to be clipped on each side
            clip_pixels = int(width * 0.25)

            # Perform cropping
            cropped_image = capture.color[:, clip_pixels:-clip_pixels, :]

            cv2.imshow("k4a", cropped_image)
            key = cv2.waitKey(10)
            if key != -1:
                cv2.destroyAllWindows()
                break

    k4a.stop()


if __name__ == "__main__":
    main()
