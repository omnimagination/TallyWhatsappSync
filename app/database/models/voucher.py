"""
Voucher Models for TallySync

Represents Tally vouchers and voucher entries.

Author: OmniMagination
Version: 1.0.0
"""

from typing import Optional, List
from app.database.models.base import BaseModel
from app.core.utils import format_currency, format_date


class Voucher(BaseModel):
    """
    Voucher model representing a Tally voucher/transaction.
    
    Attributes:
        id: Database ID
        voucher_id: Unique Tally voucher ID
        company_id: Parent company ID
        voucher_type: Type (Sales, Purchase, Payment, Receipt, etc.)
        voucher_number: Voucher number
        date: Voucher date
        amount: Total amount
        narration: Voucher narration
        reference_number: Reference number
        reference_date: Reference date
        buyer_details: Buyer details
        shipping_details: Shipping details
        invoice_date: Invoice date
        is_cancelled: Cancelled status
    """
    
    table_name = "vouchers"
    primary_key = "id"
    
    def __init__(
        self,
        id: Optional[int] = None,
        voucher_id: str = "",
        company_id: str = "",
        voucher_type: str = "",
        voucher_number: str = "",
        date: str = "",
        amount: float = 0.0,
        narration: str = "",
        reference_number: str = "",
        reference_date: str = "",
        buyer_details: str = "",
        shipping_details: str = "",
        invoice_date: str = "",
        is_cancelled: int = 0,
        created_at: str = "",
        updated_at: str = "",
        **kwargs,
    ) -> None:
        super().__init__(
            id=id,
            voucher_id=voucher_id,
            company_id=company_id,
            voucher_type=voucher_type,
            voucher_number=voucher_number,
            date=date,
            amount=amount,
            narration=narration,
            reference_number=reference_number,
            reference_date=reference_date,
            buyer_details=buyer_details,
            shipping_details=shipping_details,
            invoice_date=invoice_date,
            is_cancelled=is_cancelled,
            created_at=created_at,
            updated_at=updated_at,
            **kwargs,
        )
    
    @property
    def formatted_date(self) -> str:
        """Get formatted voucher date."""
        return format_date(self.date, "%d-%m-%Y")
    
    @property
    def formatted_amount(self) -> str:
        """Get formatted amount."""
        return format_currency(self.amount)
    
    @property
    def is_cancelled_bool(self) -> bool:
        """Check if voucher is cancelled."""
        return bool(self.is_cancelled)
    
    @property
    def display_number(self) -> str:
        """Get display voucher number."""
        if self.voucher_number:
            return self.voucher_number
        return self.voucher_id
    
    def to_dict(self) -> dict:
        """Convert to dictionary with computed properties."""
        data = super().to_dict()
        data["formatted_date"] = self.formatted_date
        data["formatted_amount"] = self.formatted_amount
        data["is_cancelled_bool"] = self.is_cancelled_bool
        data["display_number"] = self.display_number
        return data


class VoucherEntry(BaseModel):
    """
    Voucher Entry model representing a single entry in a voucher.
    
    Attributes:
        id: Database ID
        voucher_id: Parent voucher ID
        ledger_id: Ledger ID
        amount: Entry amount
        debit_credit: Dr or Cr
        narration: Entry narration
    """
    
    table_name = "voucher_entries"
    primary_key = "id"
    
    def __init__(
        self,
        id: Optional[int] = None,
        voucher_id: str = "",
        ledger_id: str = "",
        amount: float = 0.0,
        debit_credit: str = "Dr",
        narration: str = "",
        created_at: str = "",
        **kwargs,
    ) -> None:
        super().__init__(
            id=id,
            voucher_id=voucher_id,
            ledger_id=ledger_id,
            amount=amount,
            debit_credit=debit_credit,
            narration=narration,
            created_at=created_at,
            **kwargs,
        )
    
    @property
    def formatted_amount(self) -> str:
        """Get formatted amount."""
        return format_currency(self.amount)
    
    @property
    def is_debit(self) -> bool:
        """Check if entry is debit."""
        return self.debit_credit.upper() == "DR"
    
    @property
    def is_credit(self) -> bool:
        """Check if entry is credit."""
        return self.debit_credit.upper() == "CR"
    
    def to_dict(self) -> dict:
        """Convert to dictionary with computed properties."""
        data = super().to_dict()
        data["formatted_amount"] = self.formatted_amount
        data["is_debit"] = self.is_debit
        data["is_credit"] = self.is_credit
        return data
