pragma solidity >=0.4.22 <0.6.0;

contract Shop {

    address payable employee0;
    address payable employee1;
    
    uint shop_balance;

    constructor() public {
        employee0 = msg.sender;
    }

    function purchase() public payable {
        shop_balance += msg.value;
    }
    
    function get_balance() public view returns (uint) {
        return shop_balance;
    }
    
    function get_num_employees(uint employee_number) public view returns (address) {
        if (employee_number == 0) {
            return employee0;
        }
        else if (employee_number == 1) {
            return employee1;
        }
    }
}
