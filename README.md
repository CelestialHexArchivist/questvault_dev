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


# QuestVault Development Tasks

Current Closed Development Focus: Rebuilding the application with consolidated app packages for efficiency and reduced redundancy. Test themes will be implemented first with DB and other functionality having "higher priority". User modified themes will be implemented in later development cycles. The focus is currently on MVP.

## High Priority Tasks

### 1. Core System Improvements
- [ ] Fix theme repair system in `core/ui/theme.py`
  - Implement proper theme validation
  - Add theme backup/restore functionality
- [ ] Complete the `add_url` callback in `main_gui.py`
- [ ] Implement status label updates throughout the application
- [ ] Add proper error handling for database operations

### 2. GUI Enhancements
- [ ] Add missing UI components from design:
- [ ] Implement proper layout management for responsive design
- [ ] Add proper scrolling support for search results
- [ ] Create proper status feedback system

### 3. Cache System
- [ ] Complete cache cleanup implementation in `core/cache_manager.py`
- [ ] Add cache size monitoring
- [ ] Implement cache invalidation strategy
- [ ] Add error handling for cache operations

## Medium Priority Tasks

### 4. Database Management
- [ ] Add database migration system
- [ ] Implement proper concurrent operation handling
- [ ] Add database backup functionality
- [ ] Create database verification system

### 5. Testing
- [ ] Add tests for theme system
- [ ] Create GUI component tests
- [ ] Add cache system tests
- [ ] Implement database operation tests

### 6. Documentation
- [ ] Document theme customization process
- [ ] Add inline documentation for UI components
- [ ] Create developer setup guide
- [ ] Document testing procedures

## Low Priority Tasks

### 7. Performance Optimization
- [ ] Optimize image caching system
- [ ] Implement lazy loading for search results
- [ ] Add background processing for heavy operations
- [ ] Optimize database queries

### 8. User Experience
- [ ] Add loading indicators
- [ ] Implement proper error messages
- [ ] Create user preferences system
- [ ] Add keyboard shortcuts

### 9. Features
- [ ] Add export functionality for search results
- [ ] Implement advanced search filters
- [ ] Add batch operations for domains
- [ ] Create data visualization features

## Future Considerations

### 10. Advanced Features
- [ ] Multi-threaded scraping support
- [ ] Cloud sync capabilities
- [ ] Plugin system for custom scrapers
- [ ] Mobile platform support

### 11. Infrastructure
- [ ] Set up CI/CD pipeline
- [ ] Add automated deployment
- [ ] Create update mechanism
- [ ] Implement telemetry system

### 12. Security
- [ ] Add input validation
- [ ] Implement rate limiting
- [ ] Add secure storage for sensitive data
- [ ] Create access control system

## Notes
- Priority levels may change based on user feedback
- Tasks should be updated as implementation progresses
- New tasks should be added as needed
- Consider dependencies between tasks when planning implementation

## Task Labels
- 🔴 Critical
- 🟡 Important
- 🟢 Normal
- ⚪ Optional

## Progress Tracking
- Create issue for each task
- Link PRs to issues
- Update documentation as features are completed
- Regular progress reviews

---

*Last Updated: 12/06/2024*


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
   - Click "Show Domains" to list all registered domains
   - Click "Start Scraping" to begin data collection or
   - Click "Select Domains to Scrape" to open a tree view and selectively scrape to each domains' database

2. **Managing Data**
   - Use "Select Database" to choose the "Game" or associated domain
   - Search using the keyword field by name or tag

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
