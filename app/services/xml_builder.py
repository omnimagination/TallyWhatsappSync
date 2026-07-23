"""
XML Request Builder for TallySync

Author: OmniMagination
Version: 1.0.0
"""

from datetime import datetime


class XMLBuilder:
    """Builder class for creating Tally XML requests."""
    
    @staticmethod
    def get_company_info_request(company_name: str = "") -> str:
        """Build request for company information."""
        return ''.join([
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<ENVELOPE>',
            '    <HEADER>',
            '        <VERSION>1</VERSION>',
            '        <TALLYREQUEST>Export</TALLYREQUEST>',
            '        <TYPE>Collection</TYPE>',
            '        <ID>Company</ID>',
            '    </HEADER>',
            '    <BODY>',
            '        <DESC>',
            '            <STATICVARIABLES>',
            '                <SVEXPORTFORMAT>test_ledgers_only.pySysName:XML</SVEXPORTFORMAT>',
            '            </STATICVARIABLES>',
            '            <TDL>',
            '                <TDLMESSAGE>',
            '                    <COLLECTION NAME="CompanyCollection">',
            '                        <TYPE>Company</TYPE>',
            '                        <FETCH>Name</FETCH>',
            '                        <FETCH>Address</FETCH>',
            '                        <FETCH>Phone</FETCH>',
            '                        <FETCH>Email</FETCH>',
            '                    </COLLECTION>',
            '                </TDLMESSAGE>',
            '            </TDL>',
            '        </DESC>',
            '    </BODY>',
            '</ENVELOPE>'
        ])
    
    @staticmethod
    def get_ledgers_request(company_name: str = "") -> str:
        """Build request for all ledgers - WORKING FORMAT."""
        return ''.join([
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<ENVELOPE>',
            '    <HEADER>',
            '        <VERSION>1</VERSION>',
            '        <TALLYREQUEST>Export</TALLYREQUEST>',
            '        <TYPE>Collection</TYPE>',
            '        <ID>Ledger</ID>',
            '    </HEADER>',
            '    <BODY>',
            '        <DESC>',
            '            <STATICVARIABLES>',
            '                <SVEXPORTFORMAT>test_ledgers_only.pySysName:XML</SVEXPORTFORMAT>',
            '            </STATICVARIABLES>',
            '            <TDL>',
            '                <TDLMESSAGE>',
            '                    <COLLECTION NAME="LedgerCollection">',
            '                        <TYPE>Ledger</TYPE>',
            '                        <FETCH>Name</FETCH>',
            '                        <FETCH>Parent</FETCH>',
            '                        <FETCH>Group</FETCH>',
            '                        <FETCH>OpeningBalance</FETCH>',
            '                        <FETCH>ClosingBalance</FETCH>',
            '                        <FETCH>Phone</FETCH>',
            '                        <FETCH>Email</FETCH>',
            '                        <FETCH>Address</FETCH>',
            '                        <FETCH>TaxRegNumber</FETCH>',
            '                        <FETCH>IncomeTaxNumber</FETCH>',
            '                    </COLLECTION>',
            '                </TDLMESSAGE>',
            '            </TDL>',
            '        </DESC>',
            '    </BODY>',
            '</ENVELOPE>'
        ])
    
    @staticmethod
    def get_ledger_detail_request(ledger_name: str, company_name: str = "") -> str:
        """Build request for specific ledger details."""
        return ''.join([
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<ENVELOPE>',
            '    <HEADER>',
            '        <VERSION>1</VERSION>',
            '        <TALLYREQUEST>Export</TALLYREQUEST>',
            '        <TYPE>Collection</TYPE>',
            '        <ID>Ledger</ID>',
            '    </HEADER>',
            '    <BODY>',
            '        <DESC>',
            '            <STATICVARIABLES>',
            '                <SVEXPORTFORMAT>test_ledgers_only.pySysName:XML</SVEXPORTFORMAT>',
            f'                <SVLedgerName>{ledger_name}</SVLedgerName>',
            '            </STATICVARIABLES>',
            '            <TDL>',
            '                <TDLMESSAGE>',
            '                    <COLLECTION NAME="SingleLedger">',
            '                        <TYPE>Ledger</TYPE>',
            '                        <FETCH>Name</FETCH>',
            '                        <FETCH>Parent</FETCH>',
            '                        <FETCH>ClosingBalance</FETCH>',
            '                    </COLLECTION>',
            '                </TDLMESSAGE>',
            '            </TDL>',
            '        </DESC>',
            '    </BODY>',
            '</ENVELOPE>'
        ])
    
    @staticmethod
    def get_vouchers_request(company_name: str = "", from_date: str = "", to_date: str = "") -> str:
        """Build request for vouchers."""
        return ''.join([
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<ENVELOPE>',
            '    <HEADER>',
            '        <VERSION>1</VERSION>',
            '        <TALLYREQUEST>Export</TALLYREQUEST>',
            '        <TYPE>Collection</TYPE>',
            '        <ID>Voucher</ID>',
            '    </HEADER>',
            '    <BODY>',
            '        <DESC>',
            '            <STATICVARIABLES>',
            '                <SVEXPORTFORMAT>test_ledgers_only.pySysName:XML</SVEXPORTFORMAT>',
            '            </STATICVARIABLES>',
            '            <TDL>',
            '                <TDLMESSAGE>',
            '                    <COLLECTION NAME="VoucherCollection">',
            '                        <TYPE>Voucher</TYPE>',
            '                        <FETCH>Name</FETCH>',
            '                        <FETCH>VoucherTypeName</FETCH>',
            '                        <FETCH>VoucherNumber</FETCH>',
            '                        <FETCH>Date</FETCH>',
            '                        <FETCH>Amount</FETCH>',
            '                        <FETCH>Narration</FETCH>',
            '                    </COLLECTION>',
            '                </TDLMESSAGE>',
            '            </TDL>',
            '        </DESC>',
            '    </BODY>',
            '</ENVELOPE>'
        ])
    
    @staticmethod
    def get_voucher_type_request(company_name: str = "") -> str:
        """Build request for voucher types."""
        return ''.join([
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<ENVELOPE>',
            '    <HEADER>',
            '        <VERSION>1</VERSION>',
            '        <TALLYREQUEST>Export</TALLYREQUEST>',
            '        <TYPE>Collection</TYPE>',
            '        <ID>VoucherType</ID>',
            '    </HEADER>',
            '    <BODY>',
            '        <DESC>',
            '            <STATICVARIABLES>',
            '                <SVEXPORTFORMAT>test_ledgers_only.pySysName:XML</SVEXPORTFORMAT>',
            '            </STATICVARIABLES>',
            '            <TDL>',
            '                <TDLMESSAGE>',
            '                    <COLLECTION NAME="VoucherTypeCollection">',
            '                        <TYPE>VoucherType</TYPE>',
            '                        <FETCH>Name</FETCH>',
            '                    </COLLECTION>',
            '                </TDLMESSAGE>',
            '            </TDL>',
            '        </DESC>',
            '    </BODY>',
            '</ENVELOPE>'
        ])
    
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
