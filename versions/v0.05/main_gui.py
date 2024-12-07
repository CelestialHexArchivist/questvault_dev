import os
import sys
from pathlib import Path

# Add the project root to Python's path
PROJECT_ROOT = Path(__file__).parent.absolute()
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle, Line
from kivy.utils import get_color_from_hex

# Local imports
from core.ui.components import UIFactory, FallbackSystem
from core.ui.theme import Theme
from core.logger import setup_logger

class QuestVaultApp(App):
    def __init__(self):
        super().__init__()
        self.title = 'QuestVault'
        # Initialize without database for now
        # self.db = DatabaseManager('questvault.db')
        # self.db.initialize_database()
        self.theme = Theme()
        self.ui = UIFactory(self.theme)
        self.logger = setup_logger('app')
        self.theme_repair = self.theme
        # Initialize domains list (temporary until database is implemented)
        self.domains = []  # This will store your domains
        
    def add_domain(self, instance):
        """Add a new domain to scrape"""
        url = self.url_input.text
        if url:
            # Temporarily store in status instead of database
            self.status_label.text = f"Would add domain: {url}"
            self.url_input.text = ''  # Clear input
        else:
            self.status_label.text = "Please enter a URL"

    def _build_themed(self):
        """Build the main interface with current theme"""
        try:
            # Create main layout
            layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
            
            # Set background with correct path using PROJECT_ROOT
            bg_image_path = os.path.join(PROJECT_ROOT, 'resources', 'icons', 'opensource-retrowave-sunset.png')
            if not os.path.exists(bg_image_path):
                self.logger.error(f"Background image not found: {bg_image_path}")
                return self._build_fallback()
            
            with layout.canvas.before:
                self.bg_color = Color(1, 1, 1, 1)  # White to not tint the image
                self.bg_rect = Rectangle(
                    source=bg_image_path,
                    pos=(0, 0),  # Start at window origin
                    size=Window.size  # Use window size immediately
                )
            
            # Bind to window size for responsive background
            layout.bind(size=self._update_background, pos=self._update_background)
            
            # URL input
            self.url_input = self.ui.create_component(
                'input',
                hint_text='Enter URL'
            )
            layout.add_widget(self.url_input)
            
            # Add URL button
            add_btn = self.ui.create_component(
                'button',
                text='Add URL',
                callback=self.add_domain
            )
            layout.add_widget(add_btn)
            
            # Show domains button
            show_btn = self.ui.create_component(
                'button',
                text='Show Domains',
                callback=self.show_domains
            )
            layout.add_widget(show_btn)
            
            # Scrape all button
            scrape_btn = self.ui.create_component(
                'button',
                text='Scrape All',
                callback=self.scrape_all
            )
            layout.add_widget(scrape_btn)
            
            # Select domain button
            select_btn = self.ui.create_component(
                'button',
                text='Select Domain',
                callback=self.select_domain
            )
            layout.add_widget(select_btn)
            
            # Database selection button
            db_btn = self.ui.create_component(
                'button',
                text='Select Database',
                callback=self.select_database
            )
            layout.add_widget(db_btn)
            
            # Search input
            self.search_input = self.ui.create_component(
                'input',
                hint_text='Search items...'
            )
            layout.add_widget(self.search_input)
            
            # Search button
            search_btn = self.ui.create_component(
                'button',
                text='Search',
                callback=self.search_items
            )
            layout.add_widget(search_btn)
            
            # Status label
            self.status_label = self.ui.create_component(
                'label',
                text='Ready'
            )
            layout.add_widget(self.status_label)
            
            return layout
            
        except Exception as e:
            self.logger.error(f"Error in themed build: {str(e)}")
            return self._build_fallback()

    def _build_fallback(self):
        """Create minimal functional UI without theming"""
        layout = BoxLayout(orientation='vertical', padding=10, spacing=5)
        
        # Basic input
        self.url_input = FallbackSystem.get_safe_widget(
            'input',
            hint_text='Enter URL'
        )
        layout.add_widget(self.url_input)
        
        # Basic buttons
        add_btn = FallbackSystem.get_safe_widget(
            'button',
            text='Add URL',
            callback=self.add_domain
        )
        layout.add_widget(add_btn)
        
        return layout

    def build(self):
        """Build UI with theme repair"""
        try:
            # Try to build with current theme
            return self._build_themed()
        except Exception as e:
            self.logger.error(f"Theme failed, attempting repair: {str(e)}")
            # Try to repair theme
            self.theme = self.theme_repair.repair_and_save()
            try:
                # Try again with repaired theme
                return self._build_themed()
            except Exception as e:
                self.logger.error(f"Repaired theme failed, using fallback: {str(e)}")
                # Fall back to minimal UI
                return self._build_fallback()

    def _update_background(self, instance, value):
        """Update background size and position"""
        if hasattr(self, 'bg_rect'):
            self.bg_rect.size = Window.size
            self.bg_rect.pos = instance.pos

    def show_domains(self, instance):
        """Display all domains in a popup"""
        try:
            # Create content for popup
            content = BoxLayout(orientation='vertical', spacing=10, padding=10)
            domains_list = ScrollView(size_hint=(1, 1))
            domains_grid = GridLayout(cols=1, spacing=10, size_hint_y=None)
            domains_grid.bind(minimum_height=domains_grid.setter('height'))
            
            # Add domain buttons
            for domain in self.domains:  # You'll need to initialize self.domains in __init__
                domain_btn = self.ui.create_component(
                    'button',
                    text=domain,
                    size_hint_y=None,
                    height=dp(40)
                )
                domains_grid.add_widget(domain_btn)
            
            domains_list.add_widget(domains_grid)
            content.add_widget(domains_list)
            
            # Create and show popup
            popup = self.ui.create_component(
                'popup',
                title='Domains',
                content=content
            )
            popup.open()
            
        except Exception as e:
            self.status_label.text = f"Error showing domains: {str(e)}"

    def scrape_all(self, instance):
        """Scrape all domains in the list"""
        try:
            for domain in self.domains:
                # Add to status that we're scraping
                self.status_label.text = f"Scraping {domain}..."
                # Here you would call your scraping logic
                
            self.status_label.text = "Scraping complete!"
            
        except Exception as e:
            self.status_label.text = f"Error during scrape: {str(e)}"

    def select_domain(self, instance):
        """Select a specific domain to scrape"""
        try:
            content = BoxLayout(orientation='vertical', spacing=10, padding=10)
            domains_list = ScrollView(size_hint=(1, 1))
            domains_grid = GridLayout(cols=1, spacing=10, size_hint_y=None)
            domains_grid.bind(minimum_height=domains_grid.setter('height'))
            
            def on_domain_select(btn):
                self.status_label.text = f"Selected domain: {btn.text}"
                popup.dismiss()
            
            for domain in self.domains:
                domain_btn = self.ui.create_component(
                    'button',
                    text=domain,
                    size_hint_y=None,
                    height=dp(40)
                )
                domain_btn.bind(on_press=on_domain_select)
                domains_grid.add_widget(domain_btn)
            
            domains_list.add_widget(domains_grid)
            content.add_widget(domains_list)
            
            popup = self.ui.create_component(
                'popup',
                title='Select Domain',
                content=content
            )
            popup.open()
            
        except Exception as e:
            self.status_label.text = f"Error selecting domain: {str(e)}"

    def select_database(self, instance):
        """Select or create a database"""
        try:
            content = BoxLayout(orientation='vertical', spacing=10, padding=10)
            
            # Add database options
            options = ['Create New Database', 'Open Existing Database']
            for option in options:
                btn = self.ui.create_component(
                    'button',
                    text=option,
                    size_hint_y=None,
                    height=dp(40)
                )
                content.add_widget(btn)
            
            popup = self.ui.create_component(
                'popup',
                title='Database Options',
                content=content
            )
            popup.open()
            
        except Exception as e:
            self.status_label.text = f"Error with database selection: {str(e)}"

    def search_items(self, instance):
        """Search for items in the database"""
        try:
            query = self.search_input.text
            if not query:
                self.status_label.text = "Please enter a search term"
                return
                
            # Create results popup
            content = BoxLayout(orientation='vertical', spacing=10, padding=10)
            results_list = ScrollView(size_hint=(1, 1))
            results_grid = GridLayout(cols=1, spacing=10, size_hint_y=None)
            results_grid.bind(minimum_height=results_grid.setter('height'))
            
            # Here you would actually search your database
            # For now, just show the search term
            result_label = self.ui.create_component(
                'label',
                text=f"Search results for: {query}"
            )
            results_grid.add_widget(result_label)
            
            results_list.add_widget(results_grid)
            content.add_widget(results_list)
            
            popup = self.ui.create_component(
                'popup',
                title='Search Results',
                content=content
            )
            popup.open()
            
        except Exception as e:
            self.status_label.text = f"Error during search: {str(e)}"

if __name__ == '__main__':
    QuestVaultApp().run()
