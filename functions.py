from datetime import *
from scipy import optimize

def cost_basis(transactionhistory):
    totalcost = 0
    totalshares = 0
    cost_basis = -1
    for transaction in transactionhistory:
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

def avg_sale_price(transactionhistory) :
    totalcost = 0
    totalshares = 0
    for transaction in transactionhistory:
        quantity = transaction["QUANTITY"]
        unitcost = transaction["PRICE"]
        transactioncost = unitcost * quantity
        if(transaction['ACTION'] == "SELL"):
            totalshares = totalshares + quantity
            totalcost = totalcost + transactioncost
    if totalshares != 0:   
        return round(totalcost/totalshares,2) 
    else:
        return 0

def xnpv(rate,transactions):
    t0 = transactions[0][0]
    return sum([cf/(1+rate)**((t-t0).days/365.0) for (t,cf) in transactions])

def xirr(transactions,guess=0.1):
    return optimize.newton(lambda r: xnpv(r,transactions),guess)

def annualized_return(events, final_value):
    chron_order = []

    for transaction in events:
        tran_date = datetime.strptime(transaction["DATE"], '%m/%d/%Y').date()
        amount = 0
        if transaction["ACTION"] == "BUY":
            amount = transaction["PRICE"] * transaction["QUANTITY"]
        else:
            amount = -transaction["PRICE"] * transaction["QUANTITY"]
        chron_order.append((tran_date, amount))

    chron_order.append((date.today(), -final_value))

    if len(chron_order) == 2:
        today = date.today()
        invesment_date = chron_order[0][0]
        delta  = today - invesment_date

        initial_value = chron_order[0][1]

        rate_of_return = (final_value/initial_value)/(delta.days/365.0)

        return "{:.2%}".format(rate_of_return)
    else:
        return "{:.2%}".format(xirr(chron_order))
