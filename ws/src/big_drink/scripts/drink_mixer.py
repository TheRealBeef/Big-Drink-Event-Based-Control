#!/usr/bin/env python

from sys import argv
from time import sleep

import rospy
from std_msgs.msg import String, Bool

class Order:
  def __init__(self, name="Free", nr=0):
    self.name = name
    self.nr = nr

class DrinkMixer:
  
  def __init__( self, max_orders ):
    
    rospy.init_node('drink_mixer', anonymous=True)

    rospy.Subscriber('close', Bool, self.close_callback)
    rospy.Subscriber('order', String, self.order_callback)
    rospy.Subscriber('glass_state', String, self.glass_state_callback)
    
    self.pub_mixer_status = rospy.Publisher('drink_mixer_state', String, queue_size=10)
    self.pub_order_status = rospy.Publisher('order_status', String, queue_size=10)
    
    self.orders = [ Order("Free",i) for i in range(max_orders) ]
    self.current_order = self.orders[0]
    self.glass_state = "No Glass"
    self.glass_available = False
    self.should_run = True
    self.should_serve_order = False
    self.order_waiting = False
    self.drink_handled = False
    self.current_state = "Idle"
  

  def order_callback(self,order):

    log_str = " Order \"" + order.data + "\" received"
    rospy.loginfo(rospy.get_caller_id() + log_str)

    if not self.can_take_order():
      msg = "There is already " + str(len(self.orders)) + " orders that must be served."
      self.pub_order_status.publish(msg)
      rospy.loginfo(rospy.get_caller_id() + " Max number of orders reached!")

    else:
      nr = self.collect_order(order.data)
      msg = "Your order \"" + order.data + "\" has a number " + str(nr+1) + "."
      self.pub_order_status.publish(msg)
      log_str = " Order \"" + order.data + "\" received. Number " + str(nr+1) + " assigned"
      rospy.loginfo(rospy.get_caller_id() + log_str)
      if self.current_state == "Idle":
        if self.glass_state == "No Glass":
          self.current_state = "No Glass"
          self.update_state()
        elif self.glass_state == "Empty Glass Ready":
          self.should_serve_order = True
        else:
          self.invalid_glass_state()


  def glass_state_callback(self,glass_state):

    log_str = " Message \"" + glass_state.data + "\" received"
    rospy.loginfo( rospy.get_caller_id() + log_str )

    self.glass_state = glass_state.data
    if self.current_state == "Drink Ready":
      self.drink_handled = True
    elif self.glass_state == "Empty Glass Ready":
      self.glass_available = True
      if self.current_state == "No Glass":
        self.should_serve_order = True
    elif self.glass_state == "No Glass":
      self.glass_available = False
      if self.current_state == "Drink Ready":
        self.current_state = "Idle"
        self.update_state()
    else:
      self.invalid_glass_state()


  def close_callback(self, must_end):

    self.should_run = not must_end.data
    log_str = " Process must finish: " + str(must_end.data) + "."
    rospy.loginfo(rospy.get_caller_id() + log_str )


  def serve_order(self):

    self.current_order = self.take_order()
    self.current_state = "Drink Pouring"
    self.update_state()
    msg = "Your drink from order nr " + \
      str(self.current_order.nr +1) + ": '" + \
      self.current_order.name + \
      "' is getting ready!"
    self.pub_order_status.publish(msg)
    sleep(2)
    self.current_state = "Drink Ready"
    self.update_state()
    msg = "Your drink from order nr " + \
      str(self.current_order.nr + 1) + ": '" + \
      self.current_order.name + "' is ready!"
    self.pub_order_status.publish(msg)


  def update_state(self):

    self.pub_mixer_status.publish(self.current_state)
    log_str = " Change state to " + self.current_state + "."
    rospy.loginfo(rospy.get_caller_id() + log_str)


  def can_take_order(self):
    for order in self.orders:
      if order.name == "Free":
        return True
    return False


  def collect_order(self, order_name):
    for order in self.orders:
      if order.name == "Free":
        order.name = order_name
        return order.nr
      else:
        order_found = False
    if not order_found:
      rospy.logerr(rospy.get_caller_id() + " No order with a name " + order_name)
      raise ValueError("No order with a name " + order_name)


  def take_order(self):
    for order in self.orders:
      if order.name != "Free":
        return order
    rospy.logerr(rospy.get_caller_id() + " No order to serve!")
    raise ValueError("No order to serve!")


  def no_order(self):
    for order in self.orders:
      if order.name != "Free":
        return False
    return True


  def clean_order(self):
    for order in self.orders:
      if order.nr == self.current_order.nr:
        order.name = "Free"
        log_str = " Number " + str(order.nr+1) + "can be assigned to an order."
        rospy.loginfo(rospy.get_caller_id() + log_str)
        return
    log_str = " Can't clean order nr " + str(self.current_order.nr) + \
    ". It doesn't match abailable order numbers."
    rospy.logerr(rospy.get_caller_id() + log_str)
    raise ValueError(log_str)


  def invalid_glass_state(self):
    err_msg = \
    "Invalid glass state: \"" + self.glass_state + \
    "\". Valid states are:\n" + \
    "\t- \"Empty Glass Ready\" " + \
    "\t- \"No Glass\" "
    raise ValueError(err_msg)


  def run(self):

    self.update_state()
    while self.should_run:
      sleep(0.1)
      if self.should_serve_order:
        self.should_serve_order = False
        self.serve_order()
        # Drink ready
        while not self.drink_handled:
          # Wait for robotic arm
          sleep(0.1)
        self.clean_order()
        if self.no_order():
          self.current_state = "Idle"
          self.update_state()
        else:
          if self.glass_available:
            self.should_serve_order = True
          else:
            self.current_state = "No Glass"
            self.update_state()

    rospy.loginfo(rospy.get_caller_id() + " Ending a process")

if __name__ == '__main__':
  mixer = DrinkMixer( int(argv[1]) )
  mixer.run()