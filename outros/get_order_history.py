import hashlib
import hmac
import requests
import time
import json


BASE_URL_V1_1 = 'https://bittrex.com/api/v1.1'
BASE_URL_V2_0 = 'https://bittrex.com/api/v2.0'
NONCE = str(int(time.time() * 1000))

with open("secrets.json") as secrets_file:
    secrets = json.load(secrets_file)
    secrets_file.close()
    API_KEY = secrets['key']
    API_SECRET = secrets['secret']


def get_api_sign_url_private(base, complement):
    url = base+complement+'?apikey='+API_KEY+'&nonce='+NONCE
    api_sign = hmac.new(API_SECRET.encode(), url.encode(), hashlib.sha512)
    headers = {'apisign': api_sign.hexdigest()}
    token = requests.post(url, headers=headers)
    if token.status_code == 200:
        if token.json()['success']:
            return token.json()['result']
        else:
            return token.json()['message']
    else:
        print("Failed!! The server response was: ", token.status_code)


def get_public_api(base, complement, options):
    url = base+complement+options
    request = requests.get(url)
    if request.status_code == 200:
        if request.json()['success']:
            return request.json()['result']
        else:
            return request.json()['message']
    else:
        print("Failed!! The server response was: ", request.status_code)


def get_percent_colored(value):
    if value < 0:
        return '\x1b[6;30;41m' + ' {:7.2f}% '.format(value) + '\x1b[0m'
    else:
        if 0 <= value < 7:
            return '\x1b[6;30;43m' + ' {:7.2f}% '.format(value) + '\x1b[0m'
        else:
            return '\x1b[6;30;42m' + ' {:7.2f}% '.format(value) + '\x1b[0m'


def dashboard1():
    dolar_btc = get_public_api(BASE_URL_V2_0, '/pub/currencies/GetBTCPrice', '')['bpi']['USD']['rate_float']
    balances = get_api_sign_url_private(BASE_URL_V2_0, '/key/balance/getbalances')
    estimated_total_btc = 0
    total_btc_used = 0
    order_history = get_api_sign_url_private(BASE_URL_V1_1, '/account/getorderhistory')
    for elem in balances:
        if elem['Balance']['Balance'] > 0:
            currency = '?market=BTC-' + elem['Balance']['Currency']
            last_info = get_public_api(BASE_URL_V1_1, '/public/getticker', currency)
            total_currency = 0
            complete_currency = 'BTC-' + elem['Balance']['Currency']
            if last_info != 'INVALID_MARKET':
                last_value = last_info['Last']
            else:
                last_value = 1
            for order in order_history:
                if order['OrderType'] == 'LIMIT_SELL' and order['Exchange'] == complete_currency:
                    print('I sold {}$ {:.8f} for BTC$ {:.8f}(BTC$ {:.8f})'.format(order['Exchange'], order['Quantity'],
                                                                                  order['Price'], order['PricePerUnit']))
                    total_currency -= order['Quantity']
                elif order['OrderType'] == 'LIMIT_BUY' and order['Exchange'] == complete_currency:
                    gain_color = get_percent_colored(((last_value/order['PricePerUnit'])-1)*100)
                    total_btc_used += order['Price'] + order['Commission']
                    print('| I bought {:>5}$ {:13.8f} for BTC$ {:.8f} (BTC$ {:.8f}) (US$ {:.2f}) and now I have BTC$ '
                          '{:.8f} (BTC$ {:.8f}) (US$ {:.2f}) gain of {} |'.format(order['Exchange'][4:],
                                                                                  order['Quantity'],
                                                                                  order['Price'], order['PricePerUnit'],
                                                                                  order['Price'] * dolar_btc,
                                                                                  order['Quantity'] * last_value,
                                                                                  last_value,
                                                                                  order['Quantity'] * last_value *
                                                                                  dolar_btc, gain_color))
                    total_currency += order['Quantity']
                if total_currency == elem['Balance']['Balance']:
                    break
            # print('Calculated total', total_currency)
            print('| {:>29} {:>131}'.format('-' * 14, '|'))
            estimated_total_btc += elem['Balance']['Balance']*last_value
            print('| Balance: {:>5}$ {:13.8f} = BTC$ {:.8f} = US$ {:6.2f} {:>100}'.format(elem['Balance']['Currency'],
                                                                                          elem['Balance']['Balance'],
                                                                                          elem['Balance']['Balance'] *
                                                                                          last_value,
                                                                                          elem['Balance']['Balance'] *
                                                                                          last_value * dolar_btc, '|'))
            print('|', '_' * 161, '|', sep='')

    print('BTC used', '{:.8f}'.format(total_btc_used))
    print('Estimated Value: BTC', '{:.8f}'.format(estimated_total_btc), 'US$', '{:.2f}'.format(estimated_total_btc*dolar_btc))
    gain_color = get_percent_colored(((estimated_total_btc/total_btc_used)-1)*100)
    print('Real gain', gain_color)


