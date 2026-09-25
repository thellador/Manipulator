import sys
import unittest
from pathlib import Path
from unittest.mock import Mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'main_python'))

from control import send_command, target_for_color


class ControlTests(unittest.TestCase):
    def test_serial_command_is_line_delimited_for_arduino(self):
        port = Mock()
        send_command(port, '75 90 90 65 90 75')
        port.write.assert_called_once_with(b'75 90 90 65 90 75\n')

    def test_missing_ball_does_not_produce_a_target(self):
        self.assertIsNone(target_for_color({'Green': [None, None]}, 'Green'))
        self.assertIsNone(target_for_color({'Green': [10, None]}, 'Green'))
        self.assertIsNone(target_for_color({}, 'Green'))
        self.assertEqual(target_for_color({'Green': [0, -12]}, 'Green'), [0, -12])


if __name__ == '__main__':
    unittest.main()
