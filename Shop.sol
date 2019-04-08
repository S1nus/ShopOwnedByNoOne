pragma solidity >=0.4.22 <0.6.0;

contract Shop {

    address property_manager;
    mapping (address => bool) public employees;
    uint min_balance = 71;
    uint lemonade_price = 50;
    uint balance;
    bool shop_up = false;

    constructor() public {
        property_manager = msg.sender;
    }

    modifier onlyEmployee() {
        require(employees[msg.sender] == true);
        _;
    }
    
    modifier onlyPropertyManager() {
        require(property_manager == msg.sender);
        _;
    }

    function buyLemonade() public payable {
        balance += msg.value;
    }

}
