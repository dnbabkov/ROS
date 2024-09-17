#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import JointState
from std_msgs.msg import Header

def move_robot():
    my_publisher = rospy.Publisher('joint_states', JointState, queue_size=10)
    rospy.init_node('move_robot', anonymous=True)
    rate_msg = rospy.Rate(15)
    
    robot_state = JointState()
    robot_state.header = Header()
    robot_state.header.stamp = rospy.Time.now()
    robot_state.name = ['base_to_body', 'body_to_arm', 'arm_to_end']

    maxExtent1 = False
    maxExtent2 = False
    maxRotation = False

    base_to_body = 0
    body_to_arm = -1.56
    arm_to_end = 0.2
    my_publisher.publish(robot_state)

    while not rospy.is_shutdown():
        robot_state.header.stamp = rospy.Time.now()
        robot_state.position = [base_to_body, body_to_arm, arm_to_end]
        if not maxExtent1:
            base_to_body += 0.05
            if base_to_body >= 1.40:
                maxExtent1 = True
        else:
            base_to_body -= 0.05
            if base_to_body <= 0.04:
                maxExtent1 = False

        if not maxRotation:
            body_to_arm += 0.1
            if body_to_arm >= 1.4:
                maxRotation = True
        else:
            body_to_arm -= 0.1
            if body_to_arm <= -1.4:
                maxRotation = False

        if not maxExtent2:
            arm_to_end += 0.05
            if arm_to_end >= 1.9:
                maxExtent2 = True
        else:
            arm_to_end -= 0.05
            if arm_to_end <= 0.06:
                maxExtent2 = False

        my_publisher.publish(robot_state)
        rate_msg.sleep()

if __name__ == "__main__":
    try:
        move_robot()
    except rospy.ROSInterruptException:
        pass
