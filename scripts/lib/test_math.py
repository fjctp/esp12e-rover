import pytest
from .math import *

class Test_is_increasing:
  def test_strict(self):
    assert is_increasing([1,2,3]) == True
    assert is_increasing([1,2,2]) == False

  def test_relax(self):
    assert is_increasing([1,2,2], False) == True

  def test_decreasing(self):
    assert is_increasing([1,-1,3]) == False

class Test_Constrain():
  def test_inRange(self):
    assert constrain(1, -1, 1) == 1

  def test_outOfRange(self):
    assert constrain(-3, -1, 1) == -1
    assert constrain(7, -1, 1) == 1

class Test_Mapping():
  def test_inRange(self):
    assert mapping(0.5, [0, 1], [0, 100]) == 50
  
  def test_outOfRange(self):
    assert mapping(-0.5, [0, 1], [0, 100]) == -50
    assert mapping(1.5, [0, 1], [0, 100]) == 150

  def test_nonlinear(self):
    val = mapping(0.5, [-1, -.2, 0, .2, 1], [-100, 0, 0, 0, 100])
    assert pytest.approx(val, .1) == 37.5
