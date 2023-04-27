import dearpygui.dearpygui as dpg 
from Interface.dpg_context import * 
from dynamixel_sdk import *

# Control table address
ADDR_MX_TORQUE = 24
ADDR_MX_GOAL_POSITION = 30
ADDR_TORQUE_LIMIT = 34
ADDR_MX_PRESENT_POSITION = 36
ADDR_MOVING = 46
ADDR_LOAD = 40

# Protocol version
PROTOCOL_VERSION = 1.0

# Default setting
DXL_ID_X = 1
DXL_ID_Y = 2

# Macrodefinitions
TORQUE_ENABLE  = 1
TORQUE_DISABLE = 0


MAX_POS_X = 849 
MIN_POS_X = 3254
MAX_POS_Y = 2431
MIN_POS_Y = 866

# Visão traseira do Juarez 
Joints = { 'OMBRO_GIRO_L'    :   4,
           'OMBRO_ELEVA_L'   :   6,
           'COTOVELO_L'      :   8, 

           'OMBRO_GIRO_R'    :   3 ,
           'OMBRO_ELEVA_R'   :   5 ,
           'COTOVELO_R'      :   7  } 


# REGISTRADORES DPG 
DEVICE     = dpg.add_string_value( tag = 'DEVICE'   , default_value = 'COM1', parent = values_registry )
BAUDRATE   = dpg.add_int_value   ( tag = 'BAUDRATE' , default_value = 57600 , parent = values_registry )
SERIAL_OK  = dpg.add_bool_value  ( tag = 'SERIAL_OK', default_value = False , parent = values_registry )

POS_MOTOR_X = dpg.add_int_value( tag = 'GO_MOTOR_X', default_value = 2048, parent = values_registry )
POS_MOTOR_Y = dpg.add_int_value( tag = 'GO_MOTOR_Y', default_value = 1864, parent = values_registry )

TORQUE = dpg.add_bool_value( tag = 'TORQUE', default_value = False, parent = values_registry )

# FUNÇÕES DO DxlCom
portHandler = PortHandler( dpg.get_value( DEVICE ) ) 
packetHandler = PacketHandler(PROTOCOL_VERSION)

def enable_torque( sender, data, user):
    dpg.set_value( TORQUE, not dpg.get_value( TORQUE ) )
    if dpg.get_value( TORQUE ):
        set_torque( True )
    else: 
        set_torque( False ) 


def set_PID():
    global packetHandler, portHandler 
    for ID in [DXL_ID_X, DXL_ID_Y]:
        packetHandler.write1ByteTxRx(portHandler, ID, 28, 7)      # P
        packetHandler.write1ByteTxRx(portHandler, ID, 27, 0)      # I
        packetHandler.write1ByteTxRx(portHandler, ID, 26, 200)    # D

def dpg_att_position( x, y ):
    dpg.set_value( POS_MOTOR_X, x )
    dpg.set_value( POS_MOTOR_Y, y )

def go_initial_position():
    packetHandler.write2ByteTxRx(portHandler, DXL_ID_X, ADDR_MX_GOAL_POSITION,  1470 )
    packetHandler.write2ByteTxRx(portHandler, DXL_ID_Y, ADDR_MX_GOAL_POSITION,  2000 )
    dpg_att_position( 1470, 2000 )

def set_abs_position( pos_x : int, pos_y : int ): 
    packetHandler.write2ByteTxRx(portHandler, DXL_ID_X, ADDR_MX_GOAL_POSITION,  pos_x )
    packetHandler.write2ByteTxRx(portHandler, DXL_ID_Y, ADDR_MX_GOAL_POSITION,  pos_y )
    dpg_att_position( pos_x, pos_y )

def set_rel_position( pos_x : int, pos_y : int ): 
    packetHandler.write2ByteTxRx(portHandler, DXL_ID_X, ADDR_MX_GOAL_POSITION,  dpg.get_value( POS_MOTOR_X ) + pos_x )
    packetHandler.write2ByteTxRx(portHandler, DXL_ID_Y, ADDR_MX_GOAL_POSITION,  dpg.get_value( POS_MOTOR_Y ) + pos_y )
    dpg_att_position( dpg.get_value( POS_MOTOR_X ) + pos_x, dpg.get_value( POS_MOTOR_Y ) + pos_y )
   
def set_torque( torque : bool ):
    if torque:
        packetHandler.write1ByteTxRx(portHandler, DXL_ID_X, ADDR_MX_TORQUE, TORQUE_ENABLE)
        packetHandler.write1ByteTxRx(portHandler, DXL_ID_Y, ADDR_MX_TORQUE, TORQUE_ENABLE)
    else:     
        packetHandler.write1ByteTxRx(portHandler, DXL_ID_X, ADDR_MX_TORQUE, TORQUE_DISABLE)
        packetHandler.write1ByteTxRx(portHandler, DXL_ID_Y, ADDR_MX_TORQUE, TORQUE_DISABLE)
    for joint in Joints.values():
        if torque:
            packetHandler.write1ByteTxRx(portHandler, joint, ADDR_MX_TORQUE, TORQUE_ENABLE)
        else:     
            packetHandler.write1ByteTxRx(portHandler, joint, ADDR_MX_TORQUE, TORQUE_DISABLE)
        

