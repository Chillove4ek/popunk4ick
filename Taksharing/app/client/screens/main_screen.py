from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

from app.client.order import Order
from app.client.user import User
from app.client.utilities import MyTextInput, ErrorPopup
from settings.config import PlACES


class MainScreen(Screen):

    def __init__(self, user: User, order: Order, name='Main', year='2023', places=PlACES):
        super().__init__()
        self.name = name
        self.user = user
        self.order = order
        self.year = year
        self.places = places
        self.add_widget(self.build())

    def update(self):
        self.remove_widget(self.children[0])
        self.add_widget(self.build())

    def build(self):
        bl_main = BoxLayout(orientation="vertical", spacing="30sp", padding=(0, 0, 0, '25sp'))

        profile_button_box = AnchorLayout(size_hint=(1, None), height="60sp", anchor_x='left', anchor_y='top')
        profile_button = Button(size_hint=(0.25, 0.5), text="Профиль", on_release=self.go_to_profile)
        profile_button_box.add_widget(profile_button)
        bl_main.add_widget(profile_button_box)

        bl_main.add_widget(Label(font_size="36sp", text='Введите данные \n о поездке', halign="center"))

        bl_data = BoxLayout(
            orientation="horizontal", pos_hint={'center_x': .5, 'center_y': .5}, size_hint=(None, None), width="300sp"
        )

        data_day = MyTextInput(
            size_hint=(1, None), height="50sp", width="75sp",
            hint_text="Число", multiline=False, char=2, font_size="20sp", padding="5sp", input_filter="int"
        )
        data_day.bind(text=lambda instance, number: setattr(self.order, "day", number))
        bl_data.add_widget(data_day)

        data_month = MyTextInput(
            size_hint=(1, None), height="50sp", width="75sp",
            hint_text="Месяц", multiline=False, char=2, font_size="20sp", padding="5sp", input_filter="int"
        )
        data_month.bind(text=lambda instance, number: setattr(self.order, "month", number))
        bl_data.add_widget(data_month)

        data_year = MyTextInput(
            size_hint=(1, None), height="50sp", width="80sp", hint_text="Год", multiline=False, char=4,
            font_size="20sp", padding="5sp", text=self.year, input_filter="int"
        )
        data_year.bind(text=lambda instance, number: setattr(self.order, "year", number))
        bl_data.add_widget(data_year)

        bl_main.add_widget(bl_data)

        box_time = BoxLayout(
            pos_hint={'center_x': .5, 'center_y': .5}, size_hint=(None, None), width="300sp", height="70sp"
        )
        box_time.add_widget(Label(
            font_size="18sp", text='Время \n выезда:', halign="center",
            pos_hint={'center_x': 0.1, 'center_y': 0.5}, size_hint=(0.3, 1)
        ))

        time_drop = DropDown(max_height="200sp", on_select=lambda instance, hours: setattr(self.order, 'hours', hours))
        time_drop.bind(on_select=lambda instance, time: setattr(data_time, 'text', time))
        for i in range(25):
            time_drop.add_widget(Button(
                text=f"{i}:00", size_hint_y=None, height="60sp", background_color=(0.7, 0.7, 0.7, 1),
                on_release=lambda btn: time_drop.select(btn.text),
            ))

        data_time = Button(
            size_hint=(1, 1), pos_hint={'center_x': 0, 'center_y': .5}, text='Выбрать',
            background_color=(0.68, 0.73, 0.85, 1), on_release=time_drop.open
        )

        box_time.add_widget(data_time)
        bl_main.add_widget(box_time)

        box_from = BoxLayout(
            orientation="horizontal", pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint=(None, None), height="70sp", width="300sp"
        )
        box_from.add_widget(Label(
           pos_hint={'center_x': 0.1, 'center_y': 0.5}, size_hint=(0.3, 1),  font_size="18sp", text='Откуда:'
        ))

        dropdown_from = DropDown(on_select=lambda instance, x: setattr(self.order, 'start', x), max_height="150sp")
        dropdown_from.bind(on_select=lambda instance, x: setattr(from_button, 'text', x))
        for place in self.places:
            dropdown_from.add_widget(Button(
                text=place, size_hint_y=None, height="60sp", background_color=(0.7, 0.7, 0.7, 1),
                on_release=lambda btn: dropdown_from.select(btn.text)
            ))

        from_button = Button(
            text='Выбрать', size_hint=(1, 1), background_color=(0.68, 0.73, 0.85, 1),
            pos_hint={'center_x': 0, 'center_y': .5}, on_release=dropdown_from.open
        )

        box_from.add_widget(from_button)

        bl_main.add_widget(box_from)

        box_to = BoxLayout(
            width="300sp", pos_hint={'center_x': 0.5, 'center_y': 0.5}, size_hint=(None, None), height="70sp"
        )
        box_to.add_widget(Label(
            font_size="18sp", text='Куда:', pos_hint={'center_x': 0.1, 'center_y': 0.5}, size_hint=(0.3, 1)
        ))
        dropdown_to = DropDown(on_select=lambda instance, x: setattr(to_button, 'text', x), max_height="150sp")
        dropdown_to.bind(on_select=lambda instance, x: setattr(self.order, 'finish', x))
        for elem in self.places:
            dropdown_to.add_widget(Button(
                text=elem, size_hint_y=None, height="60sp", background_color=(0.7, 0.7, 0.7, 1),
                on_release=lambda btn: dropdown_to.select(btn.text)
            ))

        to_button = Button(text='Выбрать', size_hint=(1, 1), background_color=(0.68, 0.73, 0.85, 1),
                           pos_hint={'center_x': 0, 'center_y': .5}, on_release=dropdown_to.open)

        box_to.add_widget(to_button)

        bl_main.add_widget(box_to)

        main_button = Button(pos_hint={'center_x': .5, 'center_y': .5}, size_hint=(None, None), height="80sp",
                             background_color=(.8, .23, .13, 1), width="300sp",
                             font_size="20sp", text="Найти попутчика", on_release=self.go_data_screen)
        bl_main.add_widget(main_button)

        bl_main.add_widget(Label(text="По вопросам и предложениям: momyoz@mail.ru", font_size="12sp"))

        return bl_main

    def go_to_profile(self, _instance):
        answer = self.user.find_orders()
        if answer != 'Completed':
            return ErrorPopup(error_text=answer).open()
        profile_screen = self.parent.get_screen(name='Profile')
        profile_screen.update()
        self.order = Order()
        self.parent.current = 'Profile'

    def go_data_screen(self, _instance):
        answer = self.order.find_companion(user=self.user)
        if answer == 'Accept':
            self.user.last_screen = self.name
            data_screen = self.parent.get_screen(name='Choose')
            data_screen.update()
            self.parent.current = 'Choose'
        else:
            ErrorPopup(error_text=answer).open()


if __name__ == "__main__":
    pass
