import socket
import keys
import time
host = "192.168.0.173"
port = 60100
bluetooth = True
data_to_send = {
    "" : bytes([0]),
    'W' : bytes([1]),
    'S': bytes([2]),
    'A': bytes([3]),
    'D': bytes([4]),
    'DW': bytes([5]),
    'AW': bytes([6]),
    'DS': bytes([7]),
    'AS': bytes([8]),
    'shiftA': bytes([9]),
    'shiftD': bytes([10]),
    'K': bytes([255]), #exit
    'P': bytes([127]) #ssemergency stop
}

if __name__ == "__main__":
    s = None
    if bluetooth:
        s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        host='d4:38:9c:ae:59:23'
    else:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host, port))
        s.listen(5)

        conn, addr = s.accept()
        print("receiver connection from " + addr[0])
        doExit = False
        time.sleep(1)
        while not doExit:
            pressed = ''.join(keys.key_check())
            print(pressed)
            if pressed in data_to_send.keys():
                conn.send(data_to_send[pressed])
                data = conn.recv(1)
            if pressed == 'K':
                doExit = True

        s.close()

