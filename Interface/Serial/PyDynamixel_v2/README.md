# PyDynamixel_v2
Python interface to the Dynamixel protocol. Supports both Protocols 1 and 2 using Dynamixel SDK python library.

Default is MX-28 control table.

This version is simpler than the one present on the 'more_robust' branch. 

Check which version suits your usage.

## Requirements
PySerial:
```
pip install pyserial
```
Dynamixel SDK python library: 
```
https://github.com/ROBOTIS-GIT/DynamixelSDK
```

## Before Usage - Maximize reading and writing speed

Give USB port permissions.
```
sudo chown username /dev/ttyUSB0
```

Set it to low_latency (1ms, instead of default 16ms)
```
setserial /dev/ttyUSB0 low_latency
```

Check if it worked.
```
cat /sys/bus/usb-serial/devices/ttyUSB0/latency_timer
```

If you encounter problems with reading and writing speeds, making use of a time.sleep(0.1) often helps

## Usage

teste.py script has main functionalities, but basically:

Create a DxlComm instance, the Joint instances, and then attach them to the first.
```
import PyDynamixel_v2 as pd
from math import pi

serial = pd.DxlComm(port='/dev/ttyUSB0', baudrate=1000000)
joint1 = pd.Joint(servo_id=1)
joint2 = pd.Joint(servo_id=2)

serial.attach_joints([joint1, joint2])
```

Get list of attached joints. It is sorted from lowest to highest id value.

```
serial.joint_ids
```

Enable joint torques and then move them with sync write (send_angles function).
You should send the values as a dict. The dict values are then sent to each of the dynamixels.
```
serial.enable_joints()
serial.send_angles({joint1: 90, joint2: 20}) 
  # send these degrees in the same order as the joints were attached
  # joint1 = 90 degrees, joint2 = 20 degrees
serial.send_angles({joint1: pi/2, joint2: pi/3}, radian=True) # angles can be sent as radians too
```

Read joints current position angle. Protocol 2.0 uses sync read.
```
angles = serial.get_angles()
  # the radian flag also works here
angles = serial.get_angles(radian=radian)
```

There are also individual read and write functions.
```
joint1.get_angle()
joint1.send_angle(pi/2, radian=True)
```

There are two ping functions, individual and broadcast. Broadcast is only available within Protocol 2.0
```
serial.broadcast_ping()
joint1.ping()
```
