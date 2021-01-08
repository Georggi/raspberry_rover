# try:
#     pass
#     #import RPi.GPIO as gpio
# except ImportError as e:
import logging
import socket
import time

import RPiSim.GPIO as gpio

bluetooth = False
ip = '192.168.0.161'
port = 60100

pwm_vals = [0.0, 0.0, 0.0, 0.0]


def execute_pwm_changes():
    for i in range(len(pwm_vals)):
        if pwm_vals[i] > 100:
            pwm_vals[i] = 100
        if pwm_vals[i] < 0:
            pwm_vals[i] = 0
    pwm_right_forward.ChangeDutyCycle(pwm_vals[0])
    pwm_right_back.ChangeDutyCycle(pwm_vals[1])
    pwm_left_back.ChangeDutyCycle(pwm_vals[2])
    pwm_left_forward.ChangeDutyCycle(pwm_vals[3])


def shift_turn_right():
    pwm_vals[0] = pwm_vals[1] = pwm_vals[2] = 0
    pwm_vals[3] = 100


def shift_turn_left():
    pwm_vals[3] = pwm_vals[1] = pwm_vals[2] = 0
    pwm_vals[0] = 100


def forward_turn_left():
    pwm_vals[1] = pwm_vals[2] = 0
    if pwm_vals[3] > pwm_vals[0]:
        pwm_vals[3] = pwm_vals[0] = 50
    if pwm_vals[0] < 100:
        pwm_vals[0] += 12.5
    if pwm_vals[3] > 50:
        pwm_vals[3] = 50
    if pwm_vals[3] < 50:
        pwm_vals[3] += 12.5


def forward_turn_right():
    pwm_vals[1] = pwm_vals[2] = 0
    if pwm_vals[0] > pwm_vals[3]:
        pwm_vals[3] = pwm_vals[0] = 50
    if pwm_vals[3] < 100:
        pwm_vals[3] += 12.5
    if pwm_vals[0] > 50:
        pwm_vals[0] = 50
    if pwm_vals[0] < 50:
        pwm_vals[0] += 12.5


def back_turn_left():
    pwm_vals[3] = pwm_vals[0] = 0
    if pwm_vals[2] > pwm_vals[1]:
        pwm_vals[2] = pwm_vals[1] = 50
    if pwm_vals[1] < 100:
        pwm_vals[1] += 12.5
    if pwm_vals[2] > 50:
        pwm_vals[2] = 50
    if pwm_vals[2] < 50:
        pwm_vals[2] += 12.5


def back_turn_right():
    pwm_vals[3] = pwm_vals[0] = 0
    if pwm_vals[1] > pwm_vals[2]:
        pwm_vals[2] = pwm_vals[1] = 50
    if pwm_vals[2] < 100:
        pwm_vals[2] += 12.5
    if pwm_vals[1] > 50:
        pwm_vals[1] = 50
    if pwm_vals[1] < 50:
        pwm_vals[1] += 12.5


def forward():
    pwm_vals[1] = pwm_vals[2] = 0
    if pwm_vals[0] < 100:
        pwm_vals[0] += 12.5
    if pwm_vals[3] < 100:
        pwm_vals[3] += 12.5


def back():
    pwm_vals[0] = pwm_vals[3] = 0
    if pwm_vals[1] < 100:
        pwm_vals[1] += 12.5
    if pwm_vals[2] < 100:
        pwm_vals[2] += 12.5


def fast_right():
    pwm_vals[0] = pwm_vals[2] = 0
    pwm_vals[3] = pwm_vals[1] = 35


def fast_left():
    pwm_vals[3] = pwm_vals[1] = 0
    pwm_vals[0] = pwm_vals[2] = 35


def gradual_stop():
    for i in range(0, len(pwm_vals)):
        if pwm_vals[i] > 0:
            pwm_vals[i] -= 12.5


def emergency_stop():
    for i in range(0, len(pwm_vals)):
        pwm_vals[i] = 0


def set_exit():
    global doExit
    doExit = False


send_to_func = {
    b'\x00': gradual_stop,
    b'\x01': forward,
    b'\x02': back,
    b'\x03': fast_left,
    b'\x04': fast_right,
    b'\x05': forward_turn_right,
    b'\x06': back_turn_right,
    b'\x07': back_turn_right,
    b'\x08': back_turn_left,
    b'\x09': shift_turn_left,
    b'\x10': shift_turn_right,
    b'\xff': set_exit,  # exit
    b'\x7f': emergency_stop  # emergency stop
}


def update_on_data(data):
    send_to_func[data]()


if __name__ == "__main__":
    if bluetooth:
        s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        ip = 'b8:27:eb:3e:b8:0a'
        s.bind((ip, port))
        s.listen(5)
        s, addr = s.accept()
        logging.info(f"received connection from {addr[0]}")
    else:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((ip, port))
        except ConnectionRefusedError:
            logging.error(f"Host server {ip}:{port} not started")
            exit(1)

    gpio.cleanup()
    gpio.setmode(gpio.BOARD)
    gpio.setup(11, gpio.OUT)
    gpio.setup(13, gpio.OUT)
    gpio.setup(16, gpio.OUT)
    gpio.setup(18, gpio.OUT)
    pwm_right_forward = gpio.PWM(11, 1000)
    pwm_right_back = gpio.PWM(13, 1000)
    pwm_left_back = gpio.PWM(16, 1000)
    pwm_left_forward = gpio.PWM(18, 1000)
    pwm_right_forward.start(0)
    pwm_right_back.start(0)
    pwm_left_back.start(0)
    pwm_left_forward.start(0)
    s.settimeout(0.05)
    doExit = False
    lastData = b""
    while not doExit:
        try:
            data = s.recv(1)
            lastData = data
            update_on_data(data)
            execute_pwm_changes()
            time.sleep(0.05)
            s.send(b'\xff')
        except socket.timeout:
            update_on_data(lastData)
            execute_pwm_changes()

    pwm_right_forward.stop()
    pwm_right_back.stop()
    pwm_left_back.stop()
    pwm_left_forward.stop()
    gpio.cleanup()
    s.close()
