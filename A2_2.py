__author__ = 'Joyce'

from scipy import stats
import math
import numpy as np
import csv

#data = []

def wirte_data(data_list, file_name):
    fp = open(file_name, "w")
    for i in data_list:
        tmp = str(i)+ "\n"
        fp.writelines(tmp)

    fp.close()



coe = 0.5
mu, sigma = 0, 1.0
X = stats.norm(mu, sigma)
x = X.rvs(size=100)
mx = np.mean(x)
vx = np.var(x)
Y = stats.norm(mu, sigma)
y = Y.rvs(size=100)
Z = 0.5 * x + math.sqrt(1-0.5**2) * y



#X = np.random.normal(mu, sigma, 100)
#Y = np.random.normal(mu, sigma, 100)

#def generate_z():
 #  for i in range(0,len(x)):
  #    Z = 0.5 * x[i] + math.sqrt(1+0.5*0.5) * y[i]
   #   return Z



#z=generate_z()
z = np.array(Z)
mz = np.mean(z)
vz = np.var(z)

wirte_data(x, "xrandom.txt")
wirte_data(y, "yrandom.txt")
wirte_data(z, "zrandom.txt")

#cov = np.mean((x-mx)*(z-mz))
coe_ver = np.mean((x-mx)*(z-mz)) / math.sqrt(vx*vz)
print coe_ver

if coe_ver == coe:
    print 'The result is: ', True
else:
    print 'The result is: ', False
    #data[x,y,z]

#optionwriter = csv.writer(open("Question2.txt",'wb'))
#optionwriter.writerow(['X','Y', 'Z'])
#optionwriter.writerows(data)