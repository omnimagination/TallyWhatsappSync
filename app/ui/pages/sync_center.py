"""
Sync Center Page for TallySync

Author: OmniMagination
Version: 1.0.0
"""

import customtkinter as ctk
from typing import Any, Optional
from datetime import datetime
import threading

from app.ui.styles import UIStyles
from app.core.logger import logger
from app.services.sync_service import SyncService
from app.database.repositories import SyncLogRepository


class SyncCenterPage(ctk.CTkScrollableFrame):
    """Sync Center page for managing Tally synchronization."""
    
    def __init__(self, master: Any, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self.configure(fg_color=UIStyles.COLOR_BG_DARK)
        
        self.sync_service: Optional[SyncService] = None
        self.sync_log_repo = SyncLogRepository()
        self.is_syncing = False
        
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Setup sync center UI."""
        self._create_header()
        self._create_connection_section()
        self._create_sync_options()
        self._create_progress_section()
        self._create_sync_history()
    
    def _create_header(self) -> None:
        """Create page header."""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))
        
        title = ctk.CTkLabel(
            header_frame, text="Sync Center",
            font=ctk.CTkFont(family=UIStyles.FONT_FAMILY, size=UIStyles.FONT_SIZE_TITLE, weight="bold"),
            text_color=UIStyles.COLOR_TEXT_PRIMARY,
        )
        title.pack(side="left")
    
    def _create_connection_section(self) -> None:
        """Create Tally connection status section."""
        conn_frame = ctk.CTkFrame(self, fg_color=UIStyles.COLOR_BG_CARD, corner_radius=UIStyles.CORNER_RADIUS_NORMAL)
        conn_frame.pack(fill="x", pady=10)
        
        title = ctk.CTkLabel(
            conn_frame, text="Tally Connection",
            font=ctk.CTkFont(family=UIStyles.FONT_FAMILY, size=UIStyles.FONT_SIZE_HEADING, weight="bold"),
            text_color=UIStyles.COLOR_TEXT_PRIMARY,
        )
        title.pack(padx=15, pady=(15, 10))
        
        status_frame = ctk.CTkFrame(conn_frame, fg_color="transparent")
        status_frame.pack(fill="x", padx=15, pady=10)
        
        self.connection_indicator = ctk.CTkLabel(
            status_frame, text="?",
            font=ctk.CTkFont(size=20), text_color=UIStyles.COLOR_ERROR,
        )
        self.connection_indicator.pack(side="left", padx=(0, 10))
        
        self.connection_status = ctk.CTkLabel(
            status_frame, text="Disconnected",
            font=ctk.CTkFont(family=UIStyles.FONT_FAMILY, size=UIStyles.FONT_SIZE_MEDIUM),
            text_color=UIStyles.COLOR_TEXT_PRIMARY,
        )
        self.connection_status.pack(side="left")
        
        test_btn = ctk.CTkButton(status_frame, text="Test Connection", command=self._test_connection, height=35, width=120)
        test_btn.pack(side="right")
        
        info_label = ctk.CTkLabel(
            conn_frame, text="URL: http://localhost:9000",
            font=ctk.CTkFont(family=UIStyles.FONT_FAMILY, size=UIStyles.FONT_SIZE_SMALL),
            text_color=UIStyles.COLOR_TEXT_SECONDARY,
        )
        info_label.pack(padx=15, pady=(0, 15))
    
    def _create_sync_options(self) -> None:
        """Create sync option buttons."""
        sync_frame = ctk.CTkFrame(self, fg_color=UIStyles.COLOR_BG_CARD, corner_radius=UIStyles.CORNER_RADIUS_NORMAL)
        sync_frame.pack(fill="x", pady=10)
        
        title = ctk.CTkLabel(
            sync_frame, text="Synchronization",
            font=ctk.CTkFont(family=UIStyles.FONT_FAMILY, size=UIStyles.FONT_SIZE_HEADING, weight="bold"),
            text_color=UIStyles.COLOR_TEXT_PRIMARY,
        )
        title.pack(padx=15, pady=(15, 10))
        
        buttons_frame = ctk.CTkFrame(sync_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=15, pady=10)
        
        self.full_sync_btn = ctk.CTkButton(buttons_frame, text="Full Sync", command=self._start_full_sync, height=45, width=150, fg_color=UIStyles.COLOR_PRIMARY)
        self.full_sync_btn.pack(side="left", padx=5)
        
        self.companies_btn = ctk.CTkButton(buttons_frame, text="Companies", command=self._start_companies_sync, height=45, width=120)
        self.companies_btn.pack(side="left", padx=5)
        
        self.ledgers_btn = ctk.CTkButton(buttons_frame, text="Ledgers", command=self._start_ledgers_sync, height=45, width=120)
        self.ledgers_btn.pack(side="left", padx=5)
        
        self.vouchers_btn = ctk.CTkButton(buttons_frame, text="Vouchers (Optional)", command=self._start_vouchers_sync, height=45, width=150)
        self.vouchers_btn.pack(side="left", padx=5)
        
        desc_label = ctk.CTkLabel(
            sync_frame, text="Note: Voucher sync may require TDL configuration in Tally",
            font=ctk.CTkFont(family=UIStyles.FONT_FAMILY, size=UIStyles.FONT_SIZE_SMALL),
            text_color=UIStyles.COLOR_WARNING,
        )
        desc_label.pack(padx=15, pady=(0, 15))
    
    def _create_progress_section(self) -> None:
        """Create progress indicator section."""
        progress_frame = ctk.CTkFrame(self, fg_color=UIStyles.COLOR_BG_CARD, corner_radius=UIStyles.CORNER_RADIUS_NORMAL)
        progress_frame.pack(fill="x", pady=10)
        
        title = ctk.CTkLabel(
            progress_frame, text="Progress",
            font=ctk.CTkFont(family=UIStyles.FONT_FAMILY, size=UIStyles.FONT_SIZE_HEADING, weight="bold"),
            text_color=UIStyles.COLOR_TEXT_PRIMARY,
        )
        title.pack(padx=15, pady=(15, 10))
        
        self.progress_bar = ctk.CTkProgressBar(progress_frame, width=500, height=20, corner_radius=10)
        self.progress_bar.pack(padx=15, pady=10)
        self.progress_bar.set(0)
        
        self.progress_label = ctk.CTkLabel(
            progress_frame, text="Ready",
            font=ctk.CTkFont(family=UIStyles.FONT_FAMILY, size=UIStyles.FONT_SIZE_NORMAL),
            text_color=UIStyles.COLOR_TEXT_SECONDARY,
        )
        self.progress_label.pack(padx=15, pady=(0, 15))
    
    def _create_sync_history(self) -> None:
        """Create sync history section."""
        history_frame = ctk.CTkFrame(self, fg_color=UIStyles.COLOR_BG_CARD, corner_radius=UIStyles.CORNER_RADIUS_NORMAL)
        history_frame.pack(fill="both", expand=True, pady=10)
        
        title = ctk.CTkLabel(
            history_frame, text="Sync History",
            font=ctk.CTkFont(family=UIStyles.FONT_FAMILY, size=UIStyles.FONT_SIZE_HEADING, weight="bold"),
            text_color=UIStyles.COLOR_TEXT_PRIMARY,
        )
        title.pack(padx=15, pady=(15, 10))
        
        self.history_frame = ctk.CTkFrame(history_frame, fg_color="transparent")
        self.history_frame.pack(fill="both", expand=True, padx=15, pady=10)
        
        refresh_btn = ctk.CTkButton(history_frame, text="Refresh History", command=self._load_sync_history, height=35, width=150)
        refresh_btn.pack(pady=(0, 15))
    
    def _test_connection(self) -> None:
        """Test connection to Tally server."""
        self.progress_label.configure(text="Testing connection...", text_color=UIStyles.COLOR_INFO)
        
        try:
            if self.sync_service is None:
                self.sync_service = SyncService()
            
            connected = self.sync_service.test_connection()
            
            if connected:
                self.connection_indicator.configure(text_color=UIStyles.COLOR_SUCCESS)
                self.connection_status.configure(text="Connected")
                self.progress_label.configure(text="Connection successful!", text_color=UIStyles.COLOR_SUCCESS)
            else:
                self.connection_indicator.configure(text_color=UIStyles.COLOR_ERROR)
                self.connection_status.configure(text="Disconnected")
                self.progress_label.configure(text="Connection failed - Is Tally running?", text_color=UIStyles.COLOR_ERROR)
        except Exception as e:
            self.connection_indicator.configure(text_color=UIStyles.COLOR_ERROR)
            self.connection_status.configure(text="Disconnected")
            self.progress_label.configure(text=f"Error: {str(e)}", text_color=UIStyles.COLOR_ERROR)
    
    def _set_buttons_state(self, state: str) -> None:
        """Enable/disable sync buttons."""
        self.full_sync_btn.configure(state=state)
        self.companies_btn.configure(state=state)
        self.ledgers_btn.configure(state=state)
        self.vouchers_btn.configure(state=state)
    
    def _start_full_sync(self) -> None:
        """Start full synchronization."""
        if self.is_syncing:
            return
        self._run_sync("full")
    
    def _start_companies_sync(self) -> None:
        """Start companies sync."""
        if self.is_syncing:
            return
        self._run_sync("companies")
    
    def _start_ledgers_sync(self) -> None:
        """Start ledgers sync."""
        if self.is_syncing:
            return
        self._run_sync("ledgers")
    
    def _start_vouchers_sync(self) -> None:
        """Start vouchers sync."""
        if self.is_syncing:
            return
        self._run_sync("vouchers")
    
    def _run_sync(self, sync_type: str) -> None:
        """Run synchronization in background thread."""
        self.is_syncing = True
        self._set_buttons_state("disabled")
        self.progress_label.configure(text="Starting sync...", text_color=UIStyles.COLOR_INFO)
        self.progress_bar.set(0.1)
        
        thread = threading.Thread(target=self._sync_worker, args=(sync_type,), daemon=True)
        thread.start()
    
    def _sync_worker(self, sync_type: str) -> None:
        """Background sync worker."""
        try:
            if self.sync_service is None:
                self.sync_service = SyncService()
            
            if sync_type == "full":
                self._update_progress(0.2, "Syncing companies...")
                self.sync_service.sync_companies()
                
                self._update_progress(0.5, "Syncing ledgers...")
                self.sync_service.sync_ledgers()
                
                self._update_progress(0.8, "Syncing vouchers (optional)...")
                self.sync_service.sync_vouchers()
                
                self._update_progress(1.0, "Full sync completed!", "success")
            
            elif sync_type == "companies":
                self._update_progress(0.3, "Syncing companies...")
                result = self.sync_service.sync_companies()
                self._update_progress(1.0, f"Companies: {result.get('records_processed', 0)}", "success" if result.get("success") else "warning")
            
            elif sync_type == "ledgers":
                self._update_progress(0.3, "Syncing ledgers...")
                result = self.sync_service.sync_ledgers()
                self._update_progress(1.0, f"Ledgers: {result.get('records_processed', 0)}", "success" if result.get("success") else "error")
            
            elif sync_type == "vouchers":
                self._update_progress(0.3, "Syncing vouchers...")
                result = self.sync_service.sync_vouchers()
                if result.get("skipped"):
                    self._update_progress(1.0, "Vouchers: Skipped (requires TDL)", "warning")
                else:
                    self._update_progress(1.0, f"Vouchers: {result.get('records_processed', 0)}", "success" if result.get("success") else "error")
        
        except Exception as e:
            self._update_progress(0, f"Error: {str(e)}", "error")
            logger.error(f"Sync error: {e}", category="sync", exc_info=True)
        
        finally:
            self.is_syncing = False
            self.after(0, lambda: self._set_buttons_state("normal"))
            self.after(0, self._load_sync_history)
    
    def _update_progress(self, value: float, message: str, level: str = "info") -> None:
        """Update progress bar and label safely."""
        def update():
            self.progress_bar.set(value)
            self.progress_label.configure(text=message)
            colors = {"success": UIStyles.COLOR_SUCCESS, "warning": UIStyles.COLOR_WARNING, "error": UIStyles.COLOR_ERROR, "info": UIStyles.COLOR_TEXT_SECONDARY}
            self.progress_label.configure(text_color=colors.get(level, UIStyles.COLOR_TEXT_SECONDARY))
        self.after(0, update)
    
    def _load_sync_history(self) -> None:
        """Load and display sync history."""
        for widget in self.history_frame.winfo_children():
            widget.destroy()
        
        try:
            logs = self.sync_log_repo.get_recent(limit=10)
            
            if not logs:
                no_logs = ctk.CTkLabel(self.history_frame, text="No sync history available", font=ctk.CTkFont(family=UIStyles.FONT_FAMILY, size=UIStyles.FONT_SIZE_NORMAL), text_color=UIStyles.COLOR_TEXT_MUTED)
                no_logs.pack(pady=20)
                return
            
            for log in logs:
                self._create_history_item(log)
        except Exception as e:
            logger.error(f"Failed to load sync history: {e}", category="ui")
    
    def _create_history_item(self, log) -> None:
        """Create a sync history item."""
        item_frame = ctk.CTkFrame(self.history_frame, fg_color=UIStyles.COLOR_BG_INPUT, corner_radius=UIStyles.CORNER_RADIUS_SMALL)
        item_frame.pack(fill="x", pady=2)
        
        status_color = UIStyles.COLOR_SUCCESS if log.is_success else (UIStyles.COLOR_WARNING if log.status == "skipped" else UIStyles.COLOR_ERROR)
        
        status_dot = ctk.CTkLabel(item_frame, text="?", font=ctk.CTkFont(size=14), text_color=status_color)
        status_dot.pack(side="left", padx=(10, 10), pady=10)
        
        type_label = ctk.CTkLabel(item_frame, text=log.sync_type.upper(), font=ctk.CTkFont(family=UIStyles.FONT_FAMILY, size=UIStyles.FONT_SIZE_SMALL, weight="bold"), text_color=UIStyles.COLOR_TEXT_PRIMARY)
        type_label.pack(side="left", padx=(0, 20), pady=10)
        
        time_label = ctk.CTkLabel(item_frame, text=log.formatted_start_time or "Unknown", font=ctk.CTkFont(family=UIStyles.FONT_FAMILY, size=UIStyles.FONT_SIZE_SMALL), text_color=UIStyles.COLOR_TEXT_SECONDARY)
        time_label.pack(side="left", padx=(0, 20), pady=10)
        
        records_label = ctk.CTkLabel(item_frame, text=f"{log.records_processed} records", font=ctk.CTkFont(family=UIStyles.FONT_FAMILY, size=UIStyles.FONT_SIZE_SMALL), text_color=UIStyles.COLOR_TEXT_SECONDARY)
        records_label.pack(side="left", pady=10)
        
        status_label = ctk.CTkLabel(item_frame, text=log.status.upper(), font=ctk.CTkFont(family=UIStyles.FONT_FAMILY, size=UIStyles.FONT_SIZE_SMALL), text_color=status_color)
        status_label.pack(side="right", padx=(0, 10), pady=10)
    
    def refresh(self) -> None:
        """Refresh sync center."""
        self._load_sync_history()
        logger.debug("Sync Center refreshed", category="ui")
