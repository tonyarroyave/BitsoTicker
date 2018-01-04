import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
pd.options.mode.chained_assignment = None
import numpy as np
import bitso
from btc_apikeys import * 
import bitso_functions as fun
import ticker_bitso as tick

api = bitso.Api(API_KEY, API_SECRET)

transcurrido = 60  #Tienen que transcurrir 1 minutos para hacer una accion

while(True):
    if (transcurrido >= 59):
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
        pm1 = 109
        pm2 = 111

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
        print('Ultimo valor en historico: ' + str(last_hist[0]))
        print('Ultimo valor en mercado: ' + str(last_price[5]))

        ob = fun.btc_update(api)
        mxn = fun.get_mxn_balance(api)
        btc = fun.get_btc_balance(api)
        count = 0

        if (decision == 1):            #significa que hay que comprar
            print ('Precio a la ALZA, deberiamos de COMPRAR!')
            if int(mxn) > 0:
                price = fun.max_bid_btc_price(ob)
                price = round(price,2)
                monto = round(mxn/price,8)
                fun.place_order_btc(api, side='buy', amount=str(monto), price=str(price))
            else:
                print('No hay moneyney (MXN), veamos si es por que todavia hay ordenes activas...')
                count = count + int(fun.view_orders(api))
                if count > 2:
                    count = 0
                    print('Suebele tantillo...')
                    fun.cancel_all_orders(api)
                    price = price/0.997
                    fun.place_order_btc(api, side='buy', amount=str(monto), price=str(price))               
                print('Vamos a esperarnos unos minutitos entonces...')
                print(' ')

        elif (decision == -1):                   #significa que hay que vender
            print ('Precio a la BAJA, deberiamos VENDER!')
            if btc > 0:
                price = fun.min_ask_btc_price(ob)
                price = round(price,2)
                fun.place_order_btc(api, side='sell', amount=str(btc), price=str(price))
            else:
                print('No hay moneyney (BTC), veamos si es por que todavia hay ordenes activas...')
                count = count + int(fun.view_orders(api))
                if count > 2:
                    count = 0
                    print('A mi se me hace que eso no se va a vender... vamos a bajarle tantillo')
                    fun.cancel_all_orders(api)
                    price = price*0.997
                    fun.place_order_btc(api, side='sell', amount=str(btc), price=str(price))
                print('Vamos a esperarnos unos minutitos entonces...')
                print(' ')

    time.sleep(10)
    transcurrido = transcurrido + 10
