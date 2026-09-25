def target_for_color(coordinates, color):
    target = coordinates.get(color)
    if not isinstance(target, (list, tuple)) or len(target) != 2:
        return None
    if any(value is None or not isinstance(value, (int, float)) for value in target):
        return None
    return target


def send_command(serial_port, command):
    serial_port.write(f"{command}\n".encode("ascii"))
