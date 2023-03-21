import cv2
import numpy as np
import time

def edge_detection_comparison(img):
    img = cv2.imread(img)
    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to the image to reduce noise
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply different edge detection methods and measure their execution time
    t1 = time.time()
    canny = cv2.Canny(blur, 100, 200)
    t2 = time.time()
    laplacian = cv2.Laplacian(blur, cv2.CV_8U)
    t3 = time.time()
    sobel_x = cv2.Sobel(blur, cv2.CV_8U, 1, 0, ksize=5)
    t4 = time.time()
    sobel_y = cv2.Sobel(blur, cv2.CV_8U, 0, 1, ksize=5)
    t5 = time.time()
    scharr_x = cv2.Scharr(blur, cv2.CV_8U, 1, 0)
    t6 = time.time()
    scharr_y = cv2.Scharr(blur, cv2.CV_8U, 0, 1)
    t7 = time.time()

    # Print the execution times for each method
    print(f"Canny edge detection execution time: {t2 - t1}")
    print(f"Laplacian edge detection execution time: {t3 - t2}")
    print(f"Sobel edge detection execution time: {t5 - t4}")
    print(f"Scharr edge detection execution time: {t7 - t6}")

edge_detection_comparison('images\Formen.jpg')
