"""Unified database management"""
import sqlite3
from typing import List, Optional, Tuple
from ..error_handler import ErrorHandler
from ..logger import setup_logger

class DatabaseManager:
    """Centralized database operations"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.error_handler = ErrorHandler()
        self.logger = setup_logger('database')
    
    def initialize_database(self):
        """Initialize database with all required tables"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                # Create domains table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS domains (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        url TEXT UNIQUE NOT NULL,
                        target_db TEXT NOT NULL DEFAULT 'main',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Create items table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS items (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        description TEXT,
                        category TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                conn.commit()
        except Exception as e:
            self.error_handler.handle_error('database', e)
            raise
    
    def add_domain(self, url: str) -> bool:
        """Add domain to database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('INSERT INTO domains (url) VALUES (?)', (url,))
            return True
        except sqlite3.IntegrityError:
            return False
        except Exception as e:
            self.error_handler.handle_error('database', e)
            return False
    
    def get_domains(self) -> List[str]:
        """Get all domains"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute('SELECT url FROM domains ORDER BY created_at DESC')
                return [row[0] for row in cursor.fetchall()]
        except Exception as e:
            self.error_handler.handle_error('database', e)
            return []
    
    def add_item(self, name: str, description: str, category: str) -> bool:
        """Add item to database"""
        query = '''
            INSERT INTO items (name, description, category)
            VALUES (?, ?, ?)
        '''
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(query, (name, description, category))
            return True
        except Exception as e:
            self.error_handler.handle_error('database', e)
            return False
    
    def search_items(self, keyword: str = None, category: str = None) -> List[Tuple]:
        """Search items with optional filters"""
        query = 'SELECT name, description, category FROM items WHERE 1=1'
        params = []
        
        if keyword:
            query += ' AND (name LIKE ? OR description LIKE ?)'
            params.extend([f'%{keyword}%'] * 2)
            
        if category:
            query += ' AND category = ?'
            params.append(category)
            
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(query, tuple(params))
                return cursor.fetchall()
        except Exception as e:
            self.error_handler.handle_error('database', e)
            return []
    
    def clear_domains(self) -> None:
        """Clear all domains"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('DELETE FROM domains')
        except Exception as e:
            self.error_handler.handle_error('database', e)
