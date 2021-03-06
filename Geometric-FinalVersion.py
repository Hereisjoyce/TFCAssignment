__author__ = 'joycelei'

import math
from scipy.stats import norm

r = 0.05
T = 3.0
s = 100.0

def AsianOption(r, T, muhat, d1hat, d2hat, K, OptionType):
    if OptionType == 'call':
        asiancall = math.exp(float(-r)*T)*(s*math.exp(muhat*T)*norm.cdf(d1hat)-float(K)*norm.cdf(d2hat))
        return asiancall
    elif OptionType == 'put':
        asianput = math.exp(-r*T)*(float(K)*norm.cdf(-d2hat)-s*math.exp(muhat*T)*norm.cdf(-d1hat))
        return asianput
    else:
        print "Not correct asian option."

def D1hat(K, muhat, sigmahat):
    #d1hat = (math.log(s/K)+(muhat+0.5*sigmahat**2)*T)/(sigmahat*math.sqrt(T))
    #d1hat = (math.log(s/K)+(muhat+0.5*math.pow(sigmahat,2))*T)/(sigmahat*math.sqrt(T))
    # print sigmahat
    d1hat = (math.log(s/K)+(muhat+0.5*math.pow(sigmahat,2))*T)/(sigmahat*math.sqrt(T))
    return d1hat

def D2hat(K, muhat, sigmahat):
    #d2hat= d1hat - sigmahat*math.sqrt(T)
    d2hat = (math.log(s/K)+(muhat+0.5*math.pow(sigmahat,2))*T)/(sigmahat*math.sqrt(T))-sigmahat*math.sqrt(T)
    return d2hat

def Muhat(sigma, sigmahat, n):
    #muhat = ((r-0.5*math.pow(sigma,2))*((n+1)/(2*n)))+0.5*math.pow(sigmahat,2)
    muhat = (r-0.5*sigma**2)*(n+1)/(2*n)+0.5*sigmahat**2
    return muhat

def Sigmahat(sigma, n):
    #sigmahat = sigma*math.sqrt(((n+1)*(2*n+1))/6*(n**2))
    sigmahat = sigma * math.sqrt(((n+1)*(2*n+1))/(6*n*n))
    return sigmahat

def BasketOption(bg,mubg,d1baskethat,d2baskethat,OptionType,K):
    if OptionType == 'call':
        basketcall = math.exp(-r*T)*(bg*math.exp(mubg*T)*norm.cdf(d1baskethat)-float(K)*norm.cdf(d2baskethat))
        return basketcall
    elif OptionType == 'put':
        basketput = math.exp(-r*T)*(float(K)*norm.cdf(-d2baskethat)-bg*math.exp(mubg*T)*norm.cdf(-d1baskethat))
        return basketput
    else:
        print "Not correct basket option."

def Volatilitybg(sigma1, sigma2, rou, n):
    sigmabg = math.sqrt(sigma1*sigma2*rou*2+sigma1*sigma1+sigma2*sigma2)/n
    return sigmabg

def Driftbg(sigma1,sigma2,n,sigmabg):
    mubg = r-0.5*((sigma1*sigma1+sigma2*sigma2)/n)+0.5*math.pow(sigmabg,2)
    return mubg

def D1BasketHat(bg,K,sigmabg,mubg):
    d1baskethat = (math.log(bg/K)+(mubg+0.5*math.pow(sigmabg,2))*T)/(sigmabg*math.sqrt(T))
    return d1baskethat

def D2BasketHat(bg,K,sigmabg,mubg):
    #d2baskethat = d1baskethat-sigmabg*math.sqrt(T)
    d2baskethat = (math.log(bg/K)+(mubg+0.5*math.pow(sigmabg,2))*T)/(sigmabg*math.sqrt(T))-sigmabg*math.sqrt(T)
    return d2baskethat


def ProcessAsian():
    Sigma = [0.3, 0.3, 0.4, 0.3, 0.3, 0.4]
    K = 100.0
    n = [50.0, 100.0, 50.0, 50.0, 100.0, 50.0]
    optionType = ['put', 'put', 'put', 'call', 'call', 'call']

    for i in range(0,len(Sigma)):
        sigmahat = Sigmahat(Sigma[i], n[i])
        muhat = Muhat(Sigma[i], sigmahat, n[i])
        #print "s: ", s
        #print "-r*T: ", -r*T
        #print "i: ",i
        print "muhat: ", muhat
        print "sigmahat: ", sigmahat
        d1hat = D1hat(K, muhat, sigmahat)
        d2hat = D2hat(K, muhat, sigmahat)
        asianOption = AsianOption(r, T, muhat, d1hat, d2hat, K, optionType[i])
        print "Asina:", asianOption

def ProcessBasket():
    S1 = 100.0
    S2 = 100.0
    bg = math.sqrt(S1*S2)
    K = [100.0, 100.0, 100.0, 80.0, 120.0, 100.0,100.0, 100.0, 100.0, 80.0, 120.0, 100.0]
    Sigma1 = [0.3,0.3,0.1,0.3,0.3,0.5,0.3,0.3,0.1,0.3,0.3,0.5]
    Sigma2 = [0.3,0.3,0.3,0.3,0.3,0.5,0.3,0.3,0.3,0.3,0.3,0.5]
    Rou = [0.5,0.9,0.5,0.5,0.5,0.5,0.5,0.9,0.5,0.5,0.5,0.5]
    optionType = ['put','put','put','put','put','put','call','call','call','call','call','call']
    for i in range(0,len(K)):
        sigmabg = Volatilitybg(Sigma1[i], Sigma2[i], Rou[i], 2)
        mubg = Driftbg(Sigma1[i],Sigma2[i],2,sigmabg)
        d1baskethat = D1BasketHat(bg,K[i],sigmabg,mubg)
        d2baskethat = D2BasketHat(bg,K[i],sigmabg,mubg)
        basketAsian = BasketOption(bg,mubg,d1baskethat,d2baskethat,optionType[i],K[i])
        #print "d1: ","d2: ","basket: "
        print "d1:",d1baskethat, "d2:",d2baskethat,"ba:",basketAsian


if __name__ == "__main__":

    print "Go! Go! Test Geometric!"
    print " "
    print "Asian Options:"
    ProcessAsian()
    print " "
    print "Basket Options:"
    ProcessBasket()
    print 'Finished!'





