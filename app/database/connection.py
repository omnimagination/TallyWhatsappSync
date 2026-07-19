"""
Database Connection Manager for TallySync

Handles SQLite database connections with:
- Connection pooling
- Transaction management
- Automatic table creation
- Backup functionality

Author: OmniMagination
Version: 1.0.0
"""

import sqlite3
from pathlib import Path
from typing import Optional, Generator
from contextlib import contextmanager
from datetime import datetime
import shutil

from app.core.config import config
from app.core.logger import logger
from app.core.exceptions import DatabaseError
from app.core.utils import get_app_path, ensure_folder_exists


class DatabaseConnection:
    """
    Singleton database connection manager for SQLite.
    
    Features:
    - Connection pooling
    - Transaction support
    - Automatic schema creation
    - Backup functionality
    """
    
    _instance: Optional["DatabaseConnection"] = None
    _connection: Optional[sqlite3.Connection] = None
    _initialized: bool = False
    
    def __new__(cls) -> "DatabaseConnection":
        """Singleton pattern."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self) -> None:
        """Initialize database connection."""
        if DatabaseConnection._initialized:
            return
        
        self.db_path: Path = config.get_database_path()
        self.backup_enabled: bool = config.get("database", "backup_enabled", default=True)
        self.backup_interval: int = config.get("database", "backup_interval", default=24)
        
        self._initialize_database()
        DatabaseConnection._initialized = True
    
    def _initialize_database(self) -> None:
        """Initialize database connection and create tables."""
        try:
            # Ensure data folder exists
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Create connection
            self._connection = sqlite3.connect(
                str(self.db_path),
                check_same_thread=False,
                timeout=30,
            )
            
            # Configure connection
            self._connection.row_factory = sqlite3.Row
            self._connection.execute("PRAGMA foreign_keys = ON")
            self._connection.execute("PRAGMA journal_mode = WAL")
            self._connection.execute("PRAGMA synchronous = NORMAL")
            self._connection.execute("PRAGMA cache_size = 10000")
            
            # Create tables
            self._create_tables()
            
            logger.info(f"Database initialized: {self.db_path}", category="database")
        
        except Exception as e:
            logger.error(f"Database initialization failed: {e}", category="database", exc_info=True)
            raise DatabaseError(f"Failed to initialize database: {e}")
    
    def _create_tables(self) -> None:
        """Create all database tables if they don't exist."""
        tables = [
            self._get_companies_table_sql(),
            self._get_ledgers_table_sql(),
            self._get_vouchers_table_sql(),
            self._get_voucher_entries_table_sql(),
            self._get_sync_logs_table_sql(),
            self._get_settings_table_sql(),
        ]
        
        for table_sql in tables:
            self._connection.execute(table_sql)
        
        self._connection.commit()
        logger.debug("Database tables created/verified", category="database")
    
    def _get_companies_table_sql(self) -> str:
        """Get SQL for companies table."""
        return """
        CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            address TEXT,
            phone TEXT,
            email TEXT,
            gst_number TEXT,
            pan_number TEXT,
            state TEXT,
            state_code TEXT,
            financial_year_from TEXT,
            financial_year_to TEXT,
            books_from_date TEXT,
            base_currency TEXT,
            is_active INTEGER DEFAULT 1,
            last_sync_date TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    
    def _get_ledgers_table_sql(self) -> str:
        """Get SQL for ledgers table."""
        return """
        CREATE TABLE IF NOT EXISTS ledgers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ledger_id TEXT UNIQUE NOT NULL,
            company_id TEXT NOT NULL,
            name TEXT NOT NULL,
            parent TEXT,
            group_name TEXT,
            ledger_type TEXT,
            opening_balance REAL DEFAULT 0,
            closing_balance REAL DEFAULT 0,
            balance_type TEXT,
            phone TEXT,
            email TEXT,
            address TEXT,
            gst_number TEXT,
            pan_number TEXT,
            contact_person TEXT,
            credit_limit REAL DEFAULT 0,
            credit_days INTEGER DEFAULT 0,
            is_active INTEGER DEFAULT 1,
            last_sync_date TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (company_id) REFERENCES companies(company_id)
        )
        """
    
    def _get_vouchers_table_sql(self) -> str:
        """Get SQL for vouchers table."""
        return """
        CREATE TABLE IF NOT EXISTS vouchers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            voucher_id TEXT UNIQUE NOT NULL,
            company_id TEXT NOT NULL,
            voucher_type TEXT NOT NULL,
            voucher_number TEXT,
            date TEXT NOT NULL,
            amount REAL DEFAULT 0,
            narration TEXT,
            reference_number TEXT,
            reference_date TEXT,
            buyer_details TEXT,
            shipping_details TEXT,
            invoice_date TEXT,
            is_cancelled INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (company_id) REFERENCES companies(company_id)
        )
        """
    
    def _get_voucher_entries_table_sql(self) -> str:
        """Get SQL for voucher entries table."""
        return """
        CREATE TABLE IF NOT EXISTS voucher_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            voucher_id TEXT NOT NULL,
            ledger_id TEXT NOT NULL,
            amount REAL DEFAULT 0,
            debit_credit TEXT NOT NULL,
            narration TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (voucher_id) REFERENCES vouchers(voucher_id),
            FOREIGN KEY (ledger_id) REFERENCES ledgers(ledger_id)
        )
        """
    
    def _get_sync_logs_table_sql(self) -> str:
        """Get SQL for sync logs table."""
        return """
        CREATE TABLE IF NOT EXISTS sync_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sync_type TEXT NOT NULL,
            status TEXT NOT NULL,
            records_processed INTEGER DEFAULT 0,
            records_failed INTEGER DEFAULT 0,
            start_time TEXT NOT NULL,
            end_time TEXT,
            error_message TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    
    def _get_settings_table_sql(self) -> str:
        """Get SQL for settings table."""
        return """
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT UNIQUE NOT NULL,
            value TEXT,
            data_type TEXT DEFAULT 'string',
            description TEXT,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    
    @contextmanager
    def get_connection(self) -> Generator[sqlite3.Connection, None, None]:
        """
        Get database connection context manager.
        
        Usage:
            with db.get_connection() as conn:
                conn.execute(query)
        """
        if self._connection is None:
            raise DatabaseError("Database connection not initialized")
        
        try:
            yield self._connection
        except Exception as e:
            logger.error(f"Database operation failed: {e}", category="database", exc_info=True)
            raise
    
    @contextmanager
    def transaction(self) -> Generator[sqlite3.Connection, None, None]:
        """
        Execute operations within a transaction.
        
        Usage:
            with db.transaction() as conn:
                conn.execute(insert_query)
                conn.execute(update_query)
            # Auto-commits on success, rolls back on error
        """
        if self._connection is None:
            raise DatabaseError("Database connection not initialized")
        
        try:
            yield self._connection
            self._connection.commit()
            logger.debug("Transaction committed", category="database")
        except Exception as e:
            self._connection.rollback()
            logger.error(f"Transaction rolled back: {e}", category="database", exc_info=True)
            raise
    
    def execute(self, query: str, params: tuple = ()) -> sqlite3.Cursor:
        """Execute a single query."""
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            return cursor
    
    def execute_many(self, query: str, params_list: list[tuple]) -> int:
        """Execute query with multiple parameter sets."""
        with self.get_connection() as conn:
            cursor = conn.executemany(query, params_list)
            return cursor.rowcount
    
    def fetch_one(self, query: str, params: tuple = ()) -> Optional[sqlite3.Row]:
        """Fetch single row from query."""
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            return cursor.fetchone()
    
    def fetch_all(self, query: str, params: tuple = ()) -> list[sqlite3.Row]:
        """Fetch all rows from query."""
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            return cursor.fetchall()
    
    def fetch_column(self, query: str, params: tuple = (), column: str = "") -> list:
        """Fetch single column from all rows."""
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            rows = cursor.fetchall()
            if column and rows:
                return [row[column] for row in rows]
            return [row[0] for row in rows]
    
    def insert(self, table: str, data: dict) -> int:
        """Insert single row and return ID."""
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?" for _ in data])
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        
        with self.transaction() as conn:
            cursor = conn.execute(query, tuple(data.values()))
            return cursor.lastrowid
    
    def update(self, table: str, data: dict, where: str, params: tuple = ()) -> int:
        """Update rows and return affected count."""
        set_clause = ", ".join([f"{key} = ?" for key in data.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE {where}"
        
        with self.transaction() as conn:
            cursor = conn.execute(query, tuple(data.values()) + params)
            return cursor.rowcount
    
    def delete(self, table: str, where: str, params: tuple = ()) -> int:
        """Delete rows and return affected count."""
        query = f"DELETE FROM {table} WHERE {where}"
        
        with self.transaction() as conn:
            cursor = conn.execute(query, params)
            return cursor.rowcount
    
    def backup(self) -> Optional[Path]:
        """Create database backup."""
        if not self.backup_enabled:
            return None
        
        try:
            backup_folder = get_app_path() / config.get("folders", "backups")
            ensure_folder_exists(backup_folder)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = backup_folder / f"tallysync_backup_{timestamp}.db"
            
            shutil.copy2(self.db_path, backup_path)
            
            logger.info(f"Database backup created: {backup_path}", category="database")
            
            # Clean old backups
            self._cleanup_old_backups(backup_folder)
            
            return backup_path
        
        except Exception as e:
            logger.error(f"Database backup failed: {e}", category="database", exc_info=True)
            return None
    
    def _cleanup_old_backups(self, backup_folder: Path) -> None:
        """Remove old backup files."""
        try:
            retention_days = self.backup_interval * self.backup_interval  # hours * days
            cutoff = datetime.now().timestamp() - (retention_days * 86400)
            
            for backup_file in backup_folder.glob("tallysync_backup_*.db"):
                if backup_file.stat().st_mtime < cutoff:
                    backup_file.unlink()
                    logger.debug(f"Old backup removed: {backup_file}", category="database")
        
        except Exception as e:
            logger.warning(f"Backup cleanup failed: {e}", category="database")
    
    def get_database_size(self) -> int:
        """Get database file size in bytes."""
        if self.db_path.exists():
            return self.db_path.stat().st_size
        return 0
    
    def get_table_count(self, table: str) -> int:
        """Get row count for a table."""
        query = f"SELECT COUNT(*) as count FROM {table}"
        result = self.fetch_one(query)
        return result["count"] if result else 0
    
    def close(self) -> None:
        """Close database connection."""
        if self._connection:
            self._connection.close()
            self._connection = None
            logger.info("Database connection closed", category="database")
    
    def __del__(self) -> None:
        """Cleanup on deletion."""
        self.close()


# Global database instance
db = DatabaseConnection()
