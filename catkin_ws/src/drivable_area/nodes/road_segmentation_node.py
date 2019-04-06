#!/usr/bin/env python
'''
Created Date: Tuesday March 26th 2019
Last Modified: Tuesday March 26th 2019 12:33:43 am
Author: ankurrc
'''

import rospy
from RoadSegmentation import RoadSegmentation


def run_network():

    rospy.init_node('road_segmentation', anonymous=True)

    # LOAD ROS PARAMETERS
    model_path = rospy.get_param("~model_path")
    crop_size = rospy.get_param("~crop_size", '240, 480').split(',')
    crop_size = tuple([int(t) for t in crop_size])
    prediction_threshold = rospy.get_param("~prediction_threshold")

    # BUILD NETWORK CLASS
    network = RoadSegmentation.RoadSegmentation(
        nn_model_path=model_path, crop_size=crop_size, prediction_threshold=prediction_threshold)

    # RUN NETWORK
    network.run()


if __name__ == "__main__":
    run_network()
