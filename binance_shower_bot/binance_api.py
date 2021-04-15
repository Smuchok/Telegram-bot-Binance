# import binance
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
# from requests.exceptions import ReadTimeout
import requests

from secure.tokens import TOKEN_BINANCE     #funcs: API_KEY(), API_SECRET()

print('binance_api.py is working...')

# API_KEY= 'tiFwliN4I9FeBIWQ42vDE72v7SZeDMNQqgBHGTK1KSjX39tWhQgfE2I9tNOcHrOu'
# API_SECRET= 'GrfOQzTbm4I4IS32YqMRLBtRMl5ksdtpF5tv66L5Zq3ubLB6aw0IPQI57Isw7dWE'
# client = Client(API_KEY, API_SECRET)

API_KEY= TOKEN_BINANCE.API_KEY()
API_SECRET= TOKEN_BINANCE.API_SECRET()
client = Client(API_KEY, API_SECRET)


# status = client.get_system_status()
# print(status)

# info = client.get_symbol_info('BNBBTC')
# print(info)

class Binance_view():
    symbols= [
        ['BTCUSDT', 'BTCUAH', 'BTCRUB'],
        ['ADAUSDT', 'ADAUAH', 'ADARUB'],
        ['XRPUSDT', 'XRPUAH', 'XRPRUB'],
        ['NEOUSDT', 'NEOUAH', 'NEORUB'],
        ['EOSUSDT', 'EOSUAH', 'EOSRUB'],
        ['IOTAUSDT', 'IOTAUAH', 'IOTARUB']
    ]

    def view_prices(symbols=symbols):
        
        try:
            print('binance_api.view_prices is working...', client.ping())
            arr= []
            for i in symbols:
                # print('_ '*4)
                arr2= []
                for j in i:
                    try:
                        price= client.get_symbol_ticker(symbol=j)
                        # print(j, ' : ', price)
                        arr2.append([ price['symbol'], float(price['price']) ])
                    except BinanceAPIException as e:
                        # print('  ', e.status_code, e.message)
                        # arr2.append({'symbol':j, 'price':'not found'})
                        pass
                arr.append(arr2)
            arr_end= {'status':True , 'result':arr}
            return arr_end
        except requests.exceptions.ReadTimeout:
            print(' - - - ReadTimeout error - - -')
            return {'status':False , 'result':None}


# Binance_view.view_prices




# client.get_system_status()
{'msg': 'normal', 'status': 0}

# client.get_symbol_info('BNBBTC')
{
    'symbol': 'BNBBTC', 
    'status': 'TRADING', 
    'baseAsset': 'BNB', 
    'baseAssetPrecision': 8, 
    'quoteAsset': 'BTC', 
    'quotePrecision': 8, 
    'quoteAssetPrecision': 8, 
    'baseCommissionPrecision': 8, 
    'quoteCommissionPrecision': 8, 
    'orderTypes': [
        'LIMIT', 
        'LIMIT_MAKER', 
        'MARKET', 
        'STOP_LOSS_LIMIT', 
        'TAKE_PROFIT_LIMIT'
    ], 
    'icebergAllowed': True, 
    'ocoAllowed': True, 
    'quoteOrderQtyMarketAllowed': True, 
    'isSpotTradingAllowed': True, 
    'isMarginTradingAllowed': True, 
    'filters': [
        {
            'filterType': 'PRICE_FILTER', 
            'minPrice': '0.00000010', 
            'maxPrice': '100000.00000000', 
            'tickSize': '0.00000010'
        }, 
        {
            'filterType': 'PERCENT_PRICE', 
            'multiplierUp': '5', 
            'multiplierDown': '0.2', 
            'avgPriceMins': 5
        }, 
        {
            'filterType': 'LOT_SIZE', 
            'minQty': '0.01000000', 
            'maxQty': '100000.00000000', 
            'stepSize': '0.01000000'
        }, 
        {
            'filterType': 'MIN_NOTIONAL', 
            'minNotional': '0.00010000', 
            'applyToMarket': True, 
            'avgPriceMins': 5
        }, 
        {
            'filterType': 'ICEBERG_PARTS', 
            'limit': 10
        }, 
        {
            'filterType': 'MARKET_LOT_SIZE', 
            'minQty': '0.00000000', 
            'maxQty': '5156.56692361', 
            'stepSize': '0.00000000'
        }, 
        {
            'filterType': 'MAX_NUM_ORDERS', 
            'maxNumOrders': 200
        }, 
        {
            'filterType': 'MAX_NUM_ALGO_ORDERS', 
            'maxNumAlgoOrders': 5
        }
    ], 
    'permissions': [
        'SPOT', 
        'MARGIN'
        ]
    }
