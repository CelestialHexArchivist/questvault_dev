### **QuestVault**

A Python-based GUI application for scraping, managing, and searching video game item data from wiki-style websites like the Subnautica Fandom Wiki. This tool allows users to dynamically add scrape domains, select or switch between databases, and perform searches with a user-friendly interface.

---

## **Features**
- **Web Scraping**:
  - Extract item names, descriptions, and categories from wiki-based websites.
  - Supports multiple scrape domains.
- **GUI Interface**:
  - Add and manage scrape domains.
  - Real-time scraping progress feedback.
  - Search by keyword or filter by category in a scrollable result list.
- **Database Management**:
  - Store scraped data in SQLite databases.
  - Dynamically select or switch databases.
- **Testing**:
  - Fully tested for database operations, scraping logic, and GUI interactions.

---

## **Getting Started**

### **Requirements**
- Python 3.8 or higher
- Libraries listed in `requirements.txt`

### **Installation**
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/subnautica-scraper.git
   cd subnautica-scraper
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## **Usage**

### **1. Run the Application**
Start the GUI application:
```bash
python main_gui.py
```

### **2. Add Scrape Domains**
1. Enter the URL of a wiki-style website in the text input field.
2. Click **Add Domain** to save the domain.

### **3. Start Scraping**
1. Ensure the domain appears in the list.
2. Click **Start Scraping** to begin data extraction.
3. Data is saved in the selected SQLite database.

### **4. Select a Database**
1. Click **Select Database** to choose or switch databases.
2. Use the default database (`subnautica_items.db`) or a custom one.

### **5. Search for Items**
1. Enter a keyword in the "Search items by keyword" text field.
2. Click **Search** to view matching items in a scrollable list.

---

## **File Structure**

```plaintext
project/
├── main_gui.py                # Main GUI entry point
├── core/                      # Core functionality
│   ├── database_manager.py    # Handles database creation, search, and filter
│   ├── scraper.py             # Scraping logic for items and domains
│   ├── url_manager.py         # Domain management functions
├── resources/                 # Additional resources
│   ├── icons/                 # GUI icons (optional)
│   ├── data/                  # Default or example databases
├── subnautica_items.db        # Default SQLite database (created at runtime)
├── test/                      # Test suite
│   ├── test_database.py       # Tests for database operations
│   ├── test_scraper.py        # Tests for scraping logic
│   ├── test_gui.py            # Tests for GUI functionality
├── README.md                  # Documentation
└── requirements.txt           # Python dependencies
```

---

## **Testing**

### **Run All Tests**
```bash
pytest test/
```

### **Test Coverage**
- **Database Tests**:
  - Validate database creation and CRUD operations.
  - Test search and filtering functionalities.
- **Scraper Tests**:
  - Ensure scraping logic works for items and domains.
  - Simulate network errors and edge cases.
- **GUI Tests**:
  - Verify GUI interactions such as adding domains, selecting databases, and searching.

---

## **Planned Features**
1. **Sorting**: Allow sorting search results by name, category, or description.
2. **Export Functionality**: Enable exporting results to CSV files.
3. **Pagination**: Improve performance for large datasets with paginated results.
4. **Multi-threaded Scraping**: Speed up scraping for multiple domains.

---

## **Contributing**
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature
   ```
3. Commit your changes and push to your branch.
4. Open a pull request.

---

## **License**
This project is licensed under the MIT License. See `LICENSE` for details.

---

## **Acknowledgments**
- **Kivy**: GUI framework.
- **BeautifulSoup**: Web scraping library.
- **SQLite**: Lightweight database management.
- **Subnautica Fandom Wiki**: Provided item data for testing.

---

Feel free to contact me if you have any questions or need further support!