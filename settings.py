import math
import numpy as np


INCH_PER_CENTIMETRES = 2.54 #1 inch =  2.54cm

################# Constants to introduce by the user #################
I_DT_THRESHOLD_ANGLE = 1.0 #I-DT threshold angle
SCREEN_INCHES = 21.5 #Screen Inches
OBSERVER_CAMERA_DISTANCE = 50 #cm 
WIDTH_SCREEN = 1920 #Screen Resolution Width
HEIGHT_SCREEN = 1080 #Screen Resolution Height


def get_distance_threshold_by_resolution(
    screen_inches=SCREEN_INCHES, 
    inch_per_centimetres=INCH_PER_CENTIMETRES, 
    observer_camera_distance=OBSERVER_CAMERA_DISTANCE, 
    width=WIDTH_SCREEN, 
    height=HEIGHT_SCREEN
    ):
    
    angle_radians = np.radians(I_DT_THRESHOLD_ANGLE)#Convert angle to radians
    sin_1_value = np.sin(angle_radians)
    print(f"sin({I_DT_THRESHOLD_ANGLE}º) = {sin_1_value}")
    
    diameter_fixation = sin_1_value*observer_camera_distance*2 #Se multiplica por 2 para obtener el diámetro
    print(f"Fixation Boundary (diameter): {diameter_fixation} cm.")

    screen_diagonal_pixels = math.sqrt((width)**2 + (height)**2)#diagonal de la pantalla en píxeles. Dependiendo de la resolución de la pantalla, tendrá un valor diferente
    print(f"Screen Diagonal Resolution (in pixels): {screen_diagonal_pixels} px.")
    
    pixels_per_inches = screen_diagonal_pixels/screen_inches
    print(f"Pixels per Inches: {pixels_per_inches} px/inches.")

    pixels_per_centimetres = pixels_per_inches/inch_per_centimetres
    print(f"Pixels per centimetres: {pixels_per_centimetres} px/centimetres.")

    pixels_threshold_i_dt = int(diameter_fixation * pixels_per_centimetres)
    print(f"I-DT threshold (in pixels): {pixels_threshold_i_dt} px.")
    return pixels_threshold_i_dt
