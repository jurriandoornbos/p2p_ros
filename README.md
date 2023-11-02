# p2p_ros2
 pix2pix (and cGAN) ROS node


Currently mainly copy-and-pasted from (CycleGAN and Pix2Pix GitHub Repo)[https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix] Mar14 edition


```

source /opt/ros/humble/setup.bash
source rosdev_ws/install/setup.bash


ros2 run image_publisher image_publisher_node test.jpg --ros-args -r image_raw:=input_pix2pix_img -p publish_rate:=0.2

```

sudo apt install python3-opencv
sudo apt install libboost-python-dev
sudo apt install ros-humble-vision-opencv
pip3 install -r requirements.txt