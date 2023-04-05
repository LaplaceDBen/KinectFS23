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
            edges = cv2.Canny(gray, 90, 110)

            # Find contours of objects
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            #print number of contorus who are within 5% of max area
            #contour circa 530
            max_area = 42733



            # Initialize the output array with the same dimensions and data type as the input image
            result = np.zeros_like(capture.color[:, :, :3])

            # Draw edges and contours on the output array
            #check which contours are within 5% of max area and are rectangles
            for contour in contours:
                area = cv2.contourArea(contour)
                #if area > max_area * 0.95 and area < max_area * 1.05:
                perimeter = cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
                #calculate are on basis of approx
                #area = cv2.contourArea(approx)
                a = True
                if a == True:
                    if a :
                        print("area: ", area)
                        print("perimeter: ", perimeter)
                        print("approx: ", approx)
                        print("len(approx): ", len(approx))
                        print("")
                    #draw area of contour
                        cv2.putText(result, str(area), (approx[0][0][0], approx[0][0][1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
                        cv2.drawContours(result, [contour], -1, (0, 255, 0), 2)
                        cv2.drawContours(result, [approx], -1, (255, 0, 0), 2)




            #cv2.drawContours(result, contours, -1, (0, 255, 0), 2)

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
