from typing import Iterable
from numbers import Number

def is_increasing(vals: Iterable[Number], is_strict: bool = True):
  """Check if a list is strictly increasing."""
  for l, r in zip(vals[:-1], vals[1:]):
    if is_strict:
      op = lambda x, y: x >= y
    else:
      op = lambda x, y: x > y
    if op(l, r):
      return False
  return True

def constrain(val: Number, minVal: Number, maxVal: Number):
  """
  Limit value within defined range.

  Args:
    val (Number): Value.
    minVal (Number): Min. value.  
    maxVal (Number): Max. value.  
  """
  return min(max(val, minVal), maxVal)

def mapping(val:Number, fromMinMax:Number, toMinMax:Number):
  """
  Remap value from old range to new range.
  """
  assert is_increasing(fromMinMax)
  assert is_increasing(toMinMax, False)
  assert len(fromMinMax) == len(toMinMax)

  if val > fromMinMax[-1]:
    # Greater than max
    minFrom = fromMinMax[-2]
    maxFrom = fromMinMax[-1]
    minTo = toMinMax[-2]
    maxTo = toMinMax[-1]
  
  elif val < fromMinMax[0]:
    # Smaller than min
    minFrom = fromMinMax[0]
    maxFrom = fromMinMax[1]
    minTo = toMinMax[0]
    maxTo = toMinMax[1]

  else:
    # Within range
    for i in range(len(fromMinMax)):
      if val <= fromMinMax[i]:
        minFrom = fromMinMax[i-1]
        maxFrom = fromMinMax[i]
        minTo = toMinMax[i-1]
        maxTo = toMinMax[i]
        break

  ratio = (val - minFrom)/(maxFrom - minFrom)
  cmd = ratio * (maxTo - minTo) + minTo
  return cmd
