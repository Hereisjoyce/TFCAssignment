__author__ = 'Joyce'

import math
from scipy.stats import norm
import numpy as np

def call_option_price(S, K, T, r, rp):

    call_price = float(S) * math.exp(-rp*(T-t)) * norm.cdf(d1) - float(K) * math.exp(-float(r)*(T-t)) * norm.cdf(d2)
    #call_price = float(S) * norm.cdf(d1) - float(K) * math.exp(-float(r)*T) * norm.cdf(d2)

    return call_price

def put_option_price(S, K, T, r,rp):

    put_price = float(K) * math.exp(-r*(T-t)) * norm.cdf(-d2)-float(S) * math.exp(-rp*(T-t)) * norm.cdf(-d1)

    return put_price

stock = 100.0 #Stock price
t = 0 #Period begins
c_true = 5.8760
strike=100.0
maturity=0.5
rate=0.01
repo = 0
tol = 1e-8
i=0
sigmadiff=1

sigmahat = math.sqrt(2*abs((math.log(stock/strike)+rate*maturity)/maturity))
sigma = sigmahat
#print sigmahat
while sigmadiff>=tol and i<=100:
#d1= ((math.log(stock/strike)+(rate-repo)*(maturity-float(t)))/sigma*math.sqrt(maturity-float(t)))+0.5*sigma*math.sqrt(maturity-float(t))
    d1 = (math.log(stock/strike)+float(rate-repo)*maturity)/(float(sigma)*math.sqrt(maturity))+0.5*float(sigma)*math.sqrt(maturity)

#d2= ((math.log(stock/strike)+(rate-repo)*(maturity-float(t)))/sigma*math.sqrt(maturity-float(t)))-0.5*sigma*math.sqrt(maturity-float(t))
    d2 = (math.log(stock/strike)+float(rate-repo)*maturity)/(float(sigma)*math.sqrt(maturity))-0.5*float(sigma)*math.sqrt(maturity)

    call_price = call_option_price(stock, strike, maturity, rate, repo)
    increment = (call_price-c_true)/(stock*math.exp(-repo*(maturity-float(t)))*math.sqrt(maturity-float(t)*norm._cdf(d1)))
    sigma = sigma-increment
    sigmadiff=abs(increment)
    i=i+1

    print "---------------------------------"
    print 'd1: %.8f'% d1
    print 'd2: %.8f'% d2
    print 'Call price: %.8f'% call_price
    print 'sigma: %.8f'% sigma



