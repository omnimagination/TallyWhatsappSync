"""
Configuration Manager for TallySync

Handles loading, saving, and accessing application configuration.
Supports YAML config files and environment variables.

Author: OmniMagination
Version: 1.0.0
"""

import os
import yaml
from pathlib import Path
from typing import Any, Optional
from dotenv import load_dotenv

from app.core.exceptions import ConfigurationError
from app.core.utils import get_app_path


class ConfigManager:
    """
    Singleton configuration manager for TallySync application.
    
    Loads configuration from:
    1. Environment variables (.env file)
    2. YAML configuration file (config.yaml)
    3. Default values
    """
    
    _instance: Optional["ConfigManager"] = None
    _config: dict = {}
    _initialized: bool = False
    
    def __new__(cls) -> "ConfigManager":
        """Singleton pattern - ensure only one instance exists."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self) -> None:
        """Initialize configuration manager."""
        if ConfigManager._initialized:
            return
        
        self._config_path: Path = get_app_path() / "config.yaml"
        self._env_path: Path = get_app_path() / ".env"
        self._load_config()
        ConfigManager._initialized = True
    
    def _load_config(self) -> None:
        """Load configuration from all sources."""
        # Load environment variables
        load_dotenv(self._env_path)
        
        # Load YAML configuration
        yaml_config = self._load_yaml_config()
        
        # Merge configurations with defaults
        self._config = self._get_default_config()
        self._merge_config(yaml_config)
        self._merge_env_config()
    
    def _load_yaml_config(self) -> dict:
        """Load configuration from YAML file."""
        if not self._config_path.exists():
            return {}
        
        try:
            with open(self._config_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except yaml.YAMLError as e:
            raise ConfigurationError(f"Invalid YAML configuration: {e}")
        except Exception as e:
            raise ConfigurationError(f"Failed to load config file: {e}")
    
    def _get_default_config(self) -> dict:
        """Return default configuration values."""
        return {
            "app": {
                "name": "TallySync",
                "version": "1.0.0",
                "developer": "OmniMagination",
            },
            "tally": {
                "host": "localhost",
                "port": 9000,
                "protocol": "http",
                "timeout": 30,
                "retry_attempts": 3,
                "retry_delay": 2,
            },
            "database": {
                "path": "data/tallysync.db",
                "backup_enabled": True,
                "backup_interval": 24,
                "backup_retention": 7,
            },
            "sync": {
                "initial_sync_on_startup": False,
                "auto_sync_enabled": False,
                "sync_interval": 1440,
                "sync_schedule": "daily",
                "sync_time": "02:00",
                "sync_company": True,
                "sync_ledgers": True,
                "sync_vouchers": True,
                "sync_inventory": False,
                "sync_reports": False,
                "batch_size": 100,
                "max_concurrent_requests": 5,
            },
            "search": {
                "instant_search": True,
                "search_delay": 300,
                "validate_on_search": True,
                "cache_results": True,
                "max_results": 100,
            },
            "pdf": {
                "output_folder": "exports/pdf",
                "auto_open": True,
                "default_format": "A4",
                "orientation": "portrait",
                "include_logo": True,
                "include_watermark": False,
                "author": "TallySync",
                "creator": "TallySync v1.0.0",
            },
            "whatsapp": {
                "enabled": True,
                "auto_attach": True,
                "default_message": "Please find attached the ledger statement.",
                "open_web": True,
                "close_after_send": False,
            },
            "ui": {
                "theme": "dark",
                "color_scheme": "blue",
                "appearance_mode": "dark",
                "width": 1280,
                "height": 720,
                "min_width": 1024,
                "min_height": 600,
                "resizable": True,
                "sidebar_width": 240,
                "sidebar_collapsed_width": 60,
                "font_family": "Segoe UI",
                "font_size": 13,
                "title_font_size": 20,
            },
            "logging": {
                "enabled": True,
                "level": "INFO",
                "log_folder": "logs",
                "max_file_size": 10485760,
                "backup_count": 5,
                "log_database": True,
                "log_sync": True,
                "log_xml": True,
                "log_pdf": True,
                "log_whatsapp": True,
                "log_ui": False,
                "console_output": True,
                "colored_output": True,
            },
            "folders": {
                "data": "data",
                "exports": "exports",
                "logs": "logs",
                "temp": "temp",
                "backups": "backups",
                "assets": "app/assets",
            },
            "security": {
                "encrypt_database": False,
                "encrypt_config": False,
                "require_password": False,
                "session_timeout": 0,
            },
            "performance": {
                "lazy_load": True,
                "cache_enabled": True,
                "cache_size": 100,
                "preload_data": False,
            },
            "notifications": {
                "enabled": True,
                "show_sync_complete": True,
                "show_errors": True,
                "show_warnings": True,
                "duration": 5000,
                "position": "bottom-right",
            },
            "advanced": {
                "debug_mode": False,
                "developer_mode": False,
                "telemetry_enabled": False,
                "auto_update_check": True,
            },
        }
    
    def _merge_config(self, yaml_config: dict) -> None:
        """Merge YAML configuration with defaults."""
        for key, value in yaml_config.items():
            if key in self._config and isinstance(value, dict):
                self._config[key].update(value)
            else:
                self._config[key] = value
    
    def _merge_env_config(self) -> None:
        """Merge environment variables with configuration."""
        env_mappings = {
            "TALLY_HOST": ("tally", "host"),
            "TALLY_PORT": ("tally", "port"),
            "DATABASE_PATH": ("database", "path"),
            "LOG_LEVEL": ("logging", "level"),
            "THEME": ("ui", "theme"),
            "WINDOW_WIDTH": ("ui", "width"),
            "WINDOW_HEIGHT": ("ui", "height"),
            "ENABLE_WHATSAPP": ("whatsapp", "enabled"),
            "ENABLE_PDF": ("pdf", "auto_open"),
            "ENABLE_AUTO_SYNC": ("sync", "auto_sync_enabled"),
            "DEBUG": ("advanced", "debug_mode"),
        }
        
        for env_var, config_path in env_mappings.items():
            env_value = os.getenv(env_var)
            if env_value is not None:
                section, key = config_path
                if section in self._config:
                    # Convert to appropriate type
                    current_value = self._config[section].get(key)
                    if isinstance(current_value, bool):
                        env_value = env_value.lower() in ("true", "1", "yes")
                    elif isinstance(current_value, int):
                        try:
                            env_value = int(env_value)
                        except ValueError:
                            continue
                    self._config[section][key] = env_value
    
    def get(self, *keys: str, default: Any = None) -> Any:
        """
        Get configuration value by keys.
        
        Example:
            config.get("tally", "host")
            config.get("ui", "theme", default="dark")
        """
        value = self._config
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        return value
    
    def get_section(self, section: str) -> dict:
        """Get entire configuration section."""
        return self._config.get(section, {}).copy()
    
    def set(self, *keys: str, value: Any) -> None:
        """
        Set configuration value by keys.
        
        Example:
            config.set("tally", "host", value="192.168.1.100")
        """
        config = self._config
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        config[keys[-1]] = value
    
    def save(self) -> bool:
        """Save current configuration to YAML file."""
        try:
            with open(self._config_path, "w", encoding="utf-8") as f:
                yaml.dump(self._config, f, default_flow_style=False, sort_keys=False)
            return True
        except Exception as e:
            raise ConfigurationError(f"Failed to save configuration: {e}")
    
    def get_tally_url(self) -> str:
        """Get full Tally XML server URL."""
        host = self.get("tally", "host")
        port = self.get("tally", "port")
        protocol = self.get("tally", "protocol")
        return f"{protocol}://{host}:{port}"
    
    def get_database_path(self) -> Path:
        """Get absolute path to database file."""
        db_path = self.get("database", "path")
        return get_app_path() / db_path
    
    def get_log_folder(self) -> Path:
        """Get absolute path to logs folder."""
        log_folder = self.get("folders", "logs")
        return get_app_path() / log_folder
    
    def get_exports_folder(self) -> Path:
        """Get absolute path to exports folder."""
        exports_folder = self.get("folders", "exports")
        return get_app_path() / exports_folder
    
    def is_debug_mode(self) -> bool:
        """Check if debug mode is enabled."""
        return self.get("advanced", "debug_mode", default=False)
    
    def __repr__(self) -> str:
        return f"ConfigManager(config_path={self._config_path})"


# Global config instance
config = ConfigManager()
