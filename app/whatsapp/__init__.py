"""
TallySync WhatsApp Module

WhatsApp Web integration for sending statements.

Author: OmniMagination
Version: 1.0.0
"""

from app.whatsapp.sender import WhatsAppSender
from app.whatsapp.contact import Contact
from app.whatsapp.utils import WhatsAppUtils

__all__ = [
    "WhatsAppSender",
    "Contact",
    "WhatsAppUtils",
]
