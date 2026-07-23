"""
PDF Generator for TallySync

Main PDF generation engine.

Author: OmniMagination
Version: 1.0.0
"""

import os
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.units import inch

from app.core.config import config
from app.core.logger import logger
from app.core.exceptions import PDFGenerationError
from app.core.utils import get_app_path, ensure_folder_exists
from app.pdf.styles import PDFStyles
from app.pdf.templates import StatementTemplate


class PDFGenerator:
    """
    Main PDF generator for TallySync.
    
    Features:
    - Ledger statements
    - Custom templates
    - Professional formatting
    - Auto-save to exports folder
    """
    
    def __init__(self) -> None:
        """Initialize PDF generator."""
        self.output_folder = get_app_path() / config.get("pdf", "output_folder")
        ensure_folder_exists(self.output_folder)
        
        logger.info(f"PDFGenerator initialized: {self.output_folder}", category="pdf")
    
    def generate_ledger_statement(
        self,
        ledger_name: str,
        transactions: List[Dict[str, Any]],
        company_name: str = "Company",
        company_address: str = "",
        company_phone: str = "",
        company_email: str = "",
        company_gst: str = "",
        ledger_group: str = "",
        ledger_phone: str = "",
        ledger_email: str = "",
        ledger_gst: str = "",
        from_date: str = "",
        to_date: str = "",
        opening_balance: float = 0,
        closing_balance: float = 0,
        total_debit: float = 0,
        total_credit: float = 0,
        filename: Optional[str] = None,
    ) -> str:
        """
        Generate ledger statement PDF.
        
        Args:
            ledger_name: Name of the ledger
            transactions: List of transaction dictionaries
            company_*: Company information
            ledger_*: Ledger information
            from_date: Statement start date
            to_date: Statement end date
            opening_balance: Opening balance amount
            closing_balance: Closing balance amount
            total_debit: Total debit amount
            total_credit: Total credit amount
            filename: Custom filename (optional)
        
        Returns:
            Path to generated PDF file
        """
        try:
            # Generate filename
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                safe_name = "".join(c for c in ledger_name if c.isalnum() or c in " -_")[:30]
                filename = f"Statement_{safe_name}_{timestamp}.pdf"
            
            output_path = self.output_folder / filename
            
            # Create document
            doc = SimpleDocTemplate(
                str(output_path),
                pagesize=A4,
                leftMargin=PDFStyles.PAGE_MARGIN,
                rightMargin=PDFStyles.PAGE_MARGIN,
                topMargin=PDFStyles.PAGE_MARGIN,
                bottomMargin=PDFStyles.PAGE_MARGIN,
            )
            
            # Create template
            template = StatementTemplate(doc)
            
            # Build document
            template.add_header(
                company_name=company_name,
                company_address=company_address,
                company_phone=company_phone,
                company_email=company_email,
                company_gst=company_gst,
            )
            
            template.add_title(
                title="Ledger Account Statement",
                subtitle=f"Statement of Account",
            )
            
            template.add_ledger_info(
                ledger_name=ledger_name,
                ledger_group=ledger_group,
                ledger_phone=ledger_phone,
                ledger_email=ledger_email,
                ledger_gst=ledger_gst,
            )
            
            template.add_period(from_date=from_date, to_date=to_date)
            
            template.add_transaction_table(
                transactions=transactions,
                opening_balance=opening_balance,
                closing_balance=closing_balance,
            )
            
            template.add_summary(
                total_debit=total_debit,
                total_credit=total_credit,
            )
            
            template.add_footer()
            
            # Build PDF
            doc.build(template.get_story())
            
            logger.log_pdf_generated(filename, str(output_path))
            
            return str(output_path)
        
        except Exception as e:
            logger.error(f"PDF generation failed: {e}", category="pdf", exc_info=True)
            raise PDFGenerationError(
                f"Failed to generate PDF: {e}",
                filename=filename,
                template="ledger_statement",
            )
    
    def generate_simple_statement(
        self,
        ledger_name: str,
        closing_balance: float,
        balance_type: str = "Dr",
        company_name: str = "Company",
        filename: Optional[str] = None,
    ) -> str:
        """
        Generate simple balance statement (quick summary).
        
        Args:
            ledger_name: Ledger name
            closing_balance: Current balance
            balance_type: Dr or Cr
            company_name: Company name
            filename: Custom filename
        
        Returns:
            Path to generated PDF
        """
        try:
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                safe_name = "".join(c for c in ledger_name if c.isalnum() or c in " -_")[:30]
                filename = f"Balance_{safe_name}_{timestamp}.pdf"
            
            output_path = self.output_folder / filename
            
            doc = SimpleDocTemplate(
                str(output_path),
                pagesize=A4,
                leftMargin=PDFStyles.PAGE_MARGIN,
                rightMargin=PDFStyles.PAGE_MARGIN,
                topMargin=PDFStyles.PAGE_MARGIN,
                bottomMargin=PDFStyles.PAGE_MARGIN,
            )
            
            template = StatementTemplate(doc)
            
            template.add_header(company_name=company_name)
            template.add_title("Balance Certificate")
            
            from app.core.utils import format_currency
            balance_para = f"""
            <br/><br/>
            This is to certify that the balance standing in the name of<br/>
            <b>{ledger_name}</b><br/>
            as on {datetime.now().strftime('%d-%m-%Y')} is:<br/><br/>
            <b style="font-size: 18pt; color: #2563EB;">
                {format_currency(abs(closing_balance))} {balance_type}
            </b>
            <br/><br/>
            This certificate is issued for information purposes only.
            """
            
            from reportlab.platypus import Paragraph
            from reportlab.lib.styles import getSampleStyleSheet
            
            styles = getSampleStyleSheet()
            para_style = styles["Normal"]
            para_style.alignment = 1  # Center
            para_style.fontSize = 11
            para_style.spaceAfter = 12
            
            template.story.append(Paragraph(balance_para, para_style))
            template.add_footer()
            
            doc.build(template.get_story())
            
            logger.log_pdf_generated(filename, str(output_path))
            
            return str(output_path)
        
        except Exception as e:
            logger.error(f"Simple statement generation failed: {e}", category="pdf", exc_info=True)
            raise PDFGenerationError(
                f"Failed to generate simple statement: {e}",
                filename=filename,
                template="simple_statement",
            )
    
    def get_output_folder(self) -> Path:
        """Get PDF output folder path."""
        return self.output_folder
    
    def list_generated_pdfs(self, limit: int = 50) -> List[Path]:
        """List recently generated PDFs."""
        pdfs = list(self.output_folder.glob("*.pdf"))
        pdfs.sort(key=lambda p: p.stat().st_mtime, reverse=True)
        return pdfs[:limit]
    
    def delete_old_pdfs(self, days: int = 30) -> int:
        """Delete PDFs older than specified days."""
        import time
        cutoff = time.time() - (days * 86400)
        deleted = 0
        
        for pdf in self.output_folder.glob("*.pdf"):
            if pdf.stat().st_mtime < cutoff:
                pdf.unlink()
                deleted += 1
        
        if deleted > 0:
            logger.info(f"Deleted {deleted} old PDF files", category="pdf")
        
        return deleted
