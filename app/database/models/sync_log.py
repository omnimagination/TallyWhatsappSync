"""
Sync Log Model for TallySync

Tracks synchronization operations.

Author: OmniMagination
Version: 1.0.0
"""

from typing import Optional
from datetime import datetime
from app.database.models.base import BaseModel


class SyncLog(BaseModel):
    """
    SyncLog model for tracking synchronization operations.
    
    Attributes:
        id: Database ID
        sync_type: Type of sync (initial, scheduled, manual, etc.)
        status: Status (success, partial, failed)
        records_processed: Number of records processed
        records_failed: Number of records failed
        start_time: Sync start time
        end_time: Sync end time
        error_message: Error message if failed
    """
    
    table_name = "sync_logs"
    primary_key = "id"
    
    def __init__(
        self,
        id: Optional[int] = None,
        sync_type: str = "",
        status: str = "pending",
        records_processed: int = 0,
        records_failed: int = 0,
        start_time: str = "",
        end_time: str = "",
        error_message: str = "",
        created_at: str = "",
        **kwargs,
    ) -> None:
        super().__init__(
            id=id,
            sync_type=sync_type,
            status=status,
            records_processed=records_processed,
            records_failed=records_failed,
            start_time=start_time,
            end_time=end_time,
            error_message=error_message,
            created_at=created_at,
            **kwargs,
        )
    
    @property
    def formatted_start_time(self) -> str:
        """Get formatted start time."""
        if self.start_time:
            try:
                dt = datetime.strptime(self.start_time, "%Y-%m-%d %H:%M:%S")
                return dt.strftime("%d-%m-%Y %H:%M")
            except (ValueError, TypeError):
                return self.start_time
        return ""
    
    @property
    def formatted_end_time(self) -> str:
        """Get formatted end time."""
        if self.end_time:
            try:
                dt = datetime.strptime(self.end_time, "%Y-%m-%d %H:%M:%S")
                return dt.strftime("%d-%m-%Y %H:%M")
            except (ValueError, TypeError):
                return self.end_time
        return ""
    
    @property
    def duration_seconds(self) -> Optional[float]:
        """Get sync duration in seconds."""
        if self.start_time and self.end_time:
            try:
                start = datetime.strptime(self.start_time, "%Y-%m-%d %H:%M:%S")
                end = datetime.strptime(self.end_time, "%Y-%m-%d %H:%M:%S")
                return (end - start).total_seconds()
            except (ValueError, TypeError):
                return None
        return None
    
    @property
    def success_rate(self) -> float:
        """Get success rate percentage."""
        total = self.records_processed + self.records_failed
        if total == 0:
            return 0.0
        return (self.records_processed / total) * 100
    
    @property
    def is_success(self) -> bool:
        """Check if sync was successful."""
        return self.status.lower() in ("success", "completed")
    
    @property
    def is_failed(self) -> bool:
        """Check if sync failed."""
        return self.status.lower() in ("failed", "error")
    
    @property
    def is_partial(self) -> bool:
        """Check if sync was partial."""
        return self.status.lower() in ("partial", "warning")
    
    def to_dict(self) -> dict:
        """Convert to dictionary with computed properties."""
        data = super().to_dict()
        data["formatted_start_time"] = self.formatted_start_time
        data["formatted_end_time"] = self.formatted_end_time
        data["duration_seconds"] = self.duration_seconds
        data["success_rate"] = self.success_rate
        data["is_success"] = self.is_success
        data["is_failed"] = self.is_failed
        data["is_partial"] = self.is_partial
        return data