def set_speed( speed : float ) -> bool:
    if speed < 0:        speed = 0
    elif speed > 1024:   speed = 1024 
    packetHandler.write2ByteTxRx(portHandler, DXL_ID_X, ADDR_TORQUE_LIMIT, speed )
    packetHandler.write2ByteTxRx(portHandler, DXL_ID_Y, ADDR_TORQUE_LIMIT, speed )
        
def get_moving( ) -> bool:
    dxl_moving_x, dxl_comm_result_x, dxl_error_x = packetHandler.read1ByteTxRx( portHandler, DXL_ID_X, ADDR_MOVING )
    dxl_moving_y, dxl_comm_result_y, dxl_error_y = packetHandler.read1ByteTxRx( portHandler, DXL_ID_Y, ADDR_MOVING )
    return ( dxl_moving_y or dxl_moving_x ) 

def get_load() -> float:
    dxl_load, dxl_comm_result_x, dxl_error_x = packetHandler.read2ByteTxRx( portHandler, DXL_ID_X, ADDR_LOAD )
    return dxl_load 



def set_speed_arms( speed : float ) -> bool:
    if speed < 0:        speed = 0
    elif speed > 1024:   speed = 1024 
    for joint in Joints.values(): 
        packetHandler.write2ByteTxRx(  portHandler, joint, ADDR_TORQUE_LIMIT, speed )

def get_moving( ) -> bool:
    moving = []
    for joint in Joints.values(): 
        dxl_moving_x, dxl_comm_result_x, dxl_error_x =  packetHandler.read1ByteTxRx(  portHandler, joint, ADDR_MOVING )
        moving.append( dxl_moving_x == 1 )
    return moving 


def exe_pos( file : str = None ):  
    with open( file, 'r' ) as file:
        OMBRO_GIRO_L    = [] 
        OMBRO_ELEVA_L   = [] 
        COTOVELO_L      = [] 
        OMBRO_GIRO_R    = [] 
        OMBRO_ELEVA_R   = [] 
        COTOVELO_R      = [] 
        for line in file.readlines():
            try:
                motor_name, pos = line.replace('\n','').split('=')
                pos = float(pos) 
                if motor_name == 'OMBRO_GIRO_L':    OMBRO_GIRO_L.append( pos )
                if motor_name == 'OMBRO_ELEVA_L':   OMBRO_ELEVA_L.append( pos )
                if motor_name == 'COTOVELO_L':      COTOVELO_L.append( pos )
                if motor_name == 'OMBRO_GIRO_R':    OMBRO_GIRO_R.append( pos )
                if motor_name == 'OMBRO_ELEVA_R':   OMBRO_ELEVA_R.append( pos )
                if motor_name == 'COTOVELO_R':      COTOVELO_R.append( pos )
            except:
                continue
    return [ OMBRO_GIRO_L, OMBRO_ELEVA_L, COTOVELO_L, OMBRO_GIRO_R, OMBRO_ELEVA_R, COTOVELO_R ] 



def make_pose( file, speed : int = 800  ):
    print( file )
    if file[:-4] != '.txt': file = PATH + '\\POSES\\' + file + '.txt'
    else:                   file = PATH + '\\POSES\\' + file
    set_torque( False ) 
    set_speed_arms( speed )
    set_torque( False ) 
    GL, EL, CL, GR, ER, CR  =  exe_pos( file ) 
    for gl, el, cl, gr, er, cr in zip( GL, EL, CL, GR, ER, CR ):
        packetHandler.write2ByteTxRx(portHandler, Joints['OMBRO_GIRO_L'], ADDR_MX_GOAL_POSITION , int(gl*(4095/360)) )
        packetHandler.write2ByteTxRx(portHandler, Joints['OMBRO_ELEVA_L'], ADDR_MX_GOAL_POSITION, int(el*(4095/360)) )
        packetHandler.write2ByteTxRx(portHandler, Joints['COTOVELO_L'], ADDR_MX_GOAL_POSITION   , int(cl*(4095/360)) )
        packetHandler.write2ByteTxRx(portHandler, Joints['OMBRO_GIRO_R'], ADDR_MX_GOAL_POSITION , int(gr*(4095/360)) )
        packetHandler.write2ByteTxRx(portHandler, Joints['OMBRO_ELEVA_R'], ADDR_MX_GOAL_POSITION, int(er*(4095/360)) )
        packetHandler.write2ByteTxRx(portHandler, Joints['COTOVELO_R'], ADDR_MX_GOAL_POSITION   , int(cr*(4095/360)) )
        while any( get_moving() ):
            continue

# Open port
def open_port(): 
    global portHandler, packetHandler
    portHandler = PortHandler( dpg.get_value( DEVICE ) ) 
    packetHandler = PacketHandler(PROTOCOL_VERSION)
    if portHandler.openPort():
        print("Succeeded to open the port")
        if portHandler.setBaudRate( dpg.get_value(BAUDRATE) ):
            print("Succeeded to change the baudrate")
            return True
        else:
            print("Failed to change the baudrate")
            return False 
    else:
        print("Failed to open the port")
        return False 


# Apenas inicia a comunicação Serial 
def init_serial():
    try:
        if open_port():
            set_PID()
            go_initial_position() 
            dpg.set_value( SERIAL_OK, True )           
        else: 
            dpg.set_value( SERIAL_OK, False )
            print( 'Serial not OK')
        
    except:
        dpg.set_value( SERIAL_OK, False )
        print( 'Serial not OK')


if __name__ == '__main__':
    dpg.set_value( DEVICE, 'COM1' )
    dpg.set_value( BAUDRATE, 57600 )
    init_serial( )
