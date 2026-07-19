"""
XML Request Builder for TallySync

Builds Tally TDL requests in XML format.

Author: OmniMagination
Version: 1.0.0
"""

from typing import Optional, List
from datetime import datetime


class XMLBuilder:
    """
    Builder class for creating Tally XML requests.
    
    All requests follow Tally's XML format specification.
    """
    
    @staticmethod
    def create_envelope(request: str) -> str:
        """
        Create XML envelope for request.
        
        Args:
            request: TDL request content
        
        Returns:
            Complete XML envelope string
        """
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<ENVELOPE>
    <HEADER>
        <VERSION>1</VERSION>
        <TALLYREQUEST>Export</TALLYREQUEST>
        <TYPE>Data</TYPE>
        <ID>{request}</ID>
    </HEADER>
    <BODY>
        <DESC>
            <STATICVARIABLES>
                <SVEXPORTFORMAT>app\services\tally_client.pySysName:XML</SVEXPORTFORMAT>
            </STATICVARIABLES>
        </DESC>
    </BODY>
</ENVELOPE>"""
    
    @staticmethod
    def get_company_info_request(company_name: str = "") -> str:
        """
        Build request for company information.
        
        Args:
            company_name: Specific company name (empty = all)
        
        Returns:
            XML request string
        """
        if company_name:
            request = f"CompanyInfo.{company_name}"
        else:
            request = "CompanyInfo"
        
        return XMLBuilder.create_envelope(request)
    
    @staticmethod
    def get_ledgers_request(company_name: str = "") -> str:
        """
        Build request for all ledgers.
        
        Args:
            company_name: Company name
        
        Returns:
            XML request string
        """
        return XMLBuilder.create_envelope(f"Ledger.{company_name}")
    
    @staticmethod
    def get_ledger_detail_request(ledger_name: str, company_name: str = "") -> str:
        """
        Build request for specific ledger details.
        
        Args:
            ledger_name: Ledger name
            company_name: Company name
        
        Returns:
            XML request string
        """
        return XMLBuilder.create_envelope(f"Ledger.{ledger_name}")
    
    @staticmethod
    def get_vouchers_request(
        company_name: str = "",
        from_date: str = "",
        to_date: str = "",
    ) -> str:
        """
        Build request for vouchers.
        
        Args:
            company_name: Company name
            from_date: Start date (YYYYMMDD)
            to_date: End date (YYYYMMDD)
        
        Returns:
            XML request string
        """
        return XMLBuilder.create_envelope(f"Voucher.{company_name}")
    
    @staticmethod
    def get_voucher_type_request(company_name: str = "") -> str:
        """
        Build request for voucher types.
        
        Args:
            company_name: Company name
        
        Returns:
            XML request string
        """
        return XMLBuilder.create_envelope(f"VoucherType.{company_name}")
    
    @staticmethod
    def get_stock_items_request(company_name: str = "") -> str:
        """
        Build request for stock items/inventory.
        
        Args:
            company_name: Company name
        
        Returns:
            XML request string
        """
        return XMLBuilder.create_envelope(f"StockItem.{company_name}")
    
    @staticmethod
    def get_outstanding_request(ledger_name: str, company_name: str = "") -> str:
        """
        Build request for outstanding details.
        
        Args:
            ledger_name: Ledger name
            company_name: Company name
        
        Returns:
            XML request string
        """
        return XMLBuilder.create_envelope(f"Outstanding.{ledger_name}")
    
    @staticmethod
    def get_ledger_statement_request(
        ledger_name: str,
        from_date: str = "",
        to_date: str = "",
        company_name: str = "",
    ) -> str:
        """
        Build request for ledger statement.
        
        Args:
            ledger_name: Ledger name
            from_date: Start date
            to_date: End date
            company_name: Company name
        
        Returns:
            XML request string
        """
        return XMLBuilder.create_envelope(f"LedgerStatement.{ledger_name}")
    
    @staticmethod
    def create_tdl_request(tdl_content: str) -> str:
        """
        Create custom TDL request.
        
        Args:
            tdl_content: TDL definition content
        
        Returns:
            XML request string
        """
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<ENVELOPE>
    <HEADER>
        <VERSION>1</VERSION>
        <TALLYREQUEST>Export</TALLYREQUEST>
        <TYPE>Data</TYPE>
        <ID>Custom Export</ID>
    </HEADER>
    <BODY>
        <DESC>
            <STATICVARIABLES>
                <SVEXPORTFORMAT>app\services\tally_client.pySysName:XML</SVEXPORTFORMAT>
                <SVTDLRECEIVEVARIABLES>Yes</SVTDLRECEIVEVARIABLES>
            </STATICVARIABLES>
            <TDL>
                <TDLMESSAGE>
                    {tdl_content}
                </TDLMESSAGE>
            </TDL>
        </DESC>
    </BODY>
</ENVELOPE>"""
    
    @staticmethod
    def get_all_companies_request() -> str:
        """
        Build request for list of all companies.
        
        Returns:
            XML request string
        """
        return """<?xml version="1.0" encoding="UTF-8"?>
<ENVELOPE>
    <HEADER>
        <VERSION>1</VERSION>
        <TALLYREQUEST>Export</TALLYREQUEST>
        <TYPE>Data</TYPE>
        <ID>List of Companies</ID>
    </HEADER>
    <BODY>
        <DESC>
            <STATICVARIABLES>
                <SVEXPORTFORMAT>app\services\tally_client.pySysName:XML</SVEXPORTFORMAT>
            </STATICVARIABLES>
        </DESC>
    </BODY>
</ENVELOPE>"""
    
    @staticmethod
    def format_date_for_tally(date_str: str) -> str:
        """
        Format date for Tally request.
        
        Args:
            date_str: Date string
        
        Returns:
            Formatted date (YYYYMMDD)
        """
        if not date_str:
            return ""
        
        try:
            # Try parsing common formats
            for fmt in ["%Y-%m-%d", "%d-%m-%Y", "%Y%m%d"]:
                try:
                    dt = datetime.strptime(date_str, fmt)
                    return dt.strftime("%Y%m%d")
                except ValueError:
                    continue
            return date_str
        except Exception:
            return date_str
