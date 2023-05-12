In the lab2 VM image, unzip the DApp_project.tar.xz and cd the DApp_project:

```shell
npm install express@4.17.1
npm install fabric-ca-client@2.1.0
npm install fabric-network@2.1.0
npm install fs@0.0.1-security
npm install grpc@1.24.3
npm install keccak@2.1.0
npm install path@0.12.7
npm install secp256k1@3.8.0
npm install url@0.11.0
npm install web3@1.2.9
npm install websocket@1.0.31
```

then,

```shell
sudo ./start_Network.sh
```

For the front end start up

```shell
npm install streamlit
npm install web3
```

then you could do

```shell
streamlit run .\EHDID.py
```

The following solidity contract (proof of concept) is installed on the Ropsten Testnet (Ethereum) but it can be replaced with any other solidity contract code. The website interacts with the Ethereum network through the web3.js library at the frontend file "index.html".
```shell
pragma solidity >=0.4.22 <0.7.0;


contract Storage {

    mapping(string=>string) assets;

 
    function store(string memory _key,string memory _value) public {
        assets[_key]=_value;
    }


    function retreive(string memory _key) public view returns (string memory){
        return assets[_key];
    }
}
```

The following smart contract (proof of concept) is installed on Hyperledger Fabric 2.0 network but it can be replaced with any other smart contract code. The website interacts with the Hyperledger Fabric network through the Node Fabric SDK at the two backend files "Query_Hyperledger.js" and "Invoke_Hyperledger.js".
```shell
package main

import (
	"fmt"
	"github.com/hyperledger/fabric-chaincode-go/shim"
	sc "github.com/hyperledger/fabric-protos-go/peer"
)


// Define the Smart Contract structure
type SmartContract struct {
}

func (s *SmartContract) Invoke(APIstub shim.ChaincodeStubInterface) sc.Response {
	// Retrieve the requested Smart Contract function and arguments
	function, args := APIstub.GetFunctionAndParameters()
	// Route to the appropriate handler function to interact with the ledger appropriately
	if function == "store" {
		return s.store(APIstub, args)
	} else if function == "Init" {
		return s.Init(APIstub)
	} else if function == "retrieve" {
		return s.retrieve(APIstub, args)
	} else {fmt.Println("Invalid Smart Contract function name.")
	return shim.Error("Invalid Smart Contract function name.")}
}


func (s *SmartContract) retrieve(APIstub shim.ChaincodeStubInterface, args []string ) sc.Response {
	var Object,_=APIstub.GetState(args[0])	
	return shim.Success([]byte(Object))
}

func (s *SmartContract) store(APIstub shim.ChaincodeStubInterface, args []string ) sc.Response {
	APIstub.PutState(args[0],[]byte(args[1]))
	return shim.Success(nil)
}

func (s *SmartContract) Init(APIstub shim.ChaincodeStubInterface ) sc.Response {
	return shim.Success(nil)
}

func main() {
	//Create a new Smart Contract
	err := shim.Start(new(SmartContract))
	if err != nil { 
		fmt.Printf("Error creating new Smart Contract: %s", err)
	}
}
```
