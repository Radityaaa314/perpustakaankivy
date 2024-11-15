# views.py
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import AsyncImage
from kivy.uix.filechooser import FileChooserIconView
from database import Database
from storage import StorageManager

class BookItem(BoxLayout):
    def __init__(self, book_id, book_data, delete_callback, edit_callback, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 150
        self.padding = 5
        self.spacing = 10

        self.book_id = book_id
        self.book_data = book_data

        # Create image layout
        image_layout = BoxLayout(size_hint_x=0.3, padding=5)
        image_url = book_data.get('image_url', None)
        if image_url:
            book_image = AsyncImage(
                source=image_url,
                allow_stretch=True,
                keep_ratio=True
            )
            image_layout.add_widget(book_image)
        else:
            image_layout.add_widget(
                Label(
                    text='No Image',
                    color=(0.5, 0.5, 0.5, 1)
                )
            )

        # Create info layout
        info_layout = BoxLayout(orientation='vertical', size_hint_x=0.5)
        
        title = book_data.get('judul', 'No Title')
        author = book_data.get('penulis', 'No Author')
        stock = book_data.get('stok', 0)
        
        info_label = Label(
            text=f"Judul: {title}\nPenulis: {author}\nStok: {stock}",
            size_hint_y=None,
            height=100,
            halign='left',
            valign='middle'
        )
        info_label.bind(size=info_label.setter('text_size'))
        info_layout.add_widget(info_label)

        # Button layout
        button_layout = BoxLayout(orientation='vertical', size_hint_x=0.2, spacing=5)
        
        edit_btn = Button(
            text='Edit',
            size_hint_y=0.5,
            background_color=(0.3, 0.5, 0.9, 1)
        )
        edit_btn.bind(on_press=lambda x: edit_callback(book_id, book_data))
        
        delete_btn = Button(
            text='Hapus',
            size_hint_y=0.5,
            background_color=(0.9, 0.3, 0.3, 1)
        )
        delete_btn.bind(on_press=lambda x: delete_callback(book_id))

        button_layout.add_widget(edit_btn)
        button_layout.add_widget(delete_btn)

        self.add_widget(image_layout)
        self.add_widget(info_layout)
        self.add_widget(button_layout)

class BookList(Screen):
    container = ObjectProperty(None)
    
    def on_enter(self):
        self.load_books()
    
    def load_books(self):
        self.container.clear_widgets()
        books = Database.get_all_books()
        
        if books:
            for book_id, book_data in books:
                book_item = BookItem(
                    book_id,
                    book_data,
                    self.delete_book,
                    self.edit_book
                )
                self.container.add_widget(book_item)
        else:
            self.container.add_widget(
                Label(
                    text="Tidak ada buku tersedia",
                    size_hint_y=None,
                    height=100
                )
            )
    
    def show_add_book(self):
        self.manager.current = 'add_book'

    def edit_book(self, book_id, book_data):
        edit_screen = self.manager.get_screen('edit_book')
        edit_screen.set_book(book_id, book_data)
        self.manager.current = 'edit_book'

    def delete_book(self, book_id):
        confirm_popup = Popup(
            title='Konfirmasi',
            size_hint=(None, None),
            size=(300, 200)
        )
        
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text='Apakah Anda yakin ingin\nmenghapus buku ini?'))
        
        buttons = BoxLayout(size_hint_y=None, height=40, spacing=10)
        
        cancel_btn = Button(text='Batal')
        cancel_btn.bind(on_press=confirm_popup.dismiss)
        
        def confirm_delete(instance):
            try:
                # Get book data to delete image if exists
                books = Database.get_all_books()
                book_data = next((data for bid, data in books if bid == book_id), None)
                
                if book_data and 'image_path' in book_data:
                    StorageManager.delete_image(book_data['image_path'])
                
                Database.delete_book(book_id)
                self.load_books()
                confirm_popup.dismiss()
                self.show_popup('Sukses', 'Buku berhasil dihapus!')
            except Exception as e:
                confirm_popup.dismiss()
                self.show_popup('Error', f'Gagal menghapus buku: {str(e)}')
        
        confirm_btn = Button(text='Hapus', background_color=(0.9, 0.3, 0.3, 1))
        confirm_btn.bind(on_press=confirm_delete)
        
        buttons.add_widget(cancel_btn)
        buttons.add_widget(confirm_btn)
        
        content.add_widget(buttons)
        confirm_popup.content = content
        confirm_popup.open()

    def show_popup(self, title, content):
        popup = Popup(
            title=title,
            content=Label(text=content),
            size_hint=(None, None),
            size=(400, 200)
        )
        popup.open()

