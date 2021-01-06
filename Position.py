import yfinance as yf 
import sys


class Position:
    
    #compute cost basis, current value, total number of shares
    #assumed that dividends are reinvested

    def __init__(self, ticker):
        self.ticker = ticker
        self.transactionhistory = []
        self.costbasis = -1
        self.numshares = 0
        try: 
            self.price = yf.Ticker(ticker).history(period="1d")["Close"][-1]
        except (IndexError, KeyError):
            print("Cannot find symbol: " + ticker)
            self.price = float(input("Enter current share price: "))

    def compute_stats(self):
        numshares = 0
        totalcost = 0
        costbasis = -1
        first_transaction = self.transactionhistory[0]['DATE']
        
        for transaction in self.transactionhistory:
            quantity = transaction["QUANTITY"]
            cost = transaction["PRICE"]
            transactioncost = cost * quantity
            if(transaction['ACTION'] == "BUY"):
                numshares = numshares + quantity
                totalcost = totalcost + transactioncost
            else:
                numshares = numshares - quantity

        if numshares == 0:
            self.costbasis = round(costbasis, 2)
        else:
            self.costbasis = round(totalcost/numshares, 2)

        if self.price < 0 or numshares < 0:
            self.currentvalue = 0
        else:
            self.currentvalue = (numshares * self.price)

    def cost_basis(self):
        totalcost = 0
        totalshares = 0
        cost_basis = -1
        #first_transaction = transaction[0]
        for transaction in self.transactionhistory:
            quantity = transaction["QUANTITY"]
            unitcost = transaction["PRICE"]
            transactioncost = unitcost * quantity
            if(transaction['ACTION'] == "BUY"):
                totalshares = totalshares + quantity
                totalcost = totalcost + transactioncost
            #else:
            #    cost_basis = totalcost/totalshares
            #    totalcost = totalcost - (totalcost*quantity/totalshares)
            #    totalshares = totalshares - quantity

        if(totalshares == 0):
            return round(cost_basis,2)
        return round(totalcost/totalshares,2)
    
    def current_value(self):
        numshares = 0

        first_transaction_date = self.transactionhistory[0]['DATE']
        print(first_transaction_date)


        #history = yf.ticker(self.ticker)
        #history(period="max")
        for transaction in self.transactionhistory:
            if transaction['ACTION'] == 'BUY':
                numshares = numshares + transaction['QUANTITY']
            else :
                numshares = numshares - transaction['QUANTITY']
        if self.price < 0 or numshares < 0:
            return 0
        else:
            return (numshares * self.price)

    def total_return(self):
        total_out = 0
        total_in = 0

        shares_held = 0

        for transaction in self.transactionhistory:
            if transaction['ACTION'] == 'BUY':
                shares_held = shares_held + transaction['QUANTITY']
                total_out = total_out + transaction['QUANTITY'] * transaction['PRICE']
            else :
                shares_held = shares_held - transaction['QUANTITY']
                total_in = total_in + transaction['QUANTITY'] * transaction['PRICE']
        #add current value of owned shares
        total_in = total_in + shares_held * self.price
        return total_in - total_out