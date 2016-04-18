#! /usr/bin/env python

from ib.ext.Contract import Contract
from ib.opt import ibConnection, message
from time import sleep
from datetime import datetime, timedelta


# handle historical data
class HistoricalData():
    def __init__(self, connection, symbol="ZS", sectype="FUT", exchange="ECBOT", expiry="201601",end_day="20160114"):
        self.connection = connection
        self.contract = Contract()
        self.contract.m_symbol = symbol
        self.contract.m_secType = sectype
        self.contract.m_exchange = exchange
        self.endtime = '%s 11:20:00' % end_day  # minute bars come back in local time zone, soybeans trade 8:30-13:20 CT
        self.contract.m_expiry = expiry         # trading hours: http://www.cmegroup.com/trading-hours.html
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


def create_con_arr(contract_strings):
    ret_l = []
    for contract_string in contract_strings:
        con_d = datetime.strptime("%s15" % contract_string, "%Y%m%d")
        ret_l.append((con_d, contract_string))

    return ret_l


def recieve_error(m):
    print m


def recieve_hist(m):
    if m.open != -1:
        fmt_str = "{},{},{},{},{},{},{}\n".format(m.date, m.open, m.high, m.low, m.close,
                                                  m.volume, m.WAP)
        fw.write(fmt_str)
        print fmt_str,

# trading holidays http://cfe.cboe.com/aboutcfe/expirationcalendar.aspx
holidays2015 = set(["20150101", "20150119", "20150216", "20150403", "20150525", "20150704", "20150907", "20151126", "20151225"])
holidays2016 = set(["20160101", "20160118", "20160215", "20160325", "20160530", "20160704", "20160905", "20161124", "20161226"])
holidays = holidays2015.union(holidays2016)

def is_trading_day(in_do):
    if in_do.weekday() > 4:
        return False  # checks if the d.o.w. is Sat or Sun
    elif in_do.strftime("%Y%m%d") in holidays:
        print "trading holiday, skipping!"
        return False
    return True




if __name__ == '__main__':
    """
    Requests historical futures data.
    If there is something wrong, make sure that you can connect the api, and you have
    market data permissions.
    """

    con = ibConnection()  # Socket port 7496
    con.register(recieve_error, message.error)
    con.register(recieve_hist, message.historicalData)
    con.connect()
    sleep(1)

    symbol = "ZS"
    exchange = "ECBOT"

    # soybeans has 7 contracts/year
    # http://www.cmegroup.com/trading/agricultural/grain-and-oilseed/soybean_contract_specifications.html
    # Jan, March, May, July, August, September, November
    # contracts = ["201605", "201603", "201601", "201511", "201509", "201508", "201507",
    #             "201505", "201503", "201501", "201411", "201409", "201408", "201407", "201405", "201403"]

    contracts = ["201603", "201601", "201511", "201509", "201508", "201507",
                 "201505", "201503", "201501", "201411", "201409", "201408", "201407", "201405", "201403"]
    con_l = create_con_arr(contracts)

    curr_con = con_l.pop(0)
    #curr_date = datetime.strptime("20160418", "%Y%m%d")
    curr_date = datetime.strptime("20160122", "%Y%m%d")
    end_date = datetime.strptime("20140418", "%Y%m%d")
    # for loop here
    while curr_date > end_date:
        print curr_date, "contract: ",curr_con[1]

        end_day = curr_date.strftime("%Y%m%d")
        # download data
        if is_trading_day(curr_date):
            f_name = "{}{}_{}.csv".format(symbol, curr_con[1], end_day)
            fw = open(f_name, 'w')
            fw.write("Date,Open,High,Low,Close,Volume,Adj Close\n")
            # GLOBEX ES local: ESU6 expiry: 20160916 FUT
            # hist = HistoricalData(con, symbol="ES", secType="FUT", exchange="GLOBEX")
            hist = HistoricalData(con,
                          symbol=symbol,
                          sectype="FUT",
                          exchange=exchange,
                          expiry=curr_con[1],
                          end_day=end_day
                          )
            hist.req()
            sleep(11)
            fw.close()


        # update current contract
        if curr_date < con_l[0][0]:
            curr_con = con_l.pop(0)

        # update current date
        curr_date = curr_date - timedelta(days=1)

    # start with most recent date

    con.disconnect()

    print "so long and thanks for all the fish"
