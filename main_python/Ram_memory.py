from multiprocessing import shared_memory
import json
from time import sleep


MEMORY_SIZE = 4096

def write_ram(data_dict, memory_name):
    json_data = json.dumps(data_dict).encode('utf-8')
    if len(json_data) > MEMORY_SIZE:
        raise ValueError('Coordinates exceed shared memory capacity')

    try:
        shm = shared_memory.SharedMemory(name=memory_name)
    except FileNotFoundError:
        shm = shared_memory.SharedMemory(create=True, name=memory_name, size=MEMORY_SIZE)

    try:
        if len(json_data) > shm.size:
            raise ValueError('Existing shared memory is too small; restart after removing the old segment')
        shm.buf[:] = json_data.ljust(shm.size, b'\x00')
    finally:
        shm.close()

def read_ram(memory_name):
    while True:
        try:
            shm = shared_memory.SharedMemory(name=memory_name)
            try:
                json_data = bytes(shm.buf[:]).rstrip(b'\x00').decode('utf-8')
            finally:
                shm.close()
            data_dict = json.loads(json_data)
            return data_dict
        except (FileNotFoundError, json.JSONDecodeError, UnicodeDecodeError):
            sleep(0.01)
