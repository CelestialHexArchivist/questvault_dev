from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView
from database_manager import initialize_database, get_all_items, search_items_by_keyword, search_items_by_category

class URLManagerApp(App):
    def build(self):
        self.root = BoxLayout(orientation='vertical')

        # Initialize the database
        self.db_name = "subnautica_items.db"
        initialize_database(self.db_name)

        # Input for new URL
        self.url_input = TextInput(hint_text="Enter new domain URL", multiline=False)
        self.root.add_widget(self.url_input)

        # Add URL button
        add_button = Button(text="Add Domain")
        add_button.bind(on_press=self.add_domain)
        self.root.add_widget(add_button)

        # Database selection button
        db_button = Button(text="Select Database")
        db_button.bind(on_press=self.select_database)
        self.root.add_widget(db_button)

        # Search field
        self.search_input = TextInput(hint_text="Search items by keyword", multiline=False)
        self.root.add_widget(self.search_input)

        # Search button
        search_button = Button(text="Search")
        search_button.bind(on_press=self.search_items)
        self.root.add_widget(search_button)

        # Scrollable container for search results
        scroll_view = ScrollView(size_hint=(1, None), size=(self.root.width, 400))
        self.result_list = BoxLayout(orientation='vertical', size_hint_y=None)
        self.result_list.bind(minimum_height=self.result_list.setter('height'))
        scroll_view.add_widget(self.result_list)
        self.root.add_widget(scroll_view)

        # Status label
        self.status_label = Label(text="Status: Waiting", size_hint_y=None, height=30)
        self.root.add_widget(self.status_label)

        return self.root

    def add_domain(self, instance):
        # Placeholder for add domain logic
        pass

    def select_database(self, instance):
        # FileChooser Popup
        def on_selection(instance, value):
            if value:
                self.db_name = value[0]
                self.show_popup("Success", f"Database selected: {self.db_name}")
        
        chooser = FileChooserIconView()
        chooser.bind(selection=on_selection)
        popup = Popup(title="Select Database", content=chooser, size_hint=(0.9, 0.9))
        popup.open()

    def search_items(self, instance):
        keyword = self.search_input.text.strip()
        if not keyword:
            self.show_popup("Error", "Enter a keyword to search.")
            return
        
        results = search_items_by_keyword(self.db_name, keyword)
        if not results:
            self.result_list.clear_widgets()
            self.result_list.add_widget(Label(text="No results found", size_hint_y=None, height=30))
            return
        
        self.result_list.clear_widgets()
        for name, description, category in results:
            item_label = Label(
                text=f"Name: {name}\nDescription: {description}\nCategory: {category}",
                size_hint_y=None,
                height=60,
            )
            self.result_list.add_widget(item_label)

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.8, 0.4))
        popup.open()

if __name__ == "__main__":
    URLManagerApp().run()
