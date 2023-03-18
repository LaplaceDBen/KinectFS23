import time
import numba as nb

@nb.jit(nopython=True, parallel=True)
def find_largest_rectangle(contours):
    max_rect_area = 0
    max_rect = None
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
        if len(approx) == 4:
            rect_area = cv2.contourArea(approx)
            if rect_area > max_rect_area:
                max_rect_area = rect_area
                max_rect = approx
    return max_rect, max_rect_area

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

    while True:
        capture = k4a.get_capture()
        if np.any(capture.color):
            gray = cv2.cvtColor(capture.color, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 100, 200)
            contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            max_rect, max_rect_area = find_largest_rectangle(contours)

            if max_rect is not None:
                timestamp = time.time()
                center_x = (max_rect[0][0][0] + max_rect[2][0][0]) / 2
                center_y = (max_rect[0][0][1] + max_rect[2][0][1]) / 2

                print("Timestamp:", timestamp)
                print("Area:", max_rect_area)
                print("Center point: ({}, {})".format(center_x, center_y))
                print("Corner coordinates:")
                for corner in max_rect:
                    print("({},{})".format(corner[0][0], corner[0][1]))
                print("\n")
            else:
                print("No rectangular object found.")

            cv2.imshow("k4a", capture.color)

            key = cv2.waitKey(10)
            if key != -1:
                cv2.destroyAllWindows()
                break

    k4a.stop()
