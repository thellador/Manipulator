import sys
import unittest
from multiprocessing import shared_memory
from pathlib import Path
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'main_python'))

from Ram_memory import read_ram, write_ram


class SharedCoordinatesTests(unittest.TestCase):
    def test_empty_detection_can_be_replaced_by_longer_and_shorter_coordinates(self):
        name = f'test_manipulator_{uuid4().hex}'
        try:
            for coordinates in (
                {'Green': [None, None], 'Yellow': [None, None]},
                {'Green': [-101, 123], 'Yellow': [-102, 124]},
                {'Green': [0, 0], 'Yellow': [None, None]},
            ):
                write_ram(coordinates, name)
                self.assertEqual(read_ram(name), coordinates)
        finally:
            try:
                shm = shared_memory.SharedMemory(name=name)
            except FileNotFoundError:
                pass
            else:
                shm.unlink()
                shm.close()


if __name__ == '__main__':
    unittest.main()
