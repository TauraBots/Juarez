import dearpygui.dearpygui as dpg 

# INICIA O CONTEXTO DO DEARPYGUI 
dpg.create_context()

import serial 
import glob
import sys 
import os 


''' CLICKED '''
with dpg.theme( ) as on_button:
    with dpg.theme_component( dpg.mvImageButton ):
        dpg.add_theme_color( dpg.mvThemeCol_Button       , (0x3c, 0xb3, 0x71, 0xff), category = dpg.mvThemeCat_Core )
        dpg.add_theme_color( dpg.mvThemeCol_ButtonHovered, (0x92, 0xe0, 0x92, 0xff), category = dpg.mvThemeCat_Core )
        dpg.add_theme_color( dpg.mvThemeCol_ButtonActive , (0x20, 0xb2, 0xaa, 0xff), category = dpg.mvThemeCat_Core )
''' NON CLICKED '''
with dpg.theme( ) as off_button:
    with dpg.theme_component( dpg.mvImageButton ):
        dpg.add_theme_color( dpg.mvThemeCol_Button       , (0xff, 0x45, 0x00, 0xff), category = dpg.mvThemeCat_Core )
        dpg.add_theme_color( dpg.mvThemeCol_ButtonHovered, (0xf0, 0x80, 0x80, 0xff), category = dpg.mvThemeCat_Core )
        dpg.add_theme_color( dpg.mvThemeCol_ButtonActive , (0x8b, 0x45, 0x13, 0xff), category = dpg.mvThemeCat_Core )
'''DEF BUTTON'''
with dpg.theme( ) as def_button:
    with dpg.theme_component( dpg.mvImageButton ):
        dpg.add_theme_color( dpg.mvThemeCol_Button       , ( 52, 140, 215, 255 ), category = dpg.mvThemeCat_Core )
        dpg.add_theme_color( dpg.mvThemeCol_ButtonHovered, ( 52, 140, 215, 175 ), category = dpg.mvThemeCat_Core )
        dpg.add_theme_color( dpg.mvThemeCol_ButtonActive , ( 75, 160, 230, 255 ), category = dpg.mvThemeCat_Core )
'''GLOBAL'''
with dpg.theme( ) as def_themes:
    with dpg.theme_component( dpg.mvImageButton ):
        dpg.add_theme_color( dpg.mvThemeCol_Button       , ( 52, 140, 215, 255 ), category = dpg.mvThemeCat_Core )
        dpg.add_theme_color( dpg.mvThemeCol_ButtonHovered, ( 52, 140, 215, 175 ), category = dpg.mvThemeCat_Core )
        dpg.add_theme_color( dpg.mvThemeCol_ButtonActive , ( 75, 160, 230, 255), category = dpg.mvThemeCat_Core )

# REGISTRADORES DE VARIAVEIS GLOBAIS DO DPG (INTERFACE) 
with dpg.value_registry() as values_registry:
    BUT_B = dpg.add_bool_value( default_value = False, tag = 'bug_B') 
    BUT_C = dpg.add_bool_value( default_value = False, tag = 'bug_C') 
    BUT_E = dpg.add_bool_value( default_value = False, tag = 'bug_E') 
    BUT_J = dpg.add_bool_value( default_value = False, tag = 'bug_J') 
    BUT_V = dpg.add_bool_value( default_value = False, tag = 'bug_V') 
    BUT_N = dpg.add_bool_value( default_value = False, tag = 'bug_N')
    BUT_S = dpg.add_bool_value( default_value = False, tag = 'bug_S')

    INIT = dpg.add_bool_value( default_value = False, tag = 'INIT')

    BUT_TOTAL = dpg.add_int_value( default_value = 10 )
    CALLBACK  = dpg.add_string_value( default_value = '' )

    TRACK_OK  = dpg.add_bool_value( default_value = False )
    TRACK_ID  = dpg.add_int_value ( default_value = 0     ) 
    
    DETECT_OK   = dpg.add_bool_value( default_value = False )
    DETECT_ID   = dpg.add_int_value ( default_value = 0     )
    BBOX_TRACK  = dpg.add_bool_value( default_value = False )


