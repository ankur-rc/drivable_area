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
    # calculate center of mass of predicted output
    com = np.argwhere(prediction == 1)
    if com.shape[0] > 0:
        com = np.mean(com, axis=0)
        com = (int(com[1]), int(com[0]))
        ego_center = (int(prediction.shape[1]/2), prediction.shape[0])
        # compute the distance and angle (in degrees)
        # translate to euclidean x-y frame with 'ego center' as the origin
        com_coords, ego_center_coords = np.array(
            [com[0], -com[1]]), np.array([ego_center[0], -ego_center[1]])
        d = com_coords - ego_center_coords
        r = np.sum(d**2)**0.5
        theta = np.arctan2(d[1], d[0])*180/np.pi

        # draw them on prediction map
        cv2.circle(prediction_img, com, 5, (255, 0, 0))
        cv2.circle(prediction_img, ego_center, 5, (0, 0, 255))
        cv2.arrowedLine(prediction_img, ego_center, com, (255, 0, 0))
        ret = cv2.putText(prediction_img, 'r:{:.02f}, theta:{:.02f}'.format(
            r, theta), (5, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255))

    cv_image = (cv_image*255).astype(np.uint8)
    alpha = 0.4

    overlay_img = cv2.addWeighted(
        prediction_img, alpha, cv_image, 1 - alpha, 0)

    return prediction_img, overlay_img


def get_cv_msg(np_array):
    msg = bridge.cv2_to_imgmsg(np_array, encoding="rgb8")
    return msg
