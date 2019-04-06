'''
Created Date: Monday March 25th 2019
Last Modified: Monday March 25th 2019 11:17:55 pm
Author: ankurrc
'''

from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
import cv2
import numpy as np

bridge = CvBridge()


def prepare_input(data, crop_size):
    try:
        image_type = data.encoding
        img = bridge.imgmsg_to_cv2(data, image_type)
    except CvBridgeError, e:
        print e

    img = cv2.resize(img, (crop_size[1], crop_size[0]))
    img = img[None, :, :, ::-1]/255.0

    return np.asarray(img, dtype=np.float32)


def prepare_output(prediction, cv_image, view_size, prediction_confidence, rgb=(255, 255, 32)):
    prediction = (prediction >= prediction_confidence).astype(np.uint8)
    channels = []
    for channel_color in rgb:
        prediction_ = np.copy(prediction)
        prediction_[prediction_ == 1] = channel_color
        channels.append(prediction_)

    prediction_img = np.dstack(channels)
    cv_image = (cv_image*255).astype(np.uint8)
    alpha = 0.2

    overlay_img = cv2.addWeighted(
        prediction_img, alpha, cv_image, 1 - alpha, 0)

    return prediction_img, overlay_img


def get_cv_msg(np_array):
    msg = bridge.cv2_to_imgmsg(np_array, encoding="rgb8")
    return msg
