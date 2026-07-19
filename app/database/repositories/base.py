"""
Base Repository for TallySync

Provides common CRUD operations for all repositories.

Author: OmniMagination
Version: 1.0.0
"""

from typing import Optional, List, Type, TypeVar, Generic, Any
from abc import ABC, abstractmethod

from app.database.connection import db
from app.database.models.base import BaseModel

T = TypeVar("T", bound=BaseModel)


class BaseRepository(ABC, Generic[T]):
    """
    Base repository implementing common CRUD operations.
    
    All repositories should inherit from this class.
    """
    
    model_class: Type[T]
    table_name: str
    primary_key: str = "id"
    
    def __init__(self) -> None:
        """Initialize repository with database connection."""
        self.db = db
    
    def get_by_id(self, id: int) -> Optional[T]:
        """
        Get single record by ID.
        
        Args:
            id: Primary key value
        
        Returns:
            Model instance or None
        """
        query = f"SELECT * FROM {self.table_name} WHERE {self.primary_key} = ?"
        row = self.db.fetch_one(query, (id,))
        return self.model_class.from_row(row) if row else None
    
    def get_by_field(self, field: str, value: Any) -> Optional[T]:
        """
        Get single record by field value.
        
        Args:
            field: Field name
            value: Field value
        
        Returns:
            Model instance or None
        """
        query = f"SELECT * FROM {self.table_name} WHERE {field} = ? LIMIT 1"
        row = self.db.fetch_one(query, (value,))
        return self.model_class.from_row(row) if row else None
    
    def get_all(self, limit: int = 0, offset: int = 0) -> List[T]:
        """
        Get all records.
        
        Args:
            limit: Maximum records to return (0 = all)
            offset: Number of records to skip
        
        Returns:
            List of model instances
        """
        query = f"SELECT * FROM {self.table_name}"
        params = []
        
        if limit > 0:
            query += " LIMIT ?"
            params.append(limit)
            if offset > 0:
                query += " OFFSET ?"
                params.append(offset)
        
        rows = self.db.fetch_all(query, tuple(params))
        return self.model_class.from_list(rows)
    
    def get_count(self) -> int:
        """
        Get total record count.
        
        Returns:
            Number of records
        """
        query = f"SELECT COUNT(*) as count FROM {self.table_name}"
        row = self.db.fetch_one(query)
        return row["count"] if row else 0
    
    def exists(self, field: str, value: Any) -> bool:
        """
        Check if record exists by field value.
        
        Args:
            field: Field name
            value: Field value
        
        Returns:
            True if exists
        """
        query = f"SELECT 1 FROM {self.table_name} WHERE {field} = ? LIMIT 1"
        row = self.db.fetch_one(query, (value,))
        return row is not None
    
    def create(self, data: dict) -> int:
        """
        Create new record.
        
        Args:
            data: Dictionary of field values
        
        Returns:
            New record ID
        """
        return self.db.insert(self.table_name, data)
    
    def update(self, id: int, data: dict) -> int:
        """
        Update record by ID.
        
        Args:
            id: Primary key value
            data: Dictionary of field values to update
        
        Returns:
            Number of affected rows
        """
        return self.db.update(
            self.table_name,
            data,
            f"{self.primary_key} = ?",
            (id,)
        )
    
    def update_by_field(self, field: str, field_value: Any, data: dict) -> int:
        """
        Update record by field value.
        
        Args:
            field: Field name to match
            field_value: Field value to match
            data: Dictionary of field values to update
        
        Returns:
            Number of affected rows
        """
        return self.db.update(
            self.table_name,
            data,
            f"{field} = ?",
            (field_value,)
        )
    
    def delete(self, id: int) -> int:
        """
        Delete record by ID.
        
        Args:
            id: Primary key value
        
        Returns:
            Number of affected rows
        """
        return self.db.delete(self.table_name, f"{self.primary_key} = ?", (id,))
    
    def delete_by_field(self, field: str, value: Any) -> int:
        """
        Delete record by field value.
        
        Args:
            field: Field name
            value: Field value
        
        Returns:
            Number of affected rows
        """
        return self.db.delete(self.table_name, f"{field} = ?", (value,))
    
    def search(
        self,
        search_term: str,
        fields: List[str],
        limit: int = 100,
    ) -> List[T]:
        """
        Search records by multiple fields.
        
        Args:
            search_term: Term to search for
            fields: List of fields to search
            limit: Maximum results
        
        Returns:
            List of matching model instances
        """
        conditions = " OR ".join([f"{field} LIKE ?" for field in fields])
        query = f"SELECT * FROM {self.table_name} WHERE {conditions} LIMIT ?"
        params = [f"%{search_term}%" for _ in fields] + [limit]
        
        rows = self.db.fetch_all(query, tuple(params))
        return self.model_class.from_list(rows)
    
    @abstractmethod
    def find_by_company(self, company_id: str) -> List[T]:
        """
        Find all records for a company.
        
        Args:
            company_id: Company ID
        
        Returns:
            List of model instances
        """
        pass
