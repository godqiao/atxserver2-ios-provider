# coding: utf-8
#

# import socket


# class FreePort(object):
#     def __init__(self):
#         self._start = 20000
#         self._end = 40000
#         self._now = self._start-1

#     def get(self):
#         while True:
#             self._now += 1
#             if self._now > self._end:
#                 self._now = self._start
#             if not self.is_port_in_use(self._now):
#                 return self._now

#     def is_port_in_use(self, port):
#         with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#             return s.connect_ex(('localhost', port)) == 0


# freeport = FreePort()

# coding: utf-8
import socket
import hashlib

class FreePort(object):
    def __init__(self):
        self._start = 20000  # 起始端口
        self._end = 40000    # 结束端口
        self._used_ports = set()
        self._udid_port_map = {}  # 存储UDID与端口的映射

    def get(self, udid=None):
        """如果提供UDID则返回固定端口，否则返回第一个可用端口"""
        if udid:
            # 为UDID生成唯一哈希值并映射到端口范围
            if udid in self._udid_port_map:
                return self._udid_port_map[udid]
                
            # 使用MD5哈希UDID并映射到端口范围
            hash_obj = hashlib.md5(udid.encode())
            hash_num = int(hash_obj.hexdigest(), 16)
            port = self._start + (hash_num % (self._end - self._start + 1))
            
            # 确保端口未被使用且在范围内
            while port in self._used_ports or port < self._start or port > self._end:
                port = self._start + ((port - self._start + 1) % (self._end - self._start + 1))
                
            self._udid_port_map[udid] = port
            self._used_ports.add(port)
            return port
        else:
            # 原有逻辑，用于非设备相关的端口分配
            port = self._start
            while port <= self._end:
                if port not in self._used_ports and not self.is_port_in_use(port):
                    self._used_ports.add(port)
                    return port
                port += 1
            raise Exception("No free ports available")

    def release(self, port):
        """释放端口"""
        if port in self._used_ports:
            self._used_ports.remove(port)
        # 从映射中移除使用该端口的UDID
        for udid, p in list(self._udid_port_map.items()):
            if p == port:
                del self._udid_port_map[udid]

    def is_port_in_use(self, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', port)) == 0


freeport = FreePort()

if __name__ == "__main__":
    for i in range(10):
        print(freeport.get())