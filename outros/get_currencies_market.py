import requests
import datetime
from outros import get_coins_market
import csv


coins = get_coins_market.get_market_names('BTC')
print('# CryptoCoins:', len(coins))

data_file = []
coin_counter = 0
for coin in coins:
    url = 'https://bittrex.com/Api/v2.0/pub/market/GetTicks?marketName=' + coin + '&tickInterval=day'
    req = requests.get(url)
    if req.status_code == 200:
        result = req.json()
    else:
        print("Failed!! The server response was: ", req.status_code)
        break
    array_result = result['result']
    title_file = ['CryptoCoin', 'Date', 'Open Value', 'Close Value', 'Highest Value', 'Lowest Value',
                  'High Low Variation', 'Open Close Variation', '24h Volume', 'Base Volume']
    coin_counter += 1
    print('#', coin_counter, 'CryptoCoin')
    for i in array_result:
        data = datetime.datetime.strptime(i['T'], '%Y-%m-%dT%H:%M:%S')
        date_formatted = datetime.datetime.strftime(data, '%Y-%m-%d')
        open_value = (i['O'])
        close = (i['C'])
        high = (i['H'])
        low = (i['L'])
        volume = i['V']
        base_volume = i['BV']
        high_low_var = (((high/low)-1)*100)
        open_close_var = (((close/open_value)-1)*100)
        data_line = [coin, date_formatted, '{:.8f}'.format(open_value), '{:.8f}'.format(close), '{:.8f}'.format(high),
                     '{:.8f}'.format(low), '{:.4f}%'.format(high_low_var), '{:.4f}%'.format(open_close_var), volume,
                     base_volume]
        data_file.append(data_line)

        # print('In', date_formatted, 'the open value is', '{:1.8f}'.format(open_value), 'and close value',
        #       '{:1.8f}'.format(close), 'highest value', '{:1.8f}'.format(high), 'lowest value',
        #       '{:.8f}'.format(low), 'high low variation', '{:.4f}%'.format(high_low_var), 'open close variation',
        #       '{:.4f}%'.format(open_close_var), '24h volume', volume, 'base volume', base_volume)


def create_file():
    file = open("all_markets.csv", 'w')
    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    writer.writerow(title_file)  # Titulo escrito manualmente
    for row in data_file:
        writer.writerow(row)  # Linhas
    file.close()


def read_file():
    file = open("all_markets.csv", newline='')
    reader = csv.reader(file)
    for row in reader:
        print(row)


create_file()
# read_file()
"""
https://www.reddit.com/r/BitcoinMarkets/comments/6k75ue/unable_to_get_historical_bittrex_data/
So far I've found "oneMin", "fiveMin", "thirtyMin", "hour" and "day". Anyone know of any more?

It appears to be a UNIX timestamp, which is the number of milliseconds since 1/1/1970. For example, 1499127220008 
happened on July 3rd. I was hoping this param lets you retrieve only historical data after the timestamp but 
I can't get it to work.
https://bittrex.com/Api/v2.0/pub/market/GetTicks?marketName=BTC-btg&tickInterval=thirtyMin&_=1499127220008

{
    success : true,
    message : "",
    result : [ // Array of candle objects.
    {
        BV: 13.14752793,          // base volume
        C: 0.000121,              // close
        H: 0.00182154,            // high
        L: 0.0001009,             // low
        O: 0.00182154,            // open
        T: "2017-07-16T23:00:00", // timestamp
        V: 68949.3719684          // 24h volume
    },
    ...
    { ... }]
}


1
down vote
accepted
Volume is the amount traded in that altcoin over the past 24 hours.

In the case of BTC-DGB, this is the amount of DGB that has been traded in 24 hours.

BaseVolume is the total value traded in the base currency, for example Bitcoin.

Volume increases regardless if it is a buy or sell order.

To find the overall volume you can go to https://coinmarketcap.com.


"""
