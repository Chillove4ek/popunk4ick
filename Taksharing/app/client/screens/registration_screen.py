from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput

from app.client.user import User
from app.client.utilities import ErrorPopup


class RegistrationScreen(Screen):

    def __init__(self, user: User, name='Register'):
        super().__init__()
        self.user = user
        self.name = name
        self.build()

    def build(self):
        bl_reg = BoxLayout(orientation="vertical", padding=(0, "20sp", 0, "100sp"), spacing="20sp")
        bl_reg.add_widget(Label(font_size="40sp", text='Регистрация', height="100sp", size_hint_y=None))

        new_username = TextInput(
            pos_hint={'center_x': .5, 'center_y': .5}, size_hint=(None, None), height="55sp", width="235sp",
            hint_text="Имя пользователя", multiline=False, font_size="23sp", padding="10sp"
        )
        new_username.bind(text=lambda instance, text: setattr(self.user, "username", text))
        bl_reg.add_widget(new_username)

        new_link = TextInput(
            pos_hint={'center_x': .5, 'center_y': .5}, height="55sp", width="235sp", size_hint=(None, None),
            hint_text="Ссылка на ВК", multiline=False, font_size="17sp", padding="14sp"
        )
        new_link.bind(text=lambda instance, text: setattr(self.user, "link", text))
        bl_reg.add_widget(new_link)

        new_password = TextInput(
            pos_hint={'center_x': .5, 'center_y': .5}, height="55sp", width="235sp", size_hint=(None, None),
            password=True, hint_text="Пароль", multiline=False, font_size="24sp", padding="10sp"
        )
        new_password.bind(text=lambda instance, text: setattr(self.user, "password", text))
        bl_reg.add_widget(new_password)

        new_password_repeat = TextInput(
            pos_hint={'center_x': .5, 'center_y': .5}, height="55sp", width="235sp", size_hint=(None, None),
            password=True, hint_text="Повторите пароль", multiline=False, font_size="24sp", padding="10sp"
        )
        new_password_repeat.bind(text=lambda instance, text: setattr(self.user, "password_check", text))
        bl_reg.add_widget(new_password_repeat)

        bl_reg.add_widget(Button(
            pos_hint={'center_x': .5, 'center_y': .5}, height="60sp", width="235sp", size_hint=(None, None),
            font_size="28", text="Создать аккаунт", on_release=self.register_new_user
        ))

        bl_reg.add_widget(Button(
            pos_hint={'center_x': .5, 'center_y': .5}, height="40sp", width="120sp", size_hint=(None, None),
            font_size="20", text="Назад", on_release=lambda x: setattr(self.parent, 'current', 'Login')
        ))
        self.add_widget(bl_reg)

    def register_new_user(self, _instance):
        answer = self.user.registration()
        if answer != 'Accept':
            return ErrorPopup(error_text=answer).open()
        self.parent.current = "Main"

if __name__ == '__main__':
    pass
