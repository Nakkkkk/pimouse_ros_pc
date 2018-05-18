#!/usr/bin/python
# -*- Coding: utf-8 -*-
import socket
import select
import ctypes
from tick_struct import TickStruct
import sys, rospy
from pimouse_ros_pc.msg import SocketMessage

rospy.init_node('socketServer')
pub = rospy.Publisher('socket',SocketMessage,queue_size=1)
s = SocketMessage()

MSGLEN = 1024
 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("10.0.1.21", 2233))
server.listen(1)
client, client_address = server.accept()
 
print "Socket server started"
tick = TickStruct()
resv_size = ctypes.sizeof(tick)
count = 0

rate= rospy.Rate(10)
while True:
    r, w, e = select.select([client], [], [])
    for reader in r:
        reader.recv_into(tick)
        print tick
        count += 1
        s.message = int(tick.ask)
        pub.publish(s) 
    if(count >= 1000):
        client.sendall("finish")
        break
    rate.sleep()
