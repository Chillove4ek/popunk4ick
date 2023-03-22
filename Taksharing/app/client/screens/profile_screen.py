import time

from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

from app.client.order import Order
from app.client.user import User
from app.client.utilities import ErrorPopup, ButtonLinks


class ProfileScreen(Screen):

    def __init__(self, user: User, name='Profile'):
        super().__init__()
        self.name = name
        self.user = user
        self.add_widget(self.build())

    def update(self):
        self.remove_widget(self.children[0])
        self.add_widget(self.build())

    def build(self):
        profile_box = BoxLayout(orientation="vertical", spacing="15sp")

        back_button_box = AnchorLayout(size_hint=(1, 0.1), anchor_x='left', anchor_y='top')
        back_button_box.add_widget(Button(text="Назад", size_hint=(0.25, 1), on_release=self.go_to_main_screen))
        profile_box.add_widget(back_button_box)

        bl_title = BoxLayout(size_hint=(1, 0.3))
        bl_title.add_widget(Image(
            source=r"C:\Users\momyo\PycharmProjects\Taksharing\app\media\profile.png",
            height="100sp", size_hint=(1, 1), pos_hint={'center_x': 0.3, 'center_y': 0.5}
        ))
        bl_title.add_widget(Label(text=f"User: {self.user.username}", size_hint=(.7, 1),
                                  text_size=(100, 100), valign="bottom"))
        profile_box.add_widget(bl_title)

        bl_info = BoxLayout(orientation="vertical", size_hint=(1, 0.2))
        bl_info_link = BoxLayout()
        bl_info_link.add_widget(Label(
            text="Ссылка ВК: ", size_hint=(0.35, None), pos_hint={'center_x': 0.5, 'center_y': 0.5}
        ))
        bl_info_input = TextInput(
            text=self.user.get_link(), pos_hint={'center_x': 0.5, 'center_y': 0.5}, size_hint=(0.65, None),
            height="30sp", halign="left", multiline=False, padding="5sp"
        )
        bl_info_input.bind(text=lambda instance, link: setattr(self.user, "link", link))
        bl_info_link.add_widget(bl_info_input)
        bl_info.add_widget(bl_info_link)

        bl_info.add_widget(Button(
            text='Сохранить', size_hint=(1, None), height="30sp", font_size="16sp", on_press=self.update_link
        ))

        save_button_box = AnchorLayout(size_hint=(1, 0.4), anchor_x='left')
        save_button_box.add_widget(Label(text="Ваши заявки: ", size_hint=(0.6, 1), font_size="22sp"))
        bl_info.add_widget(save_button_box)
        profile_box.add_widget(bl_info)

        scroll_order = ScrollView()
        if self.user.orders:
            orders_list = BoxLayout(orientation="vertical", spacing="5sp", size_hint_y=len(self.user.orders) / 5)
            for order in self.user.orders:

                order_box = BoxLayout(orientation="vertical", height=300)

                date = time.gmtime(int(order[3]))
                time_string = time.strftime("%d/%m/%Y, %H:%M", date)

                order_box.add_widget(Label(
                    text=f"Маршрут:{order[1]} - {order[2]} \n Дата: {time_string}", halign="center"
                ))

                button_box = BoxLayout(orientation="horizontal", size_hint=(1, 0.5))

                button_box.add_widget(ButtonLinks(text="Поиск", order_id=order[0], on_release=self.find_by_id))

                button_box.add_widget(ButtonLinks(
                    text="Удалить", order_id=order[0], on_release=self.delete_order_by_id
                ))

                order_box.add_widget(button_box)

                orders_list.add_widget(order_box)

            scroll_order.add_widget(orders_list)

            profile_box.add_widget(scroll_order)
        else:
            profile_box.add_widget(Label(text="У вас еще нет заявок"))

        btn_exit = Button(text="Выйти из аккаунта", size_hint=(1, .2), background_color=(0.45, 0.52, 0.6, 0.5),
                          on_release=lambda x: setattr(self.parent, "current", "Login"))
        profile_box.add_widget(btn_exit)

        return profile_box

    def go_to_main_screen(self, _instance):  # to zero order
        main_screen = self.parent.get_screen(name='Main')
        main_screen.update()
        self.parent.current = 'Main'

    def update_link(self, _instance):
        answer = self.user.update_link()
        if answer == "Updated":
            Popup(title="Выполнено", content=Label(text="Ссылка обновлена"),
                  size_hint=(None, None), size=(250, 125), pos_hint={'center_x': .5, 'center_y': .5}).open()
        else:
            ErrorPopup(error_text=answer).open()

    def server_delete_order(self, _instance):
        pass

    def find_by_id(self, instance):
        if Order(order_id=instance.order_id).find_order_by_id(self.user):
            data_screen = self.parent.get_screen("Choose")
            data_screen.update()
            self.user.last_screen = self.name
            self.parent.current = "Choose"
        else:
            ErrorPopup(error_text="Не удалось подключиться к серверу").open()

    def delete_order_by_id(self, instance):
        if Order(order_id=instance.order_id).delete_order_by_id(self.user):
            instance.parent.parent.parent.remove_widget(instance.parent.parent)
        else:
            ErrorPopup(error_text="Не удалось подключиться к серверу").open()


if __name__ == '__main__':
    pass
