from __future__ import annotations

from dataclasses import dataclass
from .math import constrain

MOTOR_SPD_STP = 0
MOTOR_SPD_MIN = 70
MOTOR_SPD_MAX = 127

@dataclass(frozen=True)
class MotorCmd:
  """Motor command.

  Contain direction and speed commands for a motor.
  """
  dir: str # '+' forward, '-' backward
  speed: int # MOTOR_SPD_MIN..MOTOR_SPD_MAX

  def __post_init__(self):
    self.__validate_data()

  def __validate_data(self):
    # Check direction
    d = '+' if self.dir == '+' else '-'

    # Check speed range
    if abs(self.speed) > 1:
      spd = constrain(self.speed, MOTOR_SPD_MIN, MOTOR_SPD_MAX)
    else:
      spd = MOTOR_SPD_STP

    # Set properties with __setattr__() because of frozen dataclass
    object.__setattr__(self, "dir", d)
    object.__setattr__(self, "speed", spd)
  
  def toString(self) -> str:
    return f"{self.dir}{chr(self.speed)}"

  def encode(self) -> bytes:
    return self.toString().encode("ascii")

@dataclass(frozen=True)
class RoverCmd:
  """Rover command.
  
  Contain left and right motor commands for a rover.
  """
  left: MotorCmd
  right: MotorCmd

  def toString(self) -> str:
    return f"{self.left.toString()}{self.right.toString()}"

  def encode(self) -> bytes:
    #return self.toString().encode("ascii")
    return self.left.encode() + self.right.encode()
