from web3 import Web3
import web3
import requests
import json
# 我们新建的合约地址，0x42f1b3900eC34848c467279c6b753226c7DE2419，https://goerli.etherscan.io/address/0x42f1b3900eC34848c467279c6b753226c7DE2419

# w3 = web3.AsyncHTTPProvider('https://goerli.infura.io/v3/1174cd813b9c497bbea261630e25a6f0')
w3 = Web3(Web3.HTTPProvider('https://goerli.infura.io/v3/1174cd813b9c497bbea261630e25a6f0'))
print(w3.isConnected())



ABI = [
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_key",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_value",
				"type": "string"
			}
		],
		"name": "store",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_key",
				"type": "string"
			}
		],
		"name": "retreive",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]

# Contract = w3.eth.contract(ABI,'0x42f1b3900eC34848c467279c6b753226c7DE2419')
contract = w3.eth.contract('0x42f1b3900eC34848c467279c6b753226c7DE2419',abi = ABI)
#[<Function retreive(string)>, <Function store(string,string)>]
# print(contract.all_functions())
# response = contract.functions.retreive('hf').call()

# my_account = w3.eth.account.create('Polyuuuuuu!')
account = {}
account['address'] = '0xc09ffDdBa648DE9835C3d4E2a6ea12BA9adbc3Fb'
account['sk'] = '0x3057f2ba37be4ea2e248747a72ff73af65270ae4c3e6bae800cdbaa0c71f1461'

    

# query_tx = contract.functions.store('Dapp','123').buildTransaction(
#     {
#         'from': account['address'],
#         'nonce': w3.eth.get_transaction_count(account['address']),
#     }
# )
# query_tx_sign = w3.eth.account.sign_transaction(query_tx,account['sk'])
# query_tx_hash = w3.eth.send_raw_transaction(query_tx_sign.rawTransaction)
# query_tx_receipt = w3.eth.wait_for_transaction_receipt(query_tx_hash)

# print(response)
# print(result)

# # 5. Build reset tx
# reset_tx = Incrementer.functions.reset().buildTransaction(
#     {
#         'from': account_from['address'],
#         'nonce': web3.eth.get_transaction_count(account_from['address']),
#     }
# )

# # 6. Sign tx with PK
# tx_create = web3.eth.account.sign_transaction(reset_tx, account_from['private_key'])

# # 7. Send tx and wait for receipt
# tx_hash = web3.eth.send_raw_transaction(tx_create.rawTransaction)
# tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

# print(f'Tx successful with hash: { tx_receipt.transactionHash.hex() }')

def Eth_Query(ID = str):
    res = contract.functions.retreive(ID).call()
    return res # string
# mycontract.methods.retreive($("#key2").val()).call().then(function (response) { if (response != '') { document.getElementById('field3').innerHTML = `This is stored on the Ethereum blockchain: {"key":"${$("#key2").val()}", {"value":"${response}"}}` } });
				# $("#field3").show()

def Eth_Invoke(ID = str, Value = str):
    query_tx = contract.functions.store(ID,Value).buildTransaction(
    {
        'from': account['address'],
        'nonce': w3.eth.get_transaction_count(account['address']),
    }
    )
    try:
        query_tx_sign = w3.eth.account.sign_transaction(query_tx,account['sk'])
        query_tx_hash = w3.eth.send_raw_transaction(query_tx_sign.rawTransaction)
        query_tx_receipt = w3.eth.wait_for_transaction_receipt(query_tx_hash)
        print(f'Tx successful with hash: { query_tx_receipt.transactionHash.hex() }')
        return query_tx_receipt.transactionHash.hex()
    except:
        return 'error'

def Fabric_Invoke(ID = str, Value = str):
    try:
        headers = {'content-type': 'application/json'}
        get_string = '?' + 'key=' + ID + '&' + 'value=' + Value
        Invoke_URL = 'http://localhost:8000/invoke_hyperledger' + get_string
        res = requests.get(url=Invoke_URL,data=None,headers=headers)
        print(res.text)
        return res.json()['status']
    except:
        return 'error'

def Fabric_Query(ID = str):
    headers = {'content-type': 'application/json'}
    get_string = '?' + 'key=' + ID
    Invoke_URL = 'http://localhost:8000/query_hyperledger' + get_string
    res = requests.get(url=Invoke_URL,data=None,headers=headers)
    content = res.text.replace('"{','{').replace('}"','}')
    content = json.loads(content)
    return content['value'] # string

def Fabric_to_Eth(ID = str):
    try:
        value = Fabric_Query(ID) # dict
        value = json.dumps(value)
        tx_hash = Eth_Invoke(ID,value)
        return tx_hash # hex
    except:
        return 'error'

def Eth_to_Fabric(ID = str):
    try:
        value = Eth_Query(ID)
        print(value)
        status = Fabric_Invoke(ID,value)
        return status
    except:
        return 'error'

# import requests
# import json

# headers = {'content-type': 'application/json'}

# # res = requests.get(url='http://localhost:8000/invoke_hyperledger?key=cityu&value=foo',data=None,headers=headers)
# res = requests.get(url='http://localhost:8000/query_hyperledger?key=cityu',data=None,headers=headers)


# print(res.json())

