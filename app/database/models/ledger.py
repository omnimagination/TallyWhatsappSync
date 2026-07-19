"""
Ledger Model for TallySync

Represents a Tally ledger account.

Author: OmniMagination
Version: 1.0.0
"""

from typing import Optional
from app.database.models.base import BaseModel
from app.core.utils import format_currency


class Ledger(BaseModel):
    """
    Ledger model representing a Tally ledger account.
    
    Attributes:
        id: Database ID
        ledger_id: Unique Tally ledger ID
        company_id: Parent company ID
        name: Ledger name
        parent: Parent ledger
        group_name: Ledger group
        ledger_type: Type (Sundry Debtor, Sundry Creditor, etc.)
        opening_balance: Opening balance amount
        closing_balance: Current closing balance
        balance_type: Dr or Cr
        phone: Contact phone
        email: Contact email
        address: Address
        gst_number: GST number
        pan_number: PAN number
        contact_person: Contact person name
        credit_limit: Credit limit amount
        credit_days: Credit period in days
        is_active: Active status
    """
    
    table_name = "ledgers"
    primary_key = "id"
    
    def __init__(
        self,
        id: Optional[int] = None,
        ledger_id: str = "",
        company_id: str = "",
        name: str = "",
        parent: str = "",
        group_name: str = "",
        ledger_type: str = "",
        opening_balance: float = 0.0,
        closing_balance: float = 0.0,
        balance_type: str = "Dr",
        phone: str = "",
        email: str = "",
        address: str = "",
        gst_number: str = "",
        pan_number: str = "",
        contact_person: str = "",
        credit_limit: float = 0.0,
        credit_days: int = 0,
        is_active: int = 1,
        last_sync_date: str = "",
        created_at: str = "",
        updated_at: str = "",
        **kwargs,
    ) -> None:
        super().__init__(
            id=id,
            ledger_id=ledger_id,
            company_id=company_id,
            name=name,
            parent=parent,
            group_name=group_name,
            ledger_type=ledger_type,
            opening_balance=opening_balance,
            closing_balance=closing_balance,
            balance_type=balance_type,
            phone=phone,
            email=email,
            address=address,
            gst_number=gst_number,
            pan_number=pan_number,
            contact_person=contact_person,
            credit_limit=credit_limit,
            credit_days=credit_days,
            is_active=is_active,
            last_sync_date=last_sync_date,
            created_at=created_at,
            updated_at=updated_at,
            **kwargs,
        )
    
    @property
    def full_name(self) -> str:
        """Get ledger full name."""
        return self.name or "Unknown Ledger"
    
    @property
    def is_active_bool(self) -> bool:
        """Check if ledger is active."""
        return bool(self.is_active)
    
    @property
    def is_debtor(self) -> bool:
        """Check if ledger is a debtor (Sundry Debtor)."""
        return self.group_name and "Sundry Debtor" in self.group_name
    
    @property
    def is_creditor(self) -> bool:
        """Check if ledger is a creditor (Sundry Creditor)."""
        return self.group_name and "Sundry Creditor" in self.group_name
    
    @property
    def formatted_opening_balance(self) -> str:
        """Get formatted opening balance."""
        return format_currency(self.opening_balance)
    
    @property
    def formatted_closing_balance(self) -> str:
        """Get formatted closing balance."""
        return format_currency(self.closing_balance)
    
    @property
    def balance_with_sign(self) -> str:
        """Get balance with Dr/Cr suffix."""
        if self.closing_balance == 0:
            return "?0.00"
        return f"{format_currency(abs(self.closing_balance))} {self.balance_type}"
    
    @property
    def has_contact(self) -> bool:
        """Check if ledger has contact information."""
        return bool(self.phone or self.email)
    
    @property
    def has_gst(self) -> bool:
        """Check if ledger has GST number."""
        return bool(self.gst_number)
    
    def to_dict(self) -> dict:
        """Convert to dictionary with computed properties."""
        data = super().to_dict()
        data["full_name"] = self.full_name
        data["is_active_bool"] = self.is_active_bool
        data["is_debtor"] = self.is_debtor
        data["is_creditor"] = self.is_creditor
        data["formatted_opening_balance"] = self.formatted_opening_balance
        data["formatted_closing_balance"] = self.formatted_closing_balance
        data["balance_with_sign"] = self.balance_with_sign
        data["has_contact"] = self.has_contact
        data["has_gst"] = self.has_gst
        return data
