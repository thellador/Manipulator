from multiprocessing import shared_memory
import json

def write_ram(data_dict, memory_name):
    json_data = json.dumps(data_dict)

    try:
        shm = shared_memory.SharedMemory(name=memory_name)
    except FileNotFoundError:
        shm = shared_memory.SharedMemory(create=True, name=memory_name, size=len(json_data.encode('utf-8')))

    shm.buf[:len(json_data)] = json_data.encode('utf-8')
    return shm

def read_ram(memory_name):
    while True:
        try:
            shm = shared_memory.SharedMemory(name=memory_name)
            json_data = bytes(shm.buf[:]).rstrip(b'\x00').decode('utf-8')
            data_dict = json.loads(json_data)
            return data_dict
        except:
            None
