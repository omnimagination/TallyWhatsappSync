"""
Utility Functions for TallySync

Common helper functions used throughout the application.

Author: OmniMagination
Version: 1.0.0
"""

import os
import re
import uuid
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Optional, Any
from decimal import Decimal, ROUND_HALF_UP


def get_app_path() -> Path:
    """
    Get the application root directory path.
    
    Handles both development and packaged (PyInstaller) environments.
    
    Returns:
        Path to application root directory
    """
    if getattr(os, "frozen", False):
        # Running as compiled executable
        return Path(sys.executable).parent
    else:
        # Running as script
        return Path(__file__).parent.parent.parent


def format_currency(
    amount: Any,
    currency: str = "?",
    decimals: int = 2,
    include_symbol: bool = True,
) -> str:
    """
    Format amount as currency string.
    
    Args:
        amount: Amount to format (int, float, Decimal, or string)
        currency: Currency symbol (default: ?)
        decimals: Number of decimal places
        include_symbol: Whether to include currency symbol
    
    Returns:
        Formatted currency string (e.g., "?1,23,456.78")
    """
    try:
        # Convert to Decimal for precision
        if isinstance(amount, str):
            amount = Decimal(amount.replace(",", ""))
        else:
            amount = Decimal(str(amount))
        
        # Round to specified decimals
        quantize_str = "0." + "0" * decimals
        amount = amount.quantize(Decimal(quantize_str), rounding=ROUND_HALF_UP)
        
        # Format with Indian numbering system
        amount_str = f"{amount:,.{decimals}f}"
        
        # Convert to Indian format (lakhs and crores)
        parts = amount_str.split(".")
        integer_part = parts[0]
        decimal_part = parts[1] if len(parts) > 1 else ""
        
        # Remove commas and reformat
        integer_part = integer_part.replace(",", "")
        
        if len(integer_part) > 3:
            last_three = integer_part[-3:]
            remaining = integer_part[:-3]
            
            # Add commas in Indian format
            formatted_remaining = ""
            for i, digit in enumerate(reversed(remaining)):
                if i > 0 and i % 2 == 0:
                    formatted_remaining = "," + formatted_remaining
                formatted_remaining = digit + formatted_remaining
            
            integer_part = formatted_remaining + "," + last_three
        
        if decimal_part:
            result = f"{integer_part}.{decimal_part}"
        else:
            result = integer_part
        
        if include_symbol:
            result = f"{currency}{result}"
        
        return result
    
    except Exception:
        return str(amount)


def format_date(
    date_value: Any,
    format_str: str = "%d-%m-%Y",
    default: str = "",
) -> str:
    """
    Format date value to string.
    
    Args:
        date_value: Date to format (datetime, date, string, or int)
        format_str: Output format string
        default: Default value if formatting fails
    
    Returns:
        Formatted date string
    """
    try:
        if date_value is None:
            return default
        
        if isinstance(date_value, (datetime,)):
            return date_value.strftime(format_str)
        
        if isinstance(date_value, str):
            # Try parsing common date formats
            for fmt in ["%Y-%m-%d", "%d-%m-%Y", "%Y%m%d", "%d/%m/%Y"]:
                try:
                    parsed = datetime.strptime(date_value, fmt)
                    return parsed.strftime(format_str)
                except ValueError:
                    continue
        
        if isinstance(date_value, int):
            # Assume Unix timestamp or YYYYMMDD
            if date_value > 1000000000:
                # Unix timestamp
                return datetime.fromtimestamp(date_value).strftime(format_str)
            else:
                # YYYYMMDD format
                return datetime.strptime(str(date_value), "%Y%m%d").strftime(format_str)
        
        return str(date_value)
    
    except Exception:
        return default


def format_datetime(
    datetime_value: Any,
    format_str: str = "%d-%m-%Y %H:%M:%S",
    default: str = "",
) -> str:
    """
    Format datetime value to string.
    
    Args:
        datetime_value: Datetime to format
        format_str: Output format string
        default: Default value if formatting fails
    
    Returns:
        Formatted datetime string
    """
    try:
        if datetime_value is None:
            return default
        
        if isinstance(datetime_value, (datetime,)):
            return datetime_value.strftime(format_str)
        
        if isinstance(datetime_value, str):
            for fmt in ["%Y-%m-%d %H:%M:%S", "%d-%m-%Y %H:%M:%S", "%Y-%m-%dT%H:%M:%S"]:
                try:
                    parsed = datetime.strptime(datetime_value, fmt)
                    return parsed.strftime(format_str)
                except ValueError:
                    continue
        
        return str(datetime_value)
    
    except Exception:
        return default


