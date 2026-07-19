"""
Base Model for TallySync Database

Provides common functionality for all model classes.

Author: OmniMagination
Version: 1.0.0
"""

from typing import Optional, Any, TypeVar, Type
from datetime import datetime

T = TypeVar("T", bound="BaseModel")


class BaseModel:
    """
    Base class for all database models.
    
    Provides:
    - Dictionary conversion
    - Attribute access
    - Comparison methods
    - String representation
    """
    
    table_name: str = ""
    primary_key: str = "id"
    
    def __init__(self, **kwargs: Any) -> None:
        """Initialize model with keyword arguments."""
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    @classmethod
    def from_row(cls: Type[T], row: Any) -> T:
        """
        Create model instance from database row.
        
        Args:
            row: sqlite3.Row or dict
        
        Returns:
            Model instance
        """
        if row is None:
            raise ValueError("Cannot create model from None row")
        
        data = dict(row) if not isinstance(row, dict) else row
        return cls(**data)
    
    @classmethod
    def from_list(cls: Type[T], rows: list) -> list[T]:
        """
        Create list of model instances from database rows.
        
        Args:
            rows: List of sqlite3.Row or dict
        
        Returns:
            List of model instances
        """
        return [cls.from_row(row) for row in rows]
    
    def to_dict(self) -> dict:
        """
        Convert model to dictionary.
        
        Returns:
            Dictionary representation
        """
        return {
            key: value
            for key, value in self.__dict__.items()
            if not key.startswith("_")
        }
    
    def to_json(self) -> str:
        """
        Convert model to JSON string.
        
        Returns:
            JSON string
        """
        import json
        return json.dumps(self.to_dict(), default=str, indent=2)
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get attribute value safely.
        
        Args:
            key: Attribute name
            default: Default value if not found
        
        Returns:
            Attribute value or default
        """
        return getattr(self, key, default)
    
    def set(self, key: str, value: Any) -> None:
        """
        Set attribute value.
        
        Args:
            key: Attribute name
            value: Value to set
        """
        setattr(self, key, value)
    
    def update(self, **kwargs: Any) -> None:
        """
        Update multiple attributes.
        
        Args:
            **kwargs: Attributes to update
        """
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def __repr__(self) -> str:
        """String representation for debugging."""
        class_name = self.__class__.__name__
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items() if not k.startswith("_"))
        return f"{class_name}({attrs})"
    
    def __str__(self) -> str:
        """String representation for display."""
        return self.__repr__()
    
    def __eq__(self, other: Any) -> bool:
        """Check equality with another model."""
        if not isinstance(other, BaseModel):
            return False
        
        # Compare by primary key if both have it
        if hasattr(self, self.primary_key) and hasattr(other, self.primary_key):
            return getattr(self, self.primary_key) == getattr(other, self.primary_key)
        
        # Otherwise compare all attributes
        return self.to_dict() == other.to_dict()
    
    def __hash__(self) -> int:
        """Hash based on primary key."""
        if hasattr(self, self.primary_key):
            return hash(getattr(self, self.primary_key))
        return hash(id(self))
    
    def is_new(self) -> bool:
        """Check if model is new (not saved to database)."""
        return getattr(self, self.primary_key, None) is None
    
    def get_created_at(self) -> Optional[datetime]:
        """Get creation timestamp."""
        created_at = getattr(self, "created_at", None)
        if created_at:
            try:
                return datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
            except (ValueError, TypeError):
                return None
        return None
    
    def get_updated_at(self) -> Optional[datetime]:
        """Get last update timestamp."""
        updated_at = getattr(self, "updated_at", None)
        if updated_at:
            try:
                return datetime.strptime(updated_at, "%Y-%m-%d %H:%M:%S")
            except (ValueError, TypeError):
                return None
        return None
