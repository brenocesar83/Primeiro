# Conectar na API do site Buxfer.com e baixar as transações de um
# determinado período, imprimindo para um CSV

import requests

username = "brenocesar@gmail.com"
password = "oioioi"

base = "https://www.buxfer.com/api"
url = base + "/login?userid=" + username + "&password=" + password

req = requests.get(url)

# print(req.status_code)

result = req.json()

response = result['response']
token = response['token']

startDate = '2017-09-20'
endDate = '2017-10-20'

url = base + "/transactions?token=" + token + "&startDate=" + startDate + "&endDate=" + endDate

req = requests.get(url)
result = req.json()
transactions = result['response']
numTransactions = transactions['numTransactions']
numPages = (int(numTransactions)//25) + 2

if numPages > 2:
    for i in range(numPages-1):
        url = base + "/transactions?token=" + token + "&startDate=" + startDate + "&endDate=" + endDate + \
              "&page=" + str(i+1)
        #print(url)
        req = requests.get(url)
        result = req.json()
        transactions = result['response']
        for transaction in transactions['transactions']:
            date = str(transaction['normalizedDate'])
            desc = str(transaction['description']).encode('utf-8').upper()
            total = str(transaction['amount']).replace('.', ',')
            print('"',date,'","' ,desc,'","',total,'"')
            #print(date, desc, total)
else:
    for transaction in transactions['transactions']:
        print('"' + str(transaction['normalizedDate']) + '","' + str(transaction['description']).upper().encode('utf-8') + '","' +
              str(transaction['amount']).replace('.', ',') + '"')
