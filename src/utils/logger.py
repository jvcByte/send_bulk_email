"""
Logger utility - handles logging operations.
Responsibility: Log messages to file and console
"""
import datetime
from typing import Optional


class Logger:
    """Simple logger for console and file output."""
    
    def __init__(self, log_file: Optional[str] = None):
        """
        Initialize logger.
        
        Args:
            log_file: Optional path to log file
        """
        self.log_file = log_file
    
    def log(self, message: str, level: str = "INFO"):
        """
        Log a message with timestamp.
        
        Args:
            message: Message to log
            level: Log level (INFO, ERROR, WARNING)
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        
        # Print to console
        print(log_entry)
        
        # Write to file if specified
        if self.log_file:
            with open(self.log_file, 'a') as f:
                f.write(log_entry + '\n')
    
    def info(self, message: str):
        """Log info message."""
        self.log(message, "INFO")
    
    def error(self, message: str):
        """Log error message."""
        self.log(message, "ERROR")
    
    def warning(self, message: str):
        """Log warning message."""
        self.log(message, "WARNING")
    
    def separator(self):
        """Log a separator line."""
        self.log("=" * 60, "")
