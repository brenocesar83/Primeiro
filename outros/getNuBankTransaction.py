import requests
import json


with open("secrets.json") as secrets_file:
    secrets = json.load(secrets_file)
    secrets_file.close()
    username = secrets['usernamen']
    password = secrets['passwordn']

# faz requisição para pegar client_id e client_secret
data = {'name': 'Nubank', 'uri': 'https://conta.nubank.com.br'}
url = 'https://prod-auth.nubank.com.br/api/registration'
headers = {'content-type': 'application/json'}
client = requests.post(url, data=json.dumps(data), headers=headers)

if client.status_code == 201:
    clientSecret = client.json()['client_secret']
    clientId = client.json()['client_id']
else:
    print("Falhou!! A resposta do servidor foi: ", client.status_code)
    exit(0)

print("Json do ClientID e ClientSecret: ", client.json())
print("clientSecret = ", clientSecret)
print("clientId = ", clientId)


# faz requisição para pegar o token
data = {'grant_type': 'password',
        'username': username,
        'password': password,
        'client_id': clientId,
        'client_secret': clientSecret,
        'nonce': 'NOT-RANDOM-YET'}
headers = {'content-type': 'application/json'}
url = "https://prod-auth.nubank.com.br/api/token"

token = requests.post(url, data=json.dumps(data), headers=headers)

if token.status_code == 200:
    accessToken = token.json()['access_token']
else:
    print("Falhou!! A resposta do servidor foi: ", token.status_code)

print("Json do token: ", token.json())
print("accessToken ", accessToken)

# pega o customer_id (identifica a pessoa)
strToken = "Bearer " + accessToken
print("strToken: ", strToken)
header_auth = {'Authorization': strToken}
url = "https://prod-customers.nubank.com.br/api/customers"

customer_id = requests.get(url, headers=header_auth)
print("Json customer_id: ", customer_id.json())
print("customerId ", customer_id.json()['customer']['id'])
customerId = customer_id.json()['customer']['id']

# pega o account_id (identifica o cartão)
url = "https://prod-credit-card-accounts.nubank.com.br/api/" + customerId + "/accounts"

account_id = requests.get(url, headers=header_auth)
accountID = account_id.json()['accounts'][0]['payment_method']['account_id']
print("Json account_id: ", account_id.json())
print("accountID ", accountID)

# baixa fatura (formato json)


def pp_json(json_thing, sort=True, indents=4):
    if type(json_thing) is str:
        print(json.dumps(json.loads(json_thing), sort_keys=sort, indent=indents))
    else:
        print(json.dumps(json_thing, sort_keys=sort, indent=indents))
    return None


url = "https://prod-accounts.nubank.com.br/api/accounts/" + accountID + "/bills/open"

resposta5 = requests.get(url, headers=header_auth)
print("Fatura: ", pp_json(resposta5.json()))

url = "https://prod-s0-feed.nubank.com.br/api/accounts/" + accountID + "/transactions"
#resposta6 = requests.get(url, headers=header_auth)


def escreverArquivo(nome, dicionario):
    file = open("/media/breno/Dados/temp/"+nome+".json", 'w')
    #writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    # rs = resultados(samples, "tr", "td")
    # writer.writerow(titulo(samples, "th"))
    # for row in rs:
    #     writer.writerow(row)
    file.write(str(dicionario.json()))
    file.close()

#escreverArquivo("tudo", resposta6.json())
# print("transactions: ", resposta6.json())

# 2017-11-28T18:57:04.273Z
#date_since = "2016-05-28T18:57:04.273Z"
#url = "https://prod-s0-feed.nubank.com.br/api/accounts/" + accountID + "/transactions?since=" + date_since + "&transactions-version=v1.5"
#resposta7 = requests.get(url, headers=header_auth)

#print("transactions sem json: ", resposta7)
#print("transactions: ", resposta7.json())

#escreverArquivo("since", resposta7)
