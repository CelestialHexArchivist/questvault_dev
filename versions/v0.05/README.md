# QuestVault

A Python-based GUI application for scraping, managing, and searching video game item data from wiki-style websites. Built with Kivy for a modern, responsive interface and featuring robust caching, theming, and error handling systems.

## Features

### Core Functionality
- **Advanced Web Scraping**
  - Multi-domain support with retry mechanisms
  - Rate-limiting and respectful crawling
  - Support for both static and dynamic content

### User Interface
- **Modern Kivy-based GUI**
  - Responsive design with custom theming
  - Fallback system for graceful degradation
  - Real-time progress feedback
  - Customizable color schemes

### Data Management
- **SQLite Database Integration**
  - Concurrent operation support
  - Dynamic database switching
  - Efficient search and filtering

### Performance
- **Smart Caching System**
  - Background image caching
  - Automatic cache cleanup
  - Size and age-based cache management

### Development Features
- **Comprehensive Logging**
  - Color-coded debug output
  - Rotating file logs
  - Structured logging format

## Installation

### Prerequisites
- Python 3.8 or higher
- Git (for cloning)

### Setup
1. Clone the repository:
```bash
git clone https://github.com/yourusername/questvault.git
cd questvault
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Starting the Application
```bash
python main_gui.py
```

### Basic Operations
1. **Adding Domains**
   - Enter the wiki URL in the input field
   - Click "Add Domain" to register

2. **Managing Data**
   - Use "Select Database" to choose storage location
   - Click "Start Scraping" to begin data collection
   - Search using the keyword field

### Configuration
- Theme customization via `resources/theme.json`
- Cache settings in `core/cache_manager.py`
- Logging configuration in `core/logger.py`

## Project Structure
```
questvault/
├── core/                  # Core application logic
│   ├── cache_manager.py   # Caching system
│   ├── database/         # Database operations
│   ├── ui/              # UI components and theme
│   └── logger.py        # Logging system
├── resources/            # Static resources
│   ├── fonts/           # Application fonts
│   ├── icons/           # UI icons
│   └── theme.json       # Theme configuration
├── cache/               # Cached resources
├── test/                # Test suite
└── main_gui.py         # Application entry point
```

## Development

### Running Tests
```bash
pytest test/
```

### Code Style
- Black for formatting
- Pylint for linting
- MyPy for type checking

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

See `CONTRIBUTING.md` for detailed guidelines.

## Testing Coverage
- Unit tests for core functionality
- Integration tests for database operations
- GUI tests using pytest-kivy
- Performance testing for cache system

## Roadmap
See `to_do_list.md` for detailed development plans, including:
- Multi-threaded scraping
- Cloud database integration
- Mobile platform support
- Enhanced search capabilities

## License
This project is licensed under the MIT License - see LICENSE file for details.

## Acknowledgments
- Kivy team for the GUI framework
- BeautifulSoup maintainers
- SQLite developers
- Open-source community

## Support
- Report issues via GitHub Issues
- Join discussions in GitHub Discussions
- Contact maintainers for security concerns

---

*For detailed documentation, visit our [Wiki](https://github.com/username/questvault/wiki)*