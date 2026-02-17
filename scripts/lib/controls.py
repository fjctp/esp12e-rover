from __future__ import annotations

from dataclasses import dataclass
from typing import Generator

from .payload import MotorCmd, RoverCmd, MOTOR_SPD_MAX, MOTOR_SPD_MIN, MOTOR_SPD_STP
from .math import mapping

@dataclass
class KeyboardConfig:
  hold_val: int = 100 # when held

class KeyboardController:
  """Arrow‑key controller (requires `keyboard` package; sudo on Linux).

  Exposes a generator of payload bytes using the README 4‑char format.
  """

  __cfg: KeyboardConfig
  __cmd: RoverCmd
  __kb: module # 'keyboard' module

  def __init__(self, cfg: KeyboardConfig | None = None):
    self.__cfg = cfg or KeyboardConfig()
    self.__cmd = RoverCmd(MotorCmd('+', 0), MotorCmd('+', 0))
    
    try:
      import keyboard as _kb # runtime import
    except Exception as e: # pragma: no cover
      raise RuntimeError("keyboard module not available") from e
    self.__kb = _kb

    # Register non‑blocking handlers
    self.__kb.on_press(self._on_press)

  def _on_press(self, ev): # pragma: no cover (integration)
    name = getattr(ev, "name", "")
    if name == "up":
      self.__cmd = RoverCmd(
        MotorCmd('+', self.__cfg.hold_val), 
        MotorCmd('+', self.__cfg.hold_val)
      )
    elif name == "down":
      self.__cmd = RoverCmd(
        MotorCmd('-', self.__cfg.hold_val), 
        MotorCmd('-', self.__cfg.hold_val)
      )
    elif name == "left":
      self.__cmd = RoverCmd(
        MotorCmd('-', self.__cfg.hold_val), 
        MotorCmd('+', self.__cfg.hold_val)
      )
    elif name == "right":
      self.__cmd = RoverCmd(
        MotorCmd('+', self.__cfg.hold_val), 
        MotorCmd('-', self.__cfg.hold_val)
      )
    elif name == "space":
      self.__cmd = RoverCmd(
        MotorCmd('+', 0), 
        MotorCmd('+', 0)
      )
    
    # debug: remove!
    print(f"Motor command: {self.__cmd.left.speed}/{self.__cmd.right.speed}")
    print(f"Payload: {self.__cmd.encode()}")

  def stream(self) -> Generator[bytes, None, None]:
    while True:
      yield self.__cmd.encode()

class JoystickController:
  """Simple pygame‑based joystick controller producing payload bytes.
  
  Method 0: Using left pad
  Method 1: Using left and right trigger and button above
  """

  def __init__(self, method : int = 0, devID : int = 0):
    import pygame

    pygame.init()
    pygame.joystick.init()
    if pygame.joystick.get_count() == 0:
      raise RuntimeError("No joystick found")
    self.__js = pygame.joystick.Joystick(devID)
    self.__js.init()
    self.__method = method
    self.__cmd = RoverCmd(MotorCmd('+', 0), MotorCmd('+', 0))
    if self.__method == 1:
      self.__ready = False
    else:
      self.__ready = True
  
  def stream(self) -> Generator[bytes, None, None]:
    import pygame

    while True:
      pygame.event.pump()
      
      if self.__method == 0:
        # Using left pad
        x_val = self.__js.get_axis(0)
        y_val = -1 * self.__js.get_axis(1)

        x_from_range = (-1, -.1, 0, .1, 1)
        x_to_range = (-MOTOR_SPD_MAX, MOTOR_SPD_STP, MOTOR_SPD_STP, MOTOR_SPD_STP, MOTOR_SPD_MAX)
        diff = mapping(x_val, x_from_range, x_to_range)
        diff = int(round(diff))

        y_from_range = (-1, -.21, -.2, 0, .2, .21, 1)
        y_to_range = (-MOTOR_SPD_MAX, -MOTOR_SPD_MIN, MOTOR_SPD_STP, MOTOR_SPD_STP, MOTOR_SPD_STP, MOTOR_SPD_MIN, MOTOR_SPD_MAX)
        spd = mapping(y_val, y_from_range, y_to_range)
        spd = int(round(spd))

        l_val, r_val = (spd + diff, spd - diff)
        l_dir = '+' if l_val > 0 else '-'
        r_dir = '+' if r_val > 0 else '-'
        print(f"S{spd}D{diff}, {l_val}/{r_val}")

        self.__cmd = RoverCmd(MotorCmd(l_dir, abs(l_val)), MotorCmd(r_dir, abs(r_val)))

      elif self.__method == 1:
        if not self.__ready:
          # Wait for a button press. otherwise axis 4 and 5 would return invalid value.
          if self.__js.get_button(9) == 1 or self.__js.get_button(10) == 1:
            self.__ready = True
        else:
          # Check direction
          l_dir = '+' if self.__js.get_button(9) == 0 else '-' # backward if pressed
          r_dir = '+' if self.__js.get_button(10) == 0 else '-' # backward if pressed

          # Using left/right triggers
          l_val = self.__js.get_axis(4)
          r_val = self.__js.get_axis(5)

          from_range = (-1, -.81, -.8, 1)
          to_range = (MOTOR_SPD_STP, MOTOR_SPD_STP, MOTOR_SPD_MIN, MOTOR_SPD_MAX)
          l_spd = int(mapping(l_val, from_range, to_range))
          r_spd = int(mapping(r_val, from_range, to_range))
          print(f"{l_val:.2f}/{r_val:.2f}, {l_spd}/{r_spd}")

          self.__cmd = RoverCmd(MotorCmd(l_dir, l_spd), MotorCmd(r_dir, r_spd))

      else:
        raise KeyError()

      yield self.__cmd.encode()
