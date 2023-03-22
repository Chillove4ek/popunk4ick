from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput

from app.client.user import User
from app.client.utilities import ErrorPopup


class LoginScreen(Screen):

    def __init__(self, user: User, name='Login'):
        super().__init__()
        self.user = user
        self.name = name
        self.add_widget(self.build())

    def build(self):
        bl_login = BoxLayout(orientation="vertical", padding=(0, '40sp', 0, '40sp'), spacing='35sp')
        bl_login.add_widget(Label(height='100sp', font_size='40sp', text='Авторизация', color='green'))
        bl_login.add_widget(Image(
            size_hint_y=None, height="100sp",
            source=r"C:\Users\momyo\PycharmProjects\Taksharing\app\media\login1.png"
        ))

        username_input = TextInput(
            pos_hint={'center_x': .5, 'center_y': .5}, size_hint=(None, None), height="60sp", width="240sp",
            hint_text="Имя пользователя", multiline=False, font_size="23sp", padding="10sp"
        )
        username_input.bind(text=lambda instance, text: setattr(self.user, "username", text))
        bl_login.add_widget(username_input)

        password_input = TextInput(
            pos_hint={'center_x': .5, 'center_y': .5}, size_hint=(None, None), height="60sp", width='240sp',
            password=True, hint_text="Пароль", multiline=False, font_size="23sp", padding="10sp"
        )
        password_input.bind(text=lambda instance, text: setattr(self.user, "password", text))
        bl_login.add_widget(password_input)

        bl_login.add_widget(Button(
            pos_hint={'center_x': .5, 'center_y': .5}, size_hint=(None, None), width="160sp", height="45sp",
            font_size="23sp", text="Войти", on_release=self.server_login
        ))

        log_underline = BoxLayout(
            pos_hint={'center_x': .5, 'center_y': .5}, orientation="horizontal", size_hint=(1, None),
            padding=("50sp", 0, "50sp", 0)
        )
        log_underline.add_widget(Label(text="Еще нет аккаунта?", font_size="14sp"))
        log_underline.add_widget(Button(
            background_color='black', text="Регистрация", font_size='15sp', color=(0, 2, 1, 1),
            on_release=lambda x: setattr(self.parent, 'current', 'Register')
        ))
        bl_login.add_widget(log_underline)
        return bl_login

    def server_login(self, _instance):
        answer = self.user.login()
        if answer != 'Accept':
           return ErrorPopup(error_text=answer).open()
        self.parent.current = "Main"


if __name__ == '__main__':
    pass
