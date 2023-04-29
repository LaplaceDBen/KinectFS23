import cv2
import numpy as np

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

    while True:
        capture = k4a.get_capture()

        if np.any(capture.color):
            color_image = np.array(capture.color)
            depth_image = np.array(capture.depth)

            # Convert depth image to grayscale
            depth_image = (depth_image / 40).astype(np.uint8)
            depth_image = cv2.applyColorMap(depth_image, cv2.COLORMAP_RAINBOW)
            gray = cv2.cvtColor(depth_image, cv2.COLOR_BGR2GRAY)

            # Threshold the grayscale image to get a binary mask
            _, mask = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

            # Find contours in the binary mask
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Draw contours and print depth on them
            for contour in contours:
                # Calculate mean depth of contour
                mean_depth = np.mean(depth_image[np.where(mask > 0)])

                # Draw contour and print depth on it
                cv2.drawContours(color_image, [contour], 0, (0, 255, 0), 2)
                cv2.putText(
                    color_image,
                    f"{mean_depth:.2f} mm",
                    tuple(contour[0][0]),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    2,
                )
                print(f"Depth: {mean_depth:.2f} mm")

            cv2.imshow("k4a", color_image[:, :, :3])
            key = cv2.waitKey(10)
            if key != -1:
                cv2.destroyAllWindows()
                break

    k4a.stop()


if __name__ == "__main__":
    main()
