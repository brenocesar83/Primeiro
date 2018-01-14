import requests
# import datetime


def web_page():
    url = "https://bittrex.com/api/v2.0/pub/markets/GetMarketSummaries"
    req = requests.get(url)
    if req.status_code == 200:
        result = req.json()
        page_result = result['result']
    else:
        print("Failed!! The server response was: ", req.status_code)
    return page_result


def get_market_names(base_currency_market):
    page_result = web_page()
    market_names = []
    for i in page_result:
        base_currency = i['Market']['BaseCurrency']
        market_name = i['Market']['MarketName']
        if base_currency == base_currency_market:
            market_names.append(market_name)
    return market_names


# print(get_market_names('BTC'))

""""
GetMarkets
Gets all markets data.

URL https://bittrex.com/api/v2.0/pub/markets/GetMarkets
    https://bittrex.com/api/v2.0/pub/markets/GetMarketSummaries

METHOD GET

PARAMS _:int

EXAMPLE GET https://bittrex.com/api/v2.0/pub/markets/GetMarkets?_=1500913483670

COMMENT Probably _ is a timestamp.

{  
   'Market':{  
      'MarketCurrency':'2GIVE',
      'BaseCurrency':'BTC',
      'MarketCurrencyLong':'2GIVE',
      'BaseCurrencyLong':'Bitcoin',
      'MinTradeSize':318.47133758,
      'MarketName':'BTC-2GIVE',
      'IsActive':True,
      'Created':'2016-05-16T06:44:15.287',
      'Notice':None,
      'IsSponsored':False,
      'LogoUrl':'https://bittrexblobstorage.blob.core.windows.net/public/a6a2227e-55fd-412d-844b-6a7866411e34.png'
   },
   'Summary':{  
      'MarketName':'BTC-2GIVE',
      'High':2.42e-06,
      'Low':1.96e-06,
      'Volume':20885106.90619006,
      'Last':2.08e-06,
      'BaseVolume':43.87911919,
      'TimeStamp':'2018-01-10T20:11:55.643',
      'Bid':2.06e-06,
      'Ask':2.08e-06,
      'OpenBuyOrders':484,
      'OpenSellOrders':1398,
      'PrevDay':2.38e-06,
      'Created':'2016-05-16T06:44:15.287'
   },
   'IsVerified':False
}

        market_currency = i['Market']['MarketCurrency']
        base_currency = i['Market']['BaseCurrency']
        market_currency_long = i['Market']['MarketCurrencyLong']
        # base_currency_long = i['Market']['BaseCurrencyLong']
        market_name = i['Market']['MarketName']

        summary_high = i['Summary']['High']
        summary_low = i['Summary']['Low']
        summary_volume = i['Summary']['Volume']
        summary_last = i['Summary']['Last']
        summary_base_volume = i['Summary']['BaseVolume']
        # summary_timestamp_aux = datetime.datetime.strptime(i['Summary']['TimeStamp'], '%Y-%m-%dT%H:%M:%S.%f')
        # summary_timestamp = datetime.datetime.strftime(summary_timestamp_aux, '%Y-%m-%d')
        summary_bid = i['Summary']['Bid']
        summary_ask = i['Summary']['Ask']
        summary_open_buy_orders = i['Summary']['OpenBuyOrders']
        summary_open_sell_orders = i['Summary']['OpenSellOrders']
        summary_prev_day = i['Summary']['PrevDay']
        summary_created = i['Summary']['Created']
        # summary_created = i['Summary']['Created']
        # summary_created_aux = datetime.datetime.strptime(i['Summary']['Created'], '%Y-%m-%dT%H:%M:%S.%f')
        # summary_created = datetime.datetime.strftime(summary_created_aux, '%Y-%m-%d')

    # if base_currency == 'BTC':  # and summary_open_sell_orders < summary_open_buy_orders:
    #     print(market_currency_long, market_currency, market_name, 'High', '{:1.8f}'.format(summary_high),
    #           'Low', '{:1.8f}'.format(summary_low), 'Volume', summary_volume,  'Last', '{:1.8f}'.format(summary_last),
    #           'BaseVolume', summary_base_volume, 'Bid', '{:1.8f}'.format(summary_bid), 'Ask',
    #           '{:1.8f}'.format(summary_ask), 'OpenBuyOrders', summary_open_buy_orders, 'OpenSellOrders',
    #           summary_open_sell_orders, 'PrevDay', '{:1.8f}'.format(summary_prev_day))
"""

