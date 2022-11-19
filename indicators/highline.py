import backtrader as bt


class HighLine(bt.Indicator):
    lines = ('high',)
    params = dict(period=252, rate=.05, color='grey')

    plotinfo = dict(subplot=False)
    plotlines = dict(
        high=dict(color='grey'),
    )

    def __init__(self):
        self.l.high = bt.indicators.Highest(self.data.close, period=self.p.period) * (1 - self.p.rate)
        self.plotlines.high.color = self.p.color

        super(HighLine, self).__init__()  # enable coopertive inheritance
