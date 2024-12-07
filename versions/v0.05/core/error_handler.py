class ErrorHandler:
    """Centralized error handling"""
    @staticmethod
    def handle_error(error_type, error, context=None):
        handlers = {
            'file': lambda e: f"File operation failed: {e}",
            'network': lambda e: f"Network error: {e}",
            'database': lambda e: f"Database error: {e}"
        }
        return handlers.get(error_type, lambda e: f"Unknown error: {e}")(error) 