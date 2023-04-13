import cv2
import numpy as np
from pyk4a import Config, PyK4A
import pyk4a
from pyzbar.pyzbar import decode
import progressbar

def detect_qr_codes():
    # Initialize K4A camera
    k4a = PyK4A(
        Config(
            color_resolution=pyk4a.ColorResolution.RES_1080P,
            depth_mode=pyk4a.DepthMode.NFOV_UNBINNED,
            synchronized_images_only=True,
        )
    )
    k4a.start()

    # Initialize progress bar
    bar = progressbar.ProgressBar(widgets=[
        progressbar.AnimatedMarker(),
        ' ',
        progressbar.Bar(),
        ' ',
        progressbar.Timer(),
    ])

    # Initialize list of found QR codes
    qr_codes = []

    # Search for QR codes for 3 seconds
    for i in range(30):
        # Get color image from K4A camera
        frame = k4a.get_frames(timeout=1000)
        color_image = frame.color

        # Decode QR codes in color image
        decoded_objects = decode(color_image)

        # Draw bounding boxes around QR codes and add them to list
        for obj in decoded_objects:
            qr_codes.append(obj)
            cv2.rectangle(color_image, obj.rect.left_top, obj.rect.right_bottom, (0, 255, 0), 2)

        # Update progress bar
        bar.update(i/29)

    # Close K4A camera
    k4a.stop()

    # Draw progress bar to 100%
    bar.finish()

    # Return number of found QR codes
    return len(qr_codes)

if __name__ == "__main__":
    # Get number of found QR codes
    num_qr_codes = detect_qr_codes()

    # Print number of found QR codes
    print(f"Found {num_qr_codes} QR codes.")