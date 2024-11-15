from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.metrics import dp

class Book3SlideScreen(Screen):
    def __init__(self, **kwargs):
        super(Book3SlideScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='horizontal', padding=20, spacing=20)

        # Gambar buku besar di sebelah kiri atas
        self.book_image = Image(source="./assets/images/3.jpg", size_hint=(None, None), size=(dp(400), dp(600)))
        self.layout.add_widget(self.book_image)

        # Layout untuk detail buku (judul dan deskripsi) di sebelah kanan gambar
        self.details_layout = BoxLayout(orientation='vertical', spacing=10, padding=(10, 0, 0, 0))
        self.layout.add_widget(self.details_layout)

        # Judul buku
        self.title_label = Label(
            text="1984",
            font_size='32sp',
            halign="left",
            valign="middle",
            size_hint_y=None,
            color=(0.2, 0.2, 0.2, 1)  # Optional color for readability
        )
        self.details_layout.add_widget(self.title_label)

        # Deskripsi buku
        self.description_label = Label(
            text="1984, karya George Orwell, menggambarkan dunia dystopia di mana totalitarianisme, pengawasan tanpa henti, "
                 "dan kontrol pikiran dijalankan oleh pemerintah yang dipimpin oleh Partai. Protagonisnya, Winston Smith, bekerja "
                 "di Kementerian Kebenaran, yang bertugas memanipulasi sejarah dan fakta. Dengan pengawasan Big Brother yang terus "
                 "menerus dan ketakutan terhadap kekuasaan negara, Winston berjuang untuk mencari kebebasan pribadi dan kebenaran "
                 "di dunia yang penuh dengan penindasan dan kebohongan.",
            font_size='18sp',
            halign="left",
            valign="top",
            text_size=(dp(350), None),
            color=(0.3, 0.3, 0.3, 1)  # Optional color for readability
        )
        self.details_layout.add_widget(self.description_label)

        # Tombol untuk meminjam buku
        borrow_button = Button(text="Pinjam Buku", size_hint=(None, None), size=(dp(150), dp(50)))
        borrow_button.bind(on_release=self.borrow_book)
        self.details_layout.add_widget(borrow_button)

        # Tambahkan layout utama ke layar
        self.add_widget(self.layout)

    def borrow_book(self, instance):
        # Notifikasi Popup ketika buku berhasil dipinjam
        popup = Popup(
            title="Buku Dipinjam",
            content=Label(text="Anda telah berhasil meminjam buku ini."),
            size_hint=(None, None),
            size=(dp(300), dp(200)),
        )
        popup.open()
        self.manager.current = 'book_screen'  # Kembali ke layar utama setelah meminjam
