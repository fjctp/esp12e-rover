import pytest
from .payload import *

class Test_MotorCmd:
  def test_constructor(self):
    a = MotorCmd('+', 100)

    assert a.dir == '+'
    assert a.speed == 100

  def test_validator(self):
    a = MotorCmd('+', 200)

    assert a.dir == '+'
    assert a.speed == 127
  
  def test_encode(self):
    a = MotorCmd('+', 100)
    assert a.encode() == '+d'

class Test_RoverCmd():
  def test_constructor(self):
    a = MotorCmd('+', 100)
    b = RoverCmd(a, a)

    assert b.left == a
    assert b.right == a

  def test_encode(self):
    a = MotorCmd('+', 100)
    b = RoverCmd(a, a)

    assert b.encode() == '+d+d'
