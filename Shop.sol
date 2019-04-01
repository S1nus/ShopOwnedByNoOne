pragma solidity ^0.4.22;

contract Shop {
    
    address property_manager;
    mapping (address => bool) public employees;
    uint min_balance = 71;
    uint lemonade_price = 50;
    uint balance;
    
    constructor() public {
        property_manager = msg.sender;
    }
    
    modifier onlyEmployee() {
        require(employees[msg.sender] == true);
        _;
    }
    
    function buyLemonade() payable {
        balance += msg.balance;
    }
    
}