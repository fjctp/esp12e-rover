#!/usr/bin/env python3 

import socket
import argparse
import time

import keyboard

DEBUG = False

def send_udp_message(ip, port, message):
  # Create a UDP socket
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

  try:
    # Send the message to the server
    sock.sendto(message.encode(), (ip, port))
    if DEBUG:
      print(f"Message '{message}' sent to {ip}:{port}")

  finally:
    # Close the socket
    sock.close()

def encodeCmd(cmd):
  return ('+' if cmd > 0 else '-') + chr(abs(cmd))

def encode(leftCmd, rightCmd):
  return encodeCmd(leftCmd) + encodeCmd(rightCmd)

def constrain(val, minVal, maxVal):
  return min(max(val, minVal), maxVal)

if __name__ == "__main__":
  # Set up the argument parser
  parser = argparse.ArgumentParser(description="Send a message via UDP to a remote server.")
  parser.add_argument("ip", nargs="?", default="192.168.4.1", help="The IP address of the server")
  parser.add_argument("port", nargs="?", default=1234, type=int, help="The port number to send the message to")
  parser.add_argument("max_speed", nargs="?", default=100, type=int, help="Max speed, 0 - 127")
  # parser.add_argument("left", type=int, help="Left, -127 to + 127")
  # parser.add_argument("right", type=int, help="Right, -127 to + 127")

  # Parse the command-line arguments
  args = parser.parse_args()

  print('Press \'q\' to quit.')

  # Send the message
  cmdLeft = 0
  cmdRight = 0
  while True:
    if keyboard.is_pressed('left'):
      cmdLeft = -args.max_speed
      cmdRight = args.max_speed
    elif keyboard.is_pressed('right'):
      cmdLeft = args.max_speed
      cmdRight = -args.max_speed
    elif keyboard.is_pressed('up'):
      cmdLeft = args.max_speed
      cmdRight = args.max_speed
    elif keyboard.is_pressed('down'):
      cmdLeft = -args.max_speed
      cmdRight = -args.max_speed
    elif keyboard.is_pressed('q'):
      break
    else:
      cmdLeft = 0
      cmdRight = 0

    cmdLeft = constrain(cmdLeft, -127, 127)
    cmdRight = constrain(cmdRight, -127, 127)
    send_udp_message(args.ip, args.port, encode(cmdLeft, cmdRight))

    time.sleep(1/100)
