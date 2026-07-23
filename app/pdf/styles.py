"""
PDF Styles for TallySync

Defines colors, fonts, and styling for PDF documents.

Author: OmniMagination
Version: 1.0.0
"""

from reportlab.lib import colors
from reportlab.lib.units import inch, cm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT


class PDFStyles:
    """
    Centralized styling for PDF documents.
    """
    
    # Colors
    COLOR_PRIMARY = colors.HexColor("#2563EB")
    COLOR_SECONDARY = colors.HexColor("#1E1E1E")
    COLOR_SUCCESS = colors.HexColor("#10B981")
    COLOR_WARNING = colors.HexColor("#F59E0B")
    COLOR_ERROR = colors.HexColor("#EF4444")
    COLOR_TEXT = colors.HexColor("#333333")
    COLOR_TEXT_LIGHT = colors.HexColor("#666666")
    COLOR_BORDER = colors.HexColor("#E0E0E0")
    COLOR_TABLE_HEADER = colors.HexColor("#F5F5F5")
    
    # Fonts
    FONT_FAMILY = "Helvetica"
    FONT_FAMILY_BOLD = "Helvetica-Bold"
    FONT_SIZE_SMALL = 8
    FONT_SIZE_NORMAL = 10
    FONT_SIZE_MEDIUM = 12
    FONT_SIZE_LARGE = 14
    FONT_SIZE_TITLE = 18
    FONT_SIZE_HEADING = 16
    
    # Page Setup
    PAGE_WIDTH = 8.27 * inch  # A4 width
    PAGE_HEIGHT = 11.69 * inch  # A4 height
    PAGE_MARGIN = 0.75 * inch
    CONTENT_WIDTH = PAGE_WIDTH - (2 * PAGE_MARGIN)
    
    # Table Styles
    TABLE_CELL_PADDING = 6
    TABLE_ROW_HEIGHT = 20
    TABLE_HEADER_HEIGHT = 25
    TABLE_BORDER_WIDTH = 0.5
    
    # Spacing
    SPACING_SMALL = 0.25 * inch
    SPACING_NORMAL = 0.5 * inch
    SPACING_LARGE = 0.75 * inch
    
    @classmethod
    def get_title_style(cls) -> dict:
        """Get title text style."""
        return {
            "fontName": cls.FONT_FAMILY_BOLD,
            "fontSize": cls.FONT_SIZE_TITLE,
            "textColor": cls.COLOR_PRIMARY,
            "alignment": TA_LEFT,
            "spaceAfter": cls.SPACING_NORMAL,
        }
    
    @classmethod
    def get_heading_style(cls) -> dict:
        """Get heading text style."""
        return {
            "fontName": cls.FONT_FAMILY_BOLD,
            "fontSize": cls.FONT_SIZE_HEADING,
            "textColor": cls.COLOR_SECONDARY,
            "alignment": TA_LEFT,
            "spaceAfter": cls.SPACING_SMALL,
        }
    
    @classmethod
    def get_normal_style(cls) -> dict:
        """Get normal text style."""
        return {
            "fontName": cls.FONT_FAMILY,
            "fontSize": cls.FONT_SIZE_NORMAL,
            "textColor": cls.COLOR_TEXT,
            "alignment": TA_LEFT,
            "spaceAfter": 6,
        }
    
    @classmethod
    def get_small_style(cls) -> dict:
        """Get small text style."""
        return {
            "fontName": cls.FONT_FAMILY,
            "fontSize": cls.FONT_SIZE_SMALL,
            "textColor": cls.COLOR_TEXT_LIGHT,
            "alignment": TA_LEFT,
        }
    
    @classmethod
    def get_right_align_style(cls) -> dict:
        """Get right-aligned text style."""
        return {
            "fontName": cls.FONT_FAMILY,
            "fontSize": cls.FONT_SIZE_NORMAL,
            "textColor": cls.COLOR_TEXT,
            "alignment": TA_RIGHT,
        }
    
    @classmethod
    def get_center_align_style(cls) -> dict:
        """Get center-aligned text style."""
        return {
            "fontName": cls.FONT_FAMILY,
            "fontSize": cls.FONT_SIZE_NORMAL,
            "textColor": cls.COLOR_TEXT,
            "alignment": TA_CENTER,
        }
    
    @classmethod
    def get_table_style(cls) -> dict:
        """Get table style."""
        return {
            "fontName": cls.FONT_FAMILY,
            "fontSize": cls.FONT_SIZE_SMALL,
            "textColor": cls.COLOR_TEXT,
            "alignment": TA_LEFT,
            "valign": "TOP",
            "leftPadding": cls.TABLE_CELL_PADDING,
            "rightPadding": cls.TABLE_CELL_PADDING,
            "topPadding": 4,
            "bottomPadding": 4,
        }
    
    @classmethod
    def get_table_header_style(cls) -> dict:
        """Get table header style."""
        return {
            "fontName": cls.FONT_FAMILY_BOLD,
            "fontSize": cls.FONT_SIZE_SMALL,
            "textColor": cls.COLOR_SECONDARY,
            "alignment": TA_LEFT,
            "valign": "MIDDLE",
            "leftPadding": cls.TABLE_CELL_PADDING,
            "rightPadding": cls.TABLE_CELL_PADDING,
            "topPadding": 6,
            "bottomPadding": 6,
            "bgColor": cls.COLOR_TABLE_HEADER,
        }
    
    @classmethod
    def get_amount_style(cls) -> dict:
        """Get amount/number style."""
        return {
            "fontName": cls.FONT_FAMILY,
            "fontSize": cls.FONT_SIZE_NORMAL,
            "textColor": cls.COLOR_TEXT,
            "alignment": TA_RIGHT,
        }
