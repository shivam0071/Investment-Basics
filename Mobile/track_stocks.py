import time
import json
import os
from bs4 import BeautifulSoup
import requests


def get_prices():
    url = "https://www.google.com/finance/quote/{ticker}:{exchange}"
    price_class = 'YMlKec fxKbKc'
    exchange = 'NSE'

    # CPR Entries are always less than current price
    # R1 Entry low means price has already crossed R1
    # R1 Entry high means price is above CPR but below R1
    if 'Mobile' in os.getcwd():
        ticker_list = json.load(open(os.path.join(os.path.normpath(os.getcwd() + os.sep + os.pardir),
                                                  'stocks.txt'), 'r')).get('SWING_TRADES', {})
    else:
        ticker_list = json.load(open(os.path.join(os.getcwd(), 'stocks.txt'), 'r')).get('SWING_TRADES', {})

    for ticker, value in ticker_list.items():
        local_url = url.format(ticker=ticker, exchange='NSE')
        res = requests.get(local_url)
        # print(f"*** GET RESPONSE FOR URL {local_url} is {res} ***")
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
            print(f"LOOKING FOR PRICE -- {val} for {key}")
            if key == 'r1_entry_low':
                if price <= val:
                    print('  *********  R1 LOW ENTRY  *****')
                    print(f'  ALERT: R1 LOW ENTRY is Possible\n  Current Price - {price}, R1 Price - {val}')
                    print('  ************************')
            elif key == 'r1_entry_high':
                if price >= val:
                    print('  ******  R1 HIGH ENTRY  ******')
                    print(f'  ALERT: R1 HIGH ENTRY is Possible\n  Current Price - {price}, R1 Price - {val}')
                    print('  ************************')
            elif key == 'cpr_entry':
                if price <= val:
                    print('  ******** CPR LOW ENTRY  ********')
                    print(f'  ALERT: CPR LOW ENTRY is Possible\n  Current Price - {price}, CPR Price - {val}')
                    print('  ************************')

        print('*' * 25)
        print('*' * 25)
        print('*' * 25)
        print()


if __name__ == '__main__':
    get_prices()
