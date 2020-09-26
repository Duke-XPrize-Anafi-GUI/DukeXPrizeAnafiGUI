# -*- coding: UTF-8 -*-

# Roll- drone left-right tilt.  (must be in [-100:100])
# Pitch- drone front-back tilt.  (must be in [-100:100])
# Gaz- drone vertical speed. (must be in [-100:100])
# Yaw- drone angular speed. (must be in [-100:100])

import olympe
from olympe.messages.ardrone3.Piloting import TakeOff, moveBy, Landing
from olympe.messages.ardrone3.PilotingState import FlyingStateChanged

DRONE_IP = "192.168.42.1"

# Test values
roll = 0
pitch = 0
yaw = 10
gaz = 0
piloting_time = 2

if __name__ == "__main__":
    drone = olympe.Drone(DRONE_IP)
    drone.connect()
    assert drone(
        TakeOff()
        >> FlyingStateChanged(state="hovering", _timeout=5)
    ).wait().success()
    assert drone(
        >> FlyingStateChanged(state="hovering", _timeout=5)
    ).wait().success()
    
    start_piloting()
    
    piloting_pcmd(roll, pitch, yaw, gaz, piloting_time)
    
    stop_piloting()
    
    
    assert drone(Landing()).wait().success()
    drone.disconnect()

    # Plan for Main GUI Loop
    # Check for Drone messeages at every refresh (at least battery and GPS coords)
    
    #              =======================
    #            /start       \sync       \end take off
    # GUI: ====================================>