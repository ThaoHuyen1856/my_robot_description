"""
display.launch.py — Khởi động RViz để xem robot (Tuần 3)
==========================================================
Nodes:
  1. robot_state_publisher (qua rsp.launch.py)
  2. joint_state_publisher_gui
  3. rviz2

Cách chạy:
  ros2 launch my_robot_description display.launch.py
"""

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():

    pkg = get_package_share_directory('my_robot_description')

    # Robot State Publisher (use_sim_time=false cho RViz thuần)
    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(pkg, 'launch', 'rsp.launch.py')
        ]),
        launch_arguments={'use_sim_time': 'false'}.items()
    )

    # GUI slider để xoay continuous joints (bánh xe)
    jsp_gui = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        output='screen'
    )

    # RViz2 với config đã cấu hình
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        output='screen',
        arguments=['-d', os.path.join(pkg, 'config', 'robot.rviz')]
    )

    return LaunchDescription([rsp, jsp_gui, rviz])
