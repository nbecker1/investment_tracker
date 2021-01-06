import yfinance as yf
import pandas as pandas
from collections import defaultdict
from datetime import *
from functions import *
from Position import Position
from matplotlib import pyplot

today = str(datetime.today()).split()[0]

#most_recent_value = 64733.86-7837.65

spy = yf.Ticker("SPY")
lastclose = spy.history(period="1d")
lastclosedate = str(lastclose.index[-1]).split()[0]

transactions = pandas.read_csv('C:/Users/nbbas/Documents/STONKS/TransactionHistory.csv', sep=',', header=0)

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
        
total_value = 0

today = datetime.today().strftime('%Y-%m-%d')
file_name = "ar_summary_" + today + ".txt"
returns_summary = open(file_name, "w+")

total_return = 0

#compute and print cost basis, average sale price,annualized return
for ticker, events in eventhistory.items() :
    print("Cost Basis for " + ticker + ": " + str(cost_basis(events)))
    avg_sale = avg_sale_price(events)

    if(avg_sale == 0):
        print("No shares sold")

    else :
        print("Average sale price for " + ticker + ": " + str(avg_sale))

    #current_value = get_current_value(ticker, events)
    value = positions[ticker].current_value()

    print("Calculating Annual Return for " + ticker)

    ticker_ar = annualized_return(events,value)
    
    print("Current value: " + '${:,.2f}'.format(value))
    print("Annualized Return for " + ticker + ": " + ticker_ar)


    ticker_return = positions[ticker].total_return()
    total_return = total_return + ticker_return
    print("Total Profit/Loss for " + ticker + ": " + '${:,.2f}'.format(ticker_return))

    total_value = total_value + value

    #write returns to file
    returns_summary.write(ticker + " annualized return: " + ticker_ar + "\n")
    returns_summary.write(ticker + " total return: " + '${:,.2f}'.format(ticker_return) + "\n")
    
    #stockquantity
    #costbasis
    #for event in events :


#for i in chron_order:
#    print(i)
total_ar = annualized_return(allevents,total_value)
print("Annualized return: " + total_ar)
print("Total Portfolio Returns: " + '${:,.2f}'.format(total_return))

returns_summary.write("Total annualized return: " + total_ar + "\n")
returns_summary.write("Total return: " + '${:,.2f}'.format(total_return))
returns_summary.close()

transactiondate = datetime.strptime(row["DATE"], '%m/%d/%Y').date()


#print(eventhistory['AMZN'])
