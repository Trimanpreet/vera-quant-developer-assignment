from quant_engine.state import PortfolioState, StateStore

def test_restart_recovery(tmp_path):
    store=StateStore(tmp_path/'state.json'); s=PortfolioState(position=2,cash='99800.00'); store.save(s); recovered=store.load(); assert recovered.position==2 and recovered.cash=='99800.00'
