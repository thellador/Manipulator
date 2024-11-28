from class_manip_for_def import *

desired_aruco_dictionary1 = "DICT_4X4_50"

ARUCO_DICT = {
    "DICT_4X4_50": cv2.aruco.DICT_4X4_50,
}

init_loc_1 = [10, 470]
init_loc_2 = [630, 470]
init_loc_3 = [630, 10]
init_loc_4 = [10, 10]

current_square_points = [init_loc_1, init_loc_2, init_loc_3, init_loc_4]

this_aruco_dictionary1 = cv2.aruco.Dictionary_get(ARUCO_DICT[desired_aruco_dictionary1])
this_aruco_parameters1 = cv2.aruco.DetectorParameters_create()

cap = initialize_camera()

window_settings()

while True:
    ret, frame = cap.read()

    markers, ids = get_markers(frame, this_aruco_dictionary1, this_aruco_parameters1)
    left_corners, corner_ids = getMarkerCoordinates(markers, ids, 0)

    if corner_ids is not None:
        count = 0
        for id in corner_ids:
            if id > 4:
                break
            current_square_points[id - 1] = left_corners[count]
            count += 1
    left_corners = current_square_points
    corner_ids = [1, 2, 3, 4]

    frame_with_square, squareFound = draw_field(frame, left_corners, corner_ids)

    if squareFound:
        square_points = left_corners

    img_wrapped = four_point_transform(frame, np.array(square_points))
    h, w, c = img_wrapped.shape

    color_coordinates = {}
    for hsv_min, hsv_max, color in color_ranges:
        color_coordinates[color] = []

    for hsv_min, hsv_max, color in color_ranges:
        hsv = cv2.cvtColor(img_wrapped, cv2.COLOR_BGR2HSV)
        thresh = cv2.inRange(hsv, hsv_min, hsv_max)

        moments = cv2.moments(thresh, 1)
        dM01 = moments['m01']
        dM10 = moments['d10']
        dArea = moments['m00']

        if dArea > 100:
            x = int(dM10 / dArea)
            y = int(dM01 / dArea)
            x_mm, y_mm = convert_pixels_to_mm(x, y, w, h)
            color_coordinates[color].append((x_mm, y_mm))
            cv2.circle(img_wrapped, (x, y), 5, color, 2)
            cv2.putText(img_wrapped, f"{x_mm:.0f},{y_mm:.0f}", (x - 65, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    cv2.imshow('img_wrapped', img_wrapped)

    ball_detector(color_coordinates)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    h1 = cv2.getTrackbarPos('h1', 'settings')
    s1 = cv2.getTrackbarPos('s1', 'settings')
    v1 = cv2.getTrackbarPos('v1', 'settings')
    h2 = cv2.getTrackbarPos('h2', 'settings')
    s2 = cv2.getTrackbarPos('s2', 'settings')
    v2 = cv2.getTrackbarPos('v2', 'settings')

    h_min = np.array((h1, s1, v1), np.uint8)
    h_max = np.array((h2, s2, v2), np.uint8)

    thresh = cv2.inRange(hsv, h_min, h_max)
    cv2.imshow('result', thresh)

    cv2.imshow('frame_with_square', frame_with_square)

    if cv2.waitKey(1) & 0xFF == ord('\r'):
        print(f"(np.array(({h1}, {s1}, {v1}), np.uint8), np.array(({h2}, {s2}, {v2}), np.uint8), (255, 255, 255))")
