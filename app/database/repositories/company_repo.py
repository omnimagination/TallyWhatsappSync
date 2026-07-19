"""
Company Repository for TallySync

Handles all database operations for Company model.

Author: OmniMagination
Version: 1.0.0
"""

from typing import Optional, List

from app.database.repositories.base import BaseRepository
from app.database.models.company import Company


class CompanyRepository(BaseRepository[Company]):
    """Repository for Company model operations."""
    
    model_class = Company
    table_name = "companies"
    primary_key = "id"
    
    def get_active(self) -> List[Company]:
        """Get all active companies."""
        query = "SELECT * FROM companies WHERE is_active = 1 ORDER BY name"
        rows = self.db.fetch_all(query)
        return Company.from_list(rows)
    
    def get_by_name(self, name: str) -> Optional[Company]:
        """Get company by name."""
        return self.get_by_field("name", name)
    
    def get_by_company_id(self, company_id: str) -> Optional[Company]:
        """Get company by Tally company ID."""
        return self.get_by_field("company_id", company_id)
    
    def update_sync_date(self, company_id: str, sync_date: str) -> int:
        """Update last sync date for company."""
        return self.update_by_field(
            "company_id",
            company_id,
            {"last_sync_date": sync_date, "updated_at": sync_date}
        )
    
    def find_by_company(self, company_id: str) -> List[Company]:
        """Find companies by company ID (returns single or empty list)."""
        company = self.get_by_company_id(company_id)
        return [company] if company else []
    
    def search_companies(self, search_term: str) -> List[Company]:
        """Search companies by name."""
        return self.search(search_term, ["name", "address", "email"], limit=50)
    
    def get_stats(self) -> dict:
        """Get company statistics."""
        total = self.get_count()
        active = self.db.fetch_column(
            "SELECT COUNT(*) FROM companies WHERE is_active = 1"
        )[0]
        return {
            "total": total,
            "active": active,
            "inactive": total - active,
        }
