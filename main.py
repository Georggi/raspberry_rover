import socket
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
import time
import getIP

port = 60100
bluetooth = False
data_to_send = {
    "": bytes([0]),
    'W': bytes([1]),
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

button_dict = {
    "down": True,
    "normal": False
}

class StackGameApp(App):

    def __init__(self):
        if bluetooth:
            self.s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
            host = 'b8:27:eb:3e:b8:0a'
            self.s.connect((host, port))
            self.conn = self.s
        else:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            host = getIP.getIP()
            self.s.bind((host, port))
            self.s.listen(5)
            self.conn, self.addr = self.s.accept()
            #print("received connection from " + self.addr[0])

        self.W_pressed = False
        self.S_pressed = False
        self.A_pressed = False
        self.D_pressed = False
        self.Shift_pressed = False
        self.doExit = False
        print("init")
        App.__init__(self)

    def callback_forw(self, instance, value):
        self.W_pressed = button_dict[value]
        self.exec_sending()

    def callback_back(self, instance, value):
        self.S_pressed = button_dict[value]
        self.exec_sending()

    def callback_left(self, instance, value):
        self.A_pressed = button_dict[value]
        self.exec_sending()

    def callback_right(self, instance, value):
        self.D_pressed = button_dict[value]
        self.exec_sending()

    def callback_shift(self, instance, value):
        self.Shift_pressed = button_dict[value]
        self.exec_sending()

    def callback_stop(self, instance, value):
        self.doExit = button_dict[value]
        self.exec_sending()

    def exec_sending(self):
        if self.doExit:
            self.conn.send(data_to_send['K'])
            time.sleep(0.5)
            self.stop()
        elif self.W_pressed and not (self.D_pressed or self.A_pressed or self.S_pressed):
            self.conn.send(data_to_send['W'])
            self.conn.recv(1)
        elif self.S_pressed and not (self.D_pressed or self.A_pressed or self.W_pressed):
            self.conn.send(data_to_send['S'])
            self.conn.recv(1)
        elif self.A_pressed and not (self.D_pressed or self.S_pressed or self.W_pressed or self.Shift_pressed):
            self.conn.send(data_to_send['A'])
            self.conn.recv(1)
        elif self.D_pressed and not (self.A_pressed or self.S_pressed or self.W_pressed or self.Shift_pressed):
            self.conn.send(data_to_send['D'])
            self.conn.recv(1)
        elif self.W_pressed and self.D_pressed and not (self.A_pressed or self.S_pressed):
            self.conn.send(data_to_send['DW'])
            self.conn.recv(1)
        elif self.W_pressed and self.A_pressed and not (self.D_pressed or self.S_pressed):
            self.conn.send(data_to_send['AW'])
            self.conn.recv(1)
        elif self.S_pressed and self.D_pressed and not (self.W_pressed or self.A_pressed):
            self.conn.send(data_to_send['DS'])
            self.conn.recv(1)
        elif self.S_pressed and self.A_pressed and not (self.W_pressed or self.D_pressed):
            self.conn.send(data_to_send['AS'])
            self.conn.recv(1)
        elif self.Shift_pressed and self.A_pressed and not (self.W_pressed or self.D_pressed or self.S_pressed):
            self.conn.send(data_to_send['shiftA'])
            self.conn.recv(1)
        elif self.Shift_pressed and self.D_pressed and not (self.W_pressed or self.A_pressed or self.S_pressed):
            self.conn.send(data_to_send['shiftD'])
            self.conn.recv(1)
        else:
            self.conn.send(data_to_send[""])
            self.conn.recv(1)

    def build(self):
        print("build")
        layout = BoxLayout(orientation='vertical')

        buttonforw = Button(text='forward')
        buttonforw.bind(state=self.callback_forw)
        buttonback = Button(text='back')
        buttonback.bind(state=self.callback_back)
        buttonleft = Button(text='left')
        buttonleft.bind(state=self.callback_left)
        buttonright = Button(text='right')
        buttonright.bind(state=self.callback_right)
        buttonshift = Button(text='shift')
        buttonshift.bind(state=self.callback_shift)
        buttonstop = Button(text='stop')
        buttonstop.bind(state=self.callback_stop)
        layout.add_widget(buttonforw)
        layout.add_widget(buttonback)
        layout.add_widget(buttonleft)
        layout.add_widget(buttonright)
        layout.add_widget(buttonshift)
        layout.add_widget(buttonstop)

        return layout

if __name__ == "__main__":
    StackGameApp().run()
