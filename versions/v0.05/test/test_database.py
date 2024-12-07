import os
import sqlite3
import pytest
from core.database_manager import DatabaseManager

TEST_DB = "test_database.db"

@pytest.fixture
def setup_test_db():
    """Setup a temporary test database."""
    initialize_database(TEST_DB)
    yield
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

def test_initialize_database(setup_test_db):
    """Test database initialization."""
    assert os.path.exists(TEST_DB), "Database file should be created"

    with sqlite3.connect(TEST_DB) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        assert "items" in tables, "Table 'items' should exist"
        assert "domains" in tables, "Table 'domains' should exist"

def test_get_all_items(setup_test_db):
    """Test retrieving all items from an empty database."""
    assert get_all_items(TEST_DB) == [], "Should return an empty list for no items"

def test_search_items_by_keyword(setup_test_db):
    """Test searching items by keyword."""
    # Insert sample data
    with sqlite3.connect(TEST_DB) as conn:
        cursor = conn.cursor()
        cursor.executemany(
            "INSERT INTO items (name, description, category) VALUES (?, ?, ?)",
            [
                ("Test Item 1", "A test description", "Category A"),
                ("Test Item 2", "Another description", "Category B"),
            ]
        )
        conn.commit()

    results = search_items_by_keyword(TEST_DB, "test")
    assert len(results) == 1, "Should return one result for keyword 'test'"
    assert results[0][0] == "Test Item 1", "Result should match inserted data"

def test_search_items_by_category(setup_test_db):
    """Test searching items by category."""
    # Insert sample data
    with sqlite3.connect(TEST_DB) as conn:
        cursor = conn.cursor()
        cursor.executemany(
            "INSERT INTO items (name, description, category) VALUES (?, ?, ?)",
            [
                ("Test Item 1", "A test description", "Category A"),
                ("Test Item 2", "Another description", "Category B"),
            ]
        )
        conn.commit()

    results = search_items_by_category(TEST_DB, "Category A")
    assert len(results) == 1, "Should return one result for Category A"
    assert results[0][0] == "Test Item 1", "Result should match the category"

def test_search_no_results(setup_test_db):
    """Test searching for a keyword that has no matches."""
    results = search_items_by_keyword(TEST_DB, "nonexistent")
    assert results == [], "Should return an empty list for nonexistent keyword"

class TestDatabaseManager:
    @pytest.fixture
    def db_manager(self):
        db = DatabaseManager(":memory:")  # Use in-memory database for testing
        db.initialize_database()
        return db
    
    def test_add_domain(self, db_manager):
        assert db_manager.add_domain("https://example.com")
        domains = db_manager.get_domains()
        assert len(domains) == 1
        assert domains[0] == "https://example.com"
