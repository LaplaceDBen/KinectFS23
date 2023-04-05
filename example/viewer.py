import cv2
import numpy as np
import time

import pyk4a
from pyk4a import Config, PyK4A


def main():
    k4a = PyK4A(
        Config(
            color_resolution=pyk4a.ColorResolution.RES_1080P,
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

    count = 0
    while 1:
        capture = k4a.get_capture()

        if np.any(capture.color):
            cv2.imshow("k4a", capture.color[:, :, :3])
            key = cv2.waitKey(10)
            if key != -1:
                cv2.destroyAllWindows()
                break

            # save image every second
            if count % 30 == 0:
                cv2.imwrite(f"image_{count}.png", capture.color[:, :, :3])
                print(f"Saved image_{count}.png")
            count += 1

        # wait for 1 millisecond
        time.sleep(0.033)

    k4a.stop()


if __name__ == "__main__":
    main()
