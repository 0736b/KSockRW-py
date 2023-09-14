import socket
import ctypes
import time
import loader

packet_magic = 0xB16B00B
server_ip = '127.0.0.1'
server_port = 6666

class Packet(ctypes.Structure):
    _fields_ = [('magic', ctypes.c_uint),
                ('mode', ctypes.c_ubyte),
                ('process_id', ctypes.c_uint),
                ('address', ctypes.c_ulonglong),
                ('size', ctypes.c_uint),
                ('result', ctypes.c_ulonglong)]

class KSock_RW:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((server_ip, server_port))
    
    def get_process_base_addr(self, process_id):
        packet = Packet(packet_magic, 0, process_id, 0, 0, 0)
        self.socket.send(packet)
        return Packet.from_buffer_copy(self.socket.recv(ctypes.sizeof(Packet))).result

    def read_memory(self, process_id, addr, size):
        packet = Packet(packet_magic, 1, process_id, addr, size, 0)
        self.socket.send(packet)
        return Packet.from_buffer_copy(self.socket.recv(ctypes.sizeof(Packet))).result

    def write_memory(self, process_id, addr, size, value):
        packet = Packet(packet_magic, 2, process_id, addr, size, value)
        self.socket.send(packet)
        return Packet.from_buffer_copy(self.socket.recv(ctypes.sizeof(Packet))).result == value

if __name__ == '__main__':

    # map driver with kdmapper
    # loader.run()

    ksock_connector = KSock_RW()

    process_id = 9999
    test_addr = 0x09999999
    test_patch = 9999

    proc_base_addr = ksock_connector.get_process_base_addr(process_id)
    print(f"base address: {hex(proc_base_addr)}")

    test_value = ksock_connector.read_memory(process_id, test_addr, ctypes.sizeof(ctypes.c_int32))
    print(f"value: {test_value}")

    write_result = ksock_connector.write_memory(process_id, test_addr, ctypes.sizeof(ctypes.c_int32), test_patch)
    print(f"is write success: {write_result}")