"""
Contact Model for WhatsApp

Represents a WhatsApp contact with ledger information.

Author: OmniMagination
Version: 1.0.0
"""

from typing import Optional
from app.database.models import Ledger
from app.whatsapp.utils import WhatsAppUtils


class Contact:
    """
    WhatsApp contact with ledger information.
    """
    
    def __init__(
        self,
        ledger: Optional[Ledger] = None,
        name: str = "",
        phone: str = "",
        email: str = "",
        company: str = "",
        balance: float = 0,
        balance_type: str = "Dr",
    ) -> None:
        """Initialize contact from ledger or direct values."""
        if ledger:
            self.ledger_id = ledger.ledger_id
            self.name = ledger.name
            self.phone = ledger.phone or ""
            self.email = ledger.email or ""
            self.company = ""
            self.balance = ledger.closing_balance
            self.balance_type = ledger.balance_type
            self.group = ledger.group_name
            self.gst = ledger.gst_number or ""
        else:
            self.ledger_id = ""
            self.name = name
            self.phone = phone
            self.email = email
            self.company = company
            self.balance = balance
            self.balance_type = balance_type
            self.group = ""
            self.gst = ""
        
        self.formatted_phone = WhatsAppUtils.format_phone_display(self.phone)
        self.international_phone = WhatsAppUtils.format_phone(self.phone)
    
    @property
    def is_valid(self) -> bool:
        """Check if contact has valid phone number."""
        is_valid, _ = WhatsAppUtils.validate_phone(self.phone)
        return is_valid
    
    @property
    def has_phone(self) -> bool:
        """Check if contact has phone number."""
        return bool(self.phone and self.phone.strip())
    
    @property
    def has_email(self) -> bool:
        """Check if contact has email."""
        return bool(self.email and self.email.strip())
    
    @property
    def balance_formatted(self) -> str:
        """Get formatted balance string."""
        from app.core.utils import format_currency
        if self.balance == 0:
            return "?0.00"
        return f"{format_currency(abs(self.balance))} {self.balance_type}"
    
    @property
    def whatsapp_url(self) -> str:
        """Get WhatsApp Web URL for this contact."""
        return WhatsAppUtils.get_whatsapp_web_url(self.phone)
    
    def get_default_message(self, statement_type: str = "statement") -> str:
        """
        Get default message for this contact.
        
        Args:
            statement_type: Type of message (statement, balance, reminder)
        
        Returns:
            Default message string
        """
        from datetime import datetime
        
        messages = {
            "statement": f"""Dear {self.name},

Please find attached your ledger statement as on {datetime.now().strftime('%d-%m-%Y')}.

Outstanding Balance: {self.balance_formatted}

For any queries, please contact us.

Thank you for your business!
""",
            "balance": f"""Dear {self.name},

This is to inform you that your outstanding balance as on {datetime.now().strftime('%d-%m-%Y')} is {self.balance_formatted}.

Please arrange for payment at your earliest convenience.

Thank you!
""",
            "reminder": f"""Dear {self.name},

This is a friendly reminder regarding your outstanding balance of {self.balance_formatted}.

Kindly make the payment at your earliest convenience.

Thank you for your cooperation!
""",
        }
        
        return messages.get(statement_type, messages["statement"])
    
    def to_dict(self) -> dict:
        """Convert contact to dictionary."""
        return {
            "ledger_id": self.ledger_id,
            "name": self.name,
            "phone": self.phone,
            "formatted_phone": self.formatted_phone,
            "international_phone": self.international_phone,
            "email": self.email,
            "company": self.company,
            "balance": self.balance,
            "balance_type": self.balance_type,
            "balance_formatted": self.balance_formatted,
            "is_valid": self.is_valid,
            "has_phone": self.has_phone,
            "has_email": self.has_email,
        }
    
    def __repr__(self) -> str:
        return f"Contact(name={self.name}, phone={self.formatted_phone})"
