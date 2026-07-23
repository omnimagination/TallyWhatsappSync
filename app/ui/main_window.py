"""
Main Application Window for TallySync

Root window with navigation and content area.

Author: OmniMagination
Version: 1.0.0
"""

import customtkinter as ctk
from typing import Dict, Any, Optional
import sys
import os

from app.core.config import config
from app.core.logger import logger
from app.ui.styles import UIStyles
from app.ui.navigation import NavigationSidebar
from app.ui.pages.dashboard import DashboardPage
from app.ui.pages.ledgers import LedgersPage
from app.ui.pages.vouchers import VouchersPage
from app.ui.pages.sync_center import SyncCenterPage
from app.ui.pages.settings import SettingsPage
from app.ui.pages.logs import LogsPage
from app.ui.pages.whatsapp import WhatsAppPage


class MainWindow(ctk.CTk):
    """
    Main application window.
    """
    
    def __init__(self) -> None:
        super().__init__()
        
        self.pages: Dict[str, Any] = {}
        self.current_page: Optional[ctk.CTkFrame] = None
        
        self._setup_window()
        self._setup_ui()
        self._load_pages()
        
        logger.info("MainWindow initialized", category="ui")
    
    def _setup_window(self) -> None:
        """Configure main window properties."""
        self.title("TallySync - TallyPrime Integration")
        self.geometry(
            f"{UIStyles.WINDOW_DEFAULT_WIDTH}x{UIStyles.WINDOW_DEFAULT_HEIGHT}"
        )
        self.minsize(
            UIStyles.WINDOW_MIN_WIDTH,
            UIStyles.WINDOW_MIN_HEIGHT,
        )
        
        UIStyles.configure_appearance()
        
        self.protocol("WM_DELETE_WINDOW", self._on_close)
    
    def _setup_ui(self) -> None:
        """Setup main UI layout."""
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.sidebar = NavigationSidebar(
            self,
            on_page_change=self._on_page_change,
            **UIStyles.get_sidebar_style(),
        )
        self.sidebar.grid(row=0, column=0, sticky="ns")
        
        self.content_frame = ctk.CTkFrame(
            self,
            fg_color=UIStyles.COLOR_BG_DARK,
        )
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=1, pady=1)
        
        self._create_status_bar()
    
    def _create_status_bar(self) -> None:
        """Create status bar at bottom."""
        status_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color=UIStyles.COLOR_BG_CARD,
            height=30,
        )
        status_frame.pack(side="bottom", fill="x", padx=10, pady=(10, 0))
        
        self.status_label = ctk.CTkLabel(
            status_frame,
            text="Ready",
            font=ctk.CTkFont(
                family=UIStyles.FONT_FAMILY,
                size=UIStyles.FONT_SIZE_SMALL,
            ),
            text_color=UIStyles.COLOR_TEXT_SECONDARY,
        )
        self.status_label.pack(side="left", padx=10, pady=5)
        
        self.connection_label = ctk.CTkLabel(
            status_frame,
            text="? Tally: Disconnected",
            font=ctk.CTkFont(
                family=UIStyles.FONT_FAMILY,
                size=UIStyles.FONT_SIZE_SMALL,
            ),
            text_color=UIStyles.COLOR_ERROR,
        )
        self.connection_label.pack(side="right", padx=10, pady=5)
    
    def _load_pages(self) -> None:
        """Load all application pages."""
        self.pages = {
            "dashboard": DashboardPage(self.content_frame),
            "ledgers": LedgersPage(self.content_frame),
            "vouchers": VouchersPage(self.content_frame),
            "sync": SyncCenterPage(self.content_frame),
            "whatsapp": WhatsAppPage(self.content_frame),
            "settings": SettingsPage(self.content_frame),
            "logs": LogsPage(self.content_frame),
        }
        
        self._show_page("dashboard")
    
    def _on_page_change(self, page_id: str) -> None:
        """Handle page navigation."""
        self._show_page(page_id)
        logger.debug(f"Navigation: {page_id}", category="ui")
    
    def _show_page(self, page_id: str) -> None:
        """Show specified page."""
        if self.current_page:
            self.current_page.pack_forget()
        
        if page_id in self.pages:
            self.current_page = self.pages[page_id]
            self.current_page.pack(fill="both", expand=True, padx=20, pady=20)
            
            if hasattr(self.current_page, "refresh"):
                self.current_page.refresh()
    
    def update_status(self, message: str) -> None:
        """Update status bar message."""
        self.status_label.configure(text=message)
    
    def update_connection_status(self, connected: bool) -> None:
        """Update Tally connection status."""
        if connected:
            self.connection_label.configure(
                text="? Tally: Connected",
                text_color=UIStyles.COLOR_SUCCESS,
            )
        else:
            self.connection_label.configure(
                text="? Tally: Disconnected",
                text_color=UIStyles.COLOR_ERROR,
            )
    
    def _on_close(self) -> None:
        """Handle window close event."""
        logger.info("Application closing", category="ui")
        
        try:
            from app.database.connection import db
            db.close()
        except Exception:
            pass
        
        self.destroy()
        sys.exit(0)
    
    def run(self) -> None:
        """Start the application."""
        logger.info("TallySync starting...", category="app")
        self.mainloop()
