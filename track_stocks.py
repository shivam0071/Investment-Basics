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
    'MOREPENLAB': {'r1_entry_low': None, 'r1_entry_high': 53, 'cpr_entry': 49.6},
    'TATAPOWER': {'r1_entry_low': None, 'r1_entry_high': 460, 'cpr_entry': 444},
    'IREDA': {'r1_entry_low': 176, 'r1_entry_high': 193, 'cpr_entry': 170},
    'IOB': {'r1_entry_low': None, 'r1_entry_high': 70, 'cpr_entry': 66.5},
    'TI': {'r1_entry_low': None, 'r1_entry_high': 248, 'cpr_entry': 236},
    'UPL': {'r1_entry_low': None, 'r1_entry_high': None, 'cpr_entry': 510},
    'PENINLAND': {'r1_entry_low': 56, 'r1_entry_high': None, 'cpr_entry': 53},
    'ORIENTHOT': {'r1_entry_low': 149, 'r1_entry_high': None, 'cpr_entry': 132},
    'TAJGVK': {'r1_entry_low': None, 'r1_entry_high': 424, 'cpr_entry': 372},
    'TRITURBINE': {'r1_entry_low': None, 'r1_entry_high': None, 'cpr_entry': 541},
    'SRF': {'r1_entry_low': 2180, 'r1_entry_high': None, 'cpr_entry': None}
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
