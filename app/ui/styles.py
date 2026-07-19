"""
UI Styles for TallySync

Defines colors, fonts, and styling constants.

Author: OmniMagination
Version: 1.0.0
"""

import customtkinter as ctk


class UIStyles:
    """
    Centralized styling for TallySync UI.
    
    Provides consistent colors, fonts, and visual properties.
    """
    
    # Color Palette - Dark Theme
    COLOR_PRIMARY = "#2563EB"        # Blue
    COLOR_PRIMARY_HOVER = "#1D4ED8"  # Darker Blue
    COLOR_SECONDARY = "#7C3AED"      # Purple
    COLOR_SUCCESS = "#10B981"        # Green
    COLOR_WARNING = "#F59E0B"        # Orange
    COLOR_ERROR = "#EF4444"          # Red
    COLOR_INFO = "#3B82F6"           # Light Blue
    
    # Background Colors
    COLOR_BG_DARK = "#1E1E1E"        # Main background
    COLOR_BG_CARD = "#2D2D2D"        # Card background
    COLOR_BG_SIDEBAR = "#181818"     # Sidebar background
    COLOR_BG_INPUT = "#3D3D3D"       # Input field background
    
    # Text Colors
    COLOR_TEXT_PRIMARY = "#FFFFFF"   # Primary text
    COLOR_TEXT_SECONDARY = "#A0A0A0" # Secondary text
    COLOR_TEXT_MUTED = "#6B6B6B"     # Muted text
    
    # Border Colors
    COLOR_BORDER = "#404040"         # Border color
    COLOR_BORDER_FOCUS = "#2563EB"   # Focus border
    
    # Glass Effect
    GLASS_ALPHA = 0.95
    GLASS_BLUR = 10
    
    # Fonts
    FONT_FAMILY = "Segoe UI"
    FONT_SIZE_SMALL = 11
    FONT_SIZE_NORMAL = 13
    FONT_SIZE_MEDIUM = 15
    FONT_SIZE_LARGE = 18
    FONT_SIZE_TITLE = 24
    FONT_SIZE_HEADING = 20
    
    # Spacing
    PADDING_SMALL = 5
    PADDING_NORMAL = 10
    PADDING_MEDIUM = 15
    PADDING_LARGE = 20
    
    # Corner Radius
    CORNER_RADIUS_SMALL = 5
    CORNER_RADIUS_NORMAL = 10
    CORNER_RADIUS_LARGE = 15
    
    # Sidebar
    SIDEBAR_WIDTH = 240
    SIDEBAR_WIDTH_COLLAPSED = 60
    
    # Window
    WINDOW_MIN_WIDTH = 1024
    WINDOW_MIN_HEIGHT = 600
    WINDOW_DEFAULT_WIDTH = 1280
    WINDOW_DEFAULT_HEIGHT = 720
    
    @classmethod
    def configure_appearance(cls) -> None:
        """Configure CustomTkinter appearance."""
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
    
    @classmethod
    def get_button_style(cls, **kwargs) -> dict:
        """Get standard button style."""
        style = {
            "fg_color": cls.COLOR_PRIMARY,
            "hover_color": cls.COLOR_PRIMARY_HOVER,
            "text_color": cls.COLOR_TEXT_PRIMARY,
            "font": ctk.CTkFont(
                family=cls.FONT_FAMILY,
                size=cls.FONT_SIZE_NORMAL,
                weight="normal",
            ),
            "corner_radius": cls.CORNER_RADIUS_NORMAL,
            "height": 35,
        }
        style.update(kwargs)
        return style
    
    @classmethod
    def get_card_style(cls, **kwargs) -> dict:
        """Get card/frame style."""
        style = {
            "fg_color": cls.COLOR_BG_CARD,
            "corner_radius": cls.CORNER_RADIUS_NORMAL,
            "border_width": 1,
            "border_color": cls.COLOR_BORDER,
        }
        style.update(kwargs)
        return style
    
    @classmethod
    def get_entry_style(cls, **kwargs) -> dict:
        """Get entry/textbox style."""
        style = {
            "fg_color": cls.COLOR_BG_INPUT,
            "border_color": cls.COLOR_BORDER,
            "text_color": cls.COLOR_TEXT_PRIMARY,
            "font": ctk.CTkFont(
                family=cls.FONT_FAMILY,
                size=cls.FONT_SIZE_NORMAL,
            ),
            "corner_radius": cls.CORNER_RADIUS_SMALL,
            "height": 35,
        }
        style.update(kwargs)
        return style
    
    @classmethod
    def get_label_style(cls, size: str = "normal", **kwargs) -> dict:
        """Get label style."""
        font_sizes = {
            "small": cls.FONT_SIZE_SMALL,
            "normal": cls.FONT_SIZE_NORMAL,
            "medium": cls.FONT_SIZE_MEDIUM,
            "large": cls.FONT_SIZE_LARGE,
            "title": cls.FONT_SIZE_TITLE,
            "heading": cls.FONT_SIZE_HEADING,
        }
        
        style = {
            "text_color": cls.COLOR_TEXT_PRIMARY,
            "font": ctk.CTkFont(
                family=cls.FONT_FAMILY,
                size=font_sizes.get(size, cls.FONT_SIZE_NORMAL),
                weight="bold" if size in ["title", "heading"] else "normal",
            ),
        }
        style.update(kwargs)
        return style
    
    @classmethod
    def get_status_colors(cls) -> dict:
        """Get status indicator colors."""
        return {
            "success": cls.COLOR_SUCCESS,
            "warning": cls.COLOR_WARNING,
            "error": cls.COLOR_ERROR,
            "info": cls.COLOR_INFO,
            "default": cls.COLOR_TEXT_SECONDARY,
        }
    
    @classmethod
    def get_sidebar_style(cls) -> dict:
        """Get sidebar style."""
        return {
            "fg_color": cls.COLOR_BG_SIDEBAR,
            "width": cls.SIDEBAR_WIDTH,
        }
    
    @classmethod
    def get_table_header_style(cls) -> dict:
        """Get table header style."""
        return {
            "fg_color": cls.COLOR_BG_CARD,
            "text_color": cls.COLOR_TEXT_PRIMARY,
            "font": ctk.CTkFont(
                family=cls.FONT_FAMILY,
                size=cls.FONT_SIZE_NORMAL,
                weight="bold",
            ),
        }
    
    @classmethod
    def get_table_row_style(cls) -> dict:
        """Get table row style."""
        return {
            "fg_color": cls.COLOR_BG_INPUT,
            "text_color": cls.COLOR_TEXT_PRIMARY,
            "font": ctk.CTkFont(
                family=cls.FONT_FAMILY,
                size=cls.FONT_SIZE_SMALL,
            ),
        }
