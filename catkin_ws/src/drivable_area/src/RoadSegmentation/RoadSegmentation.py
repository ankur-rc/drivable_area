#!/usr/bin/env python
'''
Created Date: Monday March 25th 2019
Last Modified: Monday March 25th 2019 10:49:26 pm
Author: ankurrc
'''

import rospy
from sensor_msgs.msg import Image
import numpy as np
import cv2

import utils

from keras.models import load_model


class RoadSegmentation(object):

    def __init__(self, nn_model_path=None, crop_size=(240, 480), view_size=(360, 640), prediction_threshold=0.5):

        self.seg_pub = rospy.Publisher("segmentation", Image, queue_size=1)
        self.seg_overlay_pub = rospy.Publisher(
            "segmentation_overlay", Image, queue_size=1)
        self.view_size = view_size
        self.crop_size = crop_size
        print "Loading model from {}".format(nn_model_path)
        self.model = load_model(nn_model_path)
        print "done."
        self.prediction_threshold = prediction_threshold

    def run(self):
        while not rospy.is_shutdown():

            data = None
            while data is None:
                try:
                    data = rospy.wait_for_message("camera", Image, timeout=10)
                except:
                    pass

            cv_image = utils.prepare_input(data, self.crop_size)
            prediction = self.model.predict(cv_image)
            segmentation_result, segmentation_overlay_result = utils.prepare_output(
                prediction[0, :, :, 1], cv_image[0], self.view_size, self.prediction_threshold)

            self.seg_pub.publish(utils.get_cv_msg(segmentation_result))
            self.seg_overlay_pub.publish(
                utils.get_cv_msg(segmentation_overlay_result))
