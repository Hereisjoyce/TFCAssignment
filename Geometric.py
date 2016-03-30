__author__ = 'joycelei'

import math
import numpy as np
from scipy.stats import norm

r = 0.05
T = 3.0
S0 = 100.0
m = 100000

def AsianOption(r, T, muhat, d1hat, d2hat, K, OptionType):
    if OptionType == 'call':
        asiancall = math.exp(float(-r)*T)*(S0*math.exp(muhat*T)*norm.cdf(d1hat)-float(K)*norm.cdf(d2hat))
        return asiancall
    else:
        asianput = math.exp(float(-r)*T)*(float(K)*norm.cdf(-d2hat)-S0*math.exp(muhat*T)*norm.cdf(-d1hat))
        return asianput

def D1hat(K, muhat, sigmahat):
    d1hat = (math.log(S0/float(K))+(muhat+0.5*sigmahat**2)*T)/(sigmahat*math.sqrt(T))
    return d1hat

def D2hat(d1hat,sigmahat):
    d2hat= d1hat - sigmahat*math.sqrt(T)
    return d2hat

def Muhat(sigma, sigmahat, n):
    muhat = (r-0.5*sigma**2)*((n+1)/(2*n))+0.5*sigmahat**2
    return muhat

def Sigmahat(sigma, n):
    sigmahat = sigma*math.sqrt(((n+1)/(2*n+1))/6*n**2)
    return sigmahat

def BasketOption(bg0,mubg,d1baskethat,d2baskethat,OptionType,K):
    if OptionType == 'call':
        basketcall = math.exp(-r*T)*(bg0*math.exp(mubg*T)*norm.cdf(d1baskethat)-float(K)*norm.cdf(d2baskethat))
        return basketcall
    else:
        basketput = math.exp(-r*T)*(float(K)*norm.cdf(-d2baskethat)-bg0*math.exp(mubg*T)*norm.cdf(-d1baskethat))
        return basketput

def Volatility(sigma1, sigma2, rou, n):
    sigmabg = math.sqrt(sigma1*sigma2*rou)/n
    return sigmabg

def Driftbg(sigma1,sigma2,n,sigmabg):
    mubg = r-0.5*((sigma1**2+sigma2**2)/n)+0.5*sigmabg**2
    return mubg


if __name__ == "__main__":

    print "Go! Go! Test!"
    