# REGISTRO DE TEXTURAS UTILZIADOS PARA AS IMAGENS  
with dpg.texture_registry( show = True ) as textures_registry:
    # PEGA O CAMINHO ABSOLUTO DO PATH DE IMAGENS 
    PATH = os.path.dirname( __file__ )
    # FAZER OS REGISTROS DE CADA IMAGEM COM OS MESMOS COMANDOS ABAIXO 
    B_W, B_H, B_C, B_DATA = dpg.load_image( PATH + '\\images\\B.png' )                               
    C_W, C_H, C_C, C_DATA = dpg.load_image( PATH + '\\images\\C.png' )                                           
    E_W, E_H, E_C, E_DATA = dpg.load_image( PATH + '\\images\\E.png' ) 
    J_W, J_H, J_C, J_DATA = dpg.load_image( PATH + '\\images\\J.png' )                                        
    V_W, V_H, V_C, V_DATA = dpg.load_image( PATH + '\\images\\V.png' )                   
    N_W, N_H, N_C, N_DATA = dpg.load_image( PATH + '\\images\\N.png' )                   
    S_W, S_H, S_C, S_DATA = dpg.load_image( PATH + '\\images\\S.png' )                   

    # CRIAR AS TEXTURAS DE CADA IMAGEM
    B = dpg.add_static_texture( width = B_W, height = B_H, default_value = B_DATA )           
    C = dpg.add_static_texture( width = C_W, height = C_H, default_value = C_DATA )       
    E = dpg.add_static_texture( width = E_W, height = E_H, default_value = E_DATA )                
    J = dpg.add_static_texture( width = J_W, height = J_H, default_value = J_DATA )      
    V = dpg.add_static_texture( width = V_W, height = V_H, default_value = V_DATA )              
    N = dpg.add_static_texture( width = N_W, height = N_H, default_value = N_DATA )              
    S = dpg.add_static_texture( width = S_W, height = S_H, default_value = S_DATA )              


with dpg.handler_registry() as handlers_registry:
    KEY_C = dpg.add_key_release_handler( key = dpg.mvKey_C, callback =  lambda s, d, u : dpg.set_value( BUT_C, not dpg.get_value( BUT_C) ) )
    KEY_J = dpg.add_key_release_handler( key = dpg.mvKey_J, callback =  lambda s, d, u : dpg.set_value( BUT_J, not dpg.get_value( BUT_J) ) )
    KEY_V = dpg.add_key_release_handler( key = dpg.mvKey_V, callback =  lambda s, d, u : dpg.set_value( BUT_V, not dpg.get_value( BUT_V) ) )
    KEY_B = dpg.add_key_release_handler( key = dpg.mvKey_B, callback =  lambda s, d, u : dpg.set_value( BUT_B, not dpg.get_value( BUT_B) ) )
    KEY_E = dpg.add_key_release_handler( key = dpg.mvKey_E, callback =  lambda s, d, u : dpg.set_value( BUT_E, not dpg.get_value( BUT_E) ) ) 
    KEY_S = dpg.add_key_release_handler( key = dpg.mvKey_S, callback =  lambda s, d, u : dpg.set_value( BUT_S, not dpg.get_value( BUT_S) ) ) 
    KEY_T = dpg.add_key_release_handler( key = dpg.mvKey_T, callback =  lambda s, d, u : dpg.set_value( BUT_S, not dpg.get_value( BUT_S) ) ) 
    
    # POSES 
    KEY_H = dpg.add_key_release_handler( key = dpg.mvKey_H, callback =  lambda s, d, u : dpg.set_value( BUT_S, not dpg.get_value( BUT_S) ) ) 
    KEY_D = dpg.add_key_release_handler( key = dpg.mvKey_D, callback =  lambda s, d, u : dpg.set_value( BUT_S, not dpg.get_value( BUT_S) ) ) 
    KEY_P = dpg.add_key_release_handler( key = dpg.mvKey_P, callback =  lambda s, d, u : dpg.set_value( BUT_S, not dpg.get_value( BUT_S) ) ) 
    KEY_L = dpg.add_key_release_handler( key = dpg.mvKey_L, callback =  lambda s, d, u : dpg.set_value( BUT_S, not dpg.get_value( BUT_S) ) ) 
    KEY_H = dpg.add_key_release_handler( key = dpg.mvKey_H, callback =  lambda s, d, u : dpg.set_value( BUT_S, not dpg.get_value( BUT_S) ) ) 
    KEY_Y = dpg.add_key_release_handler( key = dpg.mvKey_Y, callback =  lambda s, d, u : dpg.set_value( BUT_S, not dpg.get_value( BUT_S) ) ) 
    KEY_U = dpg.add_key_release_handler( key = dpg.mvKey_U, callback =  lambda s, d, u : dpg.set_value( BUT_S, not dpg.get_value( BUT_S) ) ) 
    KEY_I = dpg.add_key_release_handler( key = dpg.mvKey_I, callback =  lambda s, d, u : dpg.set_value( BUT_S, not dpg.get_value( BUT_S) ) ) 
    
    # Callback para encerrar o código 
    dpg.add_key_press_handler( dpg.mvKey_Escape, callback = dpg.destroy_context, parent = handlers_registry )


