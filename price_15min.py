'''
Obtener los valores cada 15 min y postearlos
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

# Sacamos todas las worksheets
WS = ss.get_all_worksheets(Historical)

transcurrido = 600
while(True):
    if (transcurrido >= 599):
        transcurrido = 0
        Values = tick.get_all(bitso)
        for x in range(0, 4):
            ss.insert_values(WS[x],Values[x])
    time.sleep(10)
    transcurrido = transcurrido + 10