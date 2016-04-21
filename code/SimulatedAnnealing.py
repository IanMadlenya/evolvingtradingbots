
from MRSingleDay import MRSingleDay

if __name__ == '__main__':
    d = MRSingleDay("ZS201605_20160314.csv", 0.8, 4)
    d.calc_returns()
    print "all done boss"