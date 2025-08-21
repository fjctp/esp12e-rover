#!/usr/bin/env python3 

import socket
import argparse
import time

import pygame

CONTROL_METHOD = 3

def send_udp_message(ip: str, port: int, message: str, debug: bool):
  """
  Send a UDP message to a UDP server.

  Args:
    ip (str): UDP server IP address
    port (int): UDP server IP address
    message (str): A message
  """
  # Create a UDP socket
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

  try:
    # Send the message to the server
    sock.sendto(message.encode(), (ip, port))
    if debug:
      print(f"Message '{message}' sent to {ip}:{port}")

  finally:
    # Close the socket
    sock.close()

def encodeCmd(cmd: int):
  """
  Encode a motor command to a pair of chars.

  Char 1         | Char 2
  Motor direction| motor speed

  Args:
    cmd (int): A motor command.
  """
  return ('+' if cmd > 0 else '-') + chr(abs(cmd))

def encode(cmdLeft: int, cmdRight: int):
  """
  Encode motor commands to a UDP message.

  A UDP message contains four chars.

  Char 1                 | Char 2             | Char 3                 | Char 4             |
  Motor direction (left) | Motor speed (left) | Motor direction (right) | Motor speed (right) |

  Args:
    cmdLeft (int): Left motor command.
    cmdRight (int): Right motor command.
  """
  return encodeCmd(cmdLeft) + encodeCmd(cmdRight)

def deadzone(val: float, tolerance: float):
  """
  Return 0 if the abs(value) is less than tolerance.

  Args:
    val (float): Value.
    tolerance (float): Tolerance.
  """

  if abs(val) < tolerance:
    return 0
  return val

def constrain(val: float, minVal: float, maxVal: float):
  """
  Limit value within defined range.

  Args:
    val (float): Value.
    minVal (float): Min. value.  
    maxVal (float): Max. value.  
  """
  return min(max(val, minVal), maxVal)

def rescale(val, fromMinMax, toMinMax):
  """
  Remap value from old range to new range.
  """
  cmd = (toMinMax[1] - toMinMax[0])/(fromMinMax[1] - fromMinMax[0]) * (val - fromMinMax[0]) + toMinMax[0]
  return cmd

if __name__ == "__main__":
  # Set up the argument parser
  parser = argparse.ArgumentParser(description="Send a message via UDP to a remote server.")
  parser.add_argument("ip", nargs="?", default="192.168.4.1", help="The IP address of the server")
  parser.add_argument("port", nargs="?", default=1234, type=int, help="The port number to send the message to")
  parser.add_argument("max_speed", nargs="?", default=100, type=int, help="Max speed, 0 - 127")
  parser.add_argument("--debug", action='store_true', help="Enable debug mode")

  # Parse the command-line arguments
  args = parser.parse_args()
  # print('Press \'q\' to quit.')

  pygame.init()
  pygame.joystick.init()
  # Check for connected joysticks
  if pygame.joystick.get_count() == 0:
    print("No joystick connected.")

    pygame.quit()
    quit()

  joystick = pygame.joystick.Joystick(0)
  joystick.init()
  print(f"Joystick {joystick.get_name()} connected")

  isInitialized = False

  try:
    while True:
      pygame.event.pump()  # Process events
      
      if CONTROL_METHOD == 1:
        # Method 1: Using left and right y-axis joysticks
        yleft = -1 * deadzone(joystick.get_axis(1), 0.1)
        yright = -1 * deadzone(joystick.get_axis(3), 0.1)

        cmdLeft = rescale(yleft, (-1, 1), (-127, 127))
        cmdRight = rescale(yright, (-1, 1), (-127, 127))

        if args.debug:
          print(f"Left: {yleft}/{cmdLeft}, Right: {yright}/{cmdRight}")
        else:
          send_udp_message(args.ip, args.port, encode(cmdLeft, cmdRight), args.debug)
      elif CONTROL_METHOD == 2:
        # Method 2: Using left and right trigger for speed and the button above for direction.
        if isInitialized:
          yleft = joystick.get_axis(4)
          yright = joystick.get_axis(5)

          spdLeft = deadzone(rescale(yleft, (-1, 1), (0, 127)), 10)
          spdRight = deadzone(rescale(yright, (-1, 1), (0, 127)), 10)

          dirLeft = 1 if joystick.get_button(9) == 0 else -1 # forward if pressed
          dirRight = 1 if joystick.get_button(10) == 0 else -1 # forward if pressed

          cmdLeft = dirLeft * spdLeft
          cmdRight = dirRight * spdRight

          if args.debug:
            print(f"Left: {yleft}/{cmdLeft}, Right: {yright}/{cmdRight}")
          else:
            send_udp_message(args.ip, args.port, encode(int(cmdLeft), int(cmdRight)), args.debug)
        else:
          # Wait for a button press or an axis movement, 
          # otherwise axis 4 and 5 would return invalid min. value (0)
          if joystick.get_button(9) == 1 or joystick.get_button(10) == 1:
            isInitialized = True
      elif CONTROL_METHOD == 3:
        # Method 3: Using left joysticks, x and y axis
        yleft = -1 * deadzone(joystick.get_axis(1), 0.1)
        xleft = deadzone(joystick.get_axis(0), 0.2)

        cmdSpd = rescale(yleft, (-1, 1), (-127, 127))
        cmdDiff = rescale(xleft, (-1, 1), (-127, 127))

        cmdLeft = int(cmdSpd + cmdDiff)
        cmdRight = int(cmdSpd - cmdDiff)

        if args.debug:
          print(f"Joy: {cmdSpd}/{cmdDiff}, Left: {cmdLeft}, Right: {cmdRight}")
        else:
          send_udp_message(args.ip, args.port, encode(cmdLeft, cmdRight), args.debug)
      else:
        raise KeyError
      
      time.sleep(1/100)

  except KeyboardInterrupt:
    print("Exiting...")
    pygame.quit()
