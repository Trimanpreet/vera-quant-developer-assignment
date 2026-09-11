from quant_engine.ta import sma, rsi, atr, obv

def test_sma(): assert sma([1,2,3,4], 2) == 3.5

def test_rsi_all_gains(): assert rsi([1,2,3,4,5], 4) == 100.0

def test_atr(): assert round(atr([11,12,13],[9,10,11],[10,11,12],2), 6) == 2.0

def test_obv(): assert obv([10,11,10,12],[100,50,20,30]) == 60
