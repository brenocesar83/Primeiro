import requests


url = "https://bittrex.com/api/v2.0/pub/currencies/GetBTCPrice"
req = requests.get(url)
if req.status_code == 200:
    result = req.json()
else:
    print("Falhou!! A resposta do servidor foi: ", req.status_code)


response = result['result']['bpi']['USD']['rate_float']
print(response)

""""

"""

