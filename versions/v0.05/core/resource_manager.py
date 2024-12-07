"""Centralized resource management"""
import os
from PIL import Image
from core.error_handler import ErrorHandler
from core.logger import setup_logger

class ResourceManager:
    """Manages application resources"""
    
    def __init__(self):
        self.logger = setup_logger('resources')
        self.resource_dir = 'resources'
        self.cache_dir = 'cache'
        self.supported_sizes = {
            'mobile': (720, 1280),
            'tablet': (1080, 1920),
            'desktop': (1920, 1080)
        }
    
    def get_background(self, size_key='mobile'):
        """Get appropriately sized background image"""
        try:
            target_size = self.supported_sizes.get(size_key)
            if not target_size:
                raise ValueError(f"Unsupported size: {size_key}")
            
            # Generate cache key
            cache_key = f"bg_{size_key}.png"
            cache_path = os.path.join(self.cache_dir, cache_key)
            
            # Return cached version if exists
            if os.path.exists(cache_path):
                return cache_path
            
            # Create new sized version
            source_path = os.path.join(self.resource_dir, 'icons', 'background.png')
            self._resize_image(source_path, cache_path, target_size)
            return cache_path
            
        except Exception as e:
            ErrorHandler.handle_error('resource', e)
            return os.path.join(self.resource_dir, 'icons', 'background.png')
    
    def _resize_image(self, source_path, target_path, size):
        """Resize image maintaining aspect ratio"""
        with Image.open(source_path) as img:
            # Calculate dimensions
            ratio = min(size[0]/img.width, size[1]/img.height)
            new_size = (int(img.width * ratio), int(img.height * ratio))
            
            # Resize and save
            img.resize(new_size, Image.Resampling.LANCZOS).save(
                target_path,
                'PNG',
                optimize=True
            ) 