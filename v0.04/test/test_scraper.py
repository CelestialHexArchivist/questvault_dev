import pytest
from unittest.mock import patch
from core.scraper import fetch_page_content, parse_item_list, scrape_item_details

MOCK_PAGE_CONTENT = """
<html>
    <body>
        <a href="/wiki/Item1">Item 1</a>
        <a href="/wiki/Item2">Item 2</a>
    </body>
</html>
"""

MOCK_ITEM_PAGE = """
<html>
    <body>
        <p>This is a test description for Item 1.</p>
        <a href="/wiki/Category:TestCategory">Category: TestCategory</a>
    </body>
</html>
"""

@patch("core.scraper.requests.get")
def test_fetch_page_content(mock_get):
    """Test fetching page content."""
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = MOCK_PAGE_CONTENT

    content = fetch_page_content("https://example.com")
    assert content == MOCK_PAGE_CONTENT, "Should return mock page content"

@patch("core.scraper.fetch_page_content", return_value=MOCK_PAGE_CONTENT)
def test_parse_item_list(mock_fetch_page_content):
    """Test parsing item list from a page."""
    items = parse_item_list("https://example.com")

    assert len(items) == 2, "Should return two items"
    assert items[0][0] == "Item 1", "First item's name should match"
    assert items[1][1] == "https://example.com/wiki/Item2", "Second item's URL should match"

@patch("core.scraper.fetch_page_content", return_value=MOCK_ITEM_PAGE)
def test_scrape_item_details(mock_fetch_page_content):
    """Test scraping item details."""
    item_details = scrape_item_details("Item 1", "https://example.com/wiki/Item1")

    assert item_details is not None, "Should return item details"
    assert item_details["name"] == "Item 1", "Name should match"
    assert item_details["description"] == "This is a test description for Item 1.", "Description should match"
    assert item_details["category"] == "Category: TestCategory", "Category should match"

@patch("core.scraper.fetch_page_content", side_effect=Exception("Network error"))
def test_fetch_page_content_failure(mock_get):
    """Test handling of failed page fetch."""
    content = fetch_page_content("https://example.com")
    assert content is None, "Should return None on failure"
