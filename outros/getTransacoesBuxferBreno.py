import requests
import json


with open("secrets.json") as secrets_file:
    secrets = json.load(secrets_file)
    secrets_file.close()
    username = secrets['username']
    password = secrets['password']

base = "https://www.buxfer.com/api"
url = base + "/login?userid=" + username + "&password=" + password

req = requests.get(url)

# print(req.status_code)

result = req.json()

response = result['response']
token = response['token']

startDate = '2017-12-23'
endDate = '2018-01-23'

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
            print('"' + str(transaction['normalizedDate']) + '","' + str(transaction['description']).upper() + '","' +
                  str(transaction['amount']).replace('.', ',') + '"')
else:
    for transaction in transactions['transactions']:
        print('"' + str(transaction['normalizedDate']) + '","' + str(transaction['description']).upper() + '","' +
              str(transaction['amount']).replace('.', ',') + '"')
