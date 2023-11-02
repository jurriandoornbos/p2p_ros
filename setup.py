from setuptools import find_packages, setup
from glob import glob
import os
package_name = 'p2p_ros'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ("share/" + package_name + "/p2p/weights/ndvi_p2p", glob('p2p_ros/p2p/weights/ndvi_p2p/*.pth')),
        ("share/" + package_name + "/p2p/weights/ndvi_p2p", glob('p2p_ros/p2p/weights/ndvi_p2p/*.txt')),
    ],
    include_package_data=True,
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='jur',
    maintainer_email='jur@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'listener=p2p_ros.subscriber_member_function:main',
        ],
    },
)
