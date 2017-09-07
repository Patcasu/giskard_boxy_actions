#!/usr/bin/env python

import rospy
from moove.msg import *
from visualization_msgs.msg import *
from geometry_msgs.msg import *

pc = []
nc = []
frame_id = "base_link"
tp = 0; i = -6; step = 3; aux = 0; ta = 1; tl = 2; tn = 3
start_points = Point32()
end_points = Point32()

def topic_listener():

    rospy.init_node("markers",anonymous=True)
    rospy.Subscriber("line_points",line,get_points)

def get_points(msg_data):

    global frame_id

    pc.append(msg_data.p.x); pc.append(msg_data.p.y); pc.append(msg_data.p.z)
    nc.append(msg_data.n.x); nc.append(msg_data.n.y); nc.append(msg_data.n.z)
    frame_id = msg_data.header.frame_id

def point_coordinates():

    global pc,i

    p = Point()
    if len(pc) > 3:
        p.x = pc[i]
        p.y = pc[i + 1]
        p.z = pc[i + 2]
        return p
    else:
        return p

def normal_coordinates(n):
    global nc, i

    if len(nc) > 3:
        if n == "x":
            x = nc[i]
            return x
        if n == "y":
            y = nc[i + 1]
            return y
        if n == "z":
            z = nc[i + 2]
            return z
    else:
        return 0.0

def line_coordinates_start():
    global pc,i
    p = Point()

    if len(pc) > 3:
            p.x = pc[i-3]
            p.y = pc[i-2]
            p.z = pc[i-1]
            return p
    else:
        return p

def additional_points():

    global pc,i,step,aux
    p = Point()

    if len(pc) > 3:

        inc = abs(pc[i+1] - pc[i + 4]) / step
        aux = aux + inc

        if pc[i+1] < pc[i+4]:
            p.x = pc[i]
            p.y = pc[i + 1] + aux
            p.z = pc[i + 2]
            return p
        else:
            p.x = pc[i]
            p.y = pc[i + 1] - aux
            p.z = pc[i + 2]
            return p
    else:
        return p

def markers():

    global i,aux,tp,ta,tl,tn
    pub = rospy.Publisher("mk_visu",Marker,queue_size=10)
    p = Point()

    while not rospy.is_shutdown():
        p = point_coordinates()
        rate = rospy.Rate(1)

        mkp = Marker()

        mkl = Marker()

        mkn = Marker()

        mkp.header.frame_id = mkl.header.frame_id = mkn.header.frame_id = frame_id

        mkp.header.stamp = mkn.header.stamp = mkl.header.stamp = rospy.Time.now()

        mkp.action = mkl.action = mkn.action = Marker.ADD

        #POINTS MARKER
        mkp.type = Marker.SPHERE

        mkp.pose.position = p
        mkp.pose.orientation.w = 1.0

        mkp.scale.x = 0.05
        mkp.scale.y = 0.05
        mkp.scale.z = 0.05

        mkp.color.b = 0.7
        mkp.color.a = 1.0

        mkp.ns = "points"

        mkp.id = tp

        mkp.lifetime = rospy.Duration()

        #LINE MARKER

        mkl.type = Marker.LINE_STRIP

        mkl.pose.orientation.w = 1.0

        mkl.scale.x = 0.025
        mkl.scale.y = 0.025
        mkl.scale.z = 0.025

        mkl.color.r = 0.0
        mkl.color.g = 1.0
        mkl.color.b = 0.5
        mkl.color.a = 1.0

        mkl.points.append(line_coordinates_start())
        mkl.points.append(p)

        mkl.ns = "line marker"

        mkl.id = tl

        mkl.lifetime = rospy.Duration()

        #NORMAL MARKER

        mkn.type = Marker.ARROW

        mkn.pose.position = p

        mkn.pose.orientation.w = 1.0
        mkn.pose.orientation.x = normal_coordinates("x")
        mkn.pose.orientation.y = normal_coordinates("y")
        mkn.pose.orientation.z = normal_coordinates("z")

        mkn.scale.x = 0.25
        mkn.scale.y = 0.025
        mkn.scale.z = 0.025

        mkn.color.r = 1.0
        mkn.color.g = 0.0
        mkn.color.b = 0.0
        mkn.color.a = 1.0

        mkn.ns = "normal"

        mkn.id = tn

        mkn.lifetime = rospy.Duration()

        #PUBLISH SECTION
        pub.publish(mkp)
        rospy.loginfo(mkp)
        tp += 1

        pub.publish(mkn)
        tn += 1

        if tp % 2 != 0:
            for k in range(0, step-1):
                pt = Point()
                pt = additional_points()
                mkn.id = tn
                mkp.id = ta
                mkp.pose.position = pt
                mkn.pose.position = pt

                pub.publish(mkp)
                pub.publish(mkn)

                ta += 1
                tn += 1

        pub.publish(mkl)
        rospy.loginfo(mkl)
        aux = 0
        tl += 1
        i += 3

        rate.sleep()

if __name__ == '__main__':
    topic_listener()
    markers()


