import customtkinter as ctk
from typing import Any
from app.ui.styles import UIStyles

class LogsPage(ctk.CTkScrollableFrame):
    def __init__(self, master: Any, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self.configure(fg_color=UIStyles.COLOR_BG_DARK)
        
        label = ctk.CTkLabel(
            self,
            text="Application Logs",
            font=ctk.CTkFont(family=UIStyles.FONT_FAMILY, size=24),
            text_color=UIStyles.COLOR_TEXT_PRIMARY,
        )
        label.pack(pady=50)
        
        desc = ctk.CTkLabel(
            self,
            text="Log viewer coming soon...",
            font=ctk.CTkFont(family=UIStyles.FONT_FAMILY, size=14),
            text_color=UIStyles.COLOR_TEXT_SECONDARY,
        )
        desc.pack()
    
    def refresh(self) -> None:
        pass
