from unittest import TestCase

from kivy.uix.boxlayout import BoxLayout

from main import RoverControllerApp


class TestRoverControllerApp(TestCase):
    def test_callback_forw(self):
        app = RoverControllerApp(no_send=True)
        app.callback_forw(None, "down")
        self.assertTrue(app.W_pressed)

    def test_callback_back(self):
        app = RoverControllerApp(no_send=True)
        app.callback_back(None, "down")
        self.assertTrue(app.S_pressed)

    def test_callback_left(self):
        app = RoverControllerApp(no_send=True)
        app.callback_left(None, "down")
        self.assertTrue(app.A_pressed)

    def test_callback_right(self):
        app = RoverControllerApp(no_send=True)
        app.callback_right(None, "down")
        self.assertTrue(app.D_pressed)

    def test_callback_shift(self):
        app = RoverControllerApp(no_send=True)
        app.callback_shift(None, "down")
        self.assertTrue(app.Shift_pressed)

    def test_callback_stop(self):
        app = RoverControllerApp(no_send=True)
        app.callback_stop(None, "down")
        self.assertTrue(app.doExit)

    def test_build(self):
        app = RoverControllerApp(no_send=True)
        result = app.build()
        self.assertIsNotNone(result)
        self.assertIsInstance(result, BoxLayout)
