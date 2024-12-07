"""Base test configuration and fixtures"""
import pytest
import os
import sqlite3
from unittest.mock import patch

class TestBase:
    """Base class for all tests"""
    TEST_DB = "test_database.db"
    
    @pytest.fixture
    def setup_test_environment(self):
        """Common test environment setup"""
        # Setup database
        self.initialize_test_db()
        
        # Setup mocks
        self.setup_mocks()
        
        yield
        
        # Cleanup
        self.cleanup_test_environment()
    
    def initialize_test_db(self):
        """Initialize test database"""
        if os.path.exists(self.TEST_DB):
            os.remove(self.TEST_DB)
        
        with sqlite3.connect(self.TEST_DB) as conn:
            conn.executescript('''
                CREATE TABLE IF NOT EXISTS items (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT,
                    category TEXT
                );
                
                CREATE TABLE IF NOT EXISTS domains (
                    id INTEGER PRIMARY KEY,
                    url TEXT UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            ''')
    
    def setup_mocks(self):
        """Setup common test mocks"""
        self.patches = [
            patch('requests.get'),
            patch('core.logger.setup_logger')
        ]
        for p in self.patches:
            p.start()
    
    def cleanup_test_environment(self):
        """Cleanup test environment"""
        # Stop all patches
        for p in self.patches:
            p.stop()
        
        # Remove test database
        if os.path.exists(self.TEST_DB):
            os.remove(self.TEST_DB) 