"""Logging configuration for the application."""
import logging
import sys
from pathlib import Path
from typing import Optional

def setup_logger(
    name: str,
    log_file: Optional[str] = None,
    level: int = logging.INFO,
    format_string: Optional[str] = None
) -> logging.Logger:
    """Set up a logger with console and optional file handlers.
    
    Args:
        name: Name of the logger
        log_file: Optional path to log file
        level: Logging level
        format_string: Optional custom format string
    
    Returns:
        logging.Logger: Configured logger instance
    """
    if format_string is None:
        format_string = "[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s"
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Create formatters and handlers
    formatter = logging.Formatter(format_string)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (optional)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

# Create default application logger
app_logger = setup_logger(
    "college_mobility",
    log_file="logs/app.log"
)
