"""Unified theme management and repair system"""
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from kivy.logger import Logger
import json
import os
from pathlib import Path

class Theme:
    """Combined theme management and repair"""
    
    # Default theme as fallback >> theme.backup.json
    DEFAULT_THEME = {
        'colors': {
            'primary': (0, 0.957, 0.843, 1),      # Cyan
            'secondary': (1, 0.165, 0.427, 1),    # Pink
            'background': (0.102, 0.102, 0.102, 1), # Dark Gray
            'text': (1, 1, 1, 1),                 # White
            'accent': (0.176, 0.886, 0.902, 1)    # Light Cyan
        },
        'fonts': {
            'name': 'Rajdhani',
            'sizes': {
                'title': dp(24),
                'button': dp(18),
                'text': dp(16)
            }
        },
        'dimensions': {
            'padding': dp(20),
            'spacing': dp(10),
            'button_height': dp(44),
            'input_height': dp(44),
            'border_radius': dp(5)
        }
    }
    
    def __init__(self):
        self.root_dir = Path(__file__).parent.parent.parent
        self.theme_path = self.root_dir / 'resources' / 'theme.json'
        self.fonts_dir = self.root_dir / 'resources' / 'fonts'
        self.current_theme = self.load_theme()
        
    def load_theme(self):
        """Load theme with automatic repair if needed"""
        try:
            # Try to load theme.json
            if self.theme_path.exists():
                with open(self.theme_path) as f:
                    theme = json.load(f)
                    if self.validate_theme(theme):
                        return theme
                    Logger.warning("Invalid theme.json, using defaults")
            
            Logger.error("No valid theme file found")
            return None
            
        except Exception as e:
            Logger.error(f"Theme loading failed: {str(e)}")
            return None
    
    def validate_theme(self, theme):
        """Validate theme structure and values"""
        required_keys = {'colors', 'fonts', 'dimensions'}
        if not all(key in theme for key in required_keys):
            return False
            
        # Validate color values
        for color in theme['colors'].values():
            if not isinstance(color, (tuple, list)) or len(color) != 4:
                return False
                
        return True
    
    def repair_and_save(self):
        """Repair corrupted theme and save"""
        try:
            # Backup existing theme if present
            if self.theme_path.exists():
                self.backup_theme()
            
            # Start with default theme
            repaired_theme = self.DEFAULT_THEME.copy()
            
            # Try to salvage values from corrupted theme
            if self.theme_path.exists():
                try:
                    with open(self.theme_path) as f:
                        old_theme = json.load(f)
                    for category in repaired_theme:
                        if category in old_theme:
                            for key, value in old_theme[category].items():
                                if self.validate_value(category, key, value):
                                    repaired_theme[category][key] = value
                except:
                    pass
            
            # Save repaired theme
            self.theme_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.theme_path, 'w') as f:
                json.dump(repaired_theme, f, indent=4)
            
            return repaired_theme
            
        except Exception as e:
            Logger.error(f"Theme repair failed: {str(e)}")
            return self.DEFAULT_THEME
    
    def validate_value(self, category, key, value):
        """Validate individual theme value"""
        if category == 'colors':
            return isinstance(value, (tuple, list)) and len(value) == 4
        elif category == 'fonts':
            if key == 'sizes':
                return isinstance(value, dict)
            return isinstance(value, str)
        elif category == 'dimensions':
            return isinstance(value, (int, float))
        return False
    
    # Accessor methods
    def get_color(self, name):
        return self.current_theme['colors'].get(name, self.DEFAULT_THEME['colors'][name])
    
    def get_font(self, size_key='text'):
        """Get font with full path"""
        try:
            font_name = self.current_theme['fonts']['name']
            # If it's just a font name without path, construct the full path
            if not font_name.endswith('.ttf'):
                font_name = f"{font_name}.ttf"
            font_path = str(self.fonts_dir / font_name)
            
            # Verify font file exists
            if not os.path.exists(font_path):
                Logger.warning(f'Font not found: {font_path}, falling back to Roboto')
                return ('Roboto', self.current_theme['fonts']['sizes'].get(size_key, dp(16)))
                
            return (
                font_path,
                self.current_theme['fonts']['sizes'].get(size_key, self.DEFAULT_THEME['fonts']['sizes'][size_key])
            )
        except Exception as e:
            Logger.error(f'Error loading font: {str(e)}')
            return ('Roboto', self.DEFAULT_THEME['fonts']['sizes'].get(size_key, dp(16)))
    
    def get_dimension(self, name):
        return self.current_theme['dimensions'].get(name, self.DEFAULT_THEME['dimensions'][name])