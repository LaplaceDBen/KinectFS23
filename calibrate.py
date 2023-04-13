import cv2
import numpy as np
from pyk4a import Config, PyK4A
import pyk4a
from pyzbar.pyzbar import decode
from PySide6.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox

def detect_objects():
    # Create application and main window
    app = QApplication([])
    window = QWidget()
    layout = QVBoxLayout()
    window.setLayout(layout)

    # Create input field and button
    input_label = QLabel("Enter the number of objects:")
    input_field = QLineEdit()
    button = QPushButton("Detect Objects")

    # Add input field and button to layout
    layout.addWidget(input_label)
    layout.addWidget(input_field)
    layout.addWidget(button)

    # Show window
    window.show()

    # Wait for button to be clicked
    def on_button_clicked():
        # Get the number of objects from the input field
        num_objects = int(input_field.text())

        # Initialize K4A camera
        k4a = PyK4A(
            Config(
                color_resolution=pyk4a.ColorResolution.RES_1080P,
                depth_mode=pyk4a.DepthMode.NFOV_UNBINNED,
                synchronized_images_only=True,
            )
        )
        k4a.start()

        # Detect QR codes
        qr_codes = []
        while len(qr_codes) < num_objects:
            # Get synchronized capture from camera
            capture = k4a.get_capture()

            # Extract color image from capture
            color_image = capture.color

            # Decode QR codes from color image
            qr_codes = decode(cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY))

            # Show error message if more QR codes found
            if len(qr_codes) > num_objects:
                QMessageBox.warning(
                    window,
                    "Error",
                    "More QR codes found than expected. Please recalibrate.",
                )

        # Stop the camera
        k4a.stop()

        # Show error message if fewer QR codes found
        if len(qr_codes) < num_objects:
            QMessageBox.warning(
                window,
                "Error",
                "Could not find all objects. Please try again.",
            )

        # Return the number of objects found
        return len(qr_codes)

    button.clicked.connect(on_button_clicked)

    # Start event loop
    app.exec_()


detect_objects()