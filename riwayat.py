from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.metrics import dp
from kivy.lang import Builder

# Load the kv file
Builder.load_file('riwayat.kv')

class RiwayatScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.riwayat_pinjam = []  # List to store borrowing history

    def add_riwayat_pinjam(self, book_title, borrow_date):
        # Format borrowing record
        riwayat = f"{book_title} - Dipinjam pada {borrow_date}"
        if riwayat not in self.riwayat_pinjam:
            self.riwayat_pinjam.append(riwayat)
            self.update_riwayat()
        else:
            self.show_popup("Error", "Riwayat sudah ada.")

    def update_riwayat(self):
        # Clear old widgets from list
        self.ids.book_list.clear_widgets()
        
        # Add each borrowing record to the list
        for riwayat in self.riwayat_pinjam:
            book_label = Label(text=riwayat, size_hint_y=None, height=dp(30))
            self.ids.book_list.add_widget(book_label)

    def go_back(self):
        # Navigate back to BookScreen
        self.manager.current = 'book_screen'

    def show_popup(self, title, message):
        popup_layout = BoxLayout(orientation='vertical', padding=dp(10))
        popup_label = Label(text=message)
        close_btn = Button(text="Close", size_hint_y=None, height=dp(40))

        popup_layout.add_widget(popup_label)
        popup_layout.add_widget(close_btn)

        popup = Popup(title=title, content=popup_layout, size_hint=(None, None), size=(dp(300), dp(200)))
        close_btn.bind(on_release=popup.dismiss)
        popup.open()
