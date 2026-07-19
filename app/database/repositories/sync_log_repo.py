"""
Sync Log Repository for TallySync

Handles all database operations for SyncLog model.

Author: OmniMagination
Version: 1.0.0
"""

from typing import Optional, List
from datetime import datetime

from app.database.repositories.base import BaseRepository
from app.database.models.sync_log import SyncLog


class SyncLogRepository(BaseRepository[SyncLog]):
    """Repository for SyncLog model operations."""
    
    model_class = SyncLog
    table_name = "sync_logs"
    primary_key = "id"
    
    def create_log(
        self,
        sync_type: str,
        start_time: str,
    ) -> int:
        """Create a new sync log entry."""
        return self.create({
            "sync_type": sync_type,
            "status": "pending",
            "start_time": start_time,
        })
    
    def update_log(
        self,
        log_id: int,
        status: str,
        records_processed: int = 0,
        records_failed: int = 0,
        error_message: str = "",
    ) -> int:
        """Update sync log entry."""
        data = {
            "status": status,
            "records_processed": records_processed,
            "records_failed": records_failed,
            "end_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        
        if error_message:
            data["error_message"] = error_message
        
        return self.update(log_id, data)
    
    def get_recent(self, limit: int = 50) -> List[SyncLog]:
        """Get recent sync logs."""
        query = """
            SELECT * FROM sync_logs 
            ORDER BY created_at DESC 
            LIMIT ?
        """
        rows = self.db.fetch_all(query, (limit,))
        return SyncLog.from_list(rows)
    
    def get_by_type(self, sync_type: str, limit: int = 50) -> List[SyncLog]:
        """Get sync logs by type."""
        query = """
            SELECT * FROM sync_logs 
            WHERE sync_type = ?
            ORDER BY created_at DESC 
            LIMIT ?
        """
        rows = self.db.fetch_all(query, (sync_type, limit))
        return SyncLog.from_list(rows)
    
    def get_failed(self, limit: int = 50) -> List[SyncLog]:
        """Get failed sync logs."""
        query = """
            SELECT * FROM sync_logs 
            WHERE status IN ('failed', 'error')
            ORDER BY created_at DESC 
            LIMIT ?
        """
        rows = self.db.fetch_all(query, (limit,))
        return SyncLog.from_list(rows)
    
    def get_stats(self) -> dict:
        """Get sync statistics."""
        total = self.get_count()
        
        success = self.db.fetch_column(
            "SELECT COUNT(*) FROM sync_logs WHERE status = 'success'"
        )[0]
        
        failed = self.db.fetch_column(
            "SELECT COUNT(*) FROM sync_logs WHERE status IN ('failed', 'error')"
        )[0]
        
        return {
            "total": total,
            "success": success,
            "failed": failed,
            "success_rate": (success / total * 100) if total > 0 else 0,
        }
    
    def find_by_company(self, company_id: str) -> List[SyncLog]:
        """Find sync logs (not company-specific, return all)."""
        return self.get_recent(limit=100)
    
    def cleanup_old_logs(self, days: int = 30) -> int:
        """Delete sync logs older than specified days."""
        query = """
            DELETE FROM sync_logs 
            WHERE created_at < datetime('now', ?)
        """
        return self.db.execute(query, (f"-{days} days",)).rowcount
