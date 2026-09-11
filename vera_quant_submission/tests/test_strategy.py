from decimal import Decimal
from quant_engine.strategy import GridStopReverseStrategy, StrategyConfig
from quant_engine.execution import Side

def series(n=30):
    close=list(range(100,n+100)); high=[x+2 for x in close]; low=[x-2 for x in close]; return high,low,close

def test_buy_signal_and_position_cap():
    h,l,c=series(); s=GridStopReverseStrategy(StrategyConfig(max_position=2)); sig=s.signal(h,l,c,0,Decimal('100'),Decimal('100')); assert sig.side is Side.BUY
    assert sig.quantity <= 2

def test_kill_switch():
    h,l,c=series(); s=GridStopReverseStrategy(); sig=s.signal(h,l,c,0,Decimal('100'),Decimal('94')); assert sig.reason=='kill_switch'
