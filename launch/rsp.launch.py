"""
rsp.launch.py — Robot State Publisher
======================================
Launch file chỉ khởi động robot_state_publisher.
Được gọi bởi cả display.launch.py (Tuần 3) và launch_sim.launch.py (Tuần 4).

Tham số:
  use_sim_time  default=false  (Tuần 3: RViz)
                true           (Tuần 4: Gazebo)
"""

import os
import xacro
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():

    pkg = get_package_share_directory('my_robot_description')

    # Tham số use_sim_time — được override từ launch file cha
    use_sim_time = LaunchConfiguration('use_sim_time')
    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Dùng đồng hồ Gazebo (true) hay wall clock (false)'
    )

    # Xử lý Xacro → URDF string
    xacro_file = os.path.join(pkg, 'urdf', 'robot.urdf.xacro')
    robot_description_content = xacro.process_file(xacro_file).toxml()

    # Robot State Publisher node
    rsp_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_description_content,
            'use_sim_time': use_sim_time,
        }]
    )

    return LaunchDescription([
        use_sim_time_arg,
        rsp_node,
    ])
