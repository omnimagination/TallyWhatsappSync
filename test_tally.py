import requests
import re

url = 'http://localhost:9000'

xml = """<?xml version="1.0" encoding="UTF-8"?>
<ENVELOPE>
    <HEADER>
        <VERSION>1</VERSION>
        <TALLYREQUEST>Export</TALLYREQUEST>
        <TYPE>Collection</TYPE>
        <ID>Ledger</ID>
    </HEADER>
    <BODY>
        <DESC>
            <STATICVARIABLES>
                <SVEXPORTFORMAT>test_tally.pySysName:XML</SVEXPORTFORMAT>
            </STATICVARIABLES>
            <TDL>
                <TDLMESSAGE>
                    <COLLECTION NAME="LedgerCollection">
                        <TYPE>Ledger</TYPE>
                        <FETCH>Name</FETCH>
                        <FETCH>Parent</FETCH>
                        <FETCH>ClosingBalance</FETCH>
                    </COLLECTION>
                </TDLMESSAGE>
            </TDL>
        </DESC>
    </BODY>
</ENVELOPE>"""

print('Testing TDL Collection...')
response = requests.post(url, data=xml, headers={'Content-Type': 'application/xml'})

print(f'Status: {response.status_code}')
print(f'Total bytes: {len(response.text)}')

# Clean invalid XML characters
cleaned = re.sub(r'&#\d+;', '', response.text)

print('\n--- LEDGER ENTRIES FOUND ---')

# Find all LEDGER tags
import re
ledgers = re.findall(r'<LEDGER[^>]*NAME="([^"]*)"[^>]*>(.*?)</LEDGER>', cleaned, re.DOTALL)

print(f'Found {len(ledgers)} ledgers!')

for i, (name, content) in enumerate(ledgers[:5]):
    print(f'\n[{i+1}] {name}')
    parent = re.search(r'<PARENT[^>]*>([^<]*)</PARENT>', content)
    balance = re.search(r'<CLOSINGBALANCE[^>]*>([^<]*)</CLOSINGBALANCE>', content)
    if parent:
        print(f'    Parent: {parent.group(1)}')
    if balance:
        print(f'    Balance: {balance.group(1)}')

if len(ledgers) > 5:
    print(f'\n... and {len(ledgers) - 5} more')

print('\n--- RAW XML (first 1500 chars) ---')
print(response.text[:1500])
