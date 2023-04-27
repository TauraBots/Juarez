# to maximize reading/writing speed before usage do:
# sudo chown username /dev/ttyUSB0
# setserial /dev/ttyUSB0 low_latency
# cat /sys/bus/usb-serial/devices/ttyUSB0/latency_timer

import PyDynamixel_v2 as pd
from time import sleep

port = '/dev/ttyUSB0'
baudrate = 1000000

serial = pd.DxlComm(port=port, baudrate=baudrate)

dyn1_id = 31
dyn2_id = 7
dyn1 = pd.Joint(dyn1_id)
dyn2 = pd.Joint(dyn2_id)

serial.attach_joints([dyn1, dyn2])

serial.enable_torques()

print(serial.joint_ids)

def sync_write_read():
    for i in range(150, 200, 10):
        serial.send_angles({31:i-10, 7:i})
        #serial.send_angles([i, i-10]) # this is sent for the dyn order from serial.joint_ids
        sleep(0.1)
        #angles = dyn.get_angle()
        angles = serial.get_angles()
        print("Sent/read angles: 7: {}, 31:{}/{}".format(i, i-10, angles))

sync_write_read()
