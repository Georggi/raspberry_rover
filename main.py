import RPi.GPIO as gpio
import time
import socket


ip = '185.175.245.51'
port = 60100

pwm_vals = [0.0, 0.0, 0.0, 0.0]



def execPWMChanges():
    print(pwm_vals)
    for i in range(0, len(pwm_vals)):
        if pwm_vals[i] > 100:
            pwm_vals[i] = 100
        if pwm_vals[i] < 0:
            pwm_vals[i] = 0
    pwm_right_forward.ChangeDutyCycle(pwm_vals[0])
    pwm_right_back.ChangeDutyCycle(pwm_vals[1])
    pwm_left_back.ChangeDutyCycle(pwm_vals[2])
    pwm_left_forward.ChangeDutyCycle(pwm_vals[3])


def shift_turnRight():
    pwm_vals[0] = pwm_vals[1] = pwm_vals[2] = 0
    pwm_vals[3] = 100


def shift_turnLeft():
    pwm_vals[3] = pwm_vals[1] = pwm_vals[2] = 0
    pwm_vals[0] = 100


def forward_turnLeft():
    pwm_vals[1] = pwm_vals[2] = 0
    if pwm_vals[3] > pwm_vals[0]:
        pwm_vals[3] = pwm_vals[0] = 0
    if pwm_vals[0] < 100:
        pwm_vals[0] += 25
    if pwm_vals[3] < 50:
        pwm_vals[3] += 12.5


def forward_turnRight():
    pwm_vals[1] = pwm_vals[2] = 0
    if pwm_vals[0] > pwm_vals[3]:
        pwm_vals[3] = pwm_vals[0] = 0
    if pwm_vals[3] < 100:
        pwm_vals[3] += 25
    if pwm_vals[0] < 50:
        pwm_vals[0] += 12.5


def back_turnLeft():
    pwm_vals[3] = pwm_vals[0] = 0
    if pwm_vals[2] > pwm_vals[1]:
        pwm_vals[2] = pwm_vals[1] = 0
    if pwm_vals[1] < 100:
        pwm_vals[1] += 25
    if pwm_vals[2] < 50:
        pwm_vals[2] += 12.5


def back_turnRight():
    pwm_vals[3] = pwm_vals[0] = 0
    if pwm_vals[1] > pwm_vals[2]:
        pwm_vals[2] = pwm_vals[1] = 0
    if pwm_vals[2] < 100:
        pwm_vals[2] += 25
    if pwm_vals[1] < 50:
        pwm_vals[1] += 12.5


def forward():
    pwm_vals[1] = pwm_vals[2] = 0
    if pwm_vals[0] < 25:
        pwm_vals[0] += 12.5
    if pwm_vals[3] < 25:
        pwm_vals[3] += 12.5


def back():
    pwm_vals[0] = pwm_vals[3] = 0
    if pwm_vals[1] < 100:
        pwm_vals[1] += 25
    if pwm_vals[2] < 100:
        pwm_vals[2] += 25


def fastRight():
    pwm_vals[0] = pwm_vals[2] = 0
    pwm_vals[3] = pwm_vals[1] = 100


def fastLeft():
    pwm_vals[3] = pwm_vals[1] = 0
    pwm_vals[0] = pwm_vals[2] = 100


def gradualStop():
    for i in range(0, len(pwm_vals)):
        if pwm_vals[i] > 0:
            pwm_vals[i] -= 12.5

def emergencyStop():
    for i in range(0, len(pwm_vals)):
        pwm_vals[i] = 0


if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((ip,port))
        except ConnectionRefusedError:
            print("Host server " + ip + ":" + str(port) + " not started")
            exit(1)
        gpio.cleanup()
        gpio.setmode(gpio.BOARD)
        gpio.setup(11, gpio.OUT)
        gpio.setup(13, gpio.OUT)
        gpio.setup(16, gpio.OUT)
        gpio.setup(18, gpio.OUT)
        pwm_right_forward = gpio.PWM(11,1000)
        pwm_right_back = gpio.PWM(13,1000)
        pwm_left_back = gpio.PWM(16,1000)
        pwm_left_forward = gpio.PWM(18,1000)
        pwm_right_forward.start(0)
        pwm_right_back.start(0)
        pwm_left_back.start(0)
        pwm_left_forward.start(0)
        s.settimeout(100)
        doExit = False

        while not doExit:
            data = s.recv(1)
            time.sleep(0.1)
            if data == bytes([0]):
                gradualStop()
            elif data == bytes([1]):
                forward()
            elif data == bytes([2]):
                back()
            elif data == bytes([3]):
                fastLeft()
            elif data == bytes([4]):
                fastRight()
            elif data == bytes([5]):
                forward_turnRight()
            elif data == bytes([6]):
                forward_turnLeft()
            elif data == bytes([7]):
                back_turnRight()
            elif data == bytes([8]):
                back_turnLeft()
            elif data == bytes([9]):
                shift_turnLeft()
            elif data == bytes([10]):
                shift_turnRight()
            elif data == bytes([127]):
                emergencyStop()
            elif data == bytes([255]):
                doExit = True
            execPWMChanges()
            print(data)
            s.send(bytes([255]))
        pwm_right_forward.stop()
        pwm_right_back.start()
        pwm_left_back.start()
        pwm_left_forward.start()
        gpio.cleanup()
        s.close()
