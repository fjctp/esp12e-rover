from __future__ import annotations

import socket
from typing import Iterable, Optional

def create_socket(*, ttl: Optional[int] = None, bind: Optional[str] = None) -> socket.socket:
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  if ttl is not None:
    # IP_TTL works for unicast; IP_MULTICAST_TTL would be for multicast.
    s.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, int(ttl))
  if bind:
    s.bind((bind, 0))
  return s

def send_once(sock: socket.socket, host: str, port: int, payloads: bytes) -> int:
  count = sock.sendto(payloads, (host, int(port)))
  print(f"Sent {count} bytes, payload: {payloads}")
  return count

def send_loop(sock: socket.socket, host: str, port: int, payloads: Iterable[bytes],
              *, rate_hz: float | None = None, time_mod=None):
  """Send each payload sequentially; throttle if rate_hz given.

  - payloads: any iterable; generators allow dynamic control input.
  - time_mod: injects module with time()/sleep() for deterministic tests.
  """
  import time as _time

  t = time_mod or _time
  period = 1.0 / rate_hz if rate_hz and rate_hz > 0 else 0.0
  next_at = t.time()
  for p in payloads:
    send_once(sock, host, port, p)
    if period:
      next_at += period
      # busy‑wait avoidance with bounded sleep
      while True:
        now = t.time()
        dt = next_at - now
        if dt <= 0:
          break
        t.sleep(min(dt, 0.01))
