#! /usr/bin/env python

from ib.ext.Contract import Contract
from ib.opt import ibConnection, message
from time import sleep
import sys


# handle historical data
class HistoricalData():
    def __init__(self, connection, symbol="ZS", sectype="FUT", exchange="ECBOT", expiry="201601"):
        self.connection = connection
        self.contract = Contract()
        self.contract.m_symbol = symbol
        self.contract.m_secType = sectype
        self.contract.m_exchange = exchange
        self.endtime = '%s15 00:00:00' % expiry
        self.contract.m_expiry = expiry
        self.contract.m_includeExpired = True

    def req(self):
        print "endtime: ", self.endtime
        self.connection.reqHistoricalData(
                tickerId=1,
                contract=self.contract,
                endDateTime=self.endtime,
                durationStr='1 D',
                barSizeSetting='1 min',
                whatToShow='TRADES',
                useRTH=0,
                formatDate=1)


if __name__ == '__main__':
    """
    Requests historical futures data.
    If there is something wrong, make sure that you can connect the api, and you have
    market data permissions.
    """
    if len(sys.argv) > 5 or len(sys.argv) < 4:
        print "usage: {} ticker expiration exchange <filename>".format(sys.argv[0])
        print "if no filename is given it will save to ./ticker_expiration.csv"
        print "example >{} ZS 201601 ECBOT ZS_201601.csv".format(sys.argv[0])
        print "for futures contracts historical data you only need"
        print "to specify the end month"
        sys.exit()

    if len(sys.argv) == 5:
        f_name = sys.argv[4]
    else:
        f_name = "{}_{}.csv".format(sys.argv[1], sys.argv[2])
    fw = open(f_name, 'w')
    fw.write("Date,Open,High,Low,Close,Volume,Adj Close\n")


    def recieve_error(m):
        print m


    def recieve_hist(m):
        if m.open != -1:
            fmt_str = "{},{},{},{},{},{},{}\n".format(m.date, m.open, m.high, m.low, m.close,
                                                      m.volume, m.WAP)
            fw.write(fmt_str)
            print fmt_str,


    con = ibConnection()  # Socket port 7496

    # GLOBEX ES local: ESU6 expiry: 20160916 FUT
    # hist = HistoricalData(con, symbol="ES", secType="FUT", exchange="GLOBEX")
    hist = HistoricalData(con,
                          symbol=sys.argv[1],
                          sectype="FUT",
                          exchange=sys.argv[3],
                          expiry=sys.argv[2])

    con.register(recieve_error, message.error)
    con.register(recieve_hist, message.historicalData)

    con.connect()
    sleep(1)

    print '* * * * REQUESTING HISTORICAL DATA * * * *'
    hist.req()
    sleep(5)
    print '* * * * CANCELING MARKET DATA * * * *'
    sleep(1)
    con.disconnect()
    fw.close()

    print "so long and thanks for all the fish"
