"""Analyze a portfolio.

Copyright 2017, Georgia Tech Research Corporation
Atlanta, Georgia 30332-0415
All Rights Reserved
"""

import pandas as pd
import numpy as np
import datetime as dt
import math
import argparse
from util import get_data, plot_data



# The student must update this code to properly implement the functionality
# This is the function that will be tested by the autograder
def assess_portfolio(sd = dt.datetime(2008,1,1), ed = dt.datetime(2009,1,1), \
    syms = ['GOOG','AAPL','GLD','XOM'], \
    allocs=[0.1,0.2,0.3,0.4], \
    sv=1000000, rfr=0.0, sf=252.0, \
    gen_plot=False):


    print allocs


    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later

    # Get daily portfolio value
    port_val = prices_SPY

    # add code here to compute daily portfolio values (functions should be in same file)
    normed = normalize(prices)
    allocated = getallocation(normed,allocs)
    pos_vals = getpositionvalues(allocated,sv)
    port_vals  = pos_vals.sum(axis = 1)

    cr, adr, sddr, sr = [0.25, 0.001, 0.0005, 2.1]

    #adr= today/yesterday - 1
    #adr and sddr calculation
    daily_rets = port_vals.copy()
    daily_rets = (port_vals/port_vals.shift(1)) - 1
    daily_rets.iloc[0] = 0
    daily_rets_without_first_row = daily_rets.iloc[1:]
    adr = daily_rets_without_first_row.mean()
    sddr = daily_rets_without_first_row.std()

    #cummulative return calculation
    cr = (port_vals/port_vals.iloc[0])-1
    cr = cr.tail(1).iloc[0]

    #calculating sharpe ratio
    numerator = (daily_rets_without_first_row - rfr).mean()
    denominator = daily_rets_without_first_row.std()
    sr =  math.sqrt(sf) * numerator/denominator

    ev = port_vals.iloc[-1]

    print "Sharpe Ratio:", sr
    print "Volatility (stdev of daily returns):", sddr
    print "Average Daily Return:", adr
    print "Cumulative Return:", cr
    print "end value", ev

    # Compare daily portfolio value with SPY using a normalized plot

    if gen_plot:

        # add code to plot here
        prices_SPY_Normed = prices_SPY.copy()
        prices_SPY_Normed = prices_SPY/prices_SPY.iloc[0]
        df_temp = pd.concat([port_vals/sv, prices_SPY_Normed], keys=['Portfolio', 'SPY'], axis=1)
        plot_data(df_temp)

    # Add code here to properly compute end value


    return cr, adr, sddr, sr, ev

def getallocation(normed,allocs):
    allocated = normed.copy()
    allocated = normed * allocs
    return allocated
def normalize(prices):
        normed = prices.copy()
        normed = prices/prices.iloc[0,:]
        return normed
def getpositionvalues(allocated,start_val):
    pos_vals = allocated.copy()
    pos_vals = allocated*start_val
    return pos_vals




def test_code():
    # This code WILL NOT be tested by the auto grader
    # It is only here to help you set up and test your code

    # Define input parameters
    # Note that ALL of these values will be set to different values by
    # the autograder!
    start_date = dt.datetime(2010,6,1)
    end_date = dt.datetime(2010,12,31)
    symbols = ['GOOG', 'AAPL', 'GLD', 'XOM']
    allocations = [0.2, 0.3, 0.4, 0.1]
    start_val = 1000000
    risk_free_rate = 0.0
    sample_freq = 252

    # Assess the portfolio
    cr, adr, sddr, sr, ev = assess_portfolio(sd = start_date, ed = end_date,\
        syms = symbols, \
        allocs = allocations,\
        sv = start_val, \
        gen_plot = True)

    # Print statistics
    print "Start Date:", start_date
    print "End Date:", end_date
    print "Symbols:", symbols
    print "Allocations:", allocations
    print "Sharpe Ratio:", sr
    print "Volatility (stdev of daily returns):", sddr
    print "Average Daily Return:", adr
    print "Cumulative Return:", cr

if __name__ == "__main__":

    parser = argparse.ArgumentParser( prog='analysis', add_help=True, description='Parses the arguments' )

    parser.add_argument('-p',action = "store_false", dest = "plot", default = "True")
    parser.add_argument('-s',action = "store", dest = "start_date", default = "start_date")
    parser.add_argument('-e',action = "store", dest = "end_date", default = "end_date")
    parser.add_argument('-x',nargs="*", action = "store", dest = "stock", default = "stock")
    parser.add_argument('-a',nargs="*", action = "store", dest = "allocations", default = "alloc", type = float)
    parser.add_argument('-sv',action = "store", dest = "sv", default = "sv", type = float)
    parser.add_argument('-rfr',action = "store", dest = "rfr", default = "rfr", type = float)
    parser.add_argument('-sf',action = "store", dest = "sf", default = "sf", type = int)

    args = parser.parse_args()

    # print args.allocations

    assess_portfolio(sd = args.start_date, ed = args.end_date, \
        syms = args.stock, \
        allocs=args.allocations, \
        sv=args.sv, rfr=args.rfr, sf=args.sf, \
        gen_plot=args.plot)

# python analysis.py -s 2010-01-01 -e 2010-12-31  -x 'GOOG' 'AAPL' 'GLD' 'XOM' -a 0.2 0.3 0.4 0.1 -sv 1000000 -rfr 0.0 -sf 252


    # test_code()
