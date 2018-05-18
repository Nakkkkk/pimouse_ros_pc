#! /usr/bin/env python
# -*- coding: utf-8 -*-
import socket
from datetime import datetime
from time import sleep
import sys, os
import rospy
from geometry_msgs.msg import Twist

s = socket.socket()

print "type port num"
port = int(raw_input())
#port = int(sys.argv[1])
s.bind(('10.0.1.21', port))

rospy.init_node('tcpCtl')
pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=1)
command = Twist()
#bef = 0

while not rospy.is_shutdown():
    print('listening')
    s.listen(5)
    c, addr = s.accept()
    print('receiving')
    command_char = c.recv(4096)
#    lx = 0.0
#    az = 0.0
#    command_int = int(command_char)

#    command_int = int(c.recv(4096))

#    print command_int + bef

#    bef = command_int

    if(command_char=='d'):
      print('### RIGHT ###')
      command.linear.x = 0.0
      command.angular.z = -2.0
#      lx = 0.0
#      az = -2.0
      pub.publish(command)

    elif(command_char=='a'):
      print('=== LEFT ===')
      command.linear.x = 0.0
      command.angular.z = 2.0
#      lx = 0.0
#      az = 2.0
      pub.publish(command)

    elif(command_char=='w'):
      print('||| STRAIGHT |||')
      command.linear.x = 2.0
      command.angular.z = 0.0
#      lx = 2.0
#      az = 0.0
      pub.publish(command)

    elif(command_char=='s'):
      print('~~~ BACK ~~~')
      command.linear.x = -2.0
      command.angular.z = 0.0
#      lx = -2.0
#      az = 0.0
      pub.publish(command)

    else:
      print('??? ELSE ???') 

#    command.linear.x = lx
#    command.angular.z = az
#    pub.publish(command)

#    print('bef + aft = '+str(float(c.recv(4096))+bef)
#export ROS_MASTER_URI=http://10.0.1.32:11311
#    print(c.recv(4096))
#    bef = float(c.recv(4096))
#    while True:
#        print('sending')
#        now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
#        try:
#            c.send(now)
#        except:
#            break
#        sleep(1)
    c.close()
#os.system("kill %s" % str(port))
s.close()
