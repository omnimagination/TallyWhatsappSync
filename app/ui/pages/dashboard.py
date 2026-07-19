"""
Dashboard Page for TallySync

Main dashboard with company info and statistics.

Author: OmniMagination
Version: 1.0.0
"""

import customtkinter as ctk
from typing import Any
from app.ui.styles import UIStyles
from app.core.logger import logger


class DashboardPage(ctk.CTkScrollableFrame):
    """
    Dashboard page showing overview and statistics.
    """
    
    def __init__(self, master: Any, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self.configure(fg_color=UIStyles.COLOR_BG_DARK)
        
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Setup dashboard UI."""
        # Header
        self._create_header()
        
        # Stats Cards
        self._create_stats_cards()
        
        # Recent Activity
        self._create_recent_activity()
        
        # Quick Actions
        self._create_quick_actions()
    
    def _create_header(self) -> None:
        """Create dashboard header."""
        header_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )
        header_frame.pack(fill="x", pady=(0, 20))
        
        title = ctk.CTkLabel(
            header_frame,
            text="Dashboard",
            font=ctk.CTkFont(
                family=UIStyles.FONT_FAMILY,
                size=UIStyles.FONT_SIZE_TITLE,
                weight="bold",
            ),
            text_color=UIStyles.COLOR_TEXT_PRIMARY,
        )
        title.pack(side="left")
        
        # Refresh button
        refresh_btn = ctk.CTkButton(
            header_frame,
            text="?? Refresh",
            command=self.refresh,
            height=35,
            width=100,
        )
        refresh_btn.pack(side="right")
    
    def _create_stats_cards(self) -> None:
        """Create statistics cards."""
        # Section title
        title = ctk.CTkLabel(
            self,
            text="Overview",
            font=ctk.CTkFont(
                family=UIStyles.FONT_FAMILY,
                size=UIStyles.FONT_SIZE_HEADING,
                weight="bold",
            ),
            text_color=UIStyles.COLOR_TEXT_PRIMARY,
        )
        title.pack(anchor="w", pady=(10, 10))
        
        # Cards container
        cards_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )
        cards_frame.pack(fill="x", pady=10)
        
        # Card data
        stats = [
            ("Companies", "0", "??", UIStyles.COLOR_PRIMARY),
            ("Ledgers", "0", "??", UIStyles.COLOR_SECONDARY),
            ("Vouchers", "0", "??", UIStyles.COLOR_SUCCESS),
            ("Sync Status", "Ready", "??", UIStyles.COLOR_INFO),
        ]
        
        # Create cards in a row using pack with side
        for label, value, icon, color in stats:
            card = self._create_stat_card(cards_frame, label, value, icon, color)
            card.pack(side="left", padx=10, expand=True, fill="both")
    
    def _create_stat_card(
        self,
        master: Any,
        label: str,
        value: str,
        icon: str,
        color: str,
    ) -> ctk.CTkFrame:
        """Create a statistics card."""
        card = ctk.CTkFrame(
            master,
            fg_color=UIStyles.COLOR_BG_CARD,
            corner_radius=UIStyles.CORNER_RADIUS_NORMAL,
            width=200,
            height=140,
        )
        card.pack_propagate(False)  # Prevent resizing
        
        # Icon
        icon_label = ctk.CTkLabel(
            card,
            text=icon,
            font=ctk.CTkFont(size=30),
        )
        icon_label.pack(pady=(15, 5))
        
        # Value
        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(
                family=UIStyles.FONT_FAMILY,
                size=24,
                weight="bold",
            ),
            text_color=color,
        )
        value_label.pack()
        
        # Label
        label_label = ctk.CTkLabel(
            card,
            text=label,
            font=ctk.CTkFont(
                family=UIStyles.FONT_FAMILY,
                size=UIStyles.FONT_SIZE_SMALL,
            ),
            text_color=UIStyles.COLOR_TEXT_SECONDARY,
        )
        label_label.pack(pady=(0, 15))
        
        return card
    
    def _create_recent_activity(self) -> None:
        """Create recent activity section."""
        activity_frame = ctk.CTkFrame(
            self,
            fg_color=UIStyles.COLOR_BG_CARD,
            corner_radius=UIStyles.CORNER_RADIUS_NORMAL,
        )
        activity_frame.pack(fill="x", pady=20)
        
        title = ctk.CTkLabel(
            activity_frame,
            text="Recent Activity",
            font=ctk.CTkFont(
                family=UIStyles.FONT_FAMILY,
                size=UIStyles.FONT_SIZE_HEADING,
                weight="bold",
            ),
            text_color=UIStyles.COLOR_TEXT_PRIMARY,
        )
        title.pack(padx=15, pady=(15, 10))
        
        # Activity list (placeholder)
        activity_list = ctk.CTkFrame(
            activity_frame,
            fg_color="transparent",
        )
        activity_list.pack(fill="x", padx=15, pady=10)
        
        no_activity = ctk.CTkLabel(
            activity_list,
            text="No recent activity - Run a sync to see data",
            font=ctk.CTkFont(
                family=UIStyles.FONT_FAMILY,
                size=UIStyles.FONT_SIZE_NORMAL,
            ),
            text_color=UIStyles.COLOR_TEXT_MUTED,
        )
        no_activity.pack(pady=20)
    
    def _create_quick_actions(self) -> None:
        """Create quick actions section."""
        actions_frame = ctk.CTkFrame(
            self,
            fg_color=UIStyles.COLOR_BG_CARD,
            corner_radius=UIStyles.CORNER_RADIUS_NORMAL,
        )
        actions_frame.pack(fill="x", pady=20)
        
        title = ctk.CTkLabel(
            actions_frame,
            text="Quick Actions",
            font=ctk.CTkFont(
                family=UIStyles.FONT_FAMILY,
                size=UIStyles.FONT_SIZE_HEADING,
                weight="bold",
            ),
            text_color=UIStyles.COLOR_TEXT_PRIMARY,
        )
        title.pack(padx=15, pady=(15, 10))
        
        # Action buttons
        buttons_frame = ctk.CTkFrame(
            actions_frame,
            fg_color="transparent",
        )
        buttons_frame.pack(fill="x", padx=15, pady=10)
        
        actions = [
            ("?? Sync Now", "sync"),
            ("?? View Ledgers", "ledgers"),
            ("?? View Vouchers", "vouchers"),
            ("?? Settings", "settings"),
        ]
        
        for text, page in actions:
            btn = ctk.CTkButton(
                buttons_frame,
                text=text,
                command=lambda p=page: self._navigate(p),
                height=40,
                width=150,
            )
            btn.pack(side="left", padx=5, pady=5)
    
    def _navigate(self, page: str) -> None:
        """Navigate to page (callback to main window)."""
        logger.debug(f"Quick action navigation: {page}", category="ui")
    
    def refresh(self) -> None:
        """Refresh dashboard data."""
        logger.debug("Dashboard refreshed", category="ui")
        self.update_status("Dashboard refreshed")
    
    def update_status(self, message: str) -> None:
        """Update status (called from main window)."""
        pass