def sanitize_string(text: str, max_length: int = 255) -> str:
    """
    Sanitize string for safe storage and display.
    
    Args:
        text: Input string to sanitize
        max_length: Maximum length of output string
    
    Returns:
        Sanitized string
    """
    if not text:
        return ""
    
    # Convert to string if not already
    text = str(text)
    
    # Remove null bytes
    text = text.replace("\x00", "")
    
    # Remove control characters except newlines and tabs
    text = "".join(char for char in text if ord(char) >= 32 or char in "\n\t")
    
    # Strip whitespace
    text = text.strip()
    
    # Limit length
    if len(text) > max_length:
        text = text[:max_length]
    
    return text


def generate_id(prefix: str = "") -> str:
    """
    Generate unique identifier.
    
    Args:
        prefix: Optional prefix for the ID
    
    Returns:
        Unique ID string (e.g., "LEDGER_550e8400e29b41d4")
    """
    unique_id = uuid.uuid4().hex[:16]
    if prefix:
        return f"{prefix}_{unique_id}"
    return unique_id


def generate_hash(data: str, algorithm: str = "sha256") -> str:
    """
    Generate hash of string data.
    
    Args:
        data: Input string to hash
        algorithm: Hash algorithm (md5, sha1, sha256, sha512)
    
    Returns:
        Hexadecimal hash string
    """
    hash_func = getattr(hashlib, algorithm, hashlib.sha256)
    return hash_func(data.encode("utf-8")).hexdigest()


def parse_bool(value: Any, default: bool = False) -> bool:
    """
    Parse value to boolean.
    
    Args:
        value: Value to parse
        default: Default value if parsing fails
    
    Returns:
        Boolean value
    """
    if isinstance(value, bool):
        return value
    
    if isinstance(value, str):
        return value.lower() in ("true", "1", "yes", "y", "on")
    
    if isinstance(value, (int, float)):
        return bool(value)
    
    return default


def parse_int(value: Any, default: int = 0) -> int:
    """
    Parse value to integer.
    
    Args:
        value: Value to parse
        default: Default value if parsing fails
    
    Returns:
        Integer value
    """
    try:
        return int(float(str(value)))
    except (ValueError, TypeError):
        return default


def parse_float(value: Any, default: float = 0.0) -> float:
    """
    Parse value to float.
    
    Args:
        value: Value to parse
        default: Default value if parsing fails
    
    Returns:
        Float value
    """
    try:
        return float(str(value))
    except (ValueError, TypeError):
        return default


def ensure_folder_exists(folder_path: Path) -> Path:
    """
    Ensure folder exists, create if necessary.
    
    Args:
        folder_path: Path to folder
    
    Returns:
        Path to folder
    """
    folder_path.mkdir(parents=True, exist_ok=True)
    return folder_path


def get_file_size(file_path: Path) -> int:
    """
    Get file size in bytes.
    
    Args:
        file_path: Path to file
    
    Returns:
        File size in bytes
    """
    if file_path.exists():
        return file_path.stat().st_size
    return 0


def format_file_size(size_bytes: int) -> str:
    """
    Format file size to human-readable string.
    
    Args:
        size_bytes: Size in bytes
    
    Returns:
        Formatted size string (e.g., "1.5 MB")
    """
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"


def is_valid_email(email: str) -> bool:
    """
    Validate email address format.
    
    Args:
        email: Email address to validate
    
    Returns:
        True if valid email format
    """
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def is_valid_phone(phone: str) -> bool:
    """
    Validate phone number format (Indian format).
    
    Args:
        phone: Phone number to validate
    
    Returns:
        True if valid phone format
    """
    # Remove spaces, dashes, and parentheses
    phone = re.sub(r"[\s\-\(\)]", "", phone)
    
    # Check for Indian phone number format
    pattern = r"^(\+91|91|0)?[6-9]\d{9}$"
    return bool(re.match(pattern, phone))


def clean_phone_number(phone: str) -> str:
    """
    Clean phone number to standard format.
    
    Args:
        phone: Phone number string
    
    Returns:
        Cleaned phone number (e.g., "919876543210")
    """
    # Remove all non-digit characters
    phone = re.sub(r"\D", "", phone)
    
    # Remove leading zeros
    phone = phone.lstrip("0")
    
    # Add country code if missing
    if len(phone) == 10:
        phone = "91" + phone
    
    return phone


# Import sys for get_app_path
import sys
