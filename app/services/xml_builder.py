"""
XML Request Builder for TallySync

Builds Tally TDL requests in XML format.

Author: OmniMagination
Version: 1.0.0
"""

from typing import Optional, List
from datetime import datetime


class XMLBuilder:
    """Builder class for creating Tally XML requests."""
    
    @staticmethod
    def get_company_info_request(company_name: str = "") -> str:
        """Build request for company information."""
        return (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<ENVELOPE>\n'
            '    <HEADER>\n'
            '        <VERSION>1</VERSION>\n'
            '        <TALLYREQUEST>Export</TALLYREQUEST>\n'
            '        <TYPE>Collection</TYPE>\n'
            '        <ID>Company</ID>\n'
            '    </HEADER>\n'
            '    <BODY>\n'
            '        <DESC>\n'
            '            <STATICVARIABLES>\n'
            '                <SVEXPORTFORMAT>)SysName:XML</SVEXPORTFORMAT>\n'
            '            </STATICVARIABLES>\n'
            '            <TDL>\n'
            '                <TDLMESSAGE>\n'
            '                    <COLLECTION NAME="CompanyCollection">\n'
            '                        <TYPE>Company</TYPE>\n'
            '                        <FETCH>Name</FETCH>\n'
            '                        <FETCH>Address</FETCH>\n'
            '                        <FETCH>Phone</FETCH>\n'
            '                        <FETCH>Email</FETCH>\n'
            '                    </COLLECTION>\n'
            '                </TDLMESSAGE>\n'
            '            </TDL>\n'
            '        </DESC>\n'
            '    </BODY>\n'
            '</ENVELOPE>'
        )
    
    @staticmethod
    def get_ledgers_request(company_name: str = "") -> str:
        """Build request for all ledgers - WORKING FORMAT."""
        return (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<ENVELOPE>\n'
            '    <HEADER>\n'
            '        <VERSION>1</VERSION>\n'
            '        <TALLYREQUEST>Export</TALLYREQUEST>\n'
            '        <TYPE>Collection</TYPE>\n'
            '        <ID>Ledger</ID>\n'
            '    </HEADER>\n'
            '    <BODY>\n'
            '        <DESC>\n'
            '            <STATICVARIABLES>\n'
            '                <SVEXPORTFORMAT>)SysName:XML</SVEXPORTFORMAT>\n'
            '            </STATICVARIABLES>\n'
            '            <TDL>\n'
            '                <TDLMESSAGE>\n'
            '                    <COLLECTION NAME="LedgerCollection">\n'
            '                        <TYPE>Ledger</TYPE>\n'
            '                        <FETCH>Name</FETCH>\n'
            '                        <FETCH>Parent</FETCH>\n'
            '                        <FETCH>Group</FETCH>\n'
            '                        <FETCH>OpeningBalance</FETCH>\n'
            '                        <FETCH>ClosingBalance</FETCH>\n'
            '                        <FETCH>Phone</FETCH>\n'
            '                        <FETCH>Email</FETCH>\n'
            '                        <FETCH>Address</FETCH>\n'
            '                        <FETCH>TaxRegNumber</FETCH>\n'
            '                        <FETCH>IncomeTaxNumber</FETCH>\n'
            '                        <FETCH>ContactPerson</FETCH>\n'
            '                        <FETCH>CreditLimit</FETCH>\n'
            '                        <FETCH>CreditDays</FETCH>\n'
            '                    </COLLECTION>\n'
            '                </TDLMESSAGE>\n'
            '            </TDL>\n'
            '        </DESC>\n'
            '    </BODY>\n'
            '</ENVELOPE>'
        )
    
    @staticmethod
    def get_ledger_detail_request(ledger_name: str, company_name: str = "") -> str:
        """Build request for specific ledger details."""
        return (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<ENVELOPE>\n'
            '    <HEADER>\n'
            '        <VERSION>1</VERSION>\n'
            '        <TALLYREQUEST>Export</TALLYREQUEST>\n'
            '        <TYPE>Collection</TYPE>\n'
            '        <ID>Ledger</ID>\n'
            '    </HEADER>\n'
            '    <BODY>\n'
            '        <DESC>\n'
            '            <STATICVARIABLES>\n'
            '                <SVEXPORTFORMAT>)SysName:XML</SVEXPORTFORMAT>\n'
            f'                <SVLedgerName>{ledger_name}</SVLedgerName>\n'
            '            </STATICVARIABLES>\n'
            '            <TDL>\n'
            '                <TDLMESSAGE>\n'
            '                    <COLLECTION NAME="SingleLedger">\n'
            '                        <TYPE>Ledger</TYPE>\n'
            '                        <FETCH>Name</FETCH>\n'
            '                        <FETCH>Parent</FETCH>\n'
            '                        <FETCH>ClosingBalance</FETCH>\n'
            '                    </COLLECTION>\n'
            '                </TDLMESSAGE>\n'
            '            </TDL>\n'
            '        </DESC>\n'
            '    </BODY>\n'
            '</ENVELOPE>'
        )
    
    @staticmethod
    def get_vouchers_request(company_name: str = "", from_date: str = "", to_date: str = "") -> str:
        """Build request for vouchers."""
        return (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<ENVELOPE>\n'
            '    <HEADER>\n'
            '        <VERSION>1</VERSION>\n'
            '        <TALLYREQUEST>Export</TALLYREQUEST>\n'
            '        <TYPE>Collection</TYPE>\n'
            '        <ID>Voucher</ID>\n'
            '    </HEADER>\n'
            '    <BODY>\n'
            '        <DESC>\n'
            '            <STATICVARIABLES>\n'
            '                <SVEXPORTFORMAT>)SysName:XML</SVEXPORTFORMAT>\n'
            '            </STATICVARIABLES>\n'
            '            <TDL>\n'
            '                <TDLMESSAGE>\n'
            '                    <COLLECTION NAME="VoucherCollection">\n'
            '                        <TYPE>Voucher</TYPE>\n'
            '                        <FETCH>Name</FETCH>\n'
            '                        <FETCH>VoucherTypeName</FETCH>\n'
            '                        <FETCH>VoucherNumber</FETCH>\n'
            '                        <FETCH>Date</FETCH>\n'
            '                        <FETCH>Amount</FETCH>\n'
            '                        <FETCH>Narration</FETCH>\n'
            '                    </COLLECTION>\n'
            '                </TDLMESSAGE>\n'
            '            </TDL>\n'
            '        </DESC>\n'
            '    </BODY>\n'
            '</ENVELOPE>'
        )
    
    @staticmethod
    def get_voucher_type_request(company_name: str = "") -> str:
        """Build request for voucher types."""
        return (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<ENVELOPE>\n'
            '    <HEADER>\n'
            '        <VERSION>1</VERSION>\n'
            '        <TALLYREQUEST>Export</TALLYREQUEST>\n'
            '        <TYPE>Collection</TYPE>\n'
            '        <ID>VoucherType</ID>\n'
            '    </HEADER>\n'
            '    <BODY>\n'
            '        <DESC>\n'
            '            <STATICVARIABLES>\n'
            '                <SVEXPORTFORMAT>)SysName:XML</SVEXPORTFORMAT>\n'
            '            </STATICVARIABLES>\n'
            '            <TDL>\n'
            '                <TDLMESSAGE>\n'
            '                    <COLLECTION NAME="VoucherTypeCollection">\n'
            '                        <TYPE>VoucherType</TYPE>\n'
            '                        <FETCH>Name</FETCH>\n'
            '                    </COLLECTION>\n'
            '                </TDLMESSAGE>\n'
            '            </TDL>\n'
            '        </DESC>\n'
            '    </BODY>\n'
            '</ENVELOPE>'
        )
    
    @staticmethod
    def format_date_for_tally(date_str: str) -> str:
        """Format date for Tally request."""
        if not date_str:
            return ""
        try:
            for fmt in ["%Y-%m-%d", "%d-%m-%Y", "%Y%m%d"]:
                try:
                    dt = datetime.strptime(date_str, fmt)
                    return dt.strftime("%Y%m%d")
                except ValueError:
                    continue
            return date_str
        except Exception:
            return date_str
