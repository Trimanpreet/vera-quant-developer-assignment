from decimal import Decimal
from quant_engine.execution import PaperBroker, Order, Side

def test_idempotent_placement():
    b=PaperBroker(); o=Order('1','same','DEMO',Side.BUY,1,Decimal('100')); a=b.place(o); c=b.place(o); assert a is c; assert len(b.orders)==1
