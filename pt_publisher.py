#!/usr/bin/env python
# license removed for brevity
import rospy
import random
import std_msgs.msg
from moove.msg import line

def talker():

    pub = rospy.Publisher('line_points', line, queue_size=10)
    rospy.init_node('point publisher', anonymous=True)
    rate = rospy.Rate(1) # 10hz
    msg = line()
    a = 2
    msg.p.z = 0.50
    msg.p.x = 0.7
    msg.p.y = -0.70

    while not rospy.is_shutdown():

        msg.header.frame_id = "base_link"
        msg.header.stamp = rospy.Time.now()
        if a % 2 == 0:
            msg.p.x = 0.7
            msg.p.y = -0.70
            msg.p.z = msg.p.z
            msg.n.x = 1.0
            msg.n.y = 0.0
            msg.n.z = 0.0
        else:
            msg.p.x = 0.7
            msg.p.y = msg.p.y + 0.4
            msg.p.z = msg.p.z + 0.10
            msg.n.x = 1.0
            msg.n.y = 0.0
            msg.n.z = 0.0
        a = a + 1
        rospy.loginfo(msg)
        pub.publish(msg)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass

