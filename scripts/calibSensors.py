#!/usr/bin/env python
#encoding: utf8
import sys, rospy
import time
from pimouse_ros.msg import LightSensorValues
from std_msgs.msg import UInt16
from geometry_msgs.msg import Twist

class CalcAverage():
  def __init__(self):
    self.count=0
    self.LAV = 0
    self.RAV = 0
    self.last_time = rospy.Time.now()
    self.buzzerCount()
    print "=======Sensor subscribing======="
    self.sub_sensor_bef = rospy.Subscriber('lightsensors', LightSensorValues, self.calc_bef)
    self.values = LightSensorValues()
    print "=======motor controling======="
    self.rate = rospy.Rate(1)
    self.sub_cmd_vel_con = rospy.Subscriber('/turtle1/cmd_vel', Twist, self.callback_cmd_vel)
    self.cmd = Twist()
    self.pub_cmd_vel_con = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

    rospy.spin()

  def calc_bef(self,data):
    self.values=data
    self.count += 1
    self.LAV += (self.values.left_forward + self.values.left_side)
    self.RAV += (self.values.right_side + self.values.right_forward)
    print "now="+str(self.count)+","+str(self.values.left_forward)+","+str(self.values.left_side)+","+str(self.values.right_side)+","+str(self.values.right_forward)
    print "from bef"

    if(self.count==30):
      self.LAV=self.LAV/self.count
      self.RAV=self.RAV/self.count
      print "L average="+str(self.LAV)
      print "R average="+str(self.RAV)
      self.sub_sensor_bef.unregister()
      sub_sensor_aft = rospy.Subscriber('lightsensors', LightSensorValues, self.calc_aft)
      print "################caliburation owata#################"
      self.rate.sleep()

  def calc_aft(self, values):
#    flag = 1
    self.count += 1
    print "Lsum="+str(values.left_forward+values.left_side)+" , Rsum="+str(values.right_side+values.right_forward)
    print "from aft"

    if(rospy.Time.now().to_sec() - self.last_time.to_sec() >= 4.0):
      self.cmd.angular.z = 0.0
      self.cmd.linear.x = 0.0
      self.pub_cmd_vel_con.publish(self.cmd)
        
    if(values.left_forward+values.left_side>self.LAV):
#      flag = 0
      print "turn RIGHT !!"
      self.cmd.angular.z = -2.0
      self.pub_cmd_vel_con.publish(self.cmd)
#      self.rate.sleep()
#      self.cmd.angular.z = 0.0
#      self.cmd.linear.x = 0.0
#      self.pub_cmd_vel_con.publish(self.cmd)
      
    elif(values.right_side+values.right_forward>self.RAV):
#      flag = 0
      print "turn LEFT !!"
      self.cmd.angular.z = 2.0
      self.pub_cmd_vel_con.publish(self.cmd)
#      self.rate.sleep()
#      self.cmd.angular.z = 0.0
#      self.cmd.linear.x = 0.0
#      self.pub_cmd_vel_con.publish(self.cmd)

#    else:
#      if(flag == 0):
#        print "as you are controling."
#        self.cmd.angular.z = 0.0
#        self.cmd.linear.x = 0.0
#        self.pub_cmd_vel_con.publish(self.cmd)
#        flag = 1
    
    else:
      self.pub_cmd_vel_con.publish(self.cmd)

# def motor_control(self, cmd):

  def callback_cmd_vel(self, message):
    self.cmd = message
    print "====== motor controling now ======"
    self.last_time = rospy.Time.now()
#    self.rate.sleep()

  def buzzerCount(self):

    for i in range(2):
      pub_cal.publish(500)
      time.sleep(0.5)
    pub_cal.publish(0)

    time.sleep(0.5)

    for i in range(1):
      pub_cal.publish(500)
      time.sleep(0.5)
    pub_cal.publish(0)

    time.sleep(0.5)

    for i in range(1):
      pub_cal.publish(1000)
      time.sleep(0.5)
    pub_cal.publish(0)

if __name__ == '__main__':
  rospy.init_node('calibSensors')
  pub_cal = rospy.Publisher('buzzer', UInt16, queue_size=1)

#  rate = rospy.Rate(1)
  c = CalcAverage()
#  c.buzzerCount()
#  c.values = LightSensorValues()

#  i=0
#  while not i>4:
#  for i in range(10):
#    print "for "+str(i)+"in __main__"
#  sub_sensor_bef=rospy.Subscriber("lightsensors", LightSensorValues, c.calc_bef)
#  rospy.spin()
#    sub_sensor_bef = rospy.Subscriber('lightsensors', LightSensorValues)
#    time.sleep(1)
#    rate.sleep()
#    i=i+1
#  sub_sensor_bef.unregister()

#  print "################caliburation owata#################"

#  while not rospy.is_shutdown():
#  for i in range(5):
#    sub_sensor_aft = rospy.Subscriber('lightsensors', LightSensorValues, c.calc_aft)
#    time.sleep(1)
#  rate.sleep()

#  for j in range(1):
#    print "now="+str(c.count)+","+str(c.values.left_forward)+","+str(c.values.left_side)+","+str(c.values.right_side)+","+str(c.values.right_forward)
#    time.sleep(1)

#  for i in range(1):
#    sub_sensor = rospy.Subscriber('lightsensors', LightSensorValues, c.calc)
#    c.values = LightSensorValues()
#    time.sleep(10)


#  averageL=c.LAV/c.count
#  averageR=c.RAV/c.count
#  print "L average="+str(averageL)
#  print "R average="+str(averageR)
