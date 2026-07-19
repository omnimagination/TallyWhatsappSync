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
from app.database.repositories import (
    CompanyRepository,
    LedgerRepository,
    VoucherRepository,
    SyncLogRepository,
)


class DashboardPage(ctk.CTkScrollableFrame):
    """
    Dashboard page showing overview and statistics.
    """
    
    def __init__(self, master: Any, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self.configure(fg_color=UIStyles.COLOR_BG_DARK)
        
        self.company_repo = CompanyRepository()
        self.ledger_repo = LedgerRepository()
        self.voucher_repo = VoucherRepository()
        self.sync_log_repo = SyncLogRepository()
        
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
        
        refresh_btn = ctk.CTkButton(
            header_frame,
            text="Refresh",
            command=self.refresh,
            height=35,
            width=100,
        )
        refresh_btn.pack(side="right")
    
    def _create_stats_cards(self) -> None:
        """Create statistics cards."""
        # Get real data from database
        stats = self._get_stats()
        
        cards_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )
        cards_frame.pack(fill="x", pady=10)
        
        # Card data with real values
        card_data = [
            ("Companies", str(stats["companies"]), "[Companies]", UIStyles.COLOR_PRIMARY),
            ("Ledgers", str(stats["ledgers"]), "[Ledgers]", UIStyles.COLOR_SECONDARY),
            ("Vouchers", str(stats["vouchers"]), "[Vouchers]", UIStyles.COLOR_SUCCESS),
            ("Last Sync", stats["last_sync"], "[Sync]", UIStyles.COLOR_INFO),
        ]
        
        for label, value, icon, color in card_data:
            card = self._create_stat_card(cards_frame, label, value, icon, color)
            card.pack(side="left", padx=10, expand=True, fill="both")
    
    def _get_stats(self) -> dict:
        """Get statistics from database."""
        try:
            companies = self.company_repo.get_count()
            ledgers = self.ledger_repo.get_count()
            vouchers = self.voucher_repo.get_count()
            
            # Get last sync time
            recent_logs = self.sync_log_repo.get_recent(limit=1)
            if recent_logs:
                last_sync = recent_logs[0].formatted_start_time or "Never"
            else:
                last_sync = "Never"
            
            return {
                "companies": companies,
                "ledgers": ledgers,
                "vouchers": vouchers,
                "last_sync": last_sync,
            }
        except Exception as e:
            logger.error(f"Failed to get stats: {e}", category="ui")
            return {
                "companies": 0,
                "ledgers": 0,
                "vouchers": 0,
                "last_sync": "Error",
            }
    
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
        card.pack_propagate(False)
        
        # Icon
        icon_label = ctk.CTkLabel(
            card,
            text=icon,
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=color,
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
            text_color=UIStyles.COLOR_TEXT_PRIMARY,
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
            text="Recent Sync Activity",
            font=ctk.CTkFont(
                family=UIStyles.FONT_FAMILY,
                size=UIStyles.FONT_SIZE_HEADING,
                weight="bold",
            ),
            text_color=UIStyles.COLOR_TEXT_PRIMARY,
        )
        title.pack(padx=15, pady=(15, 10))
        
        # Get recent sync logs
        try:
            logs = self.sync_log_repo.get_recent(limit=5)
            
            if not logs:
                no_activity = ctk.CTkLabel(
                    activity_frame,
                    text="No sync activity yet. Go to Sync Center to start.",
                    font=ctk.CTkFont(
                        family=UIStyles.FONT_FAMILY,
                        size=UIStyles.FONT_SIZE_NORMAL,
                    ),
                    text_color=UIStyles.COLOR_TEXT_MUTED,
                )
                no_activity.pack(pady=20)
            else:
                for log in logs:
                    self._create_activity_item(activity_frame, log)
        except Exception as e:
            logger.error(f"Failed to load activity: {e}", category="ui")
    
    def _create_activity_item(self, master: Any, log) -> None:
        """Create an activity item."""
        item_frame = ctk.CTkFrame(
            master,
            fg_color=UIStyles.COLOR_BG_INPUT,
            corner_radius=UIStyles.CORNER_RADIUS_SMALL,
        )
        item_frame.pack(fill="x", padx=15, pady=2)
        
        status_color = UIStyles.COLOR_SUCCESS if log.is_success else UIStyles.COLOR_ERROR
        
        status_dot = ctk.CTkLabel(
            item_frame,
            text="?",
            font=ctk.CTkFont(size=12),
            text_color=status_color,
        )
        status_dot.pack(side="left", padx=(10, 10), pady=8)
        
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
        type_label.pack(side="left", padx=(0, 20), pady=8)
        
        time_label = ctk.CTkLabel(
            item_frame,
            text=log.formatted_start_time or "Unknown",
            font=ctk.CTkFont(
                family=UIStyles.FONT_FAMILY,
                size=UIStyles.FONT_SIZE_SMALL,
            ),
            text_color=UIStyles.COLOR_TEXT_SECONDARY,
        )
        time_label.pack(side="left", pady=8)
        
        records_label = ctk.CTkLabel(
            item_frame,
            text=f"{log.records_processed} records",
            font=ctk.CTkFont(
                family=UIStyles.FONT_FAMILY,
                size=UIStyles.FONT_SIZE_SMALL,
            ),
            text_color=UIStyles.COLOR_TEXT_SECONDARY,
        )
        records_label.pack(side="right", padx=(0, 10), pady=8)
    
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
        
        buttons_frame = ctk.CTkFrame(
            actions_frame,
            fg_color="transparent",
        )
        buttons_frame.pack(fill="x", padx=15, pady=10)
        
        actions = [
            ("[Sync Now]", "sync"),
            ("[Ledgers]", "ledgers"),
            ("[Vouchers]", "vouchers"),
            ("[Settings]", "settings"),
        ]
        
        for text, page in actions:
            btn = ctk.CTkButton(
                buttons_frame,
                text=text,
                command=lambda p=page: self._navigate(p),
                height=40,
                width=120,
            )
            btn.pack(side="left", padx=5, pady=5)
    
    def _navigate(self, page: str) -> None:
        """Navigate to page."""
        logger.debug(f"Quick action navigation: {page}", category="ui")
    
    def refresh(self) -> None:
        """Refresh dashboard data."""
        logger.debug("Dashboard refreshed", category="ui")
        # Rebuild stats cards
        for widget in self.winfo_children():
            widget.destroy()
        self._setup_ui()
