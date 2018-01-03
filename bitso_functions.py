'''
Funciones para bitso
https://github.com/barucAlmaguer/bitso-py/blob/master/examples/place_order_test.py
'''

def btc_update(api):
    ob = api.order_book('btc_mxn')
    return ob

def min_ask_btc_price(ob):
	return min([ask.price for ask in ob.asks])

def max_bid_btc_price(ob):
	return max([ask.price for ask in ob.bids])

def bitso_status(api):
	status = api.account_status()
	print("Daily limit=		{}".format(status.daily_limit))
	print("Daily remaining=	{}".format(status.daily_remaining))

def place_order_btc(api, side, amount, price):
    print("Colocando orden...")
    order = api.place_order(book='btc_mxn', side=side, order_type='limit', major=amount, price=price)
    print("Orden colocada")
    print('Tipo:' + side)
    print('Monto:' + amount)
    print('Precio:' + price)

def view_orders(api):
	oo = api.open_orders('btc_mxn')
	if len(oo) > 0:
		for o in oo:
			print("-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.")
			print("Order #:  {}".format(o.oid))
			print("\tSide=   {}".format(o.side))
			print("\tAmount= BTC${}".format(o.original_amount))
			print("\tPrice=  MXN${}".format(o.price))
		print("-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.")
	else:
	    print("No current orders")

def cancel_order(api, oid):
	return api.cancel_order(oid)
		
def cancel_all_orders(api):
    oo = api.open_orders('btc_mxn')
    if len(oo) > 0:
        for o in oo:
            success = cancel_order(o.oid)
            if success:
                print("Order #{} cancelled".format(o.oid))
            else:
                print("Error cancelling order #{}".format(o.oid))
    else:
        print('No orders to cancel')

def get_mxn_balance(api):
    balances = api.balances()
    return balances.mxn.available

def get_btc_balance(api):
    balances = api.balances()
    return balances.btc.available
