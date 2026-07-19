from app.services.xml_builder import XMLBuilder
from app.services.xml_parser import XMLParser
from app.services.tally_client import TallyClient

print('=' * 60)
print('TESTING UPDATED PARSER')
print('=' * 60)

client = TallyClient()
xml_req = XMLBuilder.get_ledgers_request()
response = client.send_request(xml_req)

print(f'Response: {len(response)} bytes')

ledgers = XMLParser.parse_ledgers(response)
print(f'Parsed {len(ledgers)} ledgers!')

for i, ledger in enumerate(ledgers[:5]):
    name = ledger.get('name', 'Unknown')
    group = ledger.get('group_name', 'N/A')
    balance = ledger.get('closing_balance', 0)
    print(f'  {i+1}. {name} | Group: {group} | Balance: {balance}')

if len(ledgers) > 5:
    print(f'  ... and {len(ledgers) - 5} more')

print('=' * 60)
