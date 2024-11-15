from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.metrics import dp

class Book2SlideScreen(Screen):
    def __init__(self, **kwargs):
        super(Book2SlideScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='horizontal', padding=20, spacing=20)

        # Gambar buku besar di sebelah kiri atas
        self.book_image = Image(source="./assets/images/2.jpg", size_hint=(None, None), size=(dp(400), dp(600)))
        self.layout.add_widget(self.book_image)

        # Layout untuk detail buku (judul dan deskripsi) di sebelah kanan gambar
        self.details_layout = BoxLayout(orientation='vertical', spacing=10, padding=(10, 0, 0, 0))
        self.layout.add_widget(self.details_layout)

        # Judul buku
        self.title_label = Label(
            text="To Kill a Mockingbird",
            font_size='32sp',
            halign="left",
            valign="middle",
            size_hint_y=None,
            color=(0.2, 0.2, 0.2, 1)  # Optional color for readability
        )
        self.details_layout.add_widget(self.title_label)

        # Deskripsi buku
        self.description_label = Label(
            text="To Kill a Mockingbird, karya Harper Lee, mengisahkan kehidupan Scout Finch, seorang gadis kecil "
                 "yang tumbuh di Alabama selama era Depresi Besar. Cerita ini mengikuti perjuangan ayahnya, Atticus Finch, "
                 "seorang pengacara yang berusaha membela seorang pria kulit hitam yang dituduh melakukan pemerkosaan terhadap "
                 "seorang wanita kulit putih. Novel ini mengeksplorasi isu-isu rasial, ketidakadilan, dan moralitas di masyarakat "
                 "Amerika pada tahun 1930-an.",
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
