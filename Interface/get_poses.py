from PyDynamixel_v2.PyDynamixel_v2 import * 
import time 
import os 

PATH = os.path.dirname( __file__ )

BAUD = 57600 
PORT = 'COM1'

COMP = DxlComm( port = PORT, baudrate = BAUD )


ADDR_MX_TORQUE = 24
ADDR_MX_GOAL_POSITION = 30
ADDR_TORQUE_LIMIT = 34
ADDR_MX_PRESENT_POSITION = 36
ADDR_MOVING = 46
ADDR_LOAD = 40


# Visão traseira do Juarez 
Joints = { 'OMBRO_GIRO_L'    :   Joint( 4 ),
           'OMBRO_ELEVA_L'   :   Joint( 6 ),
           'COTOVELO_L'      :   Joint( 8 ), 

           'OMBRO_GIRO_R'    :   Joint( 3 ),
           'OMBRO_ELEVA_R'   :   Joint( 5 ),
           'COTOVELO_R'      :   Joint( 7 ) } 


# Attach joints  
for joint in Joints.values():
    COMP.attach_joint( joint )


def set_speed( speed : float ) -> bool:
    if speed < 0:        speed = 0
    elif speed > 1024:   speed = 1024 
    for joint in Joints.values(): 
        COMP.packet_handler.write2ByteTxRx( COMP.port_handler, joint.servo_id, ADDR_TORQUE_LIMIT, speed )

def get_moving( ) -> bool:
    moving = []
    for joint in Joints.values(): 
        dxl_moving_x, dxl_comm_result_x, dxl_error_x = COMP.packet_handler.read1ByteTxRx( COMP.port_handler, joint.servo_id, ADDR_MOVING )
        moving.append( dxl_moving_x == 1 )
    return moving 


def save_pos( num : int = 5, file : str = None ):
    time_spend = time.time() 
    with open( file, 'w' ) as f :
        for _ in range( num ):
            input("Pressione Enter") 
            f.write( 'OMBRO_GIRO_L='  +str(Joints['OMBRO_GIRO_L'].get_angle())  + '\n' )
            f.write( 'OMBRO_ELEVA_L=' +str(Joints['OMBRO_ELEVA_L'].get_angle()) + '\n' )
            f.write( 'COTOVELO_L='    +str(Joints['COTOVELO_L'].get_angle())    + '\n' )
            f.write( 'OMBRO_GIRO_R='  +str(Joints['OMBRO_GIRO_R'].get_angle())    + '\n' )
            f.write( 'OMBRO_ELEVA_R=' +str(Joints['OMBRO_ELEVA_R'].get_angle())    + '\n' )
            f.write( 'COTOVELO_R='    +str(Joints['COTOVELO_R'].get_angle())    + '\n' )
    print( 'time_speend: ', time.time() - time_spend  )


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



def make_pose( file : str, speed : int = 1024 ):
    if file[:-4] != '.txt': file = PATH + '\\POSES\\' + file + '.txt'
    else:                   file = PATH + '\\POSES\\' + file
    COMP.disable_torques() 
    set_speed( speed )
    COMP.enable_torques() 
    GL, EL, CL, GR, ER, CR  =  exe_pos( file ) 
    for gl, el, cl, gr, er, cr in zip( GL, EL, CL, GR, ER, CR ):
        Joints['OMBRO_GIRO_L'].send_angle( gl )
        Joints['OMBRO_ELEVA_L'].send_angle( el )
        Joints['COTOVELO_L'].send_angle( cl )
        Joints['OMBRO_GIRO_R'].send_angle( gr )
        Joints['OMBRO_ELEVA_R'].send_angle( er )
        Joints['COTOVELO_R'].send_angle( cr )
        while any( get_moving() ):
            continue


if __name__ == '__main__':

    COMP.disable_torques() 

    # make_pose( 'POS_INITIAL', speed = 500 ) 
    
    # make_pose( 'HELLO', speed = 800 ) 
    
    # make_pose( 'DEB', speed = 500 ) 
    # time.sleep( 2 )

    # make_pose( 'HIDEN', speed = 500 )
    # time.sleep( 2 ) 
    # make_pose( 'HIDEN_BACK', speed = 500 ) 

    # time.sleep(1)
    # make_pose( 'HEART', 300 )


    # make_pose( 'POINT_CALL', speed = 500 ) 

    # make_pose( 'PALMAS', speed = 500 ) 

    # make_pose( 'VIVA', speed = 500 ) 


    # COMP.disable_torques( )