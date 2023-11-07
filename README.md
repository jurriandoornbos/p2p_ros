<div align="center">
  <p>
    <a href="https://icaerus.eu" target="_blank">
      <img width="50%" src="https://icaerus.eu/wp-content/uploads/2022/09/ICAERUS-logo-white.svg"></a>
    <h3 align="center">Pix2Pix ROS node🦚</h3>
    
   <p align="center">
    pix2pix (and possibly cGAN) ROS node. It is built (mostly copied) upon the CycleGAN and Pix2Pix GitHub Repo
    <br/>
    <br/>
    <br/>
    <br/>
    <a href="https://github.com/jurriandoornbos/p2p_ros/issues">Report Bug</a>
    -
    <a href="https://github.com/jurriandoornbos/p2p_ros/issues">Request Feature</a>
  </p>
</p>
</div>

![Downloads](https://img.shields.io/github/downloads/jurriandoornbos/p2p_ros/total) ![Contributors](https://img.shields.io/github/contributors/jurriandoornbos/p2p_ros?color=dark-green) ![Forks](https://img.shields.io/github/forks/jurriandoornbos/p2p_ros?style=social) ![Stargazers](https://img.shields.io/github/stars/jurriandoornbos/p2p_ros?style=social) ![Issues](https://img.shields.io/github/issues/jurriandoornbos/p2p_ros) ![License](https://img.shields.io/github/license/jurriandoornbos/p2p_ros) 

## Table Of Contents

* [Summary](#summary)
* [Explanation](#explanation)
* [Dev notes](#dev-notes)
* [Installation](#installation)
* [Authors](#authors)
* [Acknowledgments](#acknowledgments)

## Summary
pix2pix (and possibly cGAN) ROS node. It is built (mostly copied) upon the (CycleGAN and Pix2Pix GitHub Repo)[https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix] the Mar14 2023 edition. Made to fit the RGB-> NDVI conversion, trained in a vineyard.

## Explanation

There is just a single Node with `listener:subscriber_member_function`, (`ros2 run p2p_ros listener`) listens to the `/input_pix2pix_img` topic (`sensor_msgs:Image`), converts the ros Image to a torch-tensor, normalizes it, and runs it through the loaded pix2pix model. This is then converted back into a ros Image msg and published under the `/output_pix2pix_img` topic, mostly using the `cv_bridge` functions.

Input image requirements are expected to be 256*256 and 3 RGB channels. Otherwise it will probably crash.

We are in Deep Learning territory here, so real-time conversions at 60FPS, I am not sure if pix2pix can achieve that. but tested at 0.2FPS which was okay.

## Dev notes

Essentially using the original junyanz github functions etc to pass images through the model. This also means it uses their naming schemes etc.
It expects a `latest_net_G.pth` pretrained model under `p2p/weights/ndvi_p2p`.

If you want to add your own model, change up this file. Or add your own experiment under `p2p/weights/experiment_name`. Then in the `p2p/options/base_options` change the experiment name variable. Additionally, change the options to align with your training settings.
Also change the ndvi_p2p name in `setup.py`:`data_files` to your `experiment_name`.
```python
("share/" + package_name + "/p2p/weights/ndvi_p2p", glob('p2p_ros/p2p/weights/ndvi_p2p/*.pth')), 
("share/" + package_name + "/p2p/weights/ndvi_p2p", glob('p2p_ros/p2p/weights/ndvi_p2p/*.txt')),
```

Tested only in ROS2 Humble.

## Installation
1. `cd` into your ros_ws/src/ folder, 
2. `git clone` this repository,
3. download a `latest_net_G.pth` file and place it in `p2p/weights/ndvi_p2p`.
4. installation requirements:
```
sudo apt install python3-opencv
sudo apt install libboost-python-dev
sudo apt install ros-humble-vision-opencv
pip3 install -r requirements.txt
```
5. `colcon build` it

```bash
# Test codes
source /opt/ros/humble/setup.bash
source rosdev_ws/install/setup.bash
ros2 run image_publisher image_publisher_node test.jpg --ros-args -r image_raw:=input_pix2pix_img -p publish_rate:=0.2

```

## Authors

* **Jurrian Doornbos** - *Wageningen University* - [Jurrian Doornbos](https://github.com/jurriandoornbos)

## Acknowledgements
This project is funded by the European Union, grant ID 101060643.

<img src="https://rea.ec.europa.eu/sites/default/files/styles/oe_theme_medium_no_crop/public/2021-04/EN-Funded%20by%20the%20EU-POS.jpg" alt="https://cordis.europa.eu/project/id/101060643" width="200"/>