def dashboard2():
    order_history = get_api_sign_url_private(BASE_URL_V1_1, '/account/getorderhistory')
    count = 0
    estimated_value = 0
    percent = 0
    previous_value = 0
    for elem in order_history:
        count += 1
        currency = '?market=' + elem['Exchange']
        last_info = get_public_api(BASE_URL_V1_1, '/public/getticker', currency)
        if last_info != 'INVALID_MARKET':
            last_value = last_info['Last']
        else:
            last_value = 0

        gain = ((last_value/elem['PricePerUnit'])-1)*100
        gain_color = get_percent_colored(gain)

        percent += gain
        if elem['OrderType'] == 'LIMIT_SELL':
            print('Sold {:.8f} {} for {:.8f}. The total was {:.8f} and now the price is {:.8f} {}'
                  .format(elem['Quantity'], elem['Exchange'], elem['PricePerUnit'], elem['Price'], last_value,
                          gain_color))
            estimated_value -= elem['Quantity'] * last_value - ((elem['Quantity'] * last_value) * 0.0025)
            previous_value -= elem['Price'] + elem['Commission']
        else:
            estimated_value += elem['Quantity'] * last_value - ((elem['Quantity'] * last_value) * 0.0025)
            previous_value += elem['Price'] + elem['Commission']
            print('My current position is {} for the purchase {:.8f} {} for {:.8f}. The total was {:.8f} and the '
                  'present value is {:.8f}'.format(gain_color, elem['Quantity'], elem['Exchange'], elem['PricePerUnit'],
                                                   elem['Price'], last_value))
        if count == 10:
            break
    dolar_btc = get_public_api(BASE_URL_V2_0, '/pub/currencies/GetBTCPrice', '')['bpi']['USD']['rate_float']
    real_percent = get_percent_colored(((estimated_value/previous_value)-1)*100)
    print('Wasted {:.8f} and now is {:.8f}, gain of {}'.format(previous_value, estimated_value, real_percent))
    print('Estimated Value: BTC', '{:.8f}'.format(estimated_value), 'US$', '{:.2f}'.format(estimated_value*dolar_btc))


dashboard1()
# dashboard2()

""""
// work in progress
// you need a bittrex API key and secret with read account option enabled

// I assume that all the keys are in the "keys" spreadsheet. The key is in cell B5 and the secret in cell C5
var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("keys");
var key = sheet.getRange("B5").getValue()
var secret = sheet.getRange("C5").getValue();
var baseUrl = 'https://bittrex.com/api/v1.1/';
var nonce = Math.floor(new Date().getTime()/1000);

/**
 * Used to retrieve all balances from your account.
 * @return the balance of any currency that is not 0.
 */
function bittrexGetbalances() {
  var finals = [];
  var results = bittrexPrivateRequest("account/getbalances");
  Logger.log(results)
  results.forEach(function(result,index) {
    if (result.Balance > 0){
      finals.push({'currency': result.Currency, 'balance': result.Balance})
    }
  });
  Logger.log(finals)
  return json2array_(finals);
};

/**
 * Used to retrieve the balance from your account for a specific currency.
 * @param {string} a string literal for the currency (ex: LTC).
 * @return the currency balance.
 * @customfunction
 */
function bittrexGetbalance(currency) {
 var payload = { "currency" : currency };
 var results = bittrexPrivateRequest("account/getbalance",payload);
 return results.Balance;
};


function bittrexGetLastValue(currency) {
  var moeda = 'BTC-'+currency
  var payload = { "market" : moeda };
  var results = bittrexPublicRequest("getticker",payload);
  return results.Last;
};

function bittrexGetLastValueFull(currency) {
  var payload = { "market" : currency };
  var results = bittrexPublicRequest("getticker",payload);
  return results.Last;
};


function bittrexGetOrders(){
  var finals = [];
  var results = bittrexPrivateRequest("account/getorderhistory");
  Logger.log(results)
  results.forEach(function(result,index) {
    finals.push({'OrderType': result.OrderType, 'Closed': result.Closed, 'Commission': result.Commission, 'Exchange': result.Exchange, 'Price': result.Price, 'PricePerUnit': result.PricePerUnit, 'Quantity': result.Quantity})
  });
  Logger.log(finals)
  return json2array_(finals);
};


function bittrexPublicRequest(command,payload){
  var uri = uriCreator_(command,payload);
  var response = UrlFetchApp.fetch(uri);
  var dataAll = JSON.parse(response.getContentText());
  if (dataAll.success = true) {
    return dataAll.result
  } else {
    return dataAll.message
  } 
}

function bittrexPrivateRequest(command,payload){
  var uri = uriCreator_(command,payload,true)
  var signature = Utilities.computeHmacSignature(Utilities.MacAlgorithm.HMAC_SHA_512, uri, secret);
 
 // Signature copied from comments:
 var apisign = signature.map(function(byte) {
    return ('0' + (byte & 0xFF).toString(16)).slice(-2);
  }).join('');
 
  var headers = {
    "apisign": apisign
  }
  var params = {
    "method": "get",
    "headers": headers,
    "payload": payload
  }
  var response = UrlFetchApp.fetch(uri, params);
  var dataAll = JSON.parse(response.getContentText());
  if (dataAll.success = true) {
    return dataAll.result
  } else {
    return dataAll.message
  }   
};

function uriCreator_(command,payload,private){
  if (payload) {
    var payloadEncoded = Object.keys(payload).map(function(param) {
      return encodeURIComponent(param) + '=' + encodeURIComponent(payload[param]);
    }).join('&');
  }
  if (private) {
    uri = baseUrl.concat(command + "?apikey=" + key + "&nonce=" + nonce + "&" + payloadEncoded)
  } else {
    uri = baseUrl.concat("public/" + command + "?" + payloadEncoded)
  }
  return uri
};


function json2array_(data){
  var results = [];
  var keys = [];
  var values = [];
  for (var i in data){
    for (var key in data[i]){
      if (i == 0) keys.push(key);
      values.push(data[i][key]);
    }
    if (i == 0){
      results.push(keys);
      keys = [];
    }
    results.push(values);
    values = [];
  }
  return results;
};
"""