__author__ = 'Joyce'

import math
from scipy.stats import norm

S = 100 #Stock price
t = 0 #Period begins

strike=[100.0,120.0,100.0,100.0,100.0]
maturity=[0.5,0.5,1.0,0.5,0.5]
vol=[0.2,0.2,0.2,0.3,0.2]
rate=[0.01,0.01,0.01,0.01,0.02]
i=1

#d1 = (math.log(SK)+float(r)*deltaT)/(float(sigma)*math.sqrt(deltaT))+0.5*float(sigma)*math.sqrt(deltaT)
#d2 = (math.log(SK)+float(r)*deltaT)/(float(sigma)*math.sqrt(deltaT))-0.5*float(sigma)*math.sqrt(deltaT)

def call_option_price(S, K, T, r, sigma):

    #call_price = float(S) * norm.cdf(d1) - float(K) * math.exp(-float(r)*deltaT) * norm.cdf(d2)
    call_price = float(S) * norm.cdf(d1) - float(K) * math.exp(-float(r)*T) * norm.cdf(d2)

    return call_price

def put_option_price(S, K, T, r, sigma):

     #put_price = float(K) * math.exp(-float(r)*deltaT) * norm.cdf(-d2)-S * norm.cdf(-d1)
     put_price = float(K) * math.exp(-float(r)*T) * norm.cdf(-d2)-S * norm.cdf(-d1)

     return put_price


#call_price = float(S) * norm.cdf(d1) - float(K) * math.exp(-float(r)*deltaT) * norm.cdf(d2)
#put_price = float(K) * math.exp(-float(r)*deltaT) * norm.cdf(-d2)-S * norm.cdf(-d1)


while i<6:

    K=strike[i-1]
    T=maturity[i-1]
    sigma=vol[i-1]
    r=rate[i-1]
    SK = float(S)/float(K)

    d1 = (math.log(SK)+float(r)*T)/(float(sigma)*math.sqrt(T))+0.5*float(sigma)*math.sqrt(T)
    d2 = (math.log(SK)+float(r)*T)/(float(sigma)*math.sqrt(T))-0.5*float(sigma)*math.sqrt(T)


    call_price=call_option_price(S, K, T, r, sigma)
    put_price=put_option_price(S, K, T, r, sigma)

    i=i+1
    #K = raw_input('Strike price:')
    #T = raw_input('Maturity:')
    #sigma = raw_input('sigma:')
    #r = raw_input('risk-free interest rate:')


    #d1 = (math.log(SK)+float(r)*deltaT)/(float(sigma)*math.sqrt(deltaT))+0.5*float(sigma)*math.sqrt(deltaT)
    #d2 = (math.log(SK)+float(r)*deltaT)/(float(sigma)*math.sqrt(deltaT))-0.5*float(sigma)*math.sqrt(deltaT)


    print '************************'
    print 'd1: %.4f'% d1
    print 'd2: %.4f'% d2
    print 'call: %.4f'% call_price
    print 'put: %.4f'% put_price
else:
    print '-----------------------'
    print 'Finished!'
