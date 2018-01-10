
'''
Funciones para adquirir los precios de Bitso
UPDATE:
    Se obtiene el promedio de las ultimas 10 transacciones para evitar guardar picos
'''

#TODO optimizar nuevo codigo y replicarlo para todos las cripto
import decimal

def get_values_btc(api):
    tick_btc = api.ticker('btc_mxn')
    #-------------
    trades = api.trades(book = 'btc_mxn', limit = '10')
    suma = decimal.Decimal('0.00')
    for each in trades:
        suma = suma + each.price
    prom = suma/10
    #--------------

    return [tick_btc.created_at, tick_btc.ask, tick_btc.bid, tick_btc.high, tick_btc.low, prom, tick_btc.vwap, tick_btc.volume]

def get_values_eth(api):
    tick_eth = api.ticker('eth_mxn')
    return [tick_eth.created_at, tick_eth.ask, tick_eth.bid, tick_eth.high, tick_eth.low, tick_eth.last, tick_eth.vwap, tick_eth.volume]

def get_values_xrp(api):
    tick_xrp = api.ticker('xrp_mxn')
    #-------------
    trades = api.trades(book = 'xrp_mxn', limit = '10')
    suma = decimal.Decimal('0.00')
    for each in trades:
        suma = suma + each.price
    prom = suma/10
    #--------------

    return [tick_xrp.created_at, tick_xrp.ask, tick_xrp.bid, tick_xrp.high, tick_xrp.low, prom, tick_xrp.vwap, tick_xrp.volume]

def get_values_bch(api):
    tick_bch = api.ticker('bch_btc')
    return [tick_bch.created_at, tick_bch.ask, tick_bch.bid, tick_bch.high, tick_bch.low, tick_bch.last, tick_bch.vwap, tick_bch.volume]

def get_all(api):
    return [get_values_btc(api), get_values_eth(api), get_values_xrp(api), get_values_bch(api)]