# CALLBACK DE REDIMENSIONAMENTO DA TELA PRINCIPAL 
def resize_main( sender, data, user ):
    # PROPORÇÃO DO TAMANHO DA TELA  
    prop_x, prop_y = data[2]/1473, data[3]/841
    # REDIMENSIONAMENTO DE JANELAS
    dpg.configure_item( item = 'win_cam_juarez' ,  pos = [  915*prop_x, 100*prop_y  ], width =  550*prop_x, height = 550*prop_y)
    dpg.configure_item( item = 'win_cam_tracker',  pos =  [10*prop_x , 15*prop_y  ], width =  900*prop_x, height = 700*prop_y )
    dpg.configure_item( item = 'win_info_above' ,  pos = [  10*prop_x , 730*prop_y ], width = 1455*prop_x, height = 150*prop_y )
    # REDIMENSIONAMENTO DOS ELEMENTOS  
    dpg.configure_item( item = 'img_juarez'  , width = dpg.get_item_width( 'win_cam_juarez' ), height = dpg.get_item_height( 'win_cam_juarez' )  ) 
    dpg.configure_item( item = 'img_tracker' , width = dpg.get_item_width( 'win_cam_tracker' ), height = dpg.get_item_height( 'win_cam_tracker' )  ) 
    # REDIMENSIONAMENTO DOS BOTÕES 
    dpg.configure_item( 'but_C', width = dpg.get_item_width( 'win_info_above' )/dpg.get_value(BUT_TOTAL)- 17 )
    dpg.configure_item( 'but_J', width = dpg.get_item_width( 'win_info_above' )/dpg.get_value(BUT_TOTAL)- 17 )
    dpg.configure_item( 'but_V', width = dpg.get_item_width( 'win_info_above' )/dpg.get_value(BUT_TOTAL)- 17 )
    dpg.configure_item( 'but_B', width = dpg.get_item_width( 'win_info_above' )/dpg.get_value(BUT_TOTAL)- 17 )
    dpg.configure_item( 'but_E', width = dpg.get_item_width( 'win_info_above' )/dpg.get_value(BUT_TOTAL)- 17 )
    dpg.configure_item( 'but_S', width = dpg.get_item_width( 'win_info_above' )/dpg.get_value(BUT_TOTAL)- 17 )
    # TEXT
    dpg.configure_item( item = 'fps_info'       ,  pos = [  915*prop_x , 730*prop_y ] )

