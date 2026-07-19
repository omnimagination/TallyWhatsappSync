"""
WhatsApp Utilities for TallySync

Phone number validation and formatting.

Author: OmniMagination
Version: 1.0.0
"""

import re
from typing import Optional, Tuple


class WhatsAppUtils:
    """
    Utility functions for WhatsApp operations.
    """
    
    @staticmethod
    def validate_phone(phone: str) -> Tuple[bool, str]:
        """
        Validate phone number for WhatsApp.
        
        Args:
            phone: Phone number string
        
        Returns:
            Tuple of (is_valid, message)
        """
        if not phone:
            return False, "Phone number is required"
        
        # Remove all non-digit characters
        cleaned = re.sub(r"\D", "", phone)
        
        # Check length
        if len(cleaned) < 10:
            return False, "Phone number too short (minimum 10 digits)"
        
        if len(cleaned) > 15:
            return False, "Phone number too long (maximum 15 digits)"
        
        # Check for Indian numbers
        if len(cleaned) == 10:
            # Add India country code
            if cleaned[0] in "6789":
                return True, "Valid Indian number"
            else:
                return False, "Invalid Indian number (must start with 6-9)"
        
        if len(cleaned) == 12:
            # With country code
            if cleaned.startswith("91"):
                if cleaned[2] in "6789":
                    return True, "Valid Indian number with country code"
                else:
                    return False, "Invalid Indian number (must start with 6-9)"
            else:
                return True, "Valid international number"
        
        if len(cleaned) == 13:
            # With + and country code
            if cleaned.startswith("91"):
                return True, "Valid number"
        
        return True, "Valid international number"
    
    @staticmethod
    def format_phone(phone: str) -> str:
        """
        Format phone number for WhatsApp Web URL.
        
        Args:
            phone: Phone number string
        
        Returns:
            Formatted phone number (e.g., "919876543210")
        """
        # Remove all non-digit characters
        cleaned = re.sub(r"\D", "", phone)
        
        # Remove leading zeros
        cleaned = cleaned.lstrip("0")
        
        # Add India country code if missing
        if len(cleaned) == 10:
            cleaned = "91" + cleaned
        
        # Remove leading + if present
        cleaned = cleaned.lstrip("+")
        
        return cleaned
    
    @staticmethod
    def format_phone_display(phone: str) -> str:
        """
        Format phone number for display.
        
        Args:
            phone: Phone number string
        
        Returns:
            Formatted display number (e.g., "+91 98765 43210")
        """
        cleaned = re.sub(r"\D", "", phone)
        
        if len(cleaned) == 10:
            return f"+91 {cleaned[:5]} {cleaned[5:]}"
        
        if len(cleaned) == 12 and cleaned.startswith("91"):
            return f"+91 {cleaned[2:7]} {cleaned[7:]}"
        
        if len(cleaned) >= 10:
            return f"+{cleaned[:-10]} {cleaned[-10:-5]} {cleaned[-5:]}"
        
        return phone
    
    @staticmethod
    def get_whatsapp_web_url(phone: str, message: str = "") -> str:
        """
        Generate WhatsApp Web URL with pre-filled message.
        
        Args:
            phone: Phone number
            message: Pre-filled message
        
        Returns:
            WhatsApp Web URL
        """
        import urllib.parse
        
        formatted_phone = WhatsAppUtils.format_phone(phone)
        
        base_url = f"https://wa.me/{formatted_phone}"
        
        if message:
            encoded_message = urllib.parse.quote(message)
            return f"{base_url}?text={encoded_message}"
        
        return base_url
    
    @staticmethod
    def open_whatsapp_web(phone: str, message: str = "") -> bool:
        """
        Open WhatsApp Web with phone number and message.
        
        Args:
            phone: Phone number
            message: Pre-filled message
        
        Returns:
            True if opened successfully
        """
        import webbrowser
        
        try:
            url = WhatsAppUtils.get_whatsapp_web_url(phone, message)
            webbrowser.open(url, new=2)
            return True
        except Exception as e:
            return False
    
    @staticmethod
    def is_business_number(phone: str) -> bool:
        """
        Check if number might be a business (based on pattern).
        
        Args:
            phone: Phone number
        
        Returns:
            True if likely business number
        """
        cleaned = re.sub(r"\D", "", phone)
        
        # Business numbers often have repeating patterns
        if len(cleaned) >= 10:
            last_five = cleaned[-5:]
            if last_five.isdigit() and int(last_five) < 10000:
                return True
        
        return False
    
    @staticmethod
    def get_country_code(phone: str) -> str:
        """
        Extract country code from phone number.
        
        Args:
            phone: Phone number
        
        Returns:
            Country code (e.g., "91" for India)
        """
        cleaned = re.sub(r"\D", "", phone)
        
        if cleaned.startswith("91"):
            return "91"
        
        if cleaned.startswith("1"):
            return "1"
        
        if cleaned.startswith("44"):
            return "44"
        
        return "Unknown"
