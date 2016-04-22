
from MRSingleDay import MRSingleDay

if __name__ == '__main__':
    d = MRSingleDay("ZS201605_20160314.csv", 0.8, 4, 20, -20)
    ro = d.calc_returns()
    print "winning: {}, loosing: {}, profit: {}".format(ro.num_win, ro.num_loose, ro.cum_ret)


    print "all done boss"