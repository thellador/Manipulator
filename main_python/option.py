import numpy as np

port = "COM1"


area_width_mm = 303  # x
area_height_mm = 186  # y

color_ranges = [
    (np.array((66, 87, 31), np.uint8), np.array((83, 187, 93), np.uint8), (0, 255, 0)),  # Зеленый
    (np.array((23, 199, 50), np.uint8), np.array((40, 255, 140), np.uint8), (0, 255, 255)),  # Желтый
]