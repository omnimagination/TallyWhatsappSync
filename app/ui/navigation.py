"""
Navigation Sidebar for TallySync

Provides sidebar navigation with page switching.

Author: OmniMagination
Version: 1.0.0
"""

import customtkinter as ctk
from typing import Callable, Dict, Any
from app.ui.styles import UIStyles


class NavigationSidebar(ctk.CTkFrame):
    """
    Sidebar navigation component.
    """
    
    def __init__(
        self,
        master: Any,
        on_page_change: Callable[[str], None],
        **kwargs,
    ) -> None:
        super().__init__(master, **kwargs)
        
        self.on_page_change = on_page_change
        self.current_page = "dashboard"
        self.buttons: Dict[str, ctk.CTkButton] = {}
        
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Setup sidebar UI components."""
        self.configure(
            fg_color=UIStyles.COLOR_BG_SIDEBAR,
            width=UIStyles.SIDEBAR_WIDTH,
        )
        
        self._create_header()
        self._create_navigation()
        self._create_bottom_section()
    
    def _create_header(self) -> None:
        """Create header with app logo/title."""
        header_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
            height=80,
        )
        header_frame.pack(fill="x", padx=15, pady=(20, 10))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="TallySync",
            font=ctk.CTkFont(
                family=UIStyles.FONT_FAMILY,
                size=22,
                weight="bold",
            ),
            text_color=UIStyles.COLOR_TEXT_PRIMARY,
        )
        title_label.pack(pady=(10, 5))
        
        version_label = ctk.CTkLabel(
            header_frame,
            text="v1.0.0",
            font=ctk.CTkFont(
                family=UIStyles.FONT_FAMILY,
                size=11,
            ),
            text_color=UIStyles.COLOR_TEXT_MUTED,
        )
        version_label.pack()
    
    def _create_navigation(self) -> None:
        """Create navigation buttons."""
        # Using text icons that render reliably on Windows
        nav_items = [
            ("dashboard", "[Dashboard]", "Dashboard"),
            ("ledgers", "[Ledgers]", "Ledgers"),
            ("vouchers", "[Vouchers]", "Vouchers"),
            ("whatsapp", "[WhatsApp]", "WhatsApp"),
            ("sync", "[Sync]", "Sync Center"),
        ]
        
        nav_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )
        nav_frame.pack(fill="x", padx=10, pady=10)
        
        for page_id, icon, label in nav_items:
            button = self._create_nav_button(page_id, icon, label)
            button.pack(fill="x", pady=2)
            self.buttons[page_id] = button
        
        self.set_active("dashboard")
    
    def _create_nav_button(
        self,
        page_id: str,
        icon: str,
        label: str,
    ) -> ctk.CTkButton:
        """Create a navigation button."""
        button = ctk.CTkButton(
            self,
            text=f"{icon}",
            command=lambda: self._on_button_click(page_id),
            anchor="w",
            height=45,
            corner_radius=UIStyles.CORNER_RADIUS_NORMAL,
            fg_color="transparent",
            hover_color=UIStyles.COLOR_BG_CARD,
            text_color=UIStyles.COLOR_TEXT_SECONDARY,
            font=ctk.CTkFont(
                family=UIStyles.FONT_FAMILY,
                size=UIStyles.FONT_SIZE_NORMAL,
                weight="bold",
            ),
        )
        return button
    
    def _create_bottom_section(self) -> None:
        """Create bottom section with settings and logs."""
        bottom_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )
        bottom_frame.pack(side="bottom", fill="x", padx=10, pady=10)
        
        settings_btn = self._create_nav_button("settings", "[Settings]", "Settings")
        settings_btn.pack(fill="x", pady=2)
        self.buttons["settings"] = settings_btn
        
        logs_btn = self._create_nav_button("logs", "[Logs]", "Logs")
        logs_btn.pack(fill="x", pady=2)
        self.buttons["logs"] = logs_btn
    
    def _on_button_click(self, page_id: str) -> None:
        """Handle navigation button click."""
        if page_id == self.current_page:
            return
        
        self.set_active(page_id)
        self.on_page_change(page_id)
    
    def set_active(self, page_id: str) -> None:
        """Set active page and update button styles."""
        self.current_page = page_id
        
        for pid, button in self.buttons.items():
            if pid == page_id:
                button.configure(
                    fg_color=UIStyles.COLOR_PRIMARY,
                    text_color=UIStyles.COLOR_TEXT_PRIMARY,
                )
            else:
                button.configure(
                    fg_color="transparent",
                    text_color=UIStyles.COLOR_TEXT_SECONDARY,
                )
    
    def get_current_page(self) -> str:
        """Get current active page ID."""
        return self.current_page
