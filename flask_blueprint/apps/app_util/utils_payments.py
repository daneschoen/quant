

"""
Balanced charges 2.9% plus $0.30 for credit card transactions
ACH: 1% plus $0.30, $5 cap
Payments to merchants: $0.25 ACH same day/next day


CB Receiver Fee % (Adjusted) =
  CareBooker Receiver Fee (Always 6.3%) - ((Effective Service Receiver Fee - Effective Provider Fee)/2)

Effective Service Receiver Fee = given in ranges in blue on right of excel (example: $10-$24.99 = 12.7%)

Effective Provider Fee (Basic, Not Adjusted)  = 1 - (Payment to Service Provider / Appointment Value)

Payments To Service Provider (Basic, Not Adjusted)  =  Appointment Value - CB Revenue From Service Provider (6.3% * Appointment Value) - (0.25)

CB Provider Fee % (Adjusted) = CB Provider Fee (always 6.3%) + ((Effective Fee To Service Receiver (Basic / based on range) - Effective Fee To Service Provider (Basic)) / 2)
"""

from constants import *


def calcFeeAdj_customer(appt_amt):
    #return FEE_CB_CUSTOMER - (calcFee_customer(appt_amt)-calcFee_provider(appt_amt))
    pass

def calcFee_customer(appt_amt):
    pass


def calcPayment_provider(appt_amt):
    return appt_amt - ((FEE_CB_PROVIDER/100)*appt_amt) - 0.25

def calcFee_provider(appt_amt):
    return 1 - (calcPayment_provider(appt_amt)/appt_amt)

def calcFeeAdj_provider(appt_amt):
    #return FEE_CB_PROVIDER + ( ( (Basic / basedonrange) - calcFee_provider(appt_amt)) / 2 )
    pass

def calculateFee_balanced_customer(cost):
    percentage = 0
    if cost < 5:
        percentage = .35
    elif cost  < 10:
        percentage = .095
    elif cost  < 25:
        percentage = .064
    elif cost < 50:
        percentage = .0442
    elif cost < 75:
        percentage = .0383
    elif cost < 100:
        percentage = .0361
    elif cost < 125:
        percentage = .0350
    elif cost < 150:
        percentage = .0344
    elif cost < 175:
        percentage = .0339
    elif cost < 200:
        percentage = .0336
    elif cost < 225:
        percentage = .0334
    elif cost < 250:
        percentage = .0332
    elif cost < 275:
        percentage = .0331
    elif cost < 300:
        percentage = .0329
    elif cost < 350:
        percentage = .0328
    elif cost < 400:
        percentage = .0327
    elif cost < 500:
        percentage = .0326
    elif cost < 600:
        percentage = .0324
    elif cost < 700:
        percentage = .0323
    elif cost < 800:
        percentage = .0322
    elif cost < 900:
        percentage = .0322
    elif cost < 1000:
        percentage = .0321
    else:
        percentage = .0321

    return percentage

