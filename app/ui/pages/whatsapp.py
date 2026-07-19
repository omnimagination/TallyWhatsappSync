"""
WhatsApp Page for TallySync

Send statements via WhatsApp Web.

Author: OmniMagination
Version: 1.0.0
"""

import customtkinter as ctk
from typing import Any, Optional
import os

from app.ui.styles import UIStyles
from app.core.logger import logger
from app.whatsapp.sender import WhatsAppSender
from app.whatsapp.contact import Contact
from app.whatsapp.utils import WhatsAppUtils
from app.pdf.generator import PDFGenerator
from app.database.repositories import LedgerRepository


class WhatsAppPage(ctk.CTkScrollableFrame):
    """
    WhatsApp page for sending statements.
    """
    
    def __init__(self, master: Any, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self.configure(fg_color=UIStyles.COLOR_BG_DARK)
        
        self.sender = WhatsAppSender()
        self.ledger_repo = LedgerRepository()
        self.pdf_generator = PDFGenerator()
        
        self.selected_ledger = None
        self.generated_pdf = None
        
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Setup WhatsApp UI."""
        # Header
        self._create_header()
        
        # Contact Selection
        self._create_contact_section()
        
        # Preview Section
        self._create_preview_section()
        
        # Send Section
        self._create_send_section()
        
        # Instructions
        self._create_instructions()
    
    def _create_header(self) -> None:
        """Create page header."""
        header_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )
        header_frame.pack(fill="x", pady=(0, 20))
        
        title = ctk.CTkLabel(
            header_frame,
            text="Send via WhatsApp",
            font=ctk.CTkFont(
                family=UIStyles.FONT_FAMILY,
                size=UIStyles.FONT_SIZE_TITLE,
                weight="bold",
            ),
            text_color=UIStyles.COLOR_TEXT_PRIMARY,
        )
        title.pack(side="left")
    
    def _create_contact_section(self) -> None:
        """Create contact selection section."""
        contact_frame = ctk.CTkFrame(
            self,
            fg_color=UIStyles.COLOR_BG_CARD,
            corner_radius=UIStyles.CORNER_RADIUS_NORMAL,
        )
        contact_frame.pack(fill="x", pady=10)
        
        title = ctk.CTkLabel(
            contact_frame,
            text="Select Contact",
            font=ctk.CTkFont(
                family=UIStyles.FONT_FAMILY,
                size=UIStyles.FONT_SIZE_HEADING,
                weight="bold",
            ),
            text_color=UIStyles.COLOR_TEXT_PRIMARY,
        )
        title.pack(padx=15, pady=(15, 10))
        
        # Search ledger
        search_frame = ctk.CTkFrame(
            contact_frame,
            fg_color="transparent",
        )
        search_frame.pack(fill="x", padx=15, pady=10)
        
        self.ledger_search = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search ledger name...",
            width=400,
        )
        self.ledger_search.pack(side="left", padx=(0, 10))
        
        search_btn = ctk.CTkButton(
            search_frame,
            text="?? Search",
            command=self._search_ledger,
            width=100,
        )
        search_btn.pack(side="left")
        
        # Selected contact info
        self.contact_info_frame = ctk.CTkFrame(
            contact_frame,
            fg_color=UIStyles.COLOR_BG_INPUT,
            corner_radius=UIStyles.CORNER_RADIUS_SMALL,
        )
        self.contact_info_frame.pack(fill="x", padx=15, pady=10)
        
        self.contact_info_label = ctk.CTkLabel(
            self.contact_info_frame,
            text="No contact selected - Search for a ledger above",
            font=ctk.CTkFont(
                family=UIStyles.FONT_FAMILY,
                size=UIStyles.FONT_SIZE_NORMAL,
            ),
            text_color=UIStyles.COLOR_TEXT_SECONDARY,
        )
        self.contact_info_label.pack(padx=15, pady=15)
    
    def _create_preview_section(self) -> None:
        """Create message preview section."""
        preview_frame = ctk.CTkFrame(
            self,
            fg_color=UIStyles.COLOR_BG_CARD,
            corner_radius=UIStyles.CORNER_RADIUS_NORMAL,
        )
        preview_frame.pack(fill="x", pady=10)
        
        title = ctk.CTkLabel(
            preview_frame,
            text="Message Preview",
            font=ctk.CTkFont(
                family=UIStyles.FONT_FAMILY,
                size=UIStyles.FONT_SIZE_HEADING,
                weight="bold",
            ),
            text_color=UIStyles.COLOR_TEXT_PRIMARY,
        )
        title.pack(padx=15, pady=(15, 10))
        
        # Message type selector
        type_frame = ctk.CTkFrame(
            preview_frame,
            fg_color="transparent",
        )
        type_frame.pack(fill="x", padx=15, pady=5)
        
        self.message_type = ctk.CTkSegmentedButton(
            type_frame,
            values=["Statement", "Balance", "Reminder"],
            command=self._update_message,
        )
        self.message_type.pack(side="left")
        self.message_type.set("Statement")
        
        # Message text box
        self.message_text = ctk.CTkTextbox(
            preview_frame,
            height=150,
            width=500,
        )
        self.message_text.pack(padx=15, pady=10)
        
        # Copy button
        copy_btn = ctk.CTkButton(
            preview_frame,
            text="?? Copy Message",
            command=self._copy_message,
            width=150,
        )
        copy_btn.pack(padx=15, pady=(0, 15))
    
    def _create_send_section(self) -> None:
        """Create send action section."""
        send_frame = ctk.CTkFrame(
            self,
            fg_color=UIStyles.COLOR_BG_CARD,
            corner_radius=UIStyles.CORNER_RADIUS_NORMAL,
        )
        send_frame.pack(fill="x", pady=10)
        
        title = ctk.CTkLabel(
            send_frame,
            text="Send Statement",
            font=ctk.CTkFont(
                family=UIStyles.FONT_FAMILY,
                size=UIStyles.FONT_SIZE_HEADING,
                weight="bold",
            ),
            text_color=UIStyles.COLOR_TEXT_PRIMARY,
        )
        title.pack(padx=15, pady=(15, 10))
        
        # Generate PDF button
        gen_btn = ctk.CTkButton(
            send_frame,
            text="?? Generate PDF Statement",
            command=self._generate_pdf,
            height=45,
            width=200,
            fg_color=UIStyles.COLOR_PRIMARY,
        )
        gen_btn.pack(padx=15, pady=10)
        
        # PDF status
        self.pdf_status = ctk.CTkLabel(
            send_frame,
            text="PDF not generated",
            font=ctk.CTkFont(
                family=UIStyles.FONT_FAMILY,
                size=UIStyles.FONT_SIZE_SMALL,
            ),
            text_color=UIStyles.COLOR_TEXT_SECONDARY,
        )
        self.pdf_status.pack(padx=15, pady=5)
        
        # Send button
        self.send_btn = ctk.CTkButton(
            send_frame,
            text="?? Open WhatsApp Web",
            command=self._send_whatsapp,
            height=50,
            width=250,
            fg_color=UIStyles.COLOR_SUCCESS,
            state="disabled",
        )
        self.send_btn.pack(padx=15, pady=15)
    
    def _create_instructions(self) -> None:
        """Create instructions section."""
        instr_frame = ctk.CTkFrame(
            self,
            fg_color=UIStyles.COLOR_BG_CARD,
            corner_radius=UIStyles.CORNER_RADIUS_NORMAL,
        )
        instr_frame.pack(fill="x", pady=10)
        
        title = ctk.CTkLabel(
            instr_frame,
            text="How to Send",
            font=ctk.CTkFont(
                family=UIStyles.FONT_FAMILY,
                size=UIStyles.FONT_SIZE_HEADING,
                weight="bold",
            ),
            text_color=UIStyles.COLOR_TEXT_PRIMARY,
        )
        title.pack(padx=15, pady=(15, 10))
        
        instructions = self.sender.get_send_instructions()
        
        for instr in instructions:
            label = ctk.CTkLabel(
                instr_frame,
                text=instr,
                font=ctk.CTkFont(
                    family=UIStyles.FONT_FAMILY,
                    size=UIStyles.FONT_SIZE_SMALL,
                ),
                text_color=UIStyles.COLOR_TEXT_SECONDARY,
                anchor="w",
            )
            label.pack(padx=15, pady=1, anchor="w")
    
    def _search_ledger(self) -> None:
        """Search and select ledger."""
        search_term = self.ledger_search.get().strip()
        
        if not search_term:
            self.contact_info_label.configure(
                text="Please enter a ledger name to search"
            )
            return
        
        try:
            ledgers = self.ledger_repo.search_ledgers("", search_term, limit=10)
            
            if not ledgers:
                self.contact_info_label.configure(
                    text=f"No ledgers found for '{search_term}'"
                )
                self.selected_ledger = None
                return
            
            # Select first result
            self.selected_ledger = ledgers[0]
            
            contact = Contact(ledger=self.selected_ledger)
            
            self.contact_info_label.configure(
                text=f"Selected: {contact.name} | {contact.formatted_phone} | Balance: {contact.balance_formatted}",
                text_color=UIStyles.COLOR_TEXT_PRIMARY,
            )
            
            # Update message preview
            self._update_message("Statement")
            
            logger.info(f"Ledger selected for WhatsApp: {contact.name}", category="whatsapp")
        
        except Exception as e:
            self.contact_info_label.configure(
                text=f"Error: {str(e)}",
                text_color=UIStyles.COLOR_ERROR,
            )
    
    def _update_message(self, message_type: str) -> None:
        """Update message preview."""
        if not self.selected_ledger:
            return
        
        contact = Contact(ledger=self.selected_ledger)
        
        type_map = {
            "Statement": "statement",
            "Balance": "balance",
            "Reminder": "reminder",
        }
        
        message = contact.get_default_message(type_map.get(message_type, "statement"))
        
        self.message_text.delete("0.0", "end")
        self.message_text.insert("0.0", message)
    
    def _copy_message(self) -> None:
        """Copy message to clipboard."""
        message = self.message_text.get("0.0", "end").strip()
        
        if self.sender.copy_message_to_clipboard(message):
            self.pdf_status.configure(
                text="? Message copied to clipboard",
                text_color=UIStyles.COLOR_SUCCESS,
            )
        else:
            self.pdf_status.configure(
                text="? Failed to copy message",
                text_color=UIStyles.COLOR_ERROR,
            )
    
    def _generate_pdf(self) -> None:
        """Generate PDF statement."""
        if not self.selected_ledger:
            self.pdf_status.configure(
                text="? Please select a ledger first",
                text_color=UIStyles.COLOR_ERROR,
            )
            return
        
        try:
            contact = Contact(ledger=self.selected_ledger)
            
            # Generate simple balance PDF for now
            # (Full statement with transactions would require voucher data)
            self.generated_pdf = self.pdf_generator.generate_simple_statement(
                ledger_name=contact.name,
                closing_balance=contact.balance,
                balance_type=contact.balance_type,
                company_name="Company",
            )
            
            self.pdf_status.configure(
                text=f"? PDF generated: {os.path.basename(self.generated_pdf)}",
                text_color=UIStyles.COLOR_SUCCESS,
            )
            
            # Enable send button
            self.send_btn.configure(state="normal")
            
            logger.info(f"PDF generated for WhatsApp: {self.generated_pdf}", category="pdf")
        
        except Exception as e:
            self.pdf_status.configure(
                text=f"? PDF generation failed: {str(e)}",
                text_color=UIStyles.COLOR_ERROR,
            )
            logger.error(f"PDF generation for WhatsApp failed: {e}", category="pdf")
    
    def _send_whatsapp(self) -> None:
        """Open WhatsApp Web for sending."""
        if not self.selected_ledger:
            return
        
        contact = Contact(ledger=self.selected_ledger)
        message = self.message_text.get("0.0", "end").strip()
        
        result = self.sender.send_statement(
            contact=contact,
            pdf_path=self.generated_pdf or "",
            message=message,
        )
        
        if result["success"]:
            self.pdf_status.configure(
                text="? WhatsApp Web opened - Attach PDF and send",
                text_color=UIStyles.COLOR_SUCCESS,
            )
        else:
            self.pdf_status.configure(
                text=f"? Error: {result.get('error', 'Unknown')}",
                text_color=UIStyles.COLOR_ERROR,
            )
    
    def refresh(self) -> None:
        """Refresh page."""
        logger.debug("WhatsApp page refreshed", category="ui")
