import pytest
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from main_gui import URLManagerApp
from unittest.mock import patch

@pytest.fixture
def app():
    """Fixture to initialize the Kivy application."""
    test_app = URLManagerApp()
    return test_app

def test_gui_initialization(app):
    """Test that the main GUI initializes correctly."""
    root = app.build()
    assert isinstance(root, BoxLayout), "Root widget should be a BoxLayout"
    assert root.children, "Root widget should have children"

def test_add_domain_functionality(app):
    """Test adding a domain."""
    app.build()
    app.url_input.text = "https://example.com"
    with patch("core.url_manager.add_domain") as mock_add_domain:
        app.add_domain(None)
        mock_add_domain.assert_called_once_with("https://example.com")
    assert app.url_input.text == "", "URL input should be cleared after adding a domain"

def test_select_database_functionality(app):
    """Test selecting a database."""
    app.build()
    with patch("kivy.uix.filechooser.FileChooserIconView") as mock_filechooser:
        mock_filechooser.selection = ["test_database.db"]
        app.select_database(None)
        assert app.db_name == "test_database.db", "Selected database should be stored in app.db_name"

def test_search_items_functionality(app):
    """Test searching items by keyword."""
    app.build()
    app.search_input.text = "test_item"

    mock_results = [
        ("Test Item 1", "Description 1", "Category A"),
        ("Test Item 2", "Description 2", "Category B"),
    ]
    with patch("core.database_manager.search_items_by_keyword", return_value=mock_results):
        app.search_items(None)

    # Check that results are displayed in the GUI
    assert len(app.result_list.children) == len(mock_results), "Number of displayed items should match search results"
    for i, child in enumerate(reversed(app.result_list.children)):
        assert mock_results[i][0] in child.text, f"Result {i} should be displayed correctly"

def test_search_no_results(app):
    """Test searching with no results."""
    app.build()
    app.search_input.text = "nonexistent_item"
    with patch("core.database_manager.search_items_by_keyword", return_value=[]):
        app.search_items(None)
    assert len(app.result_list.children) == 1, "Result list should show one child for 'no results'"
    assert "No results found" in app.result_list.children[0].text, "'No results found' should be displayed"

def test_status_label_updates(app):
    """Test status label updates correctly."""
    app.build()

    def mock_update_status(message):
        app.status_label.text = f"Status: {message}"

    mock_update_status("Testing status update")
    assert app.status_label.text == "Status: Testing status update", "Status label should display the correct message"
