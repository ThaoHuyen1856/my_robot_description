cmake_minimum_required(VERSION 3.5)
project(my_robot_description)

find_package(ament_cmake REQUIRED)

# Cài tất cả thư mục vào share/ để ros2 launch tìm thấy
install(
  DIRECTORY urdf launch config meshes
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
