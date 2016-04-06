__author__ = 'joycelei'

import math
import numpy as np
import Geometric as Geom

#Input
r = 0.05
#T = 3.0
#S = 100.0
m = 1000000
#n: number of observation times
#dt: the time slot
#control: with control variate
#confidenceC: confidence area

def ArithAsianOption(sigma,n,S,K,OptionType,ControlKey,T):
    dt = T/float(n)
    drift = math.exp((r-0.5*sigma*sigma)*dt)

    arithPayoff = [0.0]*m
    geoPayoff = [0.0]*m
    Z = [0.0]*m
    XY = [0.0]*m

    # np.random.seed(0)
    for i in range(0,m):


        growthFactor = drift*math.exp(sigma*math.sqrt(dt)*np.random.standard_normal(1)[0])

        SPath = [0.0]*n
        SPath[0]= float(S)*growthFactor
        for j in range(1,n):

            growthFactor= drift*math.exp(sigma*math.sqrt(dt)*np.random.standard_normal(1)[0])
            SPath[j]=SPath[j-1]*growthFactor


        #Arithmetic mean
        arithMean = np.mean(SPath)
        if OptionType=='call':
            arithPayoff[i]=math.exp(-r*T)*max(arithMean-K,0)
        elif OptionType == 'put':
            arithPayoff[i]=math.exp(-r*T)*max(K-arithMean,0)

        #Geometric mean
        logSpath = [math.log(x) for x in SPath]
        geoMean=math.exp((1/float(n))*np.sum(logSpath))
        if OptionType=='call':
            geoPayoff[i]=math.exp(-r*T)*max(geoMean-K,0)
        elif OptionType == 'put':
            geoPayoff[i]=math.exp(-r*T)*max(-geoMean+K,0)

    # print arithPayoff
    #Standard Monte Carlo
    if ControlKey=='standard':
        #print "enter standard:"
        Pmean=np.mean(arithPayoff)
        Pstd=np.std(arithPayoff)
        conLow = Pmean-1.96*Pstd/math.sqrt(m)
        conUp = Pmean+1.96*Pstd/math.sqrt(m)
        print "PMean: %.6f, PStd: %.6f, [%.6f, %.6f]" % (Pmean, Pstd, conLow, conUp)

    #with control variate
    elif ControlKey =='control':

        for q in range(0,m):
            XY[q]=arithPayoff[q]*geoPayoff[q]
        covXY=np.mean(XY)-(np.mean(arithPayoff)*np.mean(geoPayoff))
        theta=covXY/np.var(geoPayoff)
        sigmahat = Geom.Sigmahat(sigma,float(n))
        muhat = Geom.Muhat(sigma,sigmahat,n)
        d1hat = Geom.D1hat(K,muhat,sigmahat)
        d2hat = Geom.D2hat(K,muhat,sigmahat)
        geo = Geom.AsianOption(r,T,muhat,d1hat,d2hat,K,OptionType)
        print sigmahat,muhat
        print d1hat,d2hat
        print geo
        for k in range(0,m):

            Z[k] = arithPayoff[k]+theta*(geo-geoPayoff[k])

        Zmean = np.mean(Z)
        Zstd = np.std(Z)
        conControlLow = Zmean-1.96*Zstd/math.sqrt(m)
        conControlUp = Zmean+1.96*Zstd/math.sqrt(m)
        print "ZMean: %.6f, ZStd: %.6f, [%.6f, %.6f]" % (Zmean, Zstd, conControlLow, conControlUp)


def ProcessMonteCarloAsianControl():
    print "enter control cal"
    arithmeticControl = ArithAsianOption(0.3,50,100.0,100.0,"put","control",3.0)
    print "control:",arithmeticControl

def ProcessMonteCarloAsianNoControl():
    ArithAsianOption(0.3,50,100.0,100.0,"put","standard",3.0)


if __name__ == '__main__':
    print "Go! Go! Test Monte Carlo Asian!"
    # ProcessMonteCarloAsianControl()
    ProcessMonteCarloAsianNoControl()