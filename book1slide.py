from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.metrics import dp
from datetime import datetime
import pyrebase
from config import get_firebase_config

config = get_firebase_config()
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

class Book1SlideScreen(Screen):
    def __init__(self, **kwargs):
        super(Book1SlideScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='horizontal', padding=20, spacing=20)

        # Gambar buku besar di sebelah kiri atas
        self.book_image = Image(source="./assets/images/1.jpg", size_hint=(None, None), size=(dp(400), dp(600)))
        self.layout.add_widget(self.book_image)

        # Layout untuk detail buku (judul dan deskripsi) di sebelah kanan gambar
        self.details_layout = BoxLayout(orientation='vertical', spacing=10, padding=(10, 0, 0, 0))
        self.layout.add_widget(self.details_layout)

        # Judul buku
        self.title_label = Label(
            text="The Great Gatsby",
            font_size='32sp',
            halign="left",
            valign="middle",
            size_hint_y=None,
            color=(0.2, 0.2, 0.2, 1)  # Optional color for readability
        )
        self.details_layout.add_widget(self.title_label)

        # Deskripsi buku
        self.description_label = Label(
            text="The Great Gatsby, karya F. Scott Fitzgerald, mengisahkan kehidupan Jay Gatsby, "
                 "seorang pria kaya dengan masa lalu misterius, yang berusaha mendapatkan kembali "
                 "cinta lamanya, Daisy Buchanan. Berlatar era Jazz tahun 1920-an, novel ini menggambarkan "
                 "dekadensi, ambisi, dan kemewahan, sekaligus mengeksplorasi tema harapan, cinta yang hilang, "
                 "dan kritik sosial terhadap masyarakat Amerika.",
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
            size=(dp(300), dp(200))
        )
        popup.open()
        self.manager.current = 'book_screen'  # Kembali ke layar utama setelah meminjam

# Fungsi untuk mencatat peminjaman buku ke Firebase
def pinjam_buku(user_id, book_id, due_date):
    try:
        # Menyimpan data peminjaman buku di Realtime Database
        db.child("book_loans").child(user_id).child(book_id).set({ # type: ignore
            "book_id": book_id,
            "user_id": user_id,
            "borrow_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "due_date": due_date
        })
        print("Peminjaman buku berhasil")
        return True, "Peminjaman buku berhasil"
    except Exception as e:
        print(f"Peminjaman buku gagal: {e}")
        return False, str(e)
