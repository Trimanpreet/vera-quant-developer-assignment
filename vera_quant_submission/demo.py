from decimal import Decimal
from random import Random
from quant_engine.backtest import Backtester, Bar
from quant_engine.strategy import GridStopReverseStrategy
from pathlib import Path
import csv, json

def make_bars(n=180):
    r = Random(7); price = 22000.0; bars=[]
    for i in range(n):
        drift = 18 if (i // 30) % 2 == 0 else -12
        o = price
        c = max(100.0, o + drift + r.uniform(-45,45))
        h = max(o,c) + r.uniform(5,30); l=min(o,c)-r.uniform(5,30)
        price=c
        bars.append(Bar(f"2026-01-{1+i:02d}", Decimal(f"{o:.2f}"), Decimal(f"{h:.2f}"), Decimal(f"{l:.2f}"), Decimal(f"{c:.2f}"), r.randint(1000,5000)))
    return bars

if __name__ == "__main__":
    bars=make_bars()
    report=Backtester(GridStopReverseStrategy()).run(bars)
    Path("data").mkdir(exist_ok=True)
    Path("data/backtest_report.json").write_text(json.dumps(report, indent=2))
    with open("data/trades.csv","w",newline="") as f:
        rows=report["trades"]; w=csv.DictWriter(f, fieldnames=rows[0].keys() if rows else ["timestamp"]); w.writeheader(); w.writerows(rows)
    print(json.dumps({k:v for k,v in report.items() if k!="trades"}, indent=2))
