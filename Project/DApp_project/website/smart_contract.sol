pragma solidity >=0.4.22 <0.9.0;


contract Storage {

    mapping(string=>string) identity;
    address Admin;

    constructor(){
        Admin = msg.sender;
    }
    
    modifier onlyAdmin {
        require(msg.sender == Admin, "Not Admin");
        _;
    }


    function store(string memory _key,string memory _value) public onlyAdmin{
        identity[_key]=_value;
    }


    function retreive(string memory _key) public view returns (string memory){
        return identity[_key];
    }
}


//This smart contract was uploaded to the goerli test network at "https://goerli.etherscan.io/address/0x42f1b3900eC34848c467279c6b753226c7DE2419"