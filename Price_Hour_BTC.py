import bitso
import csv
import time

with open('BTC_Price.csv', 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(['TIME','ASK','BID','HIGH','LAST','LOW','VWAP','VOLUME'])

api = bitso.Api()
transcurrido = 0
while(True):
    time.sleep(5)
    transcurrido = transcurrido + 5
    print('Sigo vivo...')
    if (transcurrido >= 3600):
        transcurrido = 0
        tick = api.ticker('btc_mxn')
        with open('BTC_Price.csv', 'a') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow([tick.created_at,tick.ask,tick.bid,tick.high,tick.last,tick.low,tick.vwap,tick.volume])
            print('Tengo valores :D!')
