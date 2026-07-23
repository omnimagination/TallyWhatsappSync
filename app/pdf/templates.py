"""
PDF Templates for TallySync

Pre-built templates for different document types.

Author: OmniMagination
Version: 1.0.0
"""

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
)
from reportlab.lib import colors
from reportlab.lib.units import inch, cm
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from datetime import datetime
from typing import Optional, List, Dict, Any

from app.pdf.styles import PDFStyles
from app.core.utils import format_currency, format_date


class StatementTemplate:
    """
    Template for ledger account statements.
    """
    
    def __init__(self, doc: SimpleDocTemplate) -> None:
        """Initialize template with document."""
        self.doc = doc
        self.styles = getSampleStyleSheet()
        self.story: List = []
    
    def add_header(
        self,
        company_name: str,
        company_address: str = "",
        company_phone: str = "",
        company_email: str = "",
        company_gst: str = "",
    ) -> None:
        """Add document header with company info."""
        # Company name
        company_para = Paragraph(
            company_name,
            self._create_style(
                fontName="Helvetica-Bold",
                fontSize=16,
                textColor=PDFStyles.COLOR_PRIMARY,
                alignment=TA_CENTER,
                spaceAfter=6,
            ),
        )
        self.story.append(company_para)
        
        # Company address
        if company_address:
            address_para = Paragraph(
                company_address.replace("\n", "<br/>"),
                self._create_style(
                    fontName="Helvetica",
                    fontSize=9,
                    textColor=PDFStyles.COLOR_TEXT_LIGHT,
                    alignment=TA_CENTER,
                    spaceAfter=3,
                ),
            )
            self.story.append(address_para)
        
        # Contact info
        contact_parts = []
        if company_phone:
            contact_parts.append(f"Phone: {company_phone}")
        if company_email:
            contact_parts.append(f"Email: {company_email}")
        if company_gst:
            contact_parts.append(f"GST: {company_gst}")
        
        if contact_parts:
            contact_para = Paragraph(
                " | ".join(contact_parts),
                self._create_style(
                    fontName="Helvetica",
                    fontSize=8,
                    textColor=PDFStyles.COLOR_TEXT_LIGHT,
                    alignment=TA_CENTER,
                    spaceAfter=12,
                ),
            )
            self.story.append(contact_para)
        
        # Separator line
        self.story.append(Spacer(1, 6))
    
    def add_title(self, title: str, subtitle: str = "") -> None:
        """Add document title."""
        title_para = Paragraph(
            title,
            self._create_style(
                fontName="Helvetica-Bold",
                fontSize=14,
                textColor=PDFStyles.COLOR_SECONDARY,
                alignment=TA_CENTER,
                spaceAfter=3,
            ),
        )
        self.story.append(title_para)
        
        if subtitle:
            subtitle_para = Paragraph(
                subtitle,
                self._create_style(
                    fontName="Helvetica",
                    fontSize=10,
                    textColor=PDFStyles.COLOR_TEXT_LIGHT,
                    alignment=TA_CENTER,
                    spaceAfter=12,
                ),
            )
            self.story.append(subtitle_para)
        else:
            self.story.append(Spacer(1, 12))
    
    def add_ledger_info(
        self,
        ledger_name: str,
        ledger_group: str = "",
        ledger_phone: str = "",
        ledger_email: str = "",
        ledger_gst: str = "",
    ) -> None:
        """Add ledger account information."""
        # Ledger name
        ledger_para = Paragraph(
            f"Account: <b>{ledger_name}</b>",
            self._create_style(
                fontName="Helvetica",
                fontSize=11,
                textColor=PDFStyles.COLOR_TEXT,
                alignment=TA_LEFT,
                spaceAfter=3,
            ),
        )
        self.story.append(ledger_para)
        
        # Ledger details
        details_parts = []
        if ledger_group:
            details_parts.append(f"Group: {ledger_group}")
        if ledger_phone:
            details_parts.append(f"Phone: {ledger_phone}")
        if ledger_email:
            details_parts.append(f"Email: {ledger_email}")
        if ledger_gst:
            details_parts.append(f"GST: {ledger_gst}")
        
        if details_parts:
            details_para = Paragraph(
                " | ".join(details_parts),
                self._create_style(
                    fontName="Helvetica",
                    fontSize=9,
                    textColor=PDFStyles.COLOR_TEXT_LIGHT,
                    alignment=TA_LEFT,
                    spaceAfter=12,
                ),
            )
            self.story.append(details_para)
        else:
            self.story.append(Spacer(1, 12))
    
    def add_period(self, from_date: str, to_date: str) -> None:
        """Add statement period."""
        period_para = Paragraph(
            f"Period: {format_date(from_date)} to {format_date(to_date)}",
            self._create_style(
                fontName="Helvetica",
                fontSize=10,
                textColor=PDFStyles.COLOR_TEXT,
                alignment=TA_LEFT,
                spaceAfter=12,
            ),
        )
        self.story.append(period_para)
    
    def add_transaction_table(
        self,
        transactions: List[Dict[str, Any]],
        opening_balance: float = 0,
        closing_balance: float = 0,
    ) -> None:
        """Add transaction table."""
        # Table headers
        data = [
            ["Date", "Particulars", "Debit (?)", "Credit (?)", "Balance (?)"],
        ]
        
        # Opening balance row
        if opening_balance != 0:
            balance_type = "Dr" if opening_balance > 0 else "Cr"
            data.append([
                "",
                "Opening Balance",
                "",
                "",
                f"{format_currency(abs(opening_balance))} {balance_type}",
            ])
        
        # Transaction rows
        for txn in transactions:
            date = format_date(txn.get("date", ""), "%d-%m-%Y")
            particulars = txn.get("particulars", "")[:40]
            debit = format_currency(txn.get("debit", 0)) if txn.get("debit", 0) else ""
            credit = format_currency(txn.get("credit", 0)) if txn.get("credit", 0) else ""
            balance = txn.get("balance", 0)
            balance_type = "Dr" if balance >= 0 else "Cr"
            balance_str = f"{format_currency(abs(balance))} {balance_type}"
            
            data.append([date, particulars, debit, credit, balance_str])
        
        # Closing balance row
        if closing_balance != 0:
            balance_type = "Dr" if closing_balance > 0 else "Cr"
            data.append([
                "",
                "<b>Closing Balance</b>",
                "",
                "",
                f"<b>{format_currency(abs(closing_balance))} {balance_type}</b>",
            ])
        
        # Create table
        table = Table(
            data,
            colWidths=[1.2 * inch, 3 * inch, 1.2 * inch, 1.2 * inch, 1.2 * inch],
            style=[
                # Grid
                ("GRID", (0, 0), (-1, -1), 0.5, PDFStyles.COLOR_BORDER),
                # Header
                ("BACKGROUND", (0, 0), (-1, 0), PDFStyles.COLOR_TABLE_HEADER),
                ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 9),
                ("VALIGN", (0, 0), (-1, 0), "MIDDLE"),
                # Data rows
                ("FONT", (0, 1), (-1, -1), "Helvetica", 8),
                ("VALIGN", (0, 1), (-1, -1), "TOP"),
                # Amount columns - right align
                ("ALIGN", (2, 0), (4, -1), "RIGHT"),
                # Closing balance - bold
                ("FONT", (0, -1), (-1, -1), "Helvetica-Bold", 9),
                ("BACKGROUND", (0, -1), (-1, -1), PDFStyles.COLOR_TABLE_HEADER),
            ],
        )
        
        self.story.append(table)
        self.story.append(Spacer(1, 12))
    
    def add_summary(self, total_debit: float, total_credit: float) -> None:
        """Add summary section."""
        summary_data = [
            ["Total Debit:", format_currency(total_debit)],
            ["Total Credit:", format_currency(total_credit)],
        ]
        
        table = Table(
            summary_data,
            colWidths=[2 * inch, 2 * inch],
            style=[
                ("FONT", (0, 0), (-1, -1), "Helvetica", 9),
                ("ALIGN", (1, 0), (1, -1), "RIGHT"),
                ("FONT", (1, 0), (1, -1), "Helvetica-Bold", 9),
            ],
        )
        
        self.story.append(table)
        self.story.append(Spacer(1, 12))
    
    def add_footer(self) -> None:
        """Add document footer."""
        self.story.append(Spacer(1, 0.5 * inch))
        
        # Footer text
        footer_para = Paragraph(
            "This is a computer-generated statement.",
            self._create_style(
                fontName="Helvetica",
                fontSize=8,
                textColor=PDFStyles.COLOR_TEXT_LIGHT,
                alignment=TA_CENTER,
            ),
        )
        self.story.append(footer_para)
        
        # Generated date
        generated_para = Paragraph(
            f"Generated on {datetime.now().strftime('%d-%m-%Y %H:%M')} by TallySync",
            self._create_style(
                fontName="Helvetica",
                fontSize=8,
                textColor=PDFStyles.COLOR_TEXT_LIGHT,
                alignment=TA_CENTER,
                spaceAfter=6,
            ),
        )
        self.story.append(generated_para)
    
    def add_page_break(self) -> None:
        """Add page break."""
        self.story.append(Spacer(1, 0.1 * inch))
        self.story.append(PageBreak())
    
    def _create_style(
        self,
        fontName: str = "Helvetica",
        fontSize: int = 10,
        textColor: Any = PDFStyles.COLOR_TEXT,
        alignment: int = TA_LEFT,
        spaceAfter: float = 6,
    ):
        """Create paragraph style."""
        from reportlab.lib.styles import ParagraphStyle
        return ParagraphStyle(
            "CustomStyle",
            parent=self.styles["Normal"],
            fontName=fontName,
            fontSize=fontSize,
            textColor=textColor,
            alignment=alignment,
            spaceAfter=spaceAfter,
        )
    
    def get_story(self) -> List:
        """Get document story."""
        return self.story


# Import PageBreak
from reportlab.platypus import PageBreak
