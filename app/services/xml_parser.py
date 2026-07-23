"""
XML Response Parser for TallySync

Parses Tally XML responses into Python objects.

Author: OmniMagination
Version: 1.0.0
"""

import re
from typing import Optional, List, Dict, Any
from datetime import datetime

from app.core.logger import logger
from app.core.utils import parse_float, parse_int, sanitize_string


class XMLParser:
    """
    Parser for Tally XML responses.
    """
    
    @staticmethod
    def parse(xml_string: str) -> Optional[Dict[str, Any]]:
        """Parse XML string to dictionary."""
        if not xml_string:
            return None
        
        try:
            import xmltodict
            # Clean invalid XML characters first
            cleaned = re.sub(r'&#\d+;', '', xml_string)
            parsed = xmltodict.parse(cleaned)
            logger.debug(f"XML parsed successfully: {len(xml_string)} bytes", category="xml")
            return parsed
        except Exception as e:
            logger.error(f"XML parsing failed: {e}", category="xml", exc_info=True)
            return None
    
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
        if not xml_string:
            return []
        
        ledgers = []
        
        try:
            # Use regex to extract LEDGER entries (more reliable than xmltodict for Tally)
            # Clean invalid characters first
            cleaned = re.sub(r'&#\d+;', '', xml_string)
            
            # Find all LEDGER tags with NAME attribute
            ledger_pattern = r'<LEDGER\s+NAME="([^"]*)"[^>]*>(.*?)</LEDGER>'
            ledger_matches = re.findall(ledger_pattern, cleaned, re.DOTALL | re.IGNORECASE)
            
            for name, content in ledger_matches:
                if not name or not name.strip():
                    continue
                
                # Extract fields from ledger content
                parent = XMLParser._extract_tag(content, 'PARENT')
                group = XMLParser._extract_tag(content, 'GROUP') or parent
                closing_balance = parse_float(XMLParser._extract_tag(content, 'CLOSINGBALANCE'))
                opening_balance = parse_float(XMLParser._extract_tag(content, 'OPENINGBALANCE') or XMLParser._extract_tag(content, 'LEDOPENINGBALANCE'))
                phone = XMLParser._extract_tag(content, 'PHONE')
                email = XMLParser._extract_tag(content, 'EMAIL')
                address = XMLParser._extract_tag(content, 'ADDRESS')
                gst_number = XMLParser._extract_tag(content, 'LEDGSTIN') or XMLParser._extract_tag(content, 'TAXREGNUMBER')
                pan_number = XMLParser._extract_tag(content, 'INCOMETAXNUMBER')
                contact_person = XMLParser._extract_tag(content, 'CONTACTPERSON')
                credit_limit = parse_float(XMLParser._extract_tag(content, 'CREDITLIMIT'))
                credit_days = parse_int(XMLParser._extract_tag(content, 'CREDITDAYS'))
                
                # Determine balance type
                balance_type = "Dr"
                if closing_balance < 0:
                    balance_type = "Cr"
                    closing_balance = abs(closing_balance)
                elif opening_balance < 0:
                    balance_type = "Cr"
                    opening_balance = abs(opening_balance)
                
                ledger_data = {
                    "ledger_id": sanitize_string(name),
                    "company_id": company_id,
                    "name": sanitize_string(name),
                    "parent": sanitize_string(parent),
                    "group_name": sanitize_string(group),
                    "ledger_type": sanitize_string(group),
                    "opening_balance": opening_balance,
                    "closing_balance": closing_balance,
                    "balance_type": balance_type,
                    "phone": sanitize_string(phone),
                    "email": sanitize_string(email),
                    "address": sanitize_string(address),
                    "gst_number": sanitize_string(gst_number),
                    "pan_number": sanitize_string(pan_number),
                    "contact_person": sanitize_string(contact_person),
                    "credit_limit": credit_limit,
                    "credit_days": credit_days,
                }
                
                ledgers.append(ledger_data)
            
            logger.info(f"Parsed {len(ledgers)} ledgers from XML", category="xml")
        
        except Exception as e:
            logger.error(f"Failed to parse ledgers: {e}", category="xml", exc_info=True)
        
        return ledgers
    
    @staticmethod
    def parse_companies(xml_string: str) -> List[Dict[str, Any]]:
        """Parse company data from XML."""
        companies = []
        
        try:
            cleaned = re.sub(r'&#\d+;', '', xml_string)
            
            # Look for COMPANY tags
            company_pattern = r'<COMPANY[^>]*NAME="([^"]*)"[^>]*>(.*?)</COMPANY>'
            company_matches = re.findall(company_pattern, cleaned, re.DOTALL | re.IGNORECASE)
            
            for name, content in company_matches:
                company_data = {
                    "company_id": sanitize_string(name),
                    "name": sanitize_string(name),
                    "address": XMLParser._extract_tag(content, 'ADDRESS'),
                    "phone": XMLParser._extract_tag(content, 'PHONE'),
                    "email": XMLParser._extract_tag(content, 'EMAIL'),
                    "gst_number": XMLParser._extract_tag(content, 'LEDGSTIN') or XMLParser._extract_tag(content, 'TAXREGNUMBER'),
                    "pan_number": XMLParser._extract_tag(content, 'INCOMETAXNUMBER'),
                    "state": XMLParser._extract_tag(content, 'STATE'),
                    "state_code": XMLParser._extract_tag(content, 'STATECODE'),
                }
                companies.append(company_data)
            
            # If no COMPANY tags, try to get current company info
            if not companies and 'CMPINFO' in cleaned:
                # Extract from header info
                company_name = XMLParser._extract_tag(cleaned, 'COMPANYNAME') or "Current Company"
                companies.append({
                    "company_id": sanitize_string(company_name),
                    "name": sanitize_string(company_name),
                })
            
            logger.info(f"Parsed {len(companies)} companies from XML", category="xml")
        
        except Exception as e:
            logger.error(f"Failed to parse companies: {e}", category="xml", exc_info=True)
        
        return companies
    
    @staticmethod
    def parse_vouchers(xml_string: str, company_id: str = "") -> List[Dict[str, Any]]:
        """Parse voucher data from XML."""
        vouchers = []
        
        try:
            cleaned = re.sub(r'&#\d+;', '', xml_string)
            
            # Look for VOUCHER tags
            voucher_pattern = r'<VOUCHER[^>]*NAME="([^"]*)"[^>]*>(.*?)</VOUCHER>'
            voucher_matches = re.findall(voucher_pattern, cleaned, re.DOTALL | re.IGNORECASE)
            
            for name, content in voucher_matches:
                voucher_data = {
                    "voucher_id": sanitize_string(name),
                    "company_id": company_id,
                    "voucher_type": XMLParser._extract_tag(content, 'VOUCHERTYPENAME'),
                    "voucher_number": XMLParser._extract_tag(content, 'VOUCHERNUMBER'),
                    "date": XMLParser._extract_tag(content, 'DATE'),
                    "amount": parse_float(XMLParser._extract_tag(content, 'AMOUNT')),
                    "narration": XMLParser._extract_tag(content, 'NARRATION'),
                    "reference_number": XMLParser._extract_tag(content, 'REFERENCENUMBER'),
                    "reference_date": XMLParser._extract_tag(content, 'REFERENCEDATE'),
                    "is_cancelled": 0,
                }
                vouchers.append(voucher_data)
            
            logger.info(f"Parsed {len(vouchers)} vouchers from XML", category="xml")
        
        except Exception as e:
            logger.error(f"Failed to parse vouchers: {e}", category="xml", exc_info=True)
        
        return vouchers
    
    @staticmethod
    def _extract_tag(content: str, tag_name: str) -> str:
        """Extract content from XML tag."""
        if not content:
            return ""
        
        # Try different tag formats
        patterns = [
            rf'<{tag_name}[^>]*>([^<]*)</{tag_name}>',
            rf'<{tag_name}[^>]*TYPE="[^"]*">([^<]*)</{tag_name}>',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return sanitize_string(match.group(1))
        
        return ""
    
    @staticmethod
    def get_error_message(xml_string: str) -> str:
        """Extract error message from XML response."""
        if not xml_string:
            return "Empty response"
        
        # Look for LINEERROR tag
        error_match = re.search(r'<LINEERROR>([^<]*)</LINEERROR>', xml_string)
        if error_match:
            return error_match.group(1)
        
        # Look for STATUS
        status_match = re.search(r'<STATUS>(\d+)</STATUS>', xml_string)
        if status_match and status_match.group(1) == "0":
            return "Tally returned error status"
        
        return "Unknown error"
    
    @staticmethod
    def is_valid_response(xml_string: str) -> bool:
        """Check if XML response is valid."""
        if not xml_string:
            return False
        
        # Check for error
        if '<LINEERROR>' in xml_string:
            return False
        
        # Check status
        status_match = re.search(r'<STATUS>(\d+)</STATUS>', xml_string)
        if status_match and status_match.group(1) == "0":
            return False
        
        return True
