import requests
import json

url = "http://127.0.0.1:8000/api/tokenize"
# Código com erro: @ é inválido, { sem fechar, 12abc mal formado
payload = {"source": "program Teste; begin x := 10@; { comentário aberto"}
headers = {"Content-Type": "application/json"}

try:
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    print("Status Code:", response.status_code)
    print("Response JSON:")
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print("Erro ao testar API:", e)
