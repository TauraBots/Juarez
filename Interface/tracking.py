from Interface.dpg_context import *
from Capture.capture import *

import dearpygui.dearpygui as dpg 
import mediapipe           as mp 
import time 
import cv2 


mp_face_detection = mp.solutions.face_detection
mp_drawing        = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_holistic       = mp.solutions.holistic

last_detect = time.time()

def init_tracking():
    global img_tracking, Tracking 
    try:
        print( 'Iniciando Shooter Cam ')
        Tracking, tracking_texture, w, h = init_capture( CAP_ID = dpg.get_value(TRACK_ID), w = 640, h = 480 )
        img_tracking = dpg.add_raw_texture( parent = textures_registry, height = h, width = w, default_value = tracking_texture, format = dpg.mvFormat_Float_rgb )
        dpg.configure_item( 'img_tracker', texture_tag = img_tracking )

        if Tracking == False: 
            dpg.set_value( TRACK_OK, False )
            print( 'Falha na inicialização da camerado do tracking' )
        else: 
            dpg.set_value( TRACK_OK, True )
            print( 'Tracking inicializado com sucesso' )
    except: 
        dpg.set_value( TRACK_OK, False )
        print( 'Falha na inicialização do Tracking' )
    

def run_tracking( holistic ):
    global mp_drawing, mp_drawing_styles, mp_holistic
    global last_detect
    
    success, image = get_capture_texture( Tracking )
    
    if success:
        image = cv2.flip(image, 1)
        if not success:
            return False 
        
        center_x_shooter = int(image.shape[1] * 0.5)
        center_y_shooter = int(image.shape[0] * 0.5)
        
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = holistic.process(image)
        
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS, landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
        
        distance_shooter_center_x = 0 
        distance_shooter_center_y = 0 

        if results.pose_landmarks is not None:  
            # coordinates = (left eye + right eye / 2) * screen center
            x_shooter = int((results.pose_landmarks.landmark[2].x + results.pose_landmarks.landmark[5].x) * center_x_shooter)
            y_shooter = int((results.pose_landmarks.landmark[2].y + results.pose_landmarks.landmark[5].y) * center_y_shooter)
            
            distance_shooter_center_x = center_x_shooter - x_shooter
            distance_shooter_center_y = center_y_shooter - y_shooter
            
            cv2.line(image, (x_shooter, y_shooter), (center_x_shooter, center_y_shooter), (255, 255, 255), 4)
            cv2.putText(image, f'x:{x_shooter} y:{y_shooter}', (x_shooter, y_shooter - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)  # hypotenuse
            cv2.line(image, (x_shooter, center_y_shooter), (center_x_shooter, center_y_shooter), (255, 255, 255), 2)
            cv2.putText(image, f'{distance_shooter_center_x}', (x_shooter, center_y_shooter + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)  # x
            cv2.line(image, (center_x_shooter, y_shooter), (center_x_shooter, center_y_shooter), (255, 255, 255), 4)
            cv2.putText(image, f'{distance_shooter_center_y}', (center_x_shooter + 20, y_shooter + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)  # y
            
            dpg.set_value( INIT, True )
            last_detect = time.time() 

        else: 
            dpg.set_value( INIT, False )

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
        # Atualiza a imagem para ficar de acordo com o padrão dpg 
        image = att_capture_texture( image  )
        dpg.set_value( img_tracking, image )
        dpg.configure_item( 'img_tracker', texture_tag = img_tracking )

        return [ distance_shooter_center_x, distance_shooter_center_y ]