#!/usr/bin/env python

from sys import argv
from time import sleep

import rospy
from std_msgs.msg import String, Bool

class DrinkMixer:
  
  def __init__( self, max_orders ):
    
    rospy.init_node('drink_mixer', anonymous=True)

    rospy.Subscriber('close', Bool, self.close_callback)
    rospy.Subscriber('order', String, self.order_callback)
    rospy.Subscriber('glass_state', String, self.glass_state_callback)
    
    self.pub_mixer_status = rospy.Publisher('drink_mixer_state', String, queue_size=10)
    self.pub_order_status = rospy.Publisher('order_status', String, queue_size=10)
    
    self.orders = [ "Free" for i in range(max_orders) ]
    self.glass_state = "No Glass"
    self.glass_available = False
    self.should_run = True
    self.current_state = "Idle"

    self.update_state()
  

  def order_callback(self,order):

    if not self.can_take_order():
      msg = "There is already " + len(self.orders) + " orders that must be served."
      self.pub_order_status.publish(msg)
      rospy.loginfo(rospy.get_caller_id() + " Max number of orders reached!")

    else:
      nr = self.take_order(order.data)
      msg = "Your order \"" + order.data + "\" has a number " + nr+1 + "."
      self.pub_order_status.publish(msg)
      log_str = " Order \"" + order.data + "\" received. Number " + nr+1 + " assigned"
      rospy.loginfo(rospy.get_caller_id() + log_str)


  def glass_state_callback(self,glass_state):

    self.glass_state = glass_state.data
    if self.glass_state == "Empty Glass Ready":
      self.glass_available = True
    elif self.glass_state == "No Glass":
      self.glass_available = False
    else:
      err_msg = \
      "Invalid glass state: \"" + self.glass_state + \
      "\". Valid states are:\n" + \
      "\t- \"Empty Glass Ready\" " + \
      "\t- \"No Glass\" "
      raise ValueError(err_msg)


  def close_callback(self, must_end):

    self.should_run = not must_end.data
    rospy.loginfo(rospy.get_caller_id() + " Process must finish: " + str(must_end.data) + "." )
  
  def serve_order(self):
    #TODO: CHANGE IT 
    order = self.orders.get()
    self.current_state = "Drink Pouring"
    self.update_state()
    self.pub_order_status.publish("Your drink from \"" + order + "\" is getting ready!")
    sleep(2)
    self.current_state = "Drink Ready"
    self.pub_order_status.publish("Your drink from \"" + order + "\" is ready!")


  def update_state(self):

    self.pub_mixer_status.publish(self.current_state)
    rospy.loginfo(rospy.get_caller_id() + " Status: " + self.current_state + ".")


  def can_take_order(self):
    if "Free" in self.orders:
      return True
    else:
      return False

  def take_order(self, order):
    id = self.orders.index("Free")
    self.order[id] = order
    return id


  def no_order(self):
    for i in range(len(self.orders)):
      if not self.orders[i] == "Free":
        return False
    return True


  def run(self):

    # TODO: IT ITERATES EVERY 0.001s!!
    while self.should_run:
      if self.no_order():
        self.current_state = "Idle"
      elif not self.glass_available:
        self.current_state = "No Glass"
      elif self.current_state == "Drink Ready":
        sleep(0.01)
      else:
        self.serve_order()

      self.update_state()

    rospy.loginfo(rospy.get_caller_id() + " Ending a process")

if __name__ == '__main__':
  mixer = DrinkMixer( int(argv[1]) )
  mixer.run()