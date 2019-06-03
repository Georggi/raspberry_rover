import socket
import keys
import time
host = "127.0.0.1"
port = 60100

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
    'P': bytes([127]) #emergency stop
}

if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(5)

        conn, addr = s.accept()
        doExit = False
        while not doExit:
            pressed = ''.join(keys.key_check())
            s.send(data_to_send[pressed])
            if pressed == 'K':
                doExit = True
        s.close()

