from __future__ import annotations

import argparse
from typing import Iterable

from .udp import create_socket, send_loop
from .controls import KeyboardController, JoystickController

def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
  p = argparse.ArgumentParser(description="ESP12e rover UDP client")
  grp1 = p.add_argument_group("Server Config")
  grp1.add_argument("--host", default="192.168.4.1", help="rover IP")
  grp1.add_argument("--port", type=int, default=1234, help="rover port")
  grp1.add_argument("--rate", type=float, default=20.0, help="UDP message send rate in Hz")
  grp1.add_argument("--ttl", type=int, default=None)
  grp1.add_argument("--bind", default=None, help="local bind address")

  src = p.add_mutually_exclusive_group()
  src.add_argument("--keyboard", action="store_true", help="use keyboard arrows")
  src.add_argument("--joystick", action="store_true", help="use pygame joystick")
  p.add_argument("--joystick-method", type=int, default=0, help="joystick control method")
  
  p.add_argument("--message", default=None, help="(Debug) literal 4‑char message to repeat")
  p.add_argument("--count", type=int, default=None, help="(Debug) number of frames to send (default infinite)")
  return p.parse_args(argv)

def _iter_from_message(msg: str) -> Iterable[bytes]:
  if len(msg) != 4:
    raise ValueError("message must be exactly 4 chars, e.g. '+a-2'")
  yield msg.encode("ascii")
  while True:
    yield msg.encode("ascii")

def main(argv: list[str] | None = None) -> int:
  ns = parse_args(argv)

  if ns.keyboard:
    source = KeyboardController().stream()
  elif ns.joystick:
    source = JoystickController().stream()
  elif ns.message:
    source = _iter_from_message(ns.message)
  else:
    # default: gentle forward crawl
    source = _iter_from_message("+\x20+\x20") # space (32) ≈ slow

  print("test")

  # cap the stream if count provided
  if ns.count is not None:
    def capped(it, n):
      for i, b in enumerate(it):
        if i >= n:
          break
        yield b
    source = capped(source, ns.count)

  sock = create_socket(ttl=ns.ttl, bind=ns.bind)
  try:
    send_loop(sock, ns.host, ns.port, source, rate_hz=ns.rate)
  except KeyboardInterrupt:
    pass
  finally:
    sock.close()
  return 0