# CRIAÇÃO DA TELA PRINCIOAL
# TODOS ELEMENTOS DESENHADOS NA TELA FORAM FEITOS AQUI 
# PARA ADICIONAR UM BOTÃO OU ALGUMA FUNCIONALIDADE A MAIS, DEVE SER FEITA AQUI 
def init_main( window_name ):
    with dpg.window( tag = 'main_window', no_close = True, no_collapse = True, no_move = True, no_scrollbar = True, no_title_bar = False ):
        # Janela de apresentação da camera spotter 
        with dpg.window( tag = 'win_cam_juarez', no_close = True,no_resize = True, no_collapse = True, no_move = True, no_scrollbar = True, no_title_bar = True ): 
            dpg.add_image( tag = 'img_juarez', texture_tag = J, width = dpg.get_item_width( 'win_cam_juarez' ), height = dpg.get_item_height( 'win_cam_juarez' )  ) 
        # Janela de de apresentação da camera shooter 
        with dpg.window( tag = 'win_cam_tracker', no_close = True, no_resize = True,no_collapse = True, no_move = True, no_scrollbar = True, no_title_bar = True ):
            dpg.add_image( tag = 'img_tracker', texture_tag = V, width = dpg.get_item_width( 'win_cam_tracker' ), height = dpg.get_item_height( 'win_cam_tracker' )  ) 

        # Janela de inputs para o programa 
        with dpg.window( tag = 'win_info_above', no_close = True,no_resize = True, no_collapse = True, no_move = True, no_scrollbar = True, no_title_bar = True ):
            # Botões de execução
            with dpg.child_window( tag = 'inputs', width = -1, height = 90, border = False, no_scrollbar = True ): 
                with dpg.group( horizontal = True, pos = [5,0] ):
                    dpg.add_image_button( tag = 'but_C', height = 75, width = dpg.get_item_width( dpg.last_container() )/dpg.get_value(BUT_TOTAL) -6, texture_tag = C, callback =  lambda s, d, u : dpg.set_value( BUT_C, not dpg.get_value( BUT_C) )  )
                    dpg.add_image_button( tag = 'but_J', height = 75, width = dpg.get_item_width( dpg.last_container() )/dpg.get_value(BUT_TOTAL) -6, texture_tag = J, callback =  lambda s, d, u : dpg.set_value( BUT_J, not dpg.get_value( BUT_J) )  )
                    dpg.add_image_button( tag = 'but_V', height = 75, width = dpg.get_item_width( dpg.last_container() )/dpg.get_value(BUT_TOTAL) -6, texture_tag = V, callback =  lambda s, d, u : dpg.set_value( BUT_V, not dpg.get_value( BUT_V) )  )
                    dpg.add_image_button( tag = 'but_B', height = 75, width = dpg.get_item_width( dpg.last_container() )/dpg.get_value(BUT_TOTAL) -6, texture_tag = B, callback =  lambda s, d, u : dpg.set_value( BUT_B, not dpg.get_value( BUT_B) )  )
                    dpg.add_image_button( tag = 'but_E', height = 75, width = dpg.get_item_width( dpg.last_container() )/dpg.get_value(BUT_TOTAL) -6, texture_tag = E, callback =  lambda s, d, u : dpg.set_value( BUT_E, not dpg.get_value( BUT_E) ) )
                    dpg.add_image_button( tag = 'but_S', height = 75, width = dpg.get_item_width( dpg.last_container() )/dpg.get_value(BUT_TOTAL) -6, texture_tag = S, callback =  lambda s, d, u : dpg.set_value( BUT_S, not dpg.get_value( BUT_S) ) )

                dpg.add_text(  tag = 'fps_info', default_value = 'FPS: ')
        
        with dpg.theme() as no_border:
            with dpg.theme_component( dpg.mvWindowAppItem ):        
                dpg.add_theme_style( dpg.mvStyleVar_WindowBorderSize, False , category = dpg.mvThemeCat_Core )

        dpg.bind_item_theme( 'inputs', no_border  )

    # CONFIGURAÇÕES DE VIEWPORT
    # O SISTEMA OPERACIONAL IRÁ ENXERGAR ESSA VIEWPORT NA ÁRVORE DE PROCESSOS 
    dpg.create_viewport( title = window_name, width = 600, min_width = 1000, height = 200,  min_height = 800  )
    
    # INCIA O DEARPYGUI 
    dpg.setup_dearpygui()

    # DEFINE E HABILITA A JANELA PRINCIPAL 
    dpg.set_primary_window("main_window", True) 
    dpg.set_viewport_resize_callback( resize_main )
    dpg.maximize_viewport() 
    dpg.show_viewport()
    
    dpg.bind_theme( def_themes )


# FUNÇÃO PARA RENDERIZAÇÃO DA JANELA PRINCIPAL 
states = [ BUT_C, BUT_J, BUT_V, BUT_B, BUT_E, BUT_S ]
names  = ['but_C', 'but_J', 'but_V', 'but_B', 'but_E', 'but_S']

def render_main():
    for B, N in zip(states, names):
        if dpg.get_value( B ):
            dpg.bind_item_theme( N, theme = on_button )
        else:
            dpg.bind_item_theme( N, theme = def_button )
            

''' Avalia quais portas seriais estão disponíveis'''
def serial_ports_available( sender, data, user ):
    dpg.configure_item( 'refresh_serial', label = 'Procurando' )
    # Abre se o SO for Windows
    if sys.platform.startswith('win'):  
        ports = ['COM%s' % (i + 1) for i in range( user )]
    # Abre se o SO for Linux
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        ports = glob.glob('/dev/tty[A-Za-z]*')
    # Caso não seja nenhum dos dois, ele não suporta
    else:
        print("Sistema Operacional não suportado")
    # Testa as portas disponíveis 
    portList = []
    for port in ports:
        try:
            s = serial.Serial( port )
            s.close()
            portList.append(port)
        except (OSError, serial.SerialException):
            pass
    dpg.configure_item( 'refresh_serial', label = 'Procurar' )
    dpg.configure_item( 'device_info', items = portList )

