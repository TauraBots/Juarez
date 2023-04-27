import  dearpygui.dearpygui    as     dpg

from    Interface.dpg_context import * 
from    Capture.capture import * 
from    serial_dy import * 

from    tracking import *
from    detect import *

import  time
import  os 

PATH = os.path.dirname( __file__ )



init_main( 'Juarez - TAURA 2022' )

dpg.set_frame_callback( 3, init_serial   )
dpg.set_frame_callback( 4, init_tracking )
dpg.set_frame_callback( 5, init_detect   )

dpg.set_value( DETECT_ID, 0  )
dpg.set_value( TRACK_ID , 0  ) 

dpg.configure_item( KEY_C, callback = go_initial_position )
dpg.configure_item( KEY_T, callback = enable_torque )

def deb():
    make_pose( 'DEB', 800 )
    time.sleep( 5 )
    make_pose( 'POS_INITIAL', 800 )

def pos_init():
    make_pose( 'POS_INITIAL', 800 )
    
def heart():
    make_pose( 'HEART', 800 )

def hello():
    make_pose( 'HELLO', 800 )

def hiden():
    make_pose( 'HIDEN', 800 )
    time.sleep( 2 )
    make_pose( 'HIDEN_BACK', 800 )

def palmas():
    make_pose( 'PALMAS', 800 )

def point_call():
    make_pose( 'POINT_CALL', 800 )

def point():
    make_pose( 'POINT', 800 )

def viva():
    make_pose( 'VIVA', 800 )



dpg.configure_item( KEY_H, callback = hello ) 
dpg.configure_item( KEY_D, callback = deb )
dpg.configure_item( KEY_P, callback = palmas )
dpg.configure_item( KEY_L, callback = heart )
dpg.configure_item( KEY_V, callback = viva )
dpg.configure_item( KEY_Y, callback = point_call )
dpg.configure_item( KEY_U, callback = point )
dpg.configure_item( KEY_I, callback = pos_init )

time_no_detect = time.time() 

# Main loop
with mp_holistic.Holistic(min_detection_confidence = 0.8, min_tracking_confidence = 0.8) as holistic:
    while dpg.is_dearpygui_running():
        dtime = time.time()
        dpg.render_dearpygui_frame()

        render_main()
        pos = run_tracking( holistic )
        run_detect()

        if pos:
            x, y = pos 
            if x > 0:   x *= -0.21 
            elif x < 0: x *= -0.21
            if y > 0:   y *= 0.21 
            elif y < 0: y *= 0.21
            set_rel_position( int(y), int(x))
    
        if not dpg.get_value( INIT ):
            if time.time() - last_detect > 5000:
                go_initial_position() 
                make_pose( 'POS_INITIAL', 500 )


    dpg.configure_item( 'fps_info', default_value = 'FPS: ' + str(round(1/(time.time()-dtime),2) if time.time()-dtime != 0 else 0) )

# Encerrando os contextos 
dpg.destroy_context()

