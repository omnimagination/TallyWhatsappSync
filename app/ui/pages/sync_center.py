"""
Sync Center Page for TallySync

Handles all synchronization operations with Tally.

Author: OmniMagination
Version: 1.0.0
"""

import customtkinter as ctk
from typing import Any, Optional
from datetime import datetime
import threading

from app.ui.styles import UIStyles
from app.core.logger import logger
from app.core.exceptions import TallyConnectionError
from app.services.sync_service import SyncService
from app.database.repositories import SyncLogRepository


class SyncCenterPage(ctk.CTkScrollableFrame):
    """
    Sync Center page for managing Tally synchronization.
    """
    
    def __init__(self, master: Any, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self.configure(fg_color=UIStyles.COLOR_BG_DARK)
        
        self.sync_service: Optional[SyncService] = None
        self.sync_log_repo = SyncLogRepository()
        self.is_syncing = False
        
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Setup sync center UI."""
        # Header
        self._create_header()
        
        # Connection Status
        self._create_connection_section()
        
        # Sync Options
        self._create_sync_options()
        
        # Progress Section
        self._create_progress_section()
        
        # Sync History
        self._create_sync_history()
    
    def _create_header(self) -> None:
        """Create page header."""
        header_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )
        header_frame.pack(fill="x", pady=(0, 20))
        
        title = ctk.CTkLabel(
            header_frame,
            text="Sync Center",
            font=ctk.CTkFont(
                family=UIStyles.FONT_FAMILY,
                size=UIStyles.FONT_SIZE_TITLE,
                weight="bold",
            ),
            text_color=UIStyles.COLOR_TEXT_PRIMARY,
        )
        title.pack(side="left")
    
    def _create_connection_section(self) -> None:
        """Create Tally connection status section."""
        conn_frame = ctk.CTkFrame(
            self,
            fg_color=UIStyles.COLOR_BG_CARD,
            corner_radius=UIStyles.CORNER_RADIUS_NORMAL,
        )
        conn_frame.pack(fill="x", pady=10)
        
        title = ctk.CTkLabel(
            conn_frame,
            text="Tally Connection",
            font=ctk.CTkFont(
                family=UIStyles.FONT_FAMILY,
                size=UIStyles.FONT_SIZE_HEADING,
                weight="bold",
            ),
            text_color=UIStyles.COLOR_TEXT_PRIMARY,
        )
        title.pack(padx=15, pady=(15, 10))
        
        # Status indicator
        status_frame = ctk.CTkFrame(
            conn_frame,
            fg_color="transparent",
        )
        status_frame.pack(fill="x", padx=15, pady=10)
        
        self.connection_indicator = ctk.CTkLabel(
            status_frame,
            text="?",
            font=ctk.CTkFont(size=20),
            text_color=UIStyles.COLOR_ERROR,
        )
        self.connection_indicator.pack(side="left", padx=(0, 10))
        
        self.connection_status = ctk.CTkLabel(
            status_frame,
            text="Disconnected",
            font=ctk.CTkFont(
                family=UIStyles.FONT_FAMILY,
                size=UIStyles.FONT_SIZE_MEDIUM,
            ),
            text_color=UIStyles.COLOR_TEXT_PRIMARY,
        )
        self.connection_status.pack(side="left")
        
        # Test connection button
        test_btn = ctk.CTkButton(
            status_frame,
            text="Test Connection",
            command=self._test_connection,
            height=35,
            width=120,
        )
        test_btn.pack(side="right")
        
        # Connection info
        info_label = ctk.CTkLabel(
            conn_frame,
            text="URL: http://localhost:9000",
            font=ctk.CTkFont(
                family=UIStyles.FONT_FAMILY,
                size=UIStyles.FONT_SIZE_SMALL,
            ),
            text_color=UIStyles.COLOR_TEXT_SECONDARY,
        )
        info_label.pack(padx=15, pady=(0, 15))
    
    def _create_sync_options(self) -> None:
        """Create sync option buttons."""
        sync_frame = ctk.CTkFrame(
            self,
            fg_color=UIStyles.COLOR_BG_CARD,
            corner_radius=UIStyles.CORNER_RADIUS_NORMAL,
        )
        sync_frame.pack(fill="x", pady=10)
        
        title = ctk.CTkLabel(
            sync_frame,
            text="Synchronization",
            font=ctk.CTkFont(
                family=UIStyles.FONT_FAMILY,
                size=UIStyles.FONT_SIZE_HEADING,
                weight="bold",
            ),
            text_color=UIStyles.COLOR_TEXT_PRIMARY,
        )
        title.pack(padx=15, pady=(15, 10))
        
        # Sync buttons
        buttons_frame = ctk.CTkFrame(
            sync_frame,
            fg_color="transparent",
        )
        buttons_frame.pack(fill="x", padx=15, pady=10)
        
        # Full Sync
        full_sync_btn = ctk.CTkButton(
            buttons_frame,
            text="?? Full Sync",
            command=self._start_full_sync,
            height=45,
            width=150,
            fg_color=UIStyles.COLOR_PRIMARY,
        )
        full_sync_btn.pack(side="left", padx=5)
        
        # Companies Only
        companies_btn = ctk.CTkButton(
            buttons_frame,
            text="?? Companies",
            command=self._start_companies_sync,
            height=45,
            width=120,
        )
        companies_btn.pack(side="left", padx=5)
        
        # Ledgers Only
        ledgers_btn = ctk.CTkButton(
            buttons_frame,
            text="?? Ledgers",
            command=self._start_ledgers_sync,
            height=45,
            width=120,
        )
        ledgers_btn.pack(side="left", padx=5)
        
        # Vouchers Only
        vouchers_btn = ctk.CTkButton(
            buttons_frame,
            text="?? Vouchers",
            command=self._start_vouchers_sync,
            height=45,
            width=120,
        )
        vouchers_btn.pack(side="left", padx=5)
        
        # Description
        desc_label = ctk.CTkLabel(
            sync_frame,
            text="Click a button to start synchronization with TallyPrime",
            font=ctk.CTkFont(
                family=UIStyles.FONT_FAMILY,
                size=UIStyles.FONT_SIZE_SMALL,
            ),
            text_color=UIStyles.COLOR_TEXT_MUTED,
        )
        desc_label.pack(padx=15, pady=(0, 15))
    
    def _create_progress_section(self) -> None:
        """Create progress indicator section."""
        progress_frame = ctk.CTkFrame(
            self,
            fg_color=UIStyles.COLOR_BG_CARD,
            corner_radius=UIStyles.CORNER_RADIUS_NORMAL,
        )
        progress_frame.pack(fill="x", pady=10)
        
        title = ctk.CTkLabel(
            progress_frame,
            text="Progress",
            font=ctk.CTkFont(
                family=UIStyles.FONT_FAMILY,
                size=UIStyles.FONT_SIZE_HEADING,
                weight="bold",
            ),
            text_color=UIStyles.COLOR_TEXT_PRIMARY,
        )
        title.pack(padx=15, pady=(15, 10))
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(
            progress_frame,
            width=500,
            height=20,
            corner_radius=10,
        )
        self.progress_bar.pack(padx=15, pady=10)
        self.progress_bar.set(0)
        
        # Status label
        self.progress_label = ctk.CTkLabel(
            progress_frame,
            text="Ready",
            font=ctk.CTkFont(
                family=UIStyles.FONT_FAMILY,
                size=UIStyles.FONT_SIZE_NORMAL,
            ),
            text_color=UIStyles.COLOR_TEXT_SECONDARY,
        )
        self.progress_label.pack(padx=15, pady=(0, 15))
    
    def _create_sync_history(self) -> None:
        """Create sync history section."""
        history_frame = ctk.CTkFrame(
            self,
            fg_color=UIStyles.COLOR_BG_CARD,
            corner_radius=UIStyles.CORNER_RADIUS_NORMAL,
        )
        history_frame.pack(fill="both", expand=True, pady=10)
        
        title = ctk.CTkLabel(
            history_frame,
            text="Sync History",
            font=ctk.CTkFont(
                family=UIStyles.FONT_FAMILY,
                size=UIStyles.FONT_SIZE_HEADING,
                weight="bold",
            ),
            text_color=UIStyles.COLOR_TEXT_PRIMARY,
        )
        title.pack(padx=15, pady=(15, 10))
        
        # History list
        self.history_frame = ctk.CTkFrame(
            history_frame,
            fg_color="transparent",
        )
        self.history_frame.pack(fill="both", expand=True, padx=15, pady=10)
        
        # Refresh button
        refresh_btn = ctk.CTkButton(
            history_frame,
            text="?? Refresh History",
            command=self._load_sync_history,
            height=35,
            width=150,
        )
        refresh_btn.pack(pady=(0, 15))
    
    def _test_connection(self) -> None:
        """Test connection to Tally server."""
        self._set_status("Testing connection...", "info")
        
        try:
            if self.sync_service is None:
                self.sync_service = SyncService()
            
            connected = self.sync_service.test_connection()
            
            if connected:
                self._set_connection_status(True)
                self._set_status("Connection successful!", "success")
            else:
                self._set_connection_status(False)
                self._set_status("Connection failed - Is Tally running?", "error")
        
        except Exception as e:
            self._set_connection_status(False)
            self._set_status(f"Error: {str(e)}", "error")
    
    def _set_connection_status(self, connected: bool) -> None:
        """Update connection status UI."""
        if connected:
            self.connection_indicator.configure(text_color=UIStyles.COLOR_SUCCESS)
            self.connection_status.configure(text="Connected")
        else:
            self.connection_indicator.configure(text_color=UIStyles.COLOR_ERROR)
            self.connection_status.configure(text="Disconnected")
    
    def _set_status(self, message: str, level: str = "info") -> None:
        """Update progress status."""
        self.progress_label.configure(text=message)
        
        colors = {
            "success": UIStyles.COLOR_SUCCESS,
            "warning": UIStyles.COLOR_WARNING,
            "error": UIStyles.COLOR_ERROR,
            "info": UIStyles.COLOR_TEXT_SECONDARY,
        }
        self.progress_label.configure(text_color=colors.get(level, UIStyles.COLOR_TEXT_SECONDARY))
    
    def _set_progress(self, value: float) -> None:
        """Update progress bar (0.0 to 1.0)."""
        self.progress_bar.set(value)
    
    def _start_full_sync(self) -> None:
        """Start full synchronization."""
        if self.is_syncing:
            self._set_status("Sync already in progress...", "warning")
            return
        
        self._run_sync("full")
    
    def _start_companies_sync(self) -> None:
        """Start companies sync."""
        if self.is_syncing:
            self._set_status("Sync already in progress...", "warning")
            return
        
        self._run_sync("companies")
    
    def _start_ledgers_sync(self) -> None:
        """Start ledgers sync."""
        if self.is_syncing:
            self._set_status("Sync already in progress...", "warning")
            return
        
        self._run_sync("ledgers")
    
    def _start_vouchers_sync(self) -> None:
        """Start vouchers sync."""
        if self.is_syncing:
            self._set_status("Sync already in progress...", "warning")
            return
        
        self._run_sync("vouchers")
    
    def _run_sync(self, sync_type: str) -> None:
        """Run synchronization in background thread."""
        self.is_syncing = True
        self._set_status("Starting sync...", "info")
        self._set_progress(0.1)
        
        # Run in background thread
        thread = threading.Thread(target=self._sync_worker, args=(sync_type,))
        thread.daemon = True
        thread.start()
    
    def _sync_worker(self, sync_type: str) -> None:
        """Background sync worker."""
        try:
            if self.sync_service is None:
                self.sync_service = SyncService()
            
            if sync_type == "full":
                self._set_status("Syncing companies...", "info")
                self._set_progress(0.2)
                result = self.sync_service.sync_companies()
                
                self._set_status("Syncing ledgers...", "info")
                self._set_progress(0.5)
                result = self.sync_service.sync_ledgers()
                
                self._set_status("Syncing vouchers...", "info")
                self._set_progress(0.8)
                result = self.sync_service.sync_vouchers()
                
                self._set_progress(1.0)
                
                if result["success"]:
                    self._set_status("Full sync completed successfully!", "success")
                else:
                    self._set_status(f"Sync completed with errors: {result.get('error', '')}", "warning")
            
            elif sync_type == "companies":
                self._set_status("Syncing companies...", "info")
                self._set_progress(0.3)
                result = self.sync_service.sync_companies()
                self._set_progress(1.0)
                
                if result["success"]:
                    self._set_status(f"Companies synced: {result['records_processed']}", "success")
                else:
                    self._set_status(f"Sync failed: {result.get('error', '')}", "error")
            
            elif sync_type == "ledgers":
                self._set_status("Syncing ledgers...", "info")
                self._set_progress(0.3)
                result = self.sync_service.sync_ledgers()
                self._set_progress(1.0)
                
                if result["success"]:
                    self._set_status(f"Ledgers synced: {result['records_processed']}", "success")
                else:
                    self._set_status(f"Sync failed: {result.get('error', '')}", "error")
            
            elif sync_type == "vouchers":
                self._set_status("Syncing vouchers...", "info")
                self._set_progress(0.3)
                result = self.sync_service.sync_vouchers()
                self._set_progress(1.0)
                
                if result["success"]:
                    self._set_status(f"Vouchers synced: {result['records_processed']}", "success")
                else:
                    self._set_status(f"Sync failed: {result.get('error', '')}", "error")
        
        except Exception as e:
            self._set_status(f"Error: {str(e)}", "error")
            logger.error(f"Sync error: {e}", category="sync", exc_info=True)
        
        finally:
            self.is_syncing = False
            self._load_sync_history()
    
    def _load_sync_history(self) -> None:
        """Load and display sync history."""
        # Clear existing
        for widget in self.history_frame.winfo_children():
            widget.destroy()
        
        try:
            logs = self.sync_log_repo.get_recent(limit=10)
            
            if not logs:
                no_logs = ctk.CTkLabel(
                    self.history_frame,
                    text="No sync history available",
                    font=ctk.CTkFont(
                        family=UIStyles.FONT_FAMILY,
                        size=UIStyles.FONT_SIZE_NORMAL,
                    ),
                    text_color=UIStyles.COLOR_TEXT_MUTED,
                )
                no_logs.pack(pady=20)
                return
            
            for log in logs:
                self._create_history_item(log)
        
        except Exception as e:
            logger.error(f"Failed to load sync history: {e}", category="ui")
    
    def _create_history_item(self, log) -> None:
        """Create a sync history item."""
        item_frame = ctk.CTkFrame(
            self.history_frame,
            fg_color=UIStyles.COLOR_BG_INPUT,
            corner_radius=UIStyles.CORNER_RADIUS_SMALL,
        )
        item_frame.pack(fill="x", pady=2)
        
        # Status color
        status_color = UIStyles.COLOR_SUCCESS if log.is_success else (
            UIStyles.COLOR_ERROR if log.is_failed else UIStyles.COLOR_WARNING
        )
        
        # Status indicator
        status_dot = ctk.CTkLabel(
            item_frame,
            text="?",
            font=ctk.CTkFont(size=14),
            text_color=status_color,
        )
        status_dot.pack(side="left", padx=(10, 10), pady=10)
        
        # Type
        type_label = ctk.CTkLabel(
            item_frame,
            text=log.sync_type.upper(),
            font=ctk.CTkFont(
                family=UIStyles.FONT_FAMILY,
                size=UIStyles.FONT_SIZE_SMALL,
                weight="bold",
            ),
            text_color=UIStyles.COLOR_TEXT_PRIMARY,
        )
        type_label.pack(side="left", padx=(0, 20), pady=10)
        
        # Time
        time_label = ctk.CTkLabel(
            item_frame,
            text=log.formatted_start_time,
            font=ctk.CTkFont(
                family=UIStyles.FONT_FAMILY,
                size=UIStyles.FONT_SIZE_SMALL,
            ),
            text_color=UIStyles.COLOR_TEXT_SECONDARY,
        )
        time_label.pack(side="left", padx=(0, 20), pady=10)
        
        # Records
        records_label = ctk.CTkLabel(
            item_frame,
            text=f"{log.records_processed} records",
            font=ctk.CTkFont(
                family=UIStyles.FONT_FAMILY,
                size=UIStyles.FONT_SIZE_SMALL,
            ),
            text_color=UIStyles.COLOR_TEXT_SECONDARY,
        )
        records_label.pack(side="left", pady=10)
        
        # Status text
        status_label = ctk.CTkLabel(
            item_frame,
            text=log.status.upper(),
            font=ctk.CTkFont(
                family=UIStyles.FONT_FAMILY,
                size=UIStyles.FONT_SIZE_SMALL,
            ),
            text_color=status_color,
        )
        status_label.pack(side="right", padx=(0, 10), pady=10)
    
    def refresh(self) -> None:
        """Refresh sync center."""
        self._load_sync_history()
        logger.debug("Sync Center refreshed", category="ui")
