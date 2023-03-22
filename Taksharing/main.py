from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition

from settings.config import PlACES
from app.client.screens.registration_screen import RegistrationScreen
from app.client.screens.login_screen import LoginScreen
from app.client.screens.main_screen import MainScreen
from app.client.screens.profile_screen import ProfileScreen
from app.client.screens.data_screen import DataScreen
from app.client.user import User
from app.client.order import Order


class TestApp(App):

    def __init__(self, user: User, order: Order, last_screen=None, places=PlACES):
        super().__init__()
        self.user = user
        self.order = order
        self.last_screen = last_screen
        self.places = places
        self.screens = ScreenManager(transition=NoTransition())

    def build(self):

        self.screens.add_widget(LoginScreen(user=self.user))
        self.screens.add_widget(RegistrationScreen(user=self.user))
        self.screens.add_widget(MainScreen(user=self.user, order=self.order))
        self.screens.add_widget(DataScreen(user=self.user))
        self.screens.add_widget(ProfileScreen(user=self.user))

        self.screens.current = "Login"

        return self.screens


if __name__ == '__main__':
    TestApp(user=User(), order=Order()).run()
