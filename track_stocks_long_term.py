import time

from bs4 import BeautifulSoup
import requests

url = "https://www.google.com/finance/quote/{ticker}:{exchange}"
price_class = 'YMlKec fxKbKc'
exchange = 'NSE'

# CPR Entries are always less than current price
# R1 Entry low means price has already crossed R1
# R1 Entry high means price is above CPR but below R1

ticker_list = {
    'TAKE': {'r1_entry_low': 20.0, 'r1_entry_high': None, 'cpr_entry': None},  # It's below CPR
    'LOVABLE': {'r1_entry_low': None, 'r1_entry_high': None, 'cpr_entry': 123.2},  # It's above CPR
    'IDFCFIRSTB': {'r1_entry_low': 71.1, 'r1_entry_high': None, 'cpr_entry': None},  # It's below CPR
    'ABFRL': {'r1_entry_low': 225.6, 'r1_entry_high': None, 'cpr_entry': None},  # Above CPR
    'NCC': {'r1_entry_low': 206.6, 'r1_entry_high': None, 'cpr_entry': None},  # BELOW CPR
    'TATAMOTORS': {'r1_entry_low': 965.6, 'r1_entry_high': 1040, 'cpr_entry': None},  # BELOW CPR
    'ONGC': {'r1_entry_low': 270, 'r1_entry_high': 292, 'cpr_entry': None},  # BELOW CPR
    'TATAPOWER': {'r1_entry_low': 405, 'r1_entry_high': 465, 'cpr_entry': None},  # ON CPR **
    'SHOPERSTOP': {'r1_entry_low': 630, 'r1_entry_high': 809, 'cpr_entry': None},  # BELOW CPR
    'MINDACORP': {'r1_entry_low': 392, 'r1_entry_high': None, 'cpr_entry': None},  # BELOW CPR
    'PNB': {'r1_entry_low': 120, 'r1_entry_high': None, 'cpr_entry': None},  # BELOW CPR
    'BHEL': {'r1_entry_low': 288, 'r1_entry_high': None, 'cpr_entry': 280},  # ON CPR **
    'IRFC': {'r1_entry_low': 140, 'r1_entry_high': None, 'cpr_entry': None},  # Below CPR
}

for ticker, value in ticker_list.items():
    local_url = url.format(ticker=ticker, exchange='NSE')
    res = requests.get(local_url)
    print(f"*** GET RESPONSE FOR URL {local_url} is {res} ***")
    if not res.ok:
        local_url = url.format(ticker=ticker, exchange='BSE')
        res = requests.get(local_url)
        time.sleep(2)
        if not res.ok:
            continue

    soup = BeautifulSoup(res.text, 'html.parser')
    price = soup.find(class_=price_class)
    price = float(soup.find(class_=price_class).text.strip()[1:].replace(',', ''))
    print(f"Current price of {ticker} is {price}")

    for key, val in value.items():
        if not val:
            continue
        print(f"LOOKING FOR PRICE -- {val}")
        if key == 'r1_entry_low':
            if price <= val:
                print('  ********************  R1 LOW ENTRY  ************************************************')
                print(f'  ALERT: R1 LOW ENTRY is Possible\n  Current Price - {price}, R1 Price - {val}')
                print('  **************************************************************************')
        elif key == 'r1_entry_high':
            if price >= val:
                print('  **********************  R1 HIGH ENTRY  ***************************************')
                print(f'  ALERT: R1 HIGH ENTRY is Possible\n  Current Price - {price}, R1 Price - {val}')
                print('  **************************************************************************')
        elif key == 'cpr_entry':
            if price <= val:
                print('  ************************* CPR LOW ENTRY  *****************************************')
                print(f'  ALERT: CPR LOW ENTRY is Possible\n  Current Price - {price}, CPR Price - {val}')
                print('  **************************************************************************')

    print('*' * 50)
    print('*' * 50)
    print('*' * 50)
    print()
