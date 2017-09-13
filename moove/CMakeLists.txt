cmake_minimum_required(VERSION 2.8.3)
project(moove)
find_package(catkin REQUIRED 
	roscpp 
	rospy 
	geometry_msgs
	message_generation
	std_msgs
	
)
add_message_files(
	FILES
	line.msg
)
generate_messages(
	DEPENDENCIES
	geometry_msgs
	std_msgs
)
catkin_package(
	CATKIN_DEPENDS 
	message_runtime
	std_msgs
	geometry_msgs
)

