pragma solidity >=0.4.22 <0.6.0;

contract Shop {

    address property_manager;
    //mapping (address => bool) public employees;
    address[] public employees = new address[](2);
    uint min_balance = 71;
    uint lemonade_price = 50;
    uint balance;
    bool shop_up = false;

    constructor() public {
        property_manager = msg.sender;
        employees.push(msg.sender);
    }

    /*modifier onlyEmployee() {
        r//equire(employees[msg.sender] == true);
        _;
    }*/
    
    modifier onlyPropertyManager() {
        require(property_manager == msg.sender);
        _;
    }

    function buyLemonade() public payable {
        balance += msg.value;
    }

    function pay_employees() internal {
        if (balance < min_balance) {
        
        }
    }

}
