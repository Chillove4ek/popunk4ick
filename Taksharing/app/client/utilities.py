import re
import webbrowser

from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput


def add_widgets(box, list_of_widgets):
    for elem in list_of_widgets:
        box.add_widget(elem)


def open_link(link):
    try:
        if link[0] == "v":
            link = "https://" + link
        webbrowser.open_new_tab(link)
    except TypeError as e:
        ErrorPopup(error_text=f"no link")
        print(e)


def check_new_link(link):
    pattern = "^(http:\/\/|https:\/\/)?(vk\.com)\/(id\d|[a-zA-Z0-9_.])+$"
    link_check = re.search(pattern, link)
    if link_check:
        return True
    else:
        return False


class ButtonLinks(Button):

    def __init__(self, vk=None, order_id=None, **kwargs):
        super().__init__(**kwargs)
        self.VKlink = vk
        self.order_id = order_id


class MyTextInput(TextInput):

    def __init__(self, char=100, **kwargs):
        super().__init__(**kwargs)
        self.char = char

    def insert_text(self, substring, from_undo=False):
        if len(self.text) >= self.char:
            substring = ""
        TextInput.insert_text(self, substring, from_undo)


class ErrorPopup(Popup):

    def __init__(self, error_text=None):
        super().__init__()
        self.title = "Ошибка"
        self.content = Label(text=error_text)
        self.size_hint = (None, None)
        self.size = ("300sp", "150sp")
        self.pos_hint = {'center_x': .5, 'center_y': .5}


if __name__ == '__main__':
    pass
