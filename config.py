import pyk4a
from pyk4a import Config, PyK4A

camera_config = PyK4A(Config(color_resolution=pyk4a.ColorResolution.RES_2160P,
                             depth_mode=pyk4a.DepthMode.NFOV_UNBINNED,
                             synchronized_images_only=True,))
