"""
Custom Exceptions for TallySync

Provides specific exception classes for different error scenarios
to enable proper error handling and user feedback.

Author: OmniMagination
Version: 1.0.0
"""

from typing import Optional


class TallySyncError(Exception):
    """
    Base exception for all TallySync errors.
    
    All custom exceptions inherit from this class.
    """
    
    def __init__(
        self,
        message: str,
        code: Optional[str] = None,
        details: Optional[dict] = None,
    ) -> None:
        self.message = message
        self.code = code or "UNKNOWN_ERROR"
        self.details = details or {}
        super().__init__(self.message)
    
    def to_dict(self) -> dict:
        """Convert exception to dictionary for serialization."""
        return {
            "error": self.__class__.__name__,
            "code": self.code,
            "message": self.message,
            "details": self.details,
        }
    
    def __str__(self) -> str:
        return f"[{self.code}] {self.message}"


class ConfigurationError(TallySyncError):
    """Raised when configuration is invalid or missing."""
    
    def __init__(self, message: str, config_key: Optional[str] = None) -> None:
        super().__init__(
            message=message,
            code="CONFIG_ERROR",
            details={"config_key": config_key} if config_key else {},
        )


class DatabaseError(TallySyncError):
    """Raised when database operation fails."""
    
    def __init__(
        self,
        message: str,
        operation: Optional[str] = None,
        table: Optional[str] = None,
    ) -> None:
        super().__init__(
            message=message,
            code="DATABASE_ERROR",
            details={
                "operation": operation,
                "table": table,
            },
        )


class SyncError(TallySyncError):
    """Raised when synchronization fails."""
    
    def __init__(
        self,
        message: str,
        sync_type: Optional[str] = None,
        records_processed: int = 0,
    ) -> None:
        super().__init__(
            message=message,
            code="SYNC_ERROR",
            details={
                "sync_type": sync_type,
                "records_processed": records_processed,
            },
        )


class TallyConnectionError(TallySyncError):
    """Raised when connection to Tally fails."""
    
    def __init__(
        self,
        message: str,
        url: Optional[str] = None,
        status_code: Optional[int] = None,
    ) -> None:
        super().__init__(
            message=message,
            code="TALLY_CONNECTION_ERROR",
            details={
                "url": url,
                "status_code": status_code,
            },
        )


class PDFGenerationError(TallySyncError):
    """Raised when PDF generation fails."""
    
    def __init__(
        self,
        message: str,
        filename: Optional[str] = None,
        template: Optional[str] = None,
    ) -> None:
        super().__init__(
            message=message,
            code="PDF_GENERATION_ERROR",
            details={
                "filename": filename,
                "template": template,
            },
        )


class WhatsAppError(TallySyncError):
    """Raised when WhatsApp operation fails."""
    
    def __init__(
        self,
        message: str,
        recipient: Optional[str] = None,
        action: Optional[str] = None,
    ) -> None:
        super().__init__(
            message=message,
            code="WHATSAPP_ERROR",
            details={
                "recipient": recipient,
                "action": action,
            },
        )


class ValidationError(TallySyncError):
    """Raised when data validation fails."""
    
    def __init__(
        self,
        message: str,
        field: Optional[str] = None,
        value: Optional[str] = None,
    ) -> None:
        super().__init__(
            message=message,
            code="VALIDATION_ERROR",
            details={
                "field": field,
                "value": value,
            },
        )


class NotFoundError(TallySyncError):
    """Raised when requested resource is not found."""
    
    def __init__(
        self,
        message: str,
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None,
    ) -> None:
        super().__init__(
            message=message,
            code="NOT_FOUND",
            details={
                "resource_type": resource_type,
                "resource_id": resource_id,
            },
        )


class PermissionError(TallySyncError):
    """Raised when user lacks permission for operation."""
    
    def __init__(
        self,
        message: str,
        operation: Optional[str] = None,
    ) -> None:
        super().__init__(
            message=message,
            code="PERMISSION_DENIED",
            details={
                "operation": operation,
            },
        )


class TimeoutError(TallySyncError):
    """Raised when operation times out."""
    
    def __init__(
        self,
        message: str,
        operation: Optional[str] = None,
        timeout_seconds: Optional[int] = None,
    ) -> None:
        super().__init__(
            message=message,
            code="TIMEOUT_ERROR",
            details={
                "operation": operation,
                "timeout_seconds": timeout_seconds,
            },
        )
