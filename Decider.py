import sys
import time
import decimal
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
pd.options.mode.chained_assignment = None
import numpy as np
import bitso
from bitso.errors import ApiError
from btc_apikeys import * 
import bitso_functions as fun
import ticker_bitso as tick

api = bitso.Api(API_KEY, API_SECRET)

transcurrido = 30  #Tienen que transcurrir 30 seg para hacer una accion
count = 0

while(True):
    if (transcurrido >= 29):
        transcurrido = 0
        scope = ['https://spreadsheets.google.com/feeds']
        creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
        client = gspread.authorize(creds)

        Historical = client.open("Historical Bitso")
        BTC = Historical.get_worksheet(0)
        #ETH = Historical.get_worksheet(1)
        #XRP = Historical.get_worksheet(2)
        #BCH = Historical.get_worksheet(3)

        def get_df(WS):

            col_names=True
            row_names=True

            raw_data = WS.get_all_values()

            start_row_int, start_col_int = WS.get_int_addr('A1')

            rows, cols  = np.shape(raw_data)

            raw_data = [row[start_col_int-1:] for row in raw_data[start_row_int-1:]]

            if row_names and col_names:
                row_names = [row[0] for row in raw_data[1:]]
                col_names = raw_data[0][1:]
                raw_data = [row[1:] for row in raw_data[1:]]
            elif row_names:
                row_names = [row[0] for row in raw_data]
                col_names = np.arange(len(raw_data[0]) - 1)
                raw_data = [row[1:] for row in raw_data]
            elif col_names:
                row_names = np.arange(len(raw_data) - 1)
                col_names = raw_data[0]
                raw_data = raw_data[1:]
            else:
                row_names = np.arange(len(raw_data))
                col_names = np.arange(len(raw_data[0]))

            df = pd.DataFrame([pd.Series(row) for row in raw_data], index=row_names)
            df.columns = col_names
            df = df.astype(float)
            return df

        #Definidos por pruebas anteriores
        pm1 = 70
        pm2 = 71

        print ('Veamos como va todo...')

        def get_strategy(pm1, pm2, Bitso):
            
            Bitso['PM1'] = Bitso['LAST'].rolling(pm1).mean()
            Bitso['PM2'] = Bitso['LAST'].rolling(pm2).mean()
            Bitso.dropna(inplace = True)
            Bitso = Bitso[['LAST','PM1','PM2']]
            Bitso['Posicion'] = np.where(Bitso['PM1'] > Bitso['PM2'], 1, -1)
            Bitso['Retornos'] = np.log(Bitso['LAST']/Bitso['LAST'].shift(1))
            Bitso.dropna(inplace = True)
            Bitso['Estrategia'] = Bitso['Retornos']* Bitso['Posicion'].shift(1)
            Bitso.dropna(inplace = True)
            Bitso['Retacum'] = Bitso['Retornos'].cumsum().apply(np.exp)
            Bitso['Estracum'] = Bitso['Estrategia'].cumsum().apply(np.exp)

            return Bitso

        estrategia = get_strategy(pm1,pm2,get_df(BTC))
        _ = estrategia['Posicion'].tail(1).copy()
        decision = _[0]

        last_hist = estrategia['LAST'].tail(1).copy()
        last_price = tick.get_values_btc(api)

        print ('------------------------------------------')
        print(' Ultimo valor en historico: ' + str(last_hist[0]))
        print(' Ultimo valor en el mercado: ' + str(last_price[5]))
        print ('------------------------------------------')

        ob = fun.btc_update(api)
        mxn = fun.get_mxn_balance(api)
        btc = fun.get_btc_balance(api)

        if (decision == 1):            #significa que hay que comprar
            try:
                print (' Tendencia a la ALZA')
                print ('------------------------------------------')
                if int(mxn) > 0:

                    price = fun.max_bid_btc_price(ob)
                    price_r = price.quantize(decimal.Decimal('.01'), rounding=decimal.ROUND_UP)
                    monto = mxn/price_r
                    monto_r = monto.quantize(decimal.Decimal('.00000001'), rounding=decimal.ROUND_DOWN) #BTC

                    fun.place_order_btc(api, side='buy', amount=str(monto_r), price=str(price_r))
                else:
                    print(' Balance actual:')
                    print('  MXN: $0.00')
                    print('  BTC: {}'.format(btc))
                    print ('------------------------------------------')

                    hay_orden = fun.view_orders(api)
                    if hay_orden == True:
                        count = count + 1
                    elif hay_orden == False and count > 0:
                        print(' Ultima orden efectuada con exito!')
                        count = 0

                    if count > 5:
                        count = 0
                        print('Pagale tantillo mas JTO...')
                        fun.cancel_all_orders(api)
                        price_r = price_r/decimal.Decimal('0.997')
                        fun.place_order_btc(api, side='buy', amount=str(monto_r), price=str(price_r))               
                    print('Vamos a esperarnos entonces...')
                    print(' ')
            except ApiError as Er:
                print(Er)
                pass                
            else:
                if sys.exc_info()[0] != None:
                    print("Unexpected error:", sys.exc_info()[0])
                pass

        elif (decision == -1):                   #significa que hay que vender
            try:
                print (' Tendencia a la BAJA')
                print ('------------------------------------------')
                if btc > 0:
                    price = fun.min_ask_btc_price(ob)
                    price_r = price.quantize(decimal.Decimal('.01'), rounding=decimal.ROUND_UP)
                    fun.place_order_btc(api, side='sell', amount=str(btc), price=str(price_r))
                else:
                    print(' Balance actual:')
                    print('  MXN: {}'.format(mxn))
                    print('  BTC: 0.0000')
                    print ('------------------------------------------')

                    hay_orden = fun.view_orders(api)
                    if hay_orden == True:
                        count = count + 1
                    elif hay_orden == False and count > 0:
                        print(' Ultima orden efectuada con exito!')
                        count = 0

                    if count > 5:
                        count = 0
                        print('A mi se me hace que eso no se va a vender... vamos a bajarle tantillo')
                        fun.cancel_all_orders(api)
                        price_r = price_r*decimal.Decimal('0.997')
                        fun.place_order_btc(api, side='sell', amount=str(btc), price=str(price_r))
                    print('Vamos a esperarnos entonces...')
                    print(' ')
            except ApiError as Er:
                print(Er)
                pass                
            else:
                if sys.exc_info()[0] != None:
                    print("Unexpected error:", sys.exc_info()[0])
                pass

    time.sleep(10)
    transcurrido = transcurrido + 10
