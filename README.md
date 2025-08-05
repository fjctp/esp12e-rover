# ESP12e Rover
WiFi controlled rover with ESP-12e.

# How does it work
The ESP-12e rover is controlled by a keyboard (arrow keys) through a wireless access point (SSID: `rover-df473fcc`) created by ESP-12e.

![](./asset/esp12e-rover.drawio.svg)

**UDP package**
A package has a length of 4 characters.

- Character 1: Left motor direction ('+': forward, '-': backward)
- Character 2: Left motor speed (0 - 127, encoded as an ASCII character. Ex. 97 -> 'a')
- Character 3: Right motor direction (Same as left motor)
- Character 4: Right motor speed (Same as left motor)

**Example**: `+a-2`

| Motor | Direction | Speed (0 - 127) |
|-------|-----------|-----------------|
| Left  | Forward   |       97        |
| Right | Backward  |       50        |

# What do you need

**Hardware**
- ESP-12e
- ESP-12e Motor Driver Board
- Battery (e.g. 9V battery)

**Software**
- Python3.12
  - 3rd party package: `keyboard`
- Arduino IDE (optional for firmware development)
  - Additional board support: `arduino-esp8266`

# Run

1. Open the project with Arduino IDE.
    - Install esp9266 board support for Arduino IDE.
    - Configure IDE for ESP-12e. (Tool -> Board and Port)
2. Upload sketch (`.ino`) to ESP-12e.
3. Power up ESP-12e
4. On the compute, connect to wireless access point (SSID: `rover-df473fcc`).
5. Run `sudo python3 scripts/udp_client.py`
    - Install dependencies: `keyboard`
