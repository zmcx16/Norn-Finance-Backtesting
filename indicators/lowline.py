import backtrader as bt


class LowLine(bt.Indicator):
    lines = ('low',)
    params = dict(period=252, rate=.05, color='grey')

    plotinfo = dict(subplot=False)
    plotlines = dict(
        low=dict(color='grey', linewidth=1),
    )

    def __init__(self):
        self.l.low = bt.indicators.Lowest(self.data.close, period=self.p.period) * (1 + self.p.rate)
        self.plotlines.low.color = self.p.color

        super(LowLine, self).__init__()  # enable coopertive inheritance
