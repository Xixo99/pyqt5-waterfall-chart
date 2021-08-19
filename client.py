from os import read
import socket
import sys
import scipy
import numpy as np
import sys
import time

server_ip = '127.0.0.1'
server_port = 9999

# rowdata = np.random.randint(0, 255, 200)
# np.save("row_random_data200.npy", rowdata)

rowdata = np.load("row_random_data200.npy")  # 随机生成的向量，用于模拟含有语义的信号
noise_db = 100
# socket.SOCK_DGRAM代表是UDP通信
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect((server_ip, server_port))

for i in range(50):
    noise = np.random.randint(0, noise_db, 200) - noise_db//2
    data = rowdata+noise
    str_ = ' '.join(str(x) for x in data)
    s.send(str_.encode())

    print("数据发送成功！")
    time.sleep(0.5)
s.close()
