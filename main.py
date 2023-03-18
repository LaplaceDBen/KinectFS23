from detection_func import *
from visual_func import *


#devices()
'''
df,image = detect_objects("images/rectangles.png", 0.7,0.95)
print(df.head())
cv2.imshow("Objects", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''
live_depth()