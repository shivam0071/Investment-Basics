"""
Mobile Friendly
"""
import sys
from Mobile import track_stocks, track_stocks_long_term

if __name__ == '__main__':
    args = sys.argv
    if len(args) == 1 or len(args) > 2:
        track_stocks.get_prices()
        print("***************")
        print("****GETTING LONG TERM DATA *****")
        print("***************")
        track_stocks_long_term.get_prices()

    if len(args) == 2:
        if args[-1].lower() == 's':
            print("GETTING SWING TRADES DATA")
            track_stocks.get_prices()
        elif args[-1].lower() == 'l':
            print("GETTING LONG TERM DATA")
            track_stocks_long_term.get_prices()
