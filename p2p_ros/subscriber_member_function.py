import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image

import os
from .p2p.options.test_options import TestOptions
from .p2p.models import create_model
from .p2p.util.util import tensor2im
import torch
from cv_bridge import CvBridge
import torchvision.transforms as transforms
import numpy as np
import cv2

class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            Image,
            'input_pix2pix_img',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning
        
        self.publisher_ = self.create_publisher(Image, 'output_pix2pix_img', 10)
        opt = TestOptions().parse()  # get test options
        # hard-code some parameters for test
        opt.num_threads = 0   # test code only supports num_threads = 0
        opt.batch_size = 1    # test code only supports batch_size = 1
        opt.serial_batches = True  # disable data shuffling; comment this line if results on randomly chosen images are needed.
        opt.no_flip = True    # no flip; comment this line if results on flipped images are needed.
        opt.display_id = -1   # no visdom display; the test code saves the results to a HTML file.
        self.model = create_model(opt)      # create a model given opt.model and other options
        self.model.setup(opt)               # regular setup: load and print networks; create schedulers
        self.bridge = CvBridge()
        self.transform = transforms.Compose([
                transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)) ]) #normalizes RGB img

    def listener_callback(self, msg):
        #preprocess ros Image msg to torch -1 : 1 what pix2pix wants
        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding = "passthrough")
        tensor_image = np.asarray(cv_image, 'float32')
        tensor_image = tensor_image.transpose((2,0,1))
        tensor_image = np.expand_dims(tensor_image,0)
        tensor_image = torch.from_numpy(tensor_image)
        tensor_image = self.transform(tensor_image)
        tensor_image = tensor_image.to(device="cuda")

        model_in = {}
        model_in["A"] = tensor_image
        model_in["A_paths"] = "no_paths"
        self.model.set_input(model_in)  # unpack data from data loader
        self.model.test()           # run inference 'forward'
        visuals = self.model.get_current_visuals()  # get image results
        
        np_img =  tensor2im(visuals["fake"])
        out_msg = self.bridge.cv2_to_imgmsg(np_img, encoding="mono8")
        self.publisher_.publish(out_msg)



def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
   main()