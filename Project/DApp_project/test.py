import requests
import json

headers = {'content-type': 'application/json'}

# res = requests.get(url='http://localhost:8000/invoke_hyperledger?key=cityu&value=foo',data=None,headers=headers)
res = requests.get(url='http://localhost:8000/query_hyperledger?key=PolyU',data=None,headers=headers)


print(res.json()['value'])
