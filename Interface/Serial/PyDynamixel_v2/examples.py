import PyDynamixel_v2 as pd
from math import pi
from time import sleep

# Declare the DxlComm variable
port = "COM5"
baudrate = 57600
serial = pd.DxlComm(port=port, baudrate=baudrate)

# Declare a dynamixel joint
dyn_id = 2
dyn = pd.Joint(dyn_id)

# Attach this joint to DxlComm to enable serial communication
print("Attach joint")
serial.attach_joint(dyn)
# You could also send all joints as a list to DxlComm varible
# serial.attach_joints([dyn, dyn2, dyn3])


# Enable single joint torque or all joints torques
print("Enable torque")
dyn.enable_torque()
serial.enable_torques()

sleep(2)

def write():
    print("Single joint write test")
    for i in range(50, 90, 10):
        dyn.send_angle(i)
        print("Set/Current angle: {}/{}".format(i, dyn.get_angle()))

def sync_write():
    # Sync write of all attached joints, or just a few (more details in code docs)
    print("Sync write test")
    for i in range(50, 90, 10): # Send angles as degrees
        serial.send_angles(values={dyn_id: i})
        sleep(0.1)
        print("Set/Current angle: {}/{}".format(i, dyn.get_angle()))
    sleep(1)
    # Angles can be sent as radians too
    serial.send_angles(values={dyn_id: pi/3}, radian=True)
    sleep(0.1)
    print("Set/Current angle: {}/{}".format("pi/3 ", dyn.get_angle()))

def sync_read():
    # Sync Read of all attached joints. Only in Protocol 2.0
    print("Sync read test")
    angles = serial.get_angles()
    print(angles)

def all_pings():
    # Broadcast ping only available for Protocol 2.0
    serial.broadcast_ping()
    dyn.ping()

sync_write()
sync_read()
all_pings()
#dyn.reboot()

# Disable all or single joints torques
print("Disable torque")
serial.disable_torques() # all joints
dyn.disable_torque()     # single joint

# Close serial port
serial.release()
