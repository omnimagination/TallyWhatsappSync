"""
Ledger Repository for TallySync

Handles all database operations for Ledger model.

Author: OmniMagination
Version: 1.0.0
"""

from typing import Optional, List

from app.database.repositories.base import BaseRepository
from app.database.models.ledger import Ledger


class LedgerRepository(BaseRepository[Ledger]):
    """Repository for Ledger model operations."""
    
    model_class = Ledger
    table_name = "ledgers"
    primary_key = "id"
    
    def get_by_company(self, company_id: str) -> List[Ledger]:
        """Get all ledgers for a company."""
        query = """
            SELECT * FROM ledgers 
            WHERE company_id = ? 
            ORDER BY name
        """
        rows = self.db.fetch_all(query, (company_id,))
        return Ledger.from_list(rows)
    
    def get_by_company_id(self, company_id: str) -> List[Ledger]:
        """Alias for get_by_company."""
        return self.get_by_company(company_id)
    
    def get_by_ledger_id(self, ledger_id: str) -> Optional[Ledger]:
        """Get ledger by Tally ledger ID."""
        return self.get_by_field("ledger_id", ledger_id)
    
    def get_by_name(self, company_id: str, name: str) -> Optional[Ledger]:
        """Get ledger by name within company."""
        query = """
            SELECT * FROM ledgers 
            WHERE company_id = ? AND name = ? 
            LIMIT 1
        """
        row = self.db.fetch_one(query, (company_id, name))
        return Ledger.from_row(row) if row else None
    
    def get_debtors(self, company_id: str) -> List[Ledger]:
        """Get all debtor ledgers for a company."""
        query = """
            SELECT * FROM ledgers 
            WHERE company_id = ? AND group_name LIKE ?
            ORDER BY name
        """
        rows = self.db.fetch_all(query, (company_id, "%Sundry Debtor%"))
        return Ledger.from_list(rows)
    
    def get_creditors(self, company_id: str) -> List[Ledger]:
        """Get all creditor ledgers for a company."""
        query = """
            SELECT * FROM ledgers 
            WHERE company_id = ? AND group_name LIKE ?
            ORDER BY name
        """
        rows = self.db.fetch_all(query, (company_id, "%Sundry Creditor%"))
        return Ledger.from_list(rows)
    
    def search_ledgers(
        self,
        company_id: str,
        search_term: str,
        limit: int = 100,
    ) -> List[Ledger]:
        """Search ledgers by name within company."""
        query = """
            SELECT * FROM ledgers 
            WHERE company_id = ? AND name LIKE ?
            ORDER BY name
            LIMIT ?
        """
        rows = self.db.fetch_all(query, (company_id, f"%{search_term}%", limit))
        return Ledger.from_list(rows)
    
    def update_balance(
        self,
        ledger_id: str,
        closing_balance: float,
        balance_type: str,
    ) -> int:
        """Update ledger balance."""
        return self.update_by_field(
            "ledger_id",
            ledger_id,
            {
                "closing_balance": closing_balance,
                "balance_type": balance_type,
            }
        )
    
    def update_sync_date(self, ledger_id: str, sync_date: str) -> int:
        """Update last sync date for ledger."""
        return self.update_by_field(
            "ledger_id",
            ledger_id,
            {"last_sync_date": sync_date}
        )
    
    def find_by_company(self, company_id: str) -> List[Ledger]:
        """Find all ledgers for a company."""
        return self.get_by_company(company_id)
    
    def get_ledger_groups(self, company_id: str) -> List[str]:
        """Get all unique ledger groups for a company."""
        query = """
            SELECT DISTINCT group_name FROM ledgers 
            WHERE company_id = ? AND group_name != ''
            ORDER BY group_name
        """
        rows = self.db.fetch_all(query, (company_id,))
        return [row["group_name"] for row in rows]
    
    def get_stats(self, company_id: str) -> dict:
        """Get ledger statistics for a company."""
        total = self.db.fetch_column(
            "SELECT COUNT(*) FROM ledgers WHERE company_id = ?",
            (company_id,)
        )[0]
        
        debtors = self.db.fetch_column(
            "SELECT COUNT(*) FROM ledgers WHERE company_id = ? AND group_name LIKE ?",
            (company_id, "%Sundry Debtor%")
        )[0]
        
        creditors = self.db.fetch_column(
            "SELECT COUNT(*) FROM ledgers WHERE company_id = ? AND group_name LIKE ?",
            (company_id, "%Sundry Creditor%")
        )[0]
        
        with_contact = self.db.fetch_column(
            "SELECT COUNT(*) FROM ledgers WHERE company_id = ? AND (phone != '' OR email != '')",
            (company_id,)
        )[0]
        
        return {
            "total": total,
            "debtors": debtors,
            "creditors": creditors,
            "with_contact": with_contact,
        }
