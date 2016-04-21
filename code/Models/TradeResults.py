

class TradeResults:
    """This forces different strategies to return the same results"""
    def __init__(self, num_win, num_loose, cum_ret):
        self.cum_ret = cum_ret
        self.num_win = num_win
        self.num_loose = num_loose