"""
launch_sim.launch.py — Khởi động Gazebo Simulation (Tuần 4)
============================================================
Khởi động 3 thành phần cùng lúc:
  1. robot_state_publisher  → publish URDF + TF (dùng sim time)
  2. gazebo                 → Gazebo 11 Classic + ROS2 bridge
  3. spawn_entity           → tạo robot trong Gazebo

Cách chạy:
  ros2 launch my_robot_description launch_sim.launch.py

Nếu muốn load world tùy chỉnh:
  ros2 launch my_robot_description launch_sim.launch.py \\
    world:=$(ros2 pkg prefix my_robot_description)/share/my_robot_description/worlds/my_world.world

Sau khi chạy, teleop robot:
  ros2 run teleop_twist_keyboard teleop_twist_keyboard \\
    --ros-args -p stamped:=true -p use_sim_time:=true
"""

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():

    # ① Đường dẫn packages
    pkg = get_package_share_directory('my_robot_description')
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')

    # ② Khai báo argument world (có thể override từ command line)
    world_arg = DeclareLaunchArgument(
        'world',
        default_value=os.path.join(pkg, 'worlds', 'my_world.world'),
        description='Đường dẫn đến file .world cho Gazebo'
    )

    # ③ Robot State Publisher
    #    QUAN TRỌNG: use_sim_time=true → dùng đồng hồ Gazebo
    #    Nếu thiếu → TF timestamp lệch → robot không hiện trong RViz
    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(pkg, 'launch', 'rsp.launch.py')
        ]),
        launch_arguments={'use_sim_time': 'true'}.items()
    )

    # ④ Gazebo 11 Classic với ROS2 support
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(pkg_gazebo_ros, 'launch', 'gazebo.launch.py')
        ]),
        launch_arguments={'world': LaunchConfiguration('world')}.items()
    )

    # ⑤ Spawn robot từ topic /robot_description
    #    spawn_entity.py chờ /robot_description rồi tạo robot trong Gazebo
    spawn = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-topic', 'robot_description',
            '-entity', 'my_robot',
            '-z', '0.1',   # spawn cao hơn sàn 10 cm để tránh clip
        ],
        output='screen'
    )

    return LaunchDescription([
        world_arg,
        rsp,
        gazebo,
        spawn,
    ])
