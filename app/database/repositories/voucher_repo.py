"""
Voucher Repository for TallySync

Handles all database operations for Voucher model.

Author: OmniMagination
Version: 1.0.0
"""

from typing import Optional, List

from app.database.repositories.base import BaseRepository
from app.database.models.voucher import Voucher, VoucherEntry


class VoucherRepository(BaseRepository[Voucher]):
    """Repository for Voucher model operations."""
    
    model_class = Voucher
    table_name = "vouchers"
    primary_key = "id"
    
    def get_by_company(self, company_id: str) -> List[Voucher]:
        """Get all vouchers for a company."""
        query = """
            SELECT * FROM vouchers 
            WHERE company_id = ? 
            ORDER BY date DESC
        """
        rows = self.db.fetch_all(query, (company_id,))
        return Voucher.from_list(rows)
    
    def get_by_voucher_id(self, voucher_id: str) -> Optional[Voucher]:
        """Get voucher by Tally voucher ID."""
        return self.get_by_field("voucher_id", voucher_id)
    
    def get_by_type(self, company_id: str, voucher_type: str) -> List[Voucher]:
        """Get vouchers by type for a company."""
        query = """
            SELECT * FROM vouchers 
            WHERE company_id = ? AND voucher_type = ?
            ORDER BY date DESC
        """
        rows = self.db.fetch_all(query, (company_id, voucher_type))
        return Voucher.from_list(rows)
    
    def get_by_date_range(
        self,
        company_id: str,
        from_date: str,
        to_date: str,
    ) -> List[Voucher]:
        """Get vouchers within date range."""
        query = """
            SELECT * FROM vouchers 
            WHERE company_id = ? AND date BETWEEN ? AND ?
            ORDER BY date DESC
        """
        rows = self.db.fetch_all(query, (company_id, from_date, to_date))
        return Voucher.from_list(rows)
    
    def get_by_ledger(self, ledger_id: str) -> List[Voucher]:
        """Get all vouchers containing a specific ledger."""
        query = """
            SELECT DISTINCT v.* FROM vouchers v
            INNER JOIN voucher_entries ve ON v.voucher_id = ve.voucher_id
            WHERE ve.ledger_id = ?
            ORDER BY v.date DESC
        """
        rows = self.db.fetch_all(query, (ledger_id,))
        return Voucher.from_list(rows)
    
    def search_vouchers(
        self,
        company_id: str,
        search_term: str,
        limit: int = 100,
    ) -> List[Voucher]:
        """Search vouchers by number or narration."""
        return self.search(
            search_term,
            ["voucher_number", "narration", "reference_number"],
            limit=limit,
        )
    
    def find_by_company(self, company_id: str) -> List[Voucher]:
        """Find all vouchers for a company."""
        return self.get_by_company(company_id)
    
    def get_entries(self, voucher_id: str) -> List[VoucherEntry]:
        """Get all entries for a voucher."""
        query = """
            SELECT * FROM voucher_entries 
            WHERE voucher_id = ?
            ORDER BY id
        """
        rows = self.db.fetch_all(query, (voucher_id,))
        return VoucherEntry.from_list(rows)
    
    def get_entries_by_ledger(self, ledger_id: str) -> List[VoucherEntry]:
        """Get all voucher entries for a ledger."""
        query = """
            SELECT * FROM voucher_entries 
            WHERE ledger_id = ?
            ORDER BY id DESC
        """
        rows = self.db.fetch_all(query, (ledger_id,))
        return VoucherEntry.from_list(rows)
    
    def get_stats(self, company_id: str) -> dict:
        """Get voucher statistics for a company."""
        total = self.get_count()
        
        # This is simplified - in production you'd filter by company_id
        return {
            "total": total,
        }


class VoucherEntryRepository(BaseRepository[VoucherEntry]):
    """Repository for VoucherEntry model operations."""
    
    model_class = VoucherEntry
    table_name = "voucher_entries"
    primary_key = "id"
    
    def find_by_company(self, company_id: str) -> List[VoucherEntry]:
        """Find entries by company (requires join)."""
        query = """
            SELECT ve.* FROM voucher_entries ve
            INNER JOIN vouchers v ON ve.voucher_id = v.voucher_id
            WHERE v.company_id = ?
        """
        rows = self.db.fetch_all(query, (company_id,))
        return VoucherEntry.from_list(rows)
    
    def get_total_by_ledger(self, ledger_id: str) -> dict:
        """Get total debit and credit for a ledger."""
        debit_query = """
            SELECT COALESCE(SUM(amount), 0) as total 
            FROM voucher_entries 
            WHERE ledger_id = ? AND debit_credit = 'Dr'
        """
        credit_query = """
            SELECT COALESCE(SUM(amount), 0) as total 
            FROM voucher_entries 
            WHERE ledger_id = ? AND debit_credit = 'Cr'
        """
        
        debit = self.db.fetch_one(debit_query, (ledger_id,))["total"]
        credit = self.db.fetch_one(credit_query, (ledger_id,))["total"]
        
        return {
            "total_debit": debit,
            "total_credit": credit,
            "balance": debit - credit,
        }
