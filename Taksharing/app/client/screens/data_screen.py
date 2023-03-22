import time

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView

from app.client.user import User
from app.client.utilities import ButtonLinks, open_link


class DataScreen(Screen):

    def __init__(self, user: User, name='Choose'):
        super().__init__()
        self.name = name
        self.user = user
        self.add_widget(self.build())

    def update(self):
        self.remove_widget(self.children[0])
        self.add_widget(self.build())

    def build(self):

        data_box = BoxLayout(orientation="vertical")

        data_box.add_widget(Label(text="Вот что мы нашли по вашему маршруту", size_hint=(1, 0.2)))

        if self.user.orders:
            btn_list = BoxLayout(orientation="vertical", size_hint_y=max(len(self.user.orders) / 5, 1))
            scroll_list = ScrollView()
            for order in self.user.orders:
                date = time.gmtime(int(order[2]))
                time_string = time.strftime("%d/%m/%Y, %H:%M", date)
                btn_user = ButtonLinks(text=f"{time_string}\n Попутчик:{order[0]} \n Ссылка: {order[1]}", halign="center",
                                       on_release=self.say_link, vk=order[1])
                btn_list.add_widget(btn_user)

            scroll_list.add_widget(btn_list)
            data_box.add_widget(scroll_list)

        else:
            data_box.add_widget(Label(text="К сожалению, попутчиков \n на эти даты нет"))

        data_box.add_widget(
            Button(text="Вернуться", size_hint=(1, .2), background_color=(18 / 256, 156 / 256, 30 / 256, 0.6),
                   on_release=lambda x: setattr(self.parent, "current", self.user.last_screen)))

        return data_box

    @staticmethod
    def say_link(instance):
        link = instance.VKlink

        pop_scr = BoxLayout(orientation="vertical")

        pop = Popup(
            title="Подтверждение", content=pop_scr, size_hint=(None, None), size=("300sp", "300sp"),
            pos_hint={'center_x': .5, 'center_y': .5}
        )
        pop_scr.add_widget(Label(text=f"Вы точно хотите открыть ссылку \n {link} ?"))

        btn_box = BoxLayout(size_hint=(1, 0.3))

        btn_yes = Button(text="Да", on_release=lambda x: open_link(link))
        btn_yes.bind(on_release=pop.dismiss)
        btn_box.add_widget(btn_yes)

        btn_box.add_widget(Button(text="Нет", on_release=pop.dismiss))
        pop_scr.add_widget(btn_box)

        pop.open()
