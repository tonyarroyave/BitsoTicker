
'''
Sencillo programilla ejemplo para adquirir los precios de Bitso para: Bitcoin, Etherium, Ripple y BTC Cash
para luego agregarlos a una spreadsheet en Google Drive
'''

import time
import bitso
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import ticker_bitso as tick
import spreadsheet_api as ss

# Inicializamos la API de Bitso
bitso = bitso.Api()

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Nombre de la spreadsheet en Google Drive
Historical = client.open("Historical Bitso")

# Sacamos todas las worksheets y valores de Bitso
WS = ss.get_all_worksheets(Historical)
Values = tick.get_all(bitso)

# Insertamos todos los valores nuevos
for x in range(0, 4):
    ss.insert_values(WS[x],Values[x])