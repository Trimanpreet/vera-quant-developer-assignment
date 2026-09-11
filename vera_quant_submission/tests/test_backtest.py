from decimal import Decimal
from quant_engine.backtest import Backtester, Bar
from quant_engine.strategy import GridStopReverseStrategy

def test_backtest_runs_without_same_bar_fill():
    bars=[]
    for i in range(80):
        p=Decimal(100+i); bars.append(Bar(str(i),p,p+1,p-1,p,1000))
    r=Backtester(GridStopReverseStrategy()).run(bars)
    assert r['ending_equity'] != r['starting_cash']
    assert r['trades'][0]['timestamp'] == '21'
