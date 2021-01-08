import logging
import socket
import time

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

bluetooth = False
host = 'b8:27:eb:3e:b8:0a' if bluetooth else "0.0.0.0"
port = 60100

data_to_send = {
    "": b'\x00',
    'W': b'\x01',
    'S': b'\x02',
    'A': b'\x03',
    'D': b'\x04',
    'DW': b'\x05',
    'AW': b'\x06',
    'DS': b'\x07',
    'AS': b'\x08',
    'shiftA': b'\x09',
    'shiftD': b'\x10',
    'K': b'\xff',  # exit
    'P': b'\x7f'  # emergency stop
}

button_dict = {
    "down": True,
    "normal": False
}


class RoverControllerApp(App):
    def __init__(self, no_send=False):
        self.no_send = no_send
        if not self.no_send:
            if bluetooth:
                self.s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
                self.s.connect((host, port))
                self.conn = self.s
            else:
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.bind((host, port))
                self.s.listen(5)
                self.conn, self.addr = self.s.accept()

        self.W_pressed = self.S_pressed = self.A_pressed = self.D_pressed = self.Shift_pressed = self.doExit = False
        logging.info("Initialization done")
        super().__init__()

    def callback_forw(self, _, value):
        self.W_pressed = button_dict[value]
        self.exec_sending()

    def callback_back(self, _, value):
        self.S_pressed = button_dict[value]
        self.exec_sending()

    def callback_left(self, _, value):
        self.A_pressed = button_dict[value]
        self.exec_sending()

    def callback_right(self, _, value):
        self.D_pressed = button_dict[value]
        self.exec_sending()

    def callback_shift(self, _, value):
        self.Shift_pressed = button_dict[value]
        self.exec_sending()

    def callback_stop(self, _, value):
        self.doExit = button_dict[value]
        self.exec_sending()

    def exec_sending(self):
        if self.no_send:
            return
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
        logging.info("Building app")
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
    RoverControllerApp().run()
