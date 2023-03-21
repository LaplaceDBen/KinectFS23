import cv2
import numpy as np
import time
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def edge_detection_comparison():
    cap = cv2.VideoCapture(0)
    


    c =[]
    l =[]
    s_x =[]
    s_y =[]
    sc_x =[]
    sc_y =[]
    # Apply different edge detection methods and measure their execution time
    i=0
    while i <1000:
        ret, frame = cap.read() # read a frame from the camera
        
        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur to the frame to reduce noise
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        
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
        c.append((t2 - t1)*1000)
        l.append((t3 - t2)*1000)
        s_x.append((t4 - t3)*1000)
        s_y.append((t5 - t4)*1000)
        sc_x.append((t6 - t5)*1000)
        sc_y.append((t7 - t6)*1000)
        i += 1
        print(i)

    # Print the execution times for each method
    print(f"Canny edge detection execution time: {np.mean(c):.6f} ms")
    print(f"Laplacian edge detection execution time: {np.mean(l):.6f} ms")
    print(f"Sobel edge detection execution time: {np.mean(s_x):.6f} ms")
    print(f"Sobel_y edge detection execution time: {np.mean(s_y):.6f} ms")
    print(f"Scharr_x edge detection execution time: {np.mean(sc_x):.6f} ms")
    print(f"Scharr_y edge detection execution time: {np.mean(sc_y):.6f} ms")

    #histogram of each method
    plt.figure(figsize=(10, 8))
    plt.hist(c, bins=20, label='Canny')
    plt.hist(l, bins=20, label='Laplacian')
    plt.hist(s_x, bins=20, label='Sobel_x')
    plt.hist(s_y, bins=20, label='Sobel_y')
    plt.hist(sc_x, bins=20, label='Scharr_x')
    plt.hist(sc_y, bins=20, label='Scharr_y')
    plt.xlabel('Execution time (ms)')
    plt.ylabel('Frequency')
    plt.legend()
    plt.show()


    #plot the execution times for each method in an ecdf plot

    sns.set_style("whitegrid")
    plt.figure(figsize=(10, 8))
    plt.plot(np.sort(c), np.linspace(0, 1, len(c), endpoint=False), label='Canny')
    plt.plot(np.sort(l), np.linspace(0, 1, len(l), endpoint=False), label='Laplacian')
    plt.plot(np.sort(s_x), np.linspace(0, 1, len(s_x), endpoint=False), label='Sobel_x')
    plt.plot(np.sort(s_y), np.linspace(0, 1, len(s_y), endpoint=False), label='Sobel_y')
    plt.plot(np.sort(sc_x), np.linspace(0, 1, len(sc_x), endpoint=False), label='Scharr_x')
    plt.plot(np.sort(sc_y), np.linspace(0, 1, len(sc_y), endpoint=False), label='Scharr_y')
    plt.xlabel('Execution time (ms)')
    plt.ylabel('ECDF')
    plt.legend()
    plt.show()


    #make a boxplot of each method

    plt.figure(figsize=(10, 8))
    plt.boxplot([c, l, s_x, s_y, sc_x, sc_y], labels=['Canny', 'Laplacian', 'Sobel_x', 'Sobel_y', 'Scharr_x', 'Scharr_y'])
    plt.xlabel('Edge detection method')
    plt.ylabel('Execution time (ms)')
    plt.show()

    






edge_detection_comparison()
