import logging
import os
from datetime import datetime
from colorama import init, Fore, Style
from logging.handlers import RotatingFileHandler

# Initialize colorama for cross-platform color support
init()

class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors"""
    
    # Custom color palette
    COLORS = {
        'DEBUG': Fore.LIGHTBLUE_EX,      # Light Blue
        'INFO': Fore.MAGENTA,            # Pink
        'WARNING': Fore.LIGHTMAGENTA_EX,  # Purple
        'ERROR': Style.DIM + Fore.WHITE,  # Readable Grey
        'CRITICAL': Fore.RED + Style.BRIGHT  # Keep Critical as bright red for emphasis
    }

    def format(self, record):
        # Add colors only if it's not a file handler
        if hasattr(self, 'is_file_handler') and self.is_file_handler:
            return super().format(record)
        
        # Color the level name and message
        color = self.COLORS.get(record.levelname, '')
        record.levelname = f'{color}{record.levelname}{Style.RESET_ALL}'
        record.msg = f'{color}{record.msg}{Style.RESET_ALL}'
        
        return super().format(record)

def setup_logger(name='questvault', max_bytes=1024*1024, backup_count=5):
    """Configure and return a logger that writes to both console and file"""
    
    # Create logs directory if it doesn't exist
    log_dir = os.path.join('dev', 'dev-debug')
    os.makedirs(log_dir, exist_ok=True)
    
    # Create a unique log file name with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = os.path.join(log_dir, f'questvault_{timestamp}.log')
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Clear any existing handlers
    logger.handlers = []
    
    # Create handlers
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=max_bytes,
        backupCount=backup_count
    )
    console_handler = logging.StreamHandler()
    
    # Set levels
    file_handler.setLevel(logging.DEBUG)
    console_handler.setLevel(logging.INFO)
    
    # Create formatters
    file_formatter = ColoredFormatter(
        '%(asctime)s | %(levelname)-8s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_formatter.is_file_handler = True
    
    console_formatter = ColoredFormatter(
        '%(asctime)s | %(levelname)-8s | %(message)s',
        datefmt='%H:%M:%S'
    )
    
    file_handler.setFormatter(file_formatter)
    console_handler.setFormatter(console_formatter)
    
    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

def log_scraping_status(logger, item_name, success=True):
    """Standardized scraping status logger"""
    if success:
        logger.debug(f"Scraping status: Found item: {item_name}")
    else:
        logger.debug(f"Scraping status: Failed to fetch details for {item_name}")