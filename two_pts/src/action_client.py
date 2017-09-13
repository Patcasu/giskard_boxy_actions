#!/usr/bin/env python
import rospy
import actionlib
from giskard_msgs.msg import *
from geometry_msgs.msg import *
from visualization_msgs.msg import *
from std_msgs.msg import *

command = WholeBodyCommand()
marker_points = Point()
header = Header()
input_points = []
aux = 0

def create_goal():
    global input_points,aux
    if len(input_points) >= 3:
        command.type = 0
        header.frame_id = "base_link"

        command.right_ee.goal_pose.header = header
        command.right_ee.type = 1

        command.right_ee.goal_pose.pose.orientation.w = 1.0
        command.right_ee.goal_pose.pose.orientation.x = 0.0
        command.right_ee.goal_pose.pose.orientation.y = 1.0
        command.right_ee.goal_pose.pose.orientation.z = 0.0

        command.right_ee.goal_pose.pose.position.x = input_points[aux]
        command.right_ee.goal_pose.pose.position.y = input_points[aux+1]
        command.right_ee.goal_pose.pose.position.z = input_points[aux+2]

        aux += 3

        goal = WholeBodyGoal(command=command)
        #print "ip [aux]=",input_points[aux],"\nip[aux+1]=",input_points[aux+1],"\nip[aux+1]=",input_points[aux+2]
        #print "aux \n",aux,"input points \n",input_points, "goal ", goal.command.right_ee.goal_pose

        return goal
    else:
        command.type = 0
        header.frame_id = "base_link"

        command.right_ee.goal_pose.header = header
        command.right_ee.type = 1

        command.right_ee.goal_pose.pose.orientation.w = 1.0
        command.right_ee.goal_pose.pose.orientation.x = 0.0
        command.right_ee.goal_pose.pose.orientation.y = 1.0
        command.right_ee.goal_pose.pose.orientation.z = 0.0

        command.right_ee.goal_pose.pose.position.x = 0.5
        command.right_ee.goal_pose.pose.position.y = -0.5
        command.right_ee.goal_pose.pose.position.z = 1.0

        goal = WholeBodyGoal(command=command)

        return goal

def action_client():
    client = actionlib.SimpleActionClient("/controller_action_server/move", WholeBodyAction)

    rospy.loginfo("Waiting for action server to start.")
    client.wait_for_server()
    rospy.loginfo("Action server started, sending goal.")

    goal = create_goal()
    #print "Goal= ", goal

    client.send_goal(goal)
    client.wait_for_result(rospy.Duration(5))

    if client.get_state() == actionlib.SimpleGoalState.DONE:
        rospy.loginfo("Made it!")
    else:
        rospy.loginfo("Failed.")

def callback(data):
    global header, input_points
    a = 0
    if data.ns == "points":
        header = data.header
        input_points.append(data.pose.position.x)
        input_points.append(data.pose.position.y)
        input_points.append(data.pose.position.z)
        print data.pose.position.y

def listener():
    rospy.Subscriber("mk_visu", Marker, callback)


if __name__ == '__main__':
    rospy.init_node("action_client", anonymous=True)
    while not rospy.is_shutdown():
        listener()

        try:
            action_client()
        except rospy.ROSInterruptException:
            print("Program interrupted before completion.")
        except (KeyboardInterrupt, SystemExit):
            sys.exit(1)