from detection_func import *
from visual_func import *
import pandas as pd

#Detection.get_device_id()

'''
df,image = Detection.detect_objects(R"images/rectangles.png", 0.7,0.95)
print(df)
cv2.imshow("Objects", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''
Detection.live_depth()
#Detection.largest_rectangle()

