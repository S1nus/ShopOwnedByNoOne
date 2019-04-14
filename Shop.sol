pragma solidity >=0.4.22 <0.6.0;

contract Shop {

    address payable employee0;
    address payable employee1;
    
    uint shop_balance;
    uint shop_min_balance;

    constructor() public payable {
        employee0 = msg.sender;
        shop_min_balance = 30000000000000000;
    }
    
    modifier only_employee {
        require (msg.sender == employee0 || msg.sender == employee1);
        _;
    }

    function purchase() public payable {
        shop_balance += msg.value;
        pay_employees();
    }
    
    function get_balance() public view returns (uint) {
        return shop_balance;
    }
    
    function pay_employees() internal {
        if (shop_balance > shop_min_balance) {
            if (employee0 != address(0) && employee1 == address(0)) {
                //pay employee0 the full payment
                uint to_pay = shop_balance - shop_min_balance;
                shop_balance -= to_pay;
                employee0.transfer(to_pay);
            }
            if (employee0 != address(0) && employee1 != address(0)) {
                // split it up and pay both
                uint to_pay = (shop_balance - shop_min_balance) / 2;
                shop_balance -= (shop_balance -shop_min_balance);
                employee0.transfer(to_pay);
                employee1.transfer(to_pay);
            }
            if (employee0 == address(0) && employee1 != address(0)) {
                //pay employee1 the full payment
                uint to_pay = shop_balance - shop_min_balance;
                shop_balance -= to_pay;
                employee1.transfer(to_pay);
            }
        }
    }
    
    function become_employee() public returns (bool) {
        if (employee0 == address(0)) {
            employee0 = msg.sender;
            return true;
        }
        else if (employee1 == address(0)) {
            employee1 = msg.sender;
            return true;
        }
        else {
            return false;
        }
    }
    
    function quit() public only_employee {
        if (employee0 == msg.sender) {
            employee0 = address(0);
        }
        else if (employee1 == msg.sender) {
            employee1 = address(0);
        }
    }
    
    function get_num_employees(uint employee_number) public view returns (address) {
        if (employee_number == 0) {
            return employee0;
        }
        else if (employee_number == 1) {
            return employee1;
        }
    }
    
    function get_null_employees() public view returns (bool) {
        if (employee0 == address(0) || employee1 == address(0)) {
            return true;
        }
        else {
            return false;
        }
    }
}

