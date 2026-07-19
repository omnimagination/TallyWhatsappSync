"""
XML Response Parser for TallySync

Parses Tally XML responses into Python objects.

Author: OmniMagination
Version: 1.0.0
"""

import xmltodict
from typing import Optional, List, Dict, Any
from datetime import datetime

from app.core.logger import logger
from app.core.utils import parse_float, parse_int, sanitize_string


class XMLParser:
    """
    Parser for Tally XML responses.
    
    Converts XML responses to Python dictionaries and model data.
    """
    
    @staticmethod
    def parse(xml_string: str) -> Optional[Dict[str, Any]]:
        """
        Parse XML string to dictionary.
        
        Args:
            xml_string: XML response string
        
        Returns:
            Parsed dictionary or None
        """
        if not xml_string:
            return None
        
        try:
            parsed = xmltodict.parse(xml_string, force_list=["COMPANY", "LEDGER", "VOUCHER"])
            logger.debug(f"XML parsed successfully: {len(xml_string)} bytes", category="xml")
            return parsed
        except Exception as e:
            logger.error(f"XML parsing failed: {e}", category="xml", exc_info=True)
            return None
    
    @staticmethod
    def parse_companies(xml_string: str) -> List[Dict[str, Any]]:
        """
        Parse company data from XML.
        
        Args:
            xml_string: XML response string
        
        Returns:
            List of company dictionaries
        """
        parsed = XMLParser.parse(xml_string)
        if not parsed:
            return []
        
        companies = []
        
        try:
            envelope = parsed.get("ENVELOPE", {})
            body = envelope.get("BODY", {})
            data = body.get("DATA", {})
            
            # Handle different XML structures
            company_list = data.get("COMPANY", [])
            
            if not company_list:
                # Try alternative structure
                company_list = data.get("LISTOFCOMPANIES", {}).get("COMPANY", [])
            
            if not isinstance(company_list, list):
                company_list = [company_list]
            
            for company in company_list:
                if not company:
                    continue
                
                company_data = {
                    "company_id": XMLParser._get_value(company, "NAME"),
                    "name": XMLParser._get_value(company, "NAME"),
                    "address": XMLParser._get_value(company, "ADDRESS"),
                    "phone": XMLParser._get_value(company, "PHONE"),
                    "email": XMLParser._get_value(company, "EMAIL"),
                    "gst_number": XMLParser._get_value(company, "TAXREGNUMBER"),
                    "pan_number": XMLParser._get_value(company, "INCOMETAXNUMBER"),
                    "state": XMLParser._get_value(company, "STATE"),
                    "state_code": XMLParser._get_value(company, "STATECODE"),
                    "financial_year_from": XMLParser._get_value(company, "FINANCIALYEARFROM"),
                    "financial_year_to": XMLParser._get_value(company, "FINANCIALYEARTO"),
                    "books_from_date": XMLParser._get_value(company, "BOOKSFROMDATE"),
                    "base_currency": XMLParser._get_value(company, "BASECURRENCY", "INR"),
                }
                
                companies.append(company_data)
            
            logger.info(f"Parsed {len(companies)} companies from XML", category="xml")
        
        except Exception as e:
            logger.error(f"Failed to parse companies: {e}", category="xml", exc_info=True)
        
        return companies
    
    @staticmethod
    def parse_ledgers(xml_string: str, company_id: str = "") -> List[Dict[str, Any]]:
        """
        Parse ledger data from XML.
        
        Args:
            xml_string: XML response string
            company_id: Company ID for reference
        
        Returns:
            List of ledger dictionaries
        """
        parsed = XMLParser.parse(xml_string)
        if not parsed:
            return []
        
        ledgers = []
        
        try:
            envelope = parsed.get("ENVELOPE", {})
            body = envelope.get("BODY", {})
            data = body.get("DATA", {})
            
            ledger_list = data.get("LEDGER", [])
            
            if not isinstance(ledger_list, list):
                ledger_list = [ledger_list]
            
            for ledger in ledger_list:
                if not ledger:
                    continue
                
                opening_balance = parse_float(XMLParser._get_value(ledger, "OPENINGBALANCE"))
                closing_balance = parse_float(XMLParser._get_value(ledger, "CLOSINGBALANCE"))
                
                # Determine balance type
                balance_type = "Dr"
                if closing_balance < 0:
                    balance_type = "Cr"
                    closing_balance = abs(closing_balance)
                elif opening_balance < 0:
                    balance_type = "Cr"
                    opening_balance = abs(opening_balance)
                
                ledger_data = {
                    "ledger_id": XMLParser._get_value(ledger, "NAME"),
                    "company_id": company_id,
                    "name": XMLParser._get_value(ledger, "NAME"),
                    "parent": XMLParser._get_value(ledger, "PARENT"),
                    "group_name": XMLParser._get_value(ledger, "GROUP"),
                    "ledger_type": XMLParser._get_value(ledger, "LEDGERTYPE"),
                    "opening_balance": opening_balance,
                    "closing_balance": closing_balance,
                    "balance_type": balance_type,
                    "phone": XMLParser._get_value(ledger, "PHONE"),
                    "email": XMLParser._get_value(ledger, "EMAIL"),
                    "address": XMLParser._get_value(ledger, "ADDRESS"),
                    "gst_number": XMLParser._get_value(ledger, "TAXREGNUMBER"),
                    "pan_number": XMLParser._get_value(ledger, "INCOMETAXNUMBER"),
                    "contact_person": XMLParser._get_value(ledger, "CONTACTPERSON"),
                    "credit_limit": parse_float(XMLParser._get_value(ledger, "CREDITLIMIT")),
                    "credit_days": parse_int(XMLParser._get_value(ledger, "CREDITDAYS")),
                }
                
                ledgers.append(ledger_data)
            
            logger.info(f"Parsed {len(ledgers)} ledgers from XML", category="xml")
        
        except Exception as e:
            logger.error(f"Failed to parse ledgers: {e}", category="xml", exc_info=True)
        
        return ledgers
    
    @staticmethod
    def parse_vouchers(xml_string: str, company_id: str = "") -> List[Dict[str, Any]]:
        """
        Parse voucher data from XML.
        
        Args:
            xml_string: XML response string
            company_id: Company ID for reference
        
        Returns:
            List of voucher dictionaries
        """
        parsed = XMLParser.parse(xml_string)
        if not parsed:
            return []
        
        vouchers = []
        
        try:
            envelope = parsed.get("ENVELOPE", {})
            body = envelope.get("BODY", {})
            data = body.get("DATA", {})
            
            voucher_list = data.get("VOUCHER", [])
            
            if not isinstance(voucher_list, list):
                voucher_list = [voucher_list]
            
            for voucher in voucher_list:
                if not voucher:
                    continue
                
                voucher_data = {
                    "voucher_id": XMLParser._get_value(voucher, "NAME"),
                    "company_id": company_id,
                    "voucher_type": XMLParser._get_value(voucher, "VOUCHERTYPENAME"),
                    "voucher_number": XMLParser._get_value(voucher, "VOUCHERNUMBER"),
                    "date": XMLParser._get_value(voucher, "DATE"),
                    "amount": parse_float(XMLParser._get_value(voucher, "AMOUNT")),
                    "narration": XMLParser._get_value(voucher, "NARRATION"),
                    "reference_number": XMLParser._get_value(voucher, "REFERENCENUMBER"),
                    "reference_date": XMLParser._get_value(voucher, "REFERENCEDATE"),
                    "buyer_details": XMLParser._get_value(voucher, "BUYERDETAILS"),
                    "shipping_details": XMLParser._get_value(voucher, "SHIPPINGDETAILS"),
                    "invoice_date": XMLParser._get_value(voucher, "INVOICEDATE"),
                    "is_cancelled": 0,
                }
                
                vouchers.append(voucher_data)
            
            logger.info(f"Parsed {len(vouchers)} vouchers from XML", category="xml")
        
        except Exception as e:
            logger.error(f"Failed to parse vouchers: {e}", category="xml", exc_info=True)
        
        return vouchers
    
    @staticmethod
    def _get_value(data: Dict[str, Any], key: str, default: str = "") -> str:
        """
        Safely get value from parsed XML dictionary.
        
        Args:
            data: Parsed XML dictionary
            key: Key to look up
            default: Default value if not found
        
        Returns:
            Value as string
        """
        if not data:
            return default
        
        value = data.get(key, default)
        
        if value is None:
            return default
        
        if isinstance(value, dict):
            return value.get("#text", default)
        
        return sanitize_string(str(value))
    
    @staticmethod
    def get_error_message(xml_string: str) -> str:
        """
        Extract error message from XML response.
        
        Args:
            xml_string: XML response string
        
        Returns:
            Error message or empty string
        """
        parsed = XMLParser.parse(xml_string)
        if not parsed:
            return "Invalid XML response"
        
        try:
            envelope = parsed.get("ENVELOPE", {})
            header = envelope.get("HEADER", {})
            return header.get("ERROR", "")
        except Exception:
            return "Unknown error"
    
    @staticmethod
    def is_valid_response(xml_string: str) -> bool:
        """
        Check if XML response is valid.
        
        Args:
            xml_string: XML response string
        
        Returns:
            True if valid
        """
        if not xml_string:
            return False
        
        parsed = XMLParser.parse(xml_string)
        if not parsed:
            return False
        
        # Check for error in response
        envelope = parsed.get("ENVELOPE", {})
        header = envelope.get("HEADER", {})
        
        if "ERROR" in header:
            return False
        
        return True
