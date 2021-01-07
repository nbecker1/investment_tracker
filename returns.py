import yfinance as yf
import pandas as pandas
from collections import defaultdict
from datetime import *
from functions import *
from Position import Position
from matplotlib import pyplot
import sys
from argparse import ArgumentParser

def main(argv):

    #handle command line options
    parser = ArgumentParser()
    parser.add_argument("-c", "--compare", type=str, help='Ticker to compare against portfolio')
    
    args = vars(parser.parse_args())

    if args["compare"] :
        compare_ticker = args["compare"]

    spy = yf.Ticker("SPY")
    lastclose = spy.history(period="1d")
    lastclosedate = str(lastclose.index[-1]).split()[0]

    #transactions = pandas.read_csv('C:/Users/nbbas/Documents/investment_tracker/TransactionHistory.csv', sep=',', header=0)
    transactions = pandas.read_csv('TransactionHistory.csv', sep=',', header=0)

    eventhistory = defaultdict(list)
    positions = {}
    allevents = []

    #Store Transaction Data in transactions(a dictionary of string(ticker)->Position object)
    #Read from TransactionHistory.csv
    for idx, row in transactions.iterrows():
        event = row[1:]
        eventhistory[row["TICKER"]].append(event)
        allevents.append(event)
        if row["TICKER"] not in positions :
            positions[row["TICKER"]] = Position(row["TICKER"])
        positions[row["TICKER"]].transactionhistory.append(event)

    today = datetime.today().strftime('%Y-%m-%d')
    file_name = "ar_summary_" + today + ".txt"
    returns_summary = open(file_name, "w+")

    portfolio_return = 0
    portfolio_value = 0

    #compute and print cost basis, average sale price,annualized return
    for position in positions.values():
        ticker = position.ticker
        print("TICKER: " + ticker)

        position.compute_stats()
        portfolio_value = portfolio_value + position.current_val
        portfolio_return = portfolio_return + position.position_ret

        print("Cost Basis for " + ticker + ": " + '${:,.2f}'.format(position.cost_bas))
        print("Current Value for " + ticker + ": " + '${:,.2f}'.format(position.current_val))
        print("Annualized Return for " + ticker + ": " + position.annualized_ret)
        print("Total Return for " + ticker + ": " + '${:,.2f}'.format(position.position_ret))

        returns_summary.write(ticker + " annualized return: " + position.annualized_ret + "\n")
        returns_summary.write(ticker + " total return: " + '${:,.2f}'.format(position.position_ret) + "\n")


    #for i in chron_order:
    #    print(i)
    total_ar = annualized_return(allevents,portfolio_value)
    print("Annualized return: " + total_ar)
    print("Total Portfolio Returns: " + '${:,.2f}'.format(portfolio_return))

    returns_summary.write("Total annualized return: " + total_ar + "\n")
    returns_summary.write("Total return: " + '${:,.2f}'.format(portfolio_return))
    returns_summary.close()

    transactiondate = datetime.strptime(row["DATE"], '%m/%d/%Y').date()


    #compare to compare ticker
    if compare_ticker:
        ticker = yf.Ticker(compare_ticker)
        history = ticker.history(period="max")

        compare_position = Position(compare_ticker)

        #hypothetical_events = []
        for event in allevents:
            trade_cost = event["PRICE"] * event["QUANTITY"]
            trade_date = datetime.strptime(event["DATE"], '%m/%d/%Y').strftime('%Y-%m-%d')
            unit_cost = history.loc[trade_date]["Close"]

            new_event = {}
            new_event["DATE"] = event["DATE"]
            new_event["ACTION"] = event["ACTION"]
            new_event["PRICE"] = unit_cost
            new_event["QUANTITY"] = trade_cost / unit_cost
            
            compare_position.transactionhistory.append(new_event)

        comparative_return = compare_position.total_return()
        ann_ret = annualized_return(compare_position.transactionhistory,compare_position.current_value())
        print("Comparative annualized return for " + compare_ticker + ": " + ann_ret)
        print("Comparative total return for " + compare_ticker + ": " + '${:,.2f}'.format(comparative_return))


if __name__ == "__main__":
    main(sys.argv[1:])