class AddBook(Screen):
    title_input = ObjectProperty(None)
    author_input = ObjectProperty(None)
    stock_input = ObjectProperty(None)
    image_preview = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_image = None
    
    def choose_image(self):
        popup = ImageChooserPopup(callback=self.on_image_selected)
        popup.open()
    
    def on_image_selected(self, file_path):
        self.selected_image = file_path
        self.image_preview.source = file_path

    def clear_image(self):
        self.selected_image = None
        self.image_preview.source = ''
    
    def add_book(self):
        judul = self.title_input.text.strip()
        penulis = self.author_input.text.strip()
        stok = self.stock_input.text.strip()
        
        if judul and penulis and stok:
            try:
                stok_int = int(stok)
                
                # Upload image if selected
                image_url = None
                image_path = None
                if self.selected_image:
                    result = StorageManager.upload_image(self.selected_image)
                    if result["status"] == "success":
                        image_url = result["url"]
                        image_path = result["path"]
                
                # Create book data
                book_data = {
                    'judul': judul,
                    'penulis': penulis,
                    'stok': stok_int,
                    'image_url': image_url,
                    'image_path': image_path
                }
                
                Database.add_book(book_data)
                
                # Clear inputs
                self.title_input.text = ''
                self.author_input.text = ''
                self.stock_input.text = ''
                self.selected_image = None
                self.image_preview.source = ''
                
                self.show_popup('Sukses', 'Buku berhasil ditambahkan!')
                self.manager.current = 'book_list'
            except ValueError:
                self.show_popup('Error', 'Stok harus berupa angka!')
            except Exception as e:
                self.show_popup('Error', f'Terjadi kesalahan: {str(e)}')
        else:
            self.show_popup('Error', 'Semua field harus diisi!')

    def show_popup(self, title, content):
        popup = Popup(
            title=title,
            content=Label(text=content),
            size_hint=(None, None),
            size=(400, 200)
        )
        popup.open()
    
    def cancel(self):
        self.manager.current = 'book_list'

class EditBook(Screen):
    title_input = ObjectProperty(None)
    author_input = ObjectProperty(None)
    stock_input = ObjectProperty(None)
    image_preview = ObjectProperty(None)
    book_id = StringProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_image = None
        self.current_image_path = None
    
    def on_enter(self):
        if hasattr(self, 'book_data'):
            self.title_input.text = str(self.book_data.get('judul', ''))
            self.author_input.text = str(self.book_data.get('penulis', ''))
            self.stock_input.text = str(self.book_data.get('stok', ''))
            self.current_image_path = self.book_data.get('image_path', None)
            if self.book_data.get('image_url'):
                self.image_preview.source = self.book_data['image_url']

    def choose_image(self):
        popup = ImageChooserPopup(callback=self.on_image_selected)
        popup.open()
    
    def on_image_selected(self, file_path):
        self.selected_image = file_path
        self.image_preview.source = file_path

    def clear_image(self):
        self.selected_image = None
        self.image_preview.source = ''
        if self.current_image_path:
            StorageManager.delete_image(self.current_image_path)
            self.current_image_path = None
    
    def set_book(self, book_id, book_data):
        self.book_id = book_id
        self.book_data = book_data

    def update_book(self):
        judul = self.title_input.text.strip()
        penulis = self.author_input.text.strip()
        stok = self.stock_input.text.strip()
        
        if judul and penulis and stok:
            try:
                image_url = self.book_data.get('image_url')
                image_path = self.current_image_path
                
                if self.selected_image:
                    result = StorageManager.update_image(
                        self.current_image_path,
                        self.selected_image
                    )
                    if result["status"] == "success":
                        image_url = result["url"]
                        image_path = result["path"]
                
                book_data = {
                    'judul': judul,
                    'penulis': penulis,
                    'stok': int(stok),
                    'image_url': image_url,
                    'image_path': image_path
                }
                
                Database.update_book(self.book_id, book_data)
                self.show_popup('Sukses', 'Buku berhasil diupdate!')
                self.manager.current = 'book_list'
            except ValueError:
                self.show_popup('Error', 'Stok harus berupa angka!')
            except Exception as e:
                self.show_popup('Error', f'Terjadi kesalahan: {str(e)}')
        else:
            self.show_popup('Error', 'Semua field harus diisi!')

    def show_popup(self, title, content):
        popup = Popup(
            title=title,
            content=Label(text=content),
            size_hint=(None, None),
            size=(400, 200)
        )
        popup.open()

    def cancel(self):
        self.manager.current = 'book_list'

class ImageChooserPopup(Popup):
    def __init__(self, callback, **kwargs):
        super().__init__(**kwargs)
        self.title = 'Pilih Gambar'
        self.size_hint = (0.9, 0.9)
        self.callback = callback

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        self.file_chooser = FileChooserIconView(
            filters=['*.png', '*.jpg', '*.jpeg'],
            path='.')
        layout.add_widget(self.file_chooser)

        button_layout = BoxLayout(size_hint_y=None, height=40, spacing=10)
        
        cancel_btn = Button(text='Batal')
        cancel_btn.bind(on_press=self.dismiss)
        
        select_btn = Button(text='Pilih', background_color=(0.3, 0.5, 0.9, 1))
        select_btn.bind(on_press=self.select_image)
        
        button_layout.add_widget(cancel_btn)
        button_layout.add_widget(select_btn)
        
        layout.add_widget(button_layout)
        self.content = layout

    def select_image(self, instance):
        if self.file_chooser.selection:
            self.callback(self.file_chooser.selection[0])
            self.dismiss()
