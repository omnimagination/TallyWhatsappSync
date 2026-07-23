"""
Ledgers Page for TallySync

Search and display ledger accounts.

Author: OmniMagination
Version: 1.0.0
"""

import customtkinter as ctk
from typing import Any, Optional, List

from app.ui.styles import UIStyles
from app.core.logger import logger
from app.database.repositories import LedgerRepository
from app.database.models import Ledger


class LedgersPage(ctk.CTkScrollableFrame):
    """
    Ledgers page for searching and viewing ledger accounts.
    """
    
    def __init__(self, master: Any, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self.configure(fg_color=UIStyles.COLOR_BG_DARK)
        
        self.ledger_repo = LedgerRepository()
        self.current_ledgers: List[Ledger] = []
        
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Setup ledgers UI."""
        # Header with search
        self._create_header()
        
        # Filters
        self._create_filters()
        
        # Ledger list
        self._create_ledger_list()
    
    def _create_header(self) -> None:
        """Create page header with search."""
        header_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )
        header_frame.pack(fill="x", pady=(0, 10))
        
        # Title
        title = ctk.CTkLabel(
            header_frame,
            text="Ledgers",
            font=ctk.CTkFont(
                family=UIStyles.FONT_FAMILY,
                size=UIStyles.FONT_SIZE_TITLE,
                weight="bold",
            ),
            text_color=UIStyles.COLOR_TEXT_PRIMARY,
        )
        title.pack(side="left")
        
        # Search box
        search_frame = ctk.CTkFrame(
            header_frame,
            fg_color="transparent",
        )
        search_frame.pack(side="right")
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search ledgers...",
            width=300,
            **UIStyles.get_entry_style(),
        )
        self.search_entry.pack(side="left", padx=(0, 10))
        self.search_entry.bind("<KeyRelease>", self._on_search)
        
        # Search button
        search_btn = ctk.CTkButton(
            search_frame,
            text="?? Search",
            command=self._search_ledgers,
        )
        search_btn.pack(side="left")
    
    def _create_filters(self) -> None:
        """Create filter options."""
        filter_frame = ctk.CTkFrame(
            self,
            fg_color=UIStyles.COLOR_BG_CARD,
            corner_radius=UIStyles.CORNER_RADIUS_NORMAL,
        )
        filter_frame.pack(fill="x", pady=10)
        
        # Group filter
        ctk.CTkLabel(
            filter_frame,
            text="Filter by Group:",
            font=ctk.CTkFont(
                family=UIStyles.FONT_FAMILY,
                size=UIStyles.FONT_SIZE_NORMAL,
            ),
            text_color=UIStyles.COLOR_TEXT_PRIMARY,
        ).pack(side="left", padx=(15, 10), pady=10)
        
        self.group_filter = ctk.CTkComboBox(
            filter_frame,
            values=["All", "Sundry Debtors", "Sundry Creditors", "Cash", "Bank", "Other"],
            width=200,
            command=self._apply_filters,
        )
        self.group_filter.pack(side="left", padx=10, pady=10)
        self.group_filter.set("All")
        
        # Active filter
        self.active_filter = ctk.CTkCheckBox(
            filter_frame,
            text="Active Only",
            command=self._apply_filters,
        )
        self.active_filter.pack(side="left", padx=20, pady=10)
        self.active_filter.select()
        
        # Count label
        self.count_label = ctk.CTkLabel(
            filter_frame,
            text="0 ledgers",
            font=ctk.CTkFont(
                family=UIStyles.FONT_FAMILY,
                size=UIStyles.FONT_SIZE_SMALL,
            ),
            text_color=UIStyles.COLOR_TEXT_SECONDARY,
        )
        self.count_label.pack(side="right", padx=15, pady=10)
    
    def _create_ledger_list(self) -> None:
        """Create ledger list display."""
        list_frame = ctk.CTkFrame(
            self,
            fg_color=UIStyles.COLOR_BG_CARD,
            corner_radius=UIStyles.CORNER_RADIUS_NORMAL,
        )
        list_frame.pack(fill="both", expand=True, pady=10)
        
        # Header row
        header_frame = ctk.CTkFrame(
            list_frame,
            fg_color=UIStyles.COLOR_BG_INPUT,
        )
        header_frame.pack(fill="x", padx=1, pady=1)
        
        headers = [
            ("Name", 300),
            ("Group", 150),
            ("Balance", 120),
            ("Phone", 120),
            ("Email", 150),
        ]
        
        for text, width in headers:
            label = ctk.CTkLabel(
                header_frame,
                text=text,
                font=ctk.CTkFont(
                    family=UIStyles.FONT_FAMILY,
                    size=UIStyles.FONT_SIZE_NORMAL,
                    weight="bold",
                ),
                text_color=UIStyles.COLOR_TEXT_PRIMARY,
                width=width,
                anchor="w",
            )
            label.pack(side="left", padx=10, pady=10)
        
        # Scrollable ledger list
        self.ledger_list_frame = ctk.CTkFrame(
            list_frame,
            fg_color="transparent",
        )
        self.ledger_list_frame.pack(fill="both", expand=True, padx=1, pady=1)
    
    def _on_search(self, event=None) -> None:
        """Handle search input."""
        self._search_ledgers()
    
    def _search_ledgers(self) -> None:
        """Search ledgers based on input."""
        search_term = self.search_entry.get().strip()
        
        try:
            if search_term:
                self.current_ledgers = self.ledger_repo.search_ledgers(
                    company_id="",
                    search_term=search_term,
                    limit=100,
                )
            else:
                self.current_ledgers = self.ledger_repo.get_all(limit=100)
            
            self._apply_filters()
        
        except Exception as e:
            logger.error(f"Search failed: {e}", category="ui")
            self.current_ledgers = []
        
        self._render_ledger_list()
    
    def _apply_filters(self, *args) -> None:
        """Apply filters to ledger list."""
        group = self.group_filter.get()
        active_only = self.active_filter.get()
        
        filtered = self.current_ledgers
        
        if group != "All":
            filtered = [l for l in filtered if group.lower() in (l.group_name or "").lower()]
        
        if active_only:
            filtered = [l for l in filtered if l.is_active]
        
        self.current_ledgers = filtered
        self._render_ledger_list()
    
    def _render_ledger_list(self) -> None:
        """Render ledger list in UI."""
        # Clear existing
        for widget in self.ledger_list_frame.winfo_children():
            widget.destroy()
        
        # Update count
        self.count_label.configure(text=f"{len(self.current_ledgers)} ledgers")
        
        if not self.current_ledgers:
            no_data = ctk.CTkLabel(
                self.ledger_list_frame,
                text="No ledgers found. Run a sync to load data from Tally.",
                font=ctk.CTkFont(
                    family=UIStyles.FONT_FAMILY,
                    size=UIStyles.FONT_SIZE_NORMAL,
                ),
                text_color=UIStyles.COLOR_TEXT_MUTED,
            )
            no_data.pack(pady=30)
            return
        
        # Render ledgers
        for ledger in self.current_ledgers[:100]:
            self._create_ledger_row(ledger)
    
    def _create_ledger_row(self, ledger: Ledger) -> None:
        """Create a ledger row in the list."""
        row_frame = ctk.CTkFrame(
            self.ledger_list_frame,
            fg_color=UIStyles.COLOR_BG_INPUT,
            corner_radius=0,
        )
        row_frame.pack(fill="x", padx=1, pady=1)
        
        # Name
        name_label = ctk.CTkLabel(
            row_frame,
            text=ledger.name[:40],
            font=ctk.CTkFont(
                family=UIStyles.FONT_FAMILY,
                size=UIStyles.FONT_SIZE_SMALL,
            ),
            text_color=UIStyles.COLOR_TEXT_PRIMARY,
            width=300,
            anchor="w",
        )
        name_label.pack(side="left", padx=10, pady=8)
        
        # Group
        group_label = ctk.CTkLabel(
            row_frame,
            text=(ledger.group_name or "N/A")[:20],
            font=ctk.CTkFont(
                family=UIStyles.FONT_FAMILY,
                size=UIStyles.FONT_SIZE_SMALL,
            ),
            text_color=UIStyles.COLOR_TEXT_SECONDARY,
            width=150,
            anchor="w",
        )
        group_label.pack(side="left", padx=10, pady=8)
        
        # Balance
        balance_label = ctk.CTkLabel(
            row_frame,
            text=ledger.balance_with_sign,
            font=ctk.CTkFont(
                family=UIStyles.FONT_FAMILY,
                size=UIStyles.FONT_SIZE_SMALL,
            ),
            text_color=UIStyles.COLOR_SUCCESS if ledger.closing_balance > 0 else UIStyles.COLOR_TEXT_SECONDARY,
            width=120,
            anchor="w",
        )
        balance_label.pack(side="left", padx=10, pady=8)
        
        # Phone
        phone_label = ctk.CTkLabel(
            row_frame,
            text=ledger.phone or "-",
            font=ctk.CTkFont(
                family=UIStyles.FONT_FAMILY,
                size=UIStyles.FONT_SIZE_SMALL,
            ),
            text_color=UIStyles.COLOR_TEXT_SECONDARY,
            width=120,
            anchor="w",
        )
        phone_label.pack(side="left", padx=10, pady=8)
        
        # Email
        email_label = ctk.CTkLabel(
            row_frame,
            text=(ledger.email or "-")[:20],
            font=ctk.CTkFont(
                family=UIStyles.FONT_FAMILY,
                size=UIStyles.FONT_SIZE_SMALL,
            ),
            text_color=UIStyles.COLOR_TEXT_SECONDARY,
            width=150,
            anchor="w",
        )
        email_label.pack(side="left", padx=10, pady=8)
        
        # Bind click event
        row_frame.bind("<Button-1>", lambda e, l=ledger: self._on_ledger_click(l))
        for widget in row_frame.winfo_children():
            widget.bind("<Button-1>", lambda e, l=ledger: self._on_ledger_click(l))
    
    def _on_ledger_click(self, ledger: Ledger) -> None:
        """Handle ledger click."""
        logger.info(f"Ledger selected: {ledger.name}", category="ui")
    
    def refresh(self) -> None:
        """Refresh ledger list."""
        self._search_ledgers()
        logger.debug("Ledgers page refreshed", category="ui")
