import yfinance as yf 
import sys
from scipy import optimize
from datetime import *
from functions import *

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
        self.cost_bas = 0
        self.current_val = 0
        self.position_ret = 0
        self.annualized_ret = 0

    def compute_stats(self):
        self.cost_bas = self.cost_basis()
        self.current_val = self.current_value()
        self.position_ret = self.total_return()
        self.annualized_ret = annualized_return(self.transactionhistory, self.current_val)
        self.current_shares_held = self.current_share_count()

    def cost_basis(self):
        total_cost = 0
        current_shares = 0
        total_shares = 0
        #cost_basis = -1
        cost_basis_queue = []
        for transaction in self.transactionhistory:
            transaction_quantity = transaction["QUANTITY"]
            transaction_unitcost = transaction["PRICE"]
            transactioncost = transaction_unitcost * transaction_quantity
            if(transaction['ACTION'] == "BUY"):
                #For shares currently owned, store cost basis and quantity
                current_shares = current_shares + transaction_quantity
                cost_basis_queue.append((transaction_quantity, transaction_unitcost))

                #For all time shares purchased, store quantity and cost
                total_shares = total_shares + transaction_quantity
                total_cost = total_cost + transactioncost
            else:
                current_shares = current_shares - transaction_quantity 
                while len(cost_basis_queue) > 0 and transaction_quantity > 0:
                    next_lot_quantity = cost_basis_queue[0][0]
                    if next_lot_quantity < transaction_quantity:
                        cost_basis_queue.pop(0)
                        transaction_quantity = transaction_quantity - next_lot_quantity
                    else:
                        cost_basis_queue[0] = (next_lot_quantity - transaction_quantity, transaction_unitcost)
        if(current_shares == 0):
            return round(total_cost/total_shares,2)
        
        current_cost = 0
        for (a,b) in cost_basis_queue:
            current_cost = current_cost + a*b
        
        return round(current_cost/current_shares,2)
    
    def current_share_count(self):
        count = 0
        for transaction in self.transactionhistory:
            if transaction['ACTION'] == 'BUY':
                count = count + transaction['QUANTITY']
            else:
                count = count - transaction['QUANTITY']
        return count
    
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