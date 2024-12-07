"""Unified UI component creation and management"""
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.animation import Animation
from kivy.properties import NumericProperty, ColorProperty, ListProperty
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, RoundedRectangle, Ellipse
from kivy.metrics import dp
from kivy.clock import Clock
from functools import partial
from kivy.uix.boxlayout import BoxLayout

class UIFactory:
    """Centralized UI component creation with theming"""
    
    def __init__(self, theme):
        self.theme = theme
    
    def create_component(self, component_type: str, **kwargs) -> Widget:
        """Create themed UI component"""
        creators = {
            'button': self.create_button,
            'input': self.create_input,
            'label': self.create_label,
            'popup': self.create_popup
        }
        creator = creators.get(component_type)
        if not creator:
            return FallbackSystem.get_safe_widget(component_type, **kwargs)
        return creator(**kwargs)
    
    def create_button(self, text: str, callback=None, **kwargs) -> Button:
        """Create themed button"""
        defaults = {
            'text': text,
            'size_hint_y': None,
            'height': self.theme.get_dimension('button_height'),
            'background_color': self.theme.get_color('primary'),
            'color': self.theme.get_color('text'),
            'font_name': self.theme.get_font()[0],
            'font_size': self.theme.get_font('button')[1]
        }
        defaults.update(kwargs)
        
        button = RippleButton(**defaults)
        if callback:
            button.bind(on_press=callback)
        return button
    
    def create_input(self, **kwargs) -> TextInput:
        """Create themed input"""
        defaults = {
            'multiline': False,
            'size_hint_y': None,
            'height': self.theme.get_dimension('input_height'),
            'background_color': self.theme.get_color('background'),
            'foreground_color': self.theme.get_color('text'),
            'font_name': self.theme.get_font()[0],
            'font_size': self.theme.get_font()[1],
            'padding': [self.theme.get_dimension('padding'), 10]
        }
        defaults.update(kwargs)
        return TextInput(**defaults)
    
    def create_label(self, text: str, **kwargs) -> Label:
        """Create themed label"""
        defaults = {
            'text': text,
            'color': self.theme.get_color('text'),
            'font_name': self.theme.get_font()[0],
            'font_size': self.theme.get_font()[1]
        }
        defaults.update(kwargs)
        return Label(**defaults)
    
    def create_popup(self, title: str, content: Widget, **kwargs) -> Popup:
        """Create themed popup"""
        defaults = {
            'title': title,
            'content': content,
            'size_hint': (0.8, None),
            'height': dp(400),
            'title_color': self.theme.get_color('text'),
            'title_size': self.theme.get_font('title')[1],
            'title_font': self.theme.get_font()[0],
            'separator_color': self.theme.get_color('secondary')
        }
        defaults.update(kwargs)
        return AnimatedPopup(**defaults)

class RippleButton(Button):
    """Button with ripple effect"""
    ripple_color = ListProperty([1, 1, 1, 0.3])
    ripple_duration = NumericProperty(0.5)
    ripple_scale = NumericProperty(2.0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ripple = None
        
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self._create_ripple(touch.pos)
        return super().on_touch_down(touch)
    
    def _create_ripple(self, pos):
        ripple = Ellipse(pos=pos, size=(dp(10), dp(10)))
        with self.canvas:
            Color(*self.ripple_color)
            self.ripple = ripple
            
        anim = Animation(
            size=(dp(100), dp(100)), 
            duration=self.ripple_duration,
            t='out_quad'
        )
        anim.bind(on_complete=self._remove_ripple)
        anim.start(ripple)
    
    def _remove_ripple(self, *args):
        if self.ripple:
            self.canvas.remove(self.ripple)
            self.ripple = None

class AnimatedPopup(Popup):
    """Popup with animation effects"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.opacity = 0
        
    def open(self, *args):
        super().open(*args)
        anim = Animation(opacity=1, duration=0.2)
        anim.start(self)
    
    def dismiss(self, *args, **kwargs):
        anim = Animation(opacity=0, duration=0.2)
        anim.bind(on_complete=lambda *x: super().dismiss())
        anim.start(self) 

class FallbackSystem:
    """Provides basic UI components when theme system fails"""
    
    @staticmethod
    def get_safe_widget(widget_type, **kwargs):
        """Create basic widgets with safe default values"""
        widgets = {
            'button': Button,
            'input': TextInput,
            'label': Label,
            'layout': BoxLayout
        }
        
        # Default properties for each widget type
        defaults = {
            'button': {
                'size_hint_y': None,
                'height': dp(40),
                'background_color': (0.2, 0.2, 0.2, 1),
                'color': (1, 1, 1, 1)
            },
            'input': {
                'size_hint_y': None,
                'height': dp(40),
                'multiline': False,
                'background_color': (0.1, 0.1, 0.1, 1),
                'foreground_color': (1, 1, 1, 1)
            },
            'label': {
                'color': (1, 1, 1, 1)
            },
            'layout': {
                'orientation': 'vertical',
                'padding': dp(10),
                'spacing': dp(5)
            }
        }
        
        # Get widget class and its defaults
        widget_class = widgets.get(widget_type)
        widget_defaults = defaults.get(widget_type, {})
        
        if not widget_class:
            return Label(text=f"Error: Unknown widget type '{widget_type}'")
            
        # Merge defaults with provided kwargs
        properties = widget_defaults.copy()
        properties.update(kwargs)
        
        # Handle callback for buttons
        if widget_type == 'button' and 'callback' in properties:
            callback = properties.pop('callback')
            widget = widget_class(**properties)
            widget.bind(on_release=callback)
            return widget
            
        return widget_class(**properties) 