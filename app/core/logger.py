"""
Logging System for TallySync

Provides comprehensive logging with:
- Multiple log levels
- File and console handlers
- Colored console output
- Rotating file handlers
- Category-based logging

Author: OmniMagination
Version: 1.0.0
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional
from logging.handlers import RotatingFileHandler

import colorlog

from app.core.config import ConfigManager, config
from app.core.utils import get_app_path


class Logger:
    """
    Centralized logging system for TallySync application.
    
    Features:
    - Multiple log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    - File logging with rotation
    - Console logging with colors
    - Category-based loggers
    - Formatted log messages
    """
    
    _instance: Optional["Logger"] = None
    _loggers: dict = {}
    _initialized: bool = False
    
    def __new__(cls) -> "Logger":
        """Singleton pattern."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self) -> None:
        """Initialize logging system."""
        if Logger._initialized:
            return
        
        self.config = config
        self._setup_logging()
        Logger._initialized = True
    
    def _setup_logging(self) -> None:
        """Configure logging handlers and formatters."""
        # Get configuration
        enabled = self.config.get("logging", "enabled", default=True)
        if not enabled:
            return
        
        level = self.config.get("logging", "level", default="INFO")
        log_level = getattr(logging, level.upper(), logging.INFO)
        
        log_folder = self.config.get_log_folder()
        log_folder.mkdir(parents=True, exist_ok=True)
        
        max_size = self.config.get("logging", "max_file_size", default=10485760)
        backup_count = self.config.get("logging", "backup_count", default=5)
        console_output = self.config.get("logging", "console_output", default=True)
        colored_output = self.config.get("logging", "colored_output", default=True)
        
        # Create formatters
        file_formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)-20s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        
        console_formatter = colorlog.ColoredFormatter(
            fmt="%(log_color)s%(asctime)s | %(levelname)-8s | %(name)-20s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            },
        )
        
        # Create root logger
        self.root_logger = logging.getLogger("TallySync")
        self.root_logger.setLevel(log_level)
        
        # Clear existing handlers
        self.root_logger.handlers.clear()
        
        # File handler
        log_file = log_folder / "tallysync.log"
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=max_size,
            backupCount=backup_count,
            encoding="utf-8",
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(file_formatter)
        self.root_logger.addHandler(file_handler)
        
        # Console handler
        if console_output:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(log_level)
            
            if colored_output:
                console_handler.setFormatter(console_formatter)
            else:
                console_handler.setFormatter(file_formatter)
            
            self.root_logger.addHandler(console_handler)
        
        # Create category-specific loggers
        self._create_category_loggers(log_level, file_formatter, console_formatter)
    
    def _create_category_loggers(
        self,
        log_level: int,
        file_formatter: logging.Formatter,
        console_formatter: logging.Formatter,
    ) -> None:
        """Create loggers for different application categories."""
        categories = [
            ("database", "logging", "log_database"),
            ("sync", "logging", "log_sync"),
            ("xml", "logging", "log_xml"),
            ("pdf", "logging", "log_pdf"),
            ("whatsapp", "logging", "log_whatsapp"),
            ("ui", "logging", "log_ui"),
        ]
        
        for name, section, config_key in categories:
            enabled = self.config.get(section, config_key, default=True)
            
            logger = logging.getLogger(f"TallySync.{name}")
            logger.setLevel(log_level)
            logger.handlers.clear()
            
            if enabled:
                # Add handlers
                for handler in self.root_logger.handlers:
                    logger.addHandler(handler)
            
            self._loggers[name] = logger
    
    def get_logger(self, category: str = "app") -> logging.Logger:
        """
        Get logger for specific category.
        
        Args:
            category: Logger category (app, database, sync, xml, pdf, whatsapp, ui)
        
        Returns:
            Configured logger instance
        """
        if category in self._loggers:
            return self._loggers[category]
        
        # Return root logger for unknown categories
        return self.root_logger
    
    def debug(self, message: str, category: str = "app") -> None:
        """Log debug message."""
        self.get_logger(category).debug(message)
    
    def info(self, message: str, category: str = "app") -> None:
        """Log info message."""
        self.get_logger(category).info(message)
    
    def warning(self, message: str, category: str = "app") -> None:
        """Log warning message."""
        self.get_logger(category).warning(message)
    
    def error(self, message: str, category: str = "app", exc_info: bool = False) -> None:
        """Log error message."""
        self.get_logger(category).error(message, exc_info=exc_info)
    
    def critical(self, message: str, category: str = "app", exc_info: bool = False) -> None:
        """Log critical message."""
        self.get_logger(category).critical(message, exc_info=exc_info)
    
    def exception(self, message: str, category: str = "app") -> None:
        """Log exception with traceback."""
        self.get_logger(category).exception(message)
    
    def log_sync_start(self, sync_type: str) -> None:
        """Log sync operation start."""
        self.info(f"Sync started: {sync_type}", category="sync")
    
    def log_sync_complete(self, sync_type: str, records: int = 0) -> None:
        """Log sync operation completion."""
        self.info(f"Sync completed: {sync_type} - {records} records processed", category="sync")
    
    def log_sync_error(self, sync_type: str, error: str) -> None:
        """Log sync operation error."""
        self.error(f"Sync error: {sync_type} - {error}", category="sync")
    
    def log_database_operation(self, operation: str, table: str) -> None:
        """Log database operation."""
        self.debug(f"Database {operation} on {table}", category="database")
    
    def log_xml_request(self, url: str, method: str) -> None:
        """Log XML request to Tally."""
        self.debug(f"XML {method} request to {url}", category="xml")
    
    def log_xml_response(self, url: str, status: int, size: int) -> None:
        """Log XML response from Tally."""
        self.debug(f"XML response from {url} - Status: {status}, Size: {size} bytes", category="xml")
    
    def log_pdf_generated(self, filename: str, path: str) -> None:
        """Log PDF generation."""
        self.info(f"PDF generated: {filename} at {path}", category="pdf")
    
    def log_whatsapp_sent(self, recipient: str, filename: str) -> None:
        """Log WhatsApp message sent."""
        self.info(f"WhatsApp sent to {recipient}: {filename}", category="whatsapp")
    
    def get_log_file_path(self) -> Path:
        """Get path to main log file."""
        log_folder = self.config.get_log_folder()
        return log_folder / "tallysync.log"
    
    def get_recent_logs(self, lines: int = 100) -> list[str]:
        """Get recent log entries."""
        log_file = self.get_log_file_path()
        if not log_file.exists():
            return []
        
        try:
            with open(log_file, "r", encoding="utf-8") as f:
                all_lines = f.readlines()
                return all_lines[-lines:]
        except Exception:
            return []
    
    def clear_logs(self) -> bool:
        """Clear all log files."""
        try:
            log_folder = self.config.get_log_folder()
            for log_file in log_folder.glob("*.log"):
                log_file.unlink()
            self.info("Logs cleared", category="app")
            return True
        except Exception as e:
            self.error(f"Failed to clear logs: {e}", category="app")
            return False
    
    def __repr__(self) -> str:
        return f"Logger(level={self.root_logger.level})"


# Global logger instance
logger = Logger()
