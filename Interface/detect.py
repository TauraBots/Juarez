import dearpygui.dearpygui as dpg 

from Interface.dpg_context import * 
from Capture.capture import * 

import cv2
import os

PATH = os.path.dirname( __file__) 

classNames = [] 
classFile  = PATH + '\\files\\coco.names'

with open( classFile, 'rt' ) as f:
    classNames = f.read().rstrip('\n').split('\n')
configPath = PATH + '/files/mobilenet.pbtxt'
weightPath = PATH + '/files/pesos_mobilenet.pb'

# DNN configurations 
net = cv2.dnn_DetectionModel( weightPath, configPath ) 
net.setInputSize  ( 320, 320 )
net.setInputScale ( 1.0 / 127.5 )
net.setInputMean  ( [127.5, 127.5, 127.5] ) 
net.setInputSwapRB( True )


# Inicia a camera de visualização 
def init_detect( ):
    global Detect, img_detect 
    try:
        print( 'Iniciando detect Cam ')
        Detect, detect_texture, w, h = init_capture( CAP_ID = dpg.get_value(DETECT_ID) , w = 640, h = 480 )
        img_detect = dpg.add_raw_texture( parent = textures_registry, height = h, width = w, default_value = detect_texture, format = dpg.mvFormat_Float_rgb )
        dpg.configure_item( 'img_detect', texture_tag = img_detect )
        print( 'detect cam : ' + str(Detect) )
        if Detect == False:
            dpg.set_value( DETECT_OK, False )
            print( 'Falha na inicialização do detect' )
        else:
            dpg.set_value( DETECT_OK, True )
            print( 'detect inicializado com sucesso' )
    except: 
        dpg.set_value( DETECT_OK, False )
        print( 'Falha na inicialização do detect' )


def run_detect( ):
    detect_status, detect_texture = get_capture_texture( Detect )
    if detect_status: 


        classIds, confs, bbox = net.detect( detect_texture, confThreshold = 0.5 )

        # If have some classId detected in the image it will draw the rectangle and put the name of it
        if len( classIds ) != 0: 
            for classId, confidence, box in zip( classIds.flatten(), confs.flatten(), bbox ):
                cv2.rectangle( detect_texture, box, color = [255, 0, 0], thickness = 2 )
                cv2.putText  ( detect_texture, classNames[classId-1], [box[0]+10, box[1]+30], cv2.FONT_HERSHEY_COMPLEX, 0.5, (255,0,0), 2 )
                cv2.putText  ( detect_texture, str(round(confidence*100,2)), [box[0]+10, box[1]+50], cv2.FONT_HERSHEY_COMPLEX, 0.5, (255,0,0), 2 )

        # Atualiza a imagem para ficar de acordo com o padrão dpg 
        detect_texture = att_capture_texture( detect_texture  )
        dpg.set_value( img_detect, detect_texture )
        dpg.configure_item( 'img_juarez', texture_tag = img_detect )


