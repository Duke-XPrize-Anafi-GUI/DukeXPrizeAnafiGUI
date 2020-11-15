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
yaw = 1
gaz = 0
piloting_time = 2

if __name__ == "__main__":
    # Connect to drone using IP (same for all ANAFI units)
    drone = olympe.Drone(DRONE_IP)
    drone.connect()
    # Takeoff sequence
    assert drone(
        # Wait for takeoff to complete before resuming execution
        TakeOff()
        >> FlyingStateChanged(state="hovering", _timeout=5)
    ).wait().success()
    assert drone(
        moveBy(0, 0, 0, 0)
        >> FlyingStateChanged(state="hovering", _timeout=5)
    ).wait().success()
    # Begin manual control of drone 
    start_piloting()
    # Spin drone on axis 
    piloting_pcmd(roll, pitch, yaw, gaz, piloting_time)
    # End manual control 
    stop_piloting()
    
    # Issue land command and wait for success message before disconnecting
    assert drone(Landing()).wait().success()
    drone.disconnect()

    # Plan for Main GUI Loop
    # Check for Drone messeages at every refresh (at least battery and GPS coords)
    
    #              =======================
    #            /start       \sync       \end take off
    # GUI: ====================================>