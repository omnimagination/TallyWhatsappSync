"""
Company Model for TallySync

Represents a Tally company with all its metadata.

Author: OmniMagination
Version: 1.0.0
"""

from typing import Optional
from app.database.models.base import BaseModel


class Company(BaseModel):
    """
    Company model representing a TallyPrime company.
    
    Attributes:
        id: Database ID
        company_id: Unique Tally company ID
        name: Company name
        address: Registered address
        phone: Contact phone
        email: Contact email
        gst_number: GST registration number
        pan_number: PAN number
        state: State name
        state_code: State code
        financial_year_from: Financial year start
        financial_year_to: Financial year end
        books_from_date: Books beginning date
        base_currency: Base currency
        is_active: Active status
        last_sync_date: Last synchronization date
    """
    
    table_name = "companies"
    primary_key = "id"
    
    def __init__(
        self,
        id: Optional[int] = None,
        company_id: str = "",
        name: str = "",
        address: str = "",
        phone: str = "",
        email: str = "",
        gst_number: str = "",
        pan_number: str = "",
        state: str = "",
        state_code: str = "",
        financial_year_from: str = "",
        financial_year_to: str = "",
        books_from_date: str = "",
        base_currency: str = "INR",
        is_active: int = 1,
        last_sync_date: str = "",
        created_at: str = "",
        updated_at: str = "",
        **kwargs,
    ) -> None:
        super().__init__(
            id=id,
            company_id=company_id,
            name=name,
            address=address,
            phone=phone,
            email=email,
            gst_number=gst_number,
            pan_number=pan_number,
            state=state,
            state_code=state_code,
            financial_year_from=financial_year_from,
            financial_year_to=financial_year_to,
            books_from_date=books_from_date,
            base_currency=base_currency,
            is_active=is_active,
            last_sync_date=last_sync_date,
            created_at=created_at,
            updated_at=updated_at,
            **kwargs,
        )
    
    @property
    def full_name(self) -> str:
        """Get company full name."""
        return self.name or "Unknown Company"
    
    @property
    def display_name(self) -> str:
        """Get display name with state."""
        if self.state:
            return f"{self.name} ({self.state})"
        return self.name
    
    @property
    def is_active_bool(self) -> bool:
        """Check if company is active."""
        return bool(self.is_active)
    
    @property
    def financial_year(self) -> str:
        """Get financial year as string."""
        if self.financial_year_from and self.financial_year_to:
            return f"{self.financial_year_from} - {self.financial_year_to}"
        return ""
    
    def get_gstin_formatted(self) -> str:
        """Get formatted GST number."""
        if self.gst_number:
            return self.gst_number
        return "Not Available"
    
    def to_dict(self) -> dict:
        """Convert to dictionary with computed properties."""
        data = super().to_dict()
        data["full_name"] = self.full_name
        data["display_name"] = self.display_name
        data["is_active_bool"] = self.is_active_bool
        data["financial_year"] = self.financial_year
        return data
