import os
import json
import hashlib
from time import time
from PIL import Image
import shutil

class CacheManager:
    """Manages caching of background images and other assets"""
    
    def __init__(self, cache_dir='cache'):
        self.cache_dir = cache_dir
        self.cache_info_file = os.path.join(cache_dir, 'cache_info.json')
        self.max_age = 7 * 24 * 60 * 60  # 7 days in seconds
        self.max_size = 100 * 1024 * 1024  # 100MB in bytes
        self._init_cache()
    
    def _init_cache(self):
        """Initialize cache directory and info file"""
        os.makedirs(self.cache_dir, exist_ok=True)
        if not os.path.exists(self.cache_info_file):
            self._save_cache_info({})
    
    def _load_cache_info(self):
        """Load cache information from JSON file"""
        try:
            with open(self.cache_info_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def _save_cache_info(self, info):
        """Save cache information to JSON file"""
        with open(self.cache_info_file, 'w') as f:
            json.dump(info, f)
    
    def _get_file_hash(self, file_path):
        """Generate hash for a file"""
        hasher = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hasher.update(chunk)
        return hasher.hexdigest()
    
    def _cleanup_cache(self):
        """Remove old cache entries"""
        info = self._load_cache_info()
        current_time = time()
        total_size = 0
        entries_to_remove = []
        
        # Check age and calculate total size
        for cache_key, entry in info.items():
            if current_time - entry['timestamp'] > self.max_age:
                entries_to_remove.append(cache_key)
            else:
                total_size += entry['size']
        
        # Remove old entries
        for cache_key in entries_to_remove:
            self._remove_cache_entry(cache_key, info)
        
        # Check size limit
        if total_size > self.max_size:
            # Sort by timestamp and remove oldest until under limit
            sorted_entries = sorted(
                info.items(),
                key=lambda x: x[1]['timestamp']
            )
            while total_size > self.max_size and sorted_entries:
                cache_key, entry = sorted_entries.pop(0)
                total_size -= entry['size']
                self._remove_cache_entry(cache_key, info)
        
        self._save_cache_info(info)
    
    def _remove_cache_entry(self, cache_key, info):
        """Remove a cache entry and its file"""
        try:
            os.remove(os.path.join(self.cache_dir, cache_key))
            del info[cache_key]
        except (OSError, KeyError):
            pass
    
    def get_cached_background(self, original_path, size):
        """
        Get cached background image or create new cache entry
        
        Args:
            original_path (str): Path to original image
            size (tuple): Target size (width, height)
            
        Returns:
            str: Path to cached image
        """
        # Generate cache key
        size_str = f"{size[0]}x{size[1]}"
        file_hash = self._get_file_hash(original_path)
        cache_key = f"bg_{file_hash}_{size_str}.png"
        cache_path = os.path.join(self.cache_dir, cache_key)
        
        # Load cache info
        info = self._load_cache_info()
        
        # Check if cached version exists and is valid
        if cache_key in info:
            if os.path.exists(cache_path):
                # Update access timestamp
                info[cache_key]['timestamp'] = time()
                self._save_cache_info(info)
                return cache_path
        
        # Create new cached version
        from core.utils.image_utils import resize_background
        resize_background(original_path, cache_path, size)
        
        # Update cache info
        info[cache_key] = {
            'timestamp': time(),
            'size': os.path.getsize(cache_path),
            'original': original_path
        }
        self._save_cache_info(info)
        
        # Cleanup old cache entries
        self._cleanup_cache()
        
        return cache_path 
    
    def _file_operation(self, operation_type, file_path, *args, **kwargs):
        """Centralized file operation handler"""
        try:
            if operation_type == 'read':
                with open(file_path, 'rb') as f:
                    return f.read(*args)
            elif operation_type == 'write':
                with open(file_path, 'wb') as f:
                    f.write(*args)
            elif operation_type == 'delete':
                os.remove(file_path)
        except (OSError, IOError) as e:
            self.logger.error(f"File operation failed: {e}")
            return None