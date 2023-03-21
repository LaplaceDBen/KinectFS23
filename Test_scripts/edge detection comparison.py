import cv2
import numpy as np
import time
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def edge_detection_comparison(img):
    img = cv2.imread(img)
    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to the image to reduce noise
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    


    c =[]
    l =[]
    s_x =[]
    s_y =[]
    sc_x =[]
    sc_y =[]
    # Apply different edge detection methods and measure their execution time
    i=0
    while i <1000:
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
    plt.savefig('images\edge_detection_comparison.png')

    #plot the mean and std of the execution times for each method 

    sns.set_style("whitegrid")
    plt.figure(figsize=(10, 8))
    plt.bar(['Canny', 'Laplacian', 'Sobel_x', 'Sobel_y', 'Scharr_x', 'Scharr_y'], 
            [np.mean(c), np.mean(l), np.mean(s_x), np.mean(s_y), np.mean(sc_x), np.mean(sc_y)],
              yerr=[np.std(c), np.std(l), np.std(s_x), np.std(s_y), np.std(sc_x), np.std(sc_y)], capsize=10)
    plt.xlabel('Edge detection method')
    plt.ylabel('Execution time (ms)')
    plt.title('Mean and std of the execution times for each method')
    plt.show()
    plt.savefig('images\edge_detection_comparison_mean_std.png')




edge_detection_comparison('images\Formen.jpg')
