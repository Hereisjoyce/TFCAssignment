__author__ = 'Joyce'
import math
from scipy.stats import norm
import csv

t=0 #time beigins
rate = 0.04
q = 0.2
maturity = 8.0/365.0
#Stock price: 1.9585, 1.9565,1.9585

stock_price31 = 1.9585
stock_price32 = 1.9565


def call_option_price(S, K, T, r, q, d1, d2):

    call_price = float(S) * math.exp(-q*(T-t)) * norm.cdf(d1) - float(K) * math.exp(-float(r)*(T-t)) * norm.cdf(d2)

    return call_price

def put_option_price(S, K, T, r, q, d1, d2):

    put_price = float(K) * math.exp(-r*(T-t)) * norm.cdf(-d2)-float(S) * math.exp(-q*(T-t)) * norm.cdf(-d1)

    return put_price

def Option_price(S, K, T, r, q, d1, d2,OptionType):
    if(OptionType=='C'):
        return call_option_price(S, K, T, r, q, d1, d2)
    else:
        return put_option_price(S, K, T, r, q, d1, d2)

def D1(S,K,rate,q,sigma,maturity):
    d1 = (math.log(S/K)+float(rate-q)*maturity)/(float(sigma)*math.sqrt(maturity))+0.5*float(sigma)*math.sqrt(maturity)
    return d1

def D2(S,K,rate,q, sigma,maturity):
    d2 = (math.log(S/K)+float(rate-q)*maturity)/(float(sigma)*math.sqrt(maturity))-0.5*float(sigma)*math.sqrt(maturity)
    return d2

def sigma_hat(Stock, Strike,rate, maturity):
    sigmahat = math.sqrt(2*abs((math.log(Stock/Strike)+rate*maturity)/maturity))
    return sigmahat

def Increment(option_price,true_data,Stock,d1):
    increment = (option_price-true_data)/(Stock*math.exp(-q*(maturity-float(t)))*math.sqrt(maturity-float(t)*norm._cdf(d1)))
    return increment

def UpperBound(OptionType,S,K):
    if OptionType=="C":
        UpperC = S * math.exp(-q*maturity)
        return UpperC
    else:
        UpperP = K * math.exp(-rate*maturity)
        return UpperP

def LowBound(OptionType,S,K):
    if OptionType=='C':
        LowC = max(S*math.exp(-q*maturity)-K*math.exp(-rate*maturity),0)
        return LowC
    else:
        LowP = max(0, K*math.exp(-rate*maturity)-S*math.exp(-q*maturity))
        return LowP




def get_and_process_data():
    volatilities = {
        1.8: {},
        1.85: {},
        1.9: {},
        1.95: {},
        2: {},
        2.05: {},
        2.1: {},
        2.15: {},
        2.2: {},
        2.25: {},
        2.3: {},
        2.35: {},
        2.4: {},
        2.45: {},
        2.5: {},
        2.55: {},
        2.6: {}

    }
    instruments_reader = csv.reader(open('instruments.csv','rb'))
    options = {}

    for row in instruments_reader:
        if row[1] != "Symbol" and row[1] != "510050":
            options[row[1]] = {
                'type': row[4],
                'strike': float(row[3])
            }

    marketdata_reader = csv.reader(open('marketdata.csv','rb'))

    for row_data in marketdata_reader:
        if row_data[1] == "Symbol" or row_data[1] == "510050":
            continue
        if len(row_data) < 6:
            continue
        else:
            if get_Time(row_data[0])=="30":
                options[row_data[1]]["ask31"] = float(row_data[5])
                options[row_data[1]]["bid31"] = float(row_data[3])
            elif get_Time(row_data[0])=="31":
                options[row_data[1]]["ask32"] = float(row_data[5])
                options[row_data[1]]["bid32"] = float(row_data[3])
            else:
                options[row_data[1]]["ask33"] = float(row_data[5])
                options[row_data[1]]["bid33"]= float(row_data[3])
        # print bidBook31

    for option in options:
        # print "%s:" % option,
        label = ["ask31", "ask32", "ask33", "bid31", "bid32", "bid33"]
        stock = [1.9585, 1.9565, 1.9585, 1.9585, 1.9565, 1.9585]
        for i in range(0,6):

            upper = UpperBound(options[option]["type"],stock[i],options[option]["strike"])
            lower = LowBound(options[option]["type"],stock[i],options[option]["strike"])
            if options[option][label[i]] > upper or options[option][label[i]] < lower:
                # print "NaN",
                volatilities[options[option]["strike"]][label[i]+options[option]["type"]] = "NaN"
            else:
                # sigmahat = sigma_hat(stock[i],options[option]["strike"],rate, maturity)

                # sigma = sigmahat
                # d1 = D1(stock[i], options[option]["strike"], rate, q, sigma, maturity)
                # d2 = D2(stock[i], options[option]["strike"], rate, q, sigma, maturity)
                # option_price = Option_price(stock[i], options[option]["strike"], maturity, rate, q, d1, d2, options[option]["type"])
                #print "%.4f" % calculate_implied_v(stock[i],options[option]["strike"], maturity, rate, options[option][label[i]],options[option]["type"]),
                volatilities[options[option]["strike"]][label[i]+options[option]["type"]] = calculate_implied_v(stock[i],options[option]["strike"], maturity, rate, options[option][label[i]],options[option]["type"])

    data = []
    sortOne = sorted(volatilities.items())
    # print sortOne
    for item in sortOne:
        dataOne = []
        dataOne.append(item[0])
        sortTwo = sorted(item[1].items())
        for item in sortTwo:
            dataOne.append("%.6s" % item[1])
            # print "%s: %.6s" % (item[0], item[1]),
        data.append(dataOne)
    print data
    return data




def get_Time(LocalTime):
    return LocalTime.split(" ")[-1][3:].split(":")[0]

#get_and_process_data()

def calculate_implied_v(S, K, maturity, r, true_data, OptionType):
    tol = 1e-8
    sigmadiff=1
    sigmahat = sigma_hat(S,K,r,maturity)
    sigma = sigmahat
    i=0

    while sigmadiff>=tol and i<=100:
        d1 = D1(S,K,rate,q,sigma,maturity)
        d2 = D2(S,K,rate,q,sigma,maturity)
        option_price = Option_price(S, K, maturity, r, q, d1, d2,OptionType)
        increment = Increment(option_price,true_data,S,d1)
        sigma = sigma-increment
        sigmadiff=abs(increment)
        i=i+1

    return sigma

def write_data(file, data):

    optionwriter = csv.writer(open(file,'wb'))
    optionwriter.writerow(['strike','ask31C', 'ask31P', 'ask32C', 'ask32P', 'ask33C', 'ask33P', 'bid31C', 'bid31P', 'bid32C', 'bid32P', 'bid33C', 'bid33P'])
    optionwriter.writerows(data)


if __name__ == "__main__":

    print "test begin ..."
    data = get_and_process_data()
    write_data("test.csv", data)
    
