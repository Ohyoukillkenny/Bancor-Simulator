from smartToken import *
from customers import *
from market import *
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

def sychronizeMarket(market, timeSlot):
    market.sychronize(timeSlot)


# issue a new smart token
initIssue = 3000000
CRR = 0.2
initTransaction = initIssue * (1-CRR)
KennyCoin = Smartcoin(name='Kenny',reservetokenName='ETH',initCRR=0.2, initPrice=1,initIssueNum=initIssue)

# create two different markets
MyBancorMarket = BancorMarket(smartToken = KennyCoin)

TimeRound = 1000
bouncingInterval = 200
bouncingRange = 10
custNum = 5000
sigma = 0.1

custOriginalReserve_mu = 200
custOriginalSmartTokens_mu = 200
custOriginalReserve = np.random.normal(custOriginalReserve_mu, 0.1, custNum) # 0.5 is sigma
custOriginalSmartTokens = np.random.normal(custOriginalSmartTokens_mu, 0.1, custNum) # 0.5 is sigma