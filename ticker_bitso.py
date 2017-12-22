
'''
Funciones para adquirir los precios de Bitso
'''

def get_values_btc(api):
    tick_btc = api.ticker('btc_mxn')
    return [tick_btc.created_at, tick_btc.ask, tick_btc.bid, tick_btc.high, tick_btc.low, tick_btc.last, tick_btc.vwap, tick_btc.volume]

def get_values_eth(api):
    tick_eth = api.ticker('eth_mxn')
    return [tick_eth.created_at, tick_eth.ask, tick_eth.bid, tick_eth.high, tick_eth.low, tick_eth.last, tick_eth.vwap, tick_eth.volume]

def get_values_xrp(api):
    tick_xrp = api.ticker('xrp_mxn')
    return [tick_xrp.created_at, tick_xrp.ask, tick_xrp.bid, tick_xrp.high, tick_xrp.low, tick_xrp.last, tick_xrp.vwap, tick_xrp.volume]

def get_values_bch(api):
    tick_bch = api.ticker('bch_btc')
    return [tick_bch.created_at, tick_bch.ask, tick_bch.bid, tick_bch.high, tick_bch.low, tick_bch.last, tick_bch.vwap, tick_bch.volume]

def get_all(api):
    return [get_values_btc(api), get_values_eth(api), get_values_xrp(api), get_values_bch(api)]