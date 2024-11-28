#!/usr/bin/env python
import time
import cv2
import numpy as np
from ArucoDetection_definitions import *  # Подключение пользовательских определений
from Ram_memory import *


#from defe import *  # Подключение дополнительных пользовательских модулей
from option import *





def initialize_camera():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Захват с камеры

    # Установка разрешения камеры
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Максимальная ширина
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Максимальная высота
    return cap

def get_markers(video_frame, aruco_dictionary, aruco_parameters):
    bboxs, ids, rejected = cv2.aruco.detectMarkers(video_frame, aruco_dictionary, parameters=aruco_parameters)
    if ids is not None:
        ids_sorted = [id_number[0] for id_number in ids]
    else:
        ids_sorted = ids
    return bboxs, ids_sorted

def convert_pixels_to_mm(x_pixel, y_pixel, img_width_pixel, img_height_pixel):
    x_mm = (x_pixel / img_width_pixel) * area_width_mm - area_width_mm / 2
    y_mm = area_height_mm - (y_pixel / img_height_pixel) * area_height_mm + 185
    return x_mm, y_mm

def nothing(*arg):
    pass


def ball_detector(coordinates):
    Green_ball = [None, None]
    Yellow_ball = [None, None]
    for color, coordinate in coordinates.items():
        for x_mm, y_mm in coordinate:
            x_mm = int(x_mm)
            y_mm = int(y_mm)

            #print(f"Found {color} at {x_mm}, {y_mm}")
            if color == (0, 255, 0):  # Зеленый цвет
                Green_ball = [x_mm, y_mm]

            elif color == (0, 255, 255):  # Желтый цвет
                Yellow_ball = [x_mm, y_mm]

    Need_ball = {
        "Green": Green_ball,
        "Yellow": Yellow_ball,
    }
    memory_name = "manipulator_coordinates"
    write_ram(Need_ball, memory_name)



def window_settings():
    cv2.namedWindow("settings")
    cv2.createTrackbar('h1', 'settings', 0, 255, nothing)
    cv2.createTrackbar('s1', 'settings', 0, 255, nothing)
    cv2.createTrackbar('v1', 'settings', 0, 255, nothing)
    cv2.createTrackbar('h2', 'settings', 255, 255, nothing)
    cv2.createTrackbar('s2', 'settings', 255, 255, nothing)
    cv2.createTrackbar('v2', 'settings', 255, 255, nothing)
