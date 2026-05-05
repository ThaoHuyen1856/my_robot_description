# my_robot_description — Starter Package Tuần 3

Package mô tả robot diff-drive cho môn Kỹ thuật Robot 2.
Viện I3T – CTD, UEH | ROS2 Foxy

---

## Cài đặt

```bash
# Copy package vào workspace
cp -r my_robot_description ~/ros2_ws/src/

# Cài dependencies
sudo apt update
sudo apt install ros-foxy-robot-state-publisher \
                 ros-foxy-joint-state-publisher-gui \
                 ros-foxy-xacro \
                 ros-foxy-rviz2 -y

# Build
cd ~/ros2_ws
colcon build --packages-select my_robot_description
source install/setup.bash
```

## Chạy

```bash
# Xem robot trong RViz
ros2 launch my_robot_description display.launch.py
```

## Cấu trúc file

```
my_robot_description/
├── urdf/
│   ├── robot.urdf.xacro      ← File gốc (gộp tất cả)
│   ├── properties.xacro      ← Kích thước robot
│   ├── materials.xacro       ← Màu sắc RViz
│   ├── macros.xacro          ← Macro tính inertia
│   └── robot_core.xacro      ← Links & Joints
├── launch/
│   └── display.launch.py     ← Khởi động RViz
└── config/
    └── robot.rviz            ← Cấu hình RViz

## Tuần 4

Xem file robot.urdf.xacro — có hướng dẫn thêm 2 include cho Gazebo.
