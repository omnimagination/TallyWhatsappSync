"""
WhatsApp Sender for TallySync

Handles sending messages and PDFs via WhatsApp Web.

Author: OmniMagination
Version: 1.0.0
"""

import os
import webbrowser
import time
from pathlib import Path
from typing import Optional, List
from datetime import datetime

from app.core.config import config
from app.core.logger import logger
from app.core.exceptions import WhatsAppError
from app.whatsapp.contact import Contact
from app.whatsapp.utils import WhatsAppUtils


class WhatsAppSender:
    """
    WhatsApp sender for TallySync.
    
    IMPORTANT: This is user-initiated only.
    - Opens WhatsApp Web in browser
    - User manually attaches PDF
    - User manually sends message
    - No automation of sending
    
    This approach:
    - Complies with WhatsApp ToS
    - Avoids ban risk
    - More reliable than automation
    """
    
    def __init__(self) -> None:
        """Initialize WhatsApp sender."""
        self.default_message = config.get("whatsapp", "default_message")
        self.open_web = config.get("whatsapp", "open_web", default=True)
        self.enabled = config.get("whatsapp", "enabled", default=True)
        
        logger.info("WhatsAppSender initialized", category="whatsapp")
    
    def send_statement(
        self,
        contact: Contact,
        pdf_path: str,
        message: Optional[str] = None,
    ) -> dict:
        """
        Send ledger statement via WhatsApp.
        
        Args:
            contact: Contact to send to
            pdf_path: Path to PDF statement
            message: Custom message (optional)
        
        Returns:
            Result dictionary with status and info
        """
        result = {
            "success": False,
            "contact": contact.name,
            "phone": contact.formatted_phone,
            "pdf": pdf_path,
            "message": "",
            "error": None,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        
        if not self.enabled:
            result["error"] = "WhatsApp is disabled in settings"
            return result
        
        if not contact.has_phone:
            result["error"] = "Contact has no phone number"
            return result
        
        is_valid, msg = WhatsAppUtils.validate_phone(contact.phone)
        if not is_valid:
            result["error"] = f"Invalid phone number: {msg}"
            return result
        
        if not pdf_path or not os.path.exists(pdf_path):
            result["error"] = "PDF file not found"
            return result
        
        try:
            # Use default message if none provided
            if message is None:
                message = contact.get_default_message("statement")
            
            result["message"] = message
            
            # Open WhatsApp Web
            success = self._open_whatsapp(contact.phone, message)
            
            if success:
                result["success"] = True
                result["status"] = "WhatsApp Web opened - Please attach PDF and send"
                logger.log_whatsapp_sent(contact.formatted_phone, os.path.basename(pdf_path))
            else:
                result["error"] = "Failed to open WhatsApp Web"
            
            return result
        
        except Exception as e:
            result["error"] = str(e)
            logger.error(f"WhatsApp send failed: {e}", category="whatsapp", exc_info=True)
            return result
    
    def send_balance_certificate(
        self,
        contact: Contact,
        pdf_path: str,
        message: Optional[str] = None,
    ) -> dict:
        """
        Send balance certificate via WhatsApp.
        
        Args:
            contact: Contact to send to
            pdf_path: Path to PDF certificate
            message: Custom message (optional)
        
        Returns:
            Result dictionary
        """
        if message is None:
            message = contact.get_default_message("balance")
        
        return self.send_statement(contact, pdf_path, message)
    
    def send_payment_reminder(
        self,
        contact: Contact,
        pdf_path: str,
        message: Optional[str] = None,
    ) -> dict:
        """
        Send payment reminder via WhatsApp.
        
        Args:
            contact: Contact to send to
            pdf_path: Path to PDF statement
            message: Custom message (optional)
        
        Returns:
            Result dictionary
        """
        if message is None:
            message = contact.get_default_message("reminder")
        
        return self.send_statement(contact, pdf_path, message)
    
    def _open_whatsapp(self, phone: str, message: str) -> bool:
        """
        Open WhatsApp Web with phone and message.
        
        Args:
            phone: Phone number
            message: Pre-filled message
        
        Returns:
            True if opened successfully
        """
        try:
            url = WhatsAppUtils.get_whatsapp_web_url(phone, message)
            
            # Open in new tab
            webbrowser.open(url, new=2)
            
            logger.info(f"WhatsApp Web opened for {phone}", category="whatsapp")
            return True
        
        except Exception as e:
            logger.error(f"Failed to open WhatsApp Web: {e}", category="whatsapp")
            return False
    
    def open_whatsapp_direct(self, phone: str) -> bool:
        """
        Open WhatsApp Web for a phone number (no message).
        
        Args:
            phone: Phone number
        
        Returns:
            True if opened successfully
        """
        try:
            url = WhatsAppUtils.get_whatsapp_web_url(phone)
            webbrowser.open(url, new=2)
            return True
        except Exception:
            return False
    
    def copy_message_to_clipboard(self, message: str) -> bool:
        """
        Copy message to clipboard for manual paste.
        
        Args:
            message: Message to copy
        
        Returns:
            True if copied successfully
        """
        try:
            import pyperclip
            pyperclip.copy(message)
            return True
        except Exception:
            return False
    
    def get_send_instructions(self) -> List[str]:
        """
        Get instructions for sending via WhatsApp.
        
        Returns:
            List of instruction strings
        """
        return [
            "1. WhatsApp Web will open in your browser",
            "2. The contact and message will be pre-filled",
            "3. Click the attachment icon (??)",
            "4. Select 'Document' and choose the PDF file",
            "5. Review the message and attachment",
            "6. Click Send to deliver",
            "",
            "Note: PDF attachment must be done manually",
            "This ensures compliance with WhatsApp policies",
        ]
    
    def validate_contact(self, contact: Contact) -> dict:
        """
        Validate contact for WhatsApp sending.
        
        Args:
            contact: Contact to validate
        
        Returns:
            Validation result dictionary
        """
        result = {
            "valid": True,
            "warnings": [],
            "errors": [],
        }
        
        # Check phone
        if not contact.has_phone:
            result["valid"] = False
            result["errors"].append("No phone number")
        else:
            is_valid, msg = WhatsAppUtils.validate_phone(contact.phone)
            if not is_valid:
                result["valid"] = False
                result["errors"].append(f"Invalid phone: {msg}")
        
        # Check name
        if not contact.name:
            result["warnings"].append("Contact has no name")
        
        # Check balance
        if contact.balance == 0:
            result["warnings"].append("Balance is zero")
        
        return result
    
    def get_statistics(self) -> dict:
        """
        Get WhatsApp sending statistics.
        
        Returns:
            Statistics dictionary
        """
        # This would query the sync_logs or a dedicated whatsapp_logs table
        # For now, return basic info
        return {
            "enabled": self.enabled,
            "default_message_length": len(self.default_message),
            "status": "Ready",
        }
