from flask import Flask, request
from flask import render_template
import time
from web3 import Web3
from web3.gas_strategies import time_based
from web3.gas_strategies import rpc
import sqlite3
import string
import random

app = Flask(__name__)

#provider = Web3.HTTPProvider("http://parity:8545", request_kwargs={'timeout':60})
provider = Web3.HTTPProvider("https://kovan.infura.io/v3/42570b1c29d94b42b621f9b786c4bdd6", request_kwargs={'timeout':60})
myweb3 = Web3(provider)
abi = open("shop.abi", "r").read()
contract = myweb3.eth.contract(abi=abi, address="0xfD6157428a210df574159b39e065A1bfC15023c8")
myweb3.eth.setGasPriceStrategy(rpc.rpc_gas_price_strategy)

@app.route("/")
def homepage():
    return render_template("index.html")

@app.route("/auth", methods=["POST"])
def authenticate():
    privkey = request.form.get("privkey")
    try:
        account = myweb3.eth.account.privateKeyToAccount(privkey)
        address = account.address
        current_workers = getEmployees()
        employeeStatus = 0
        if (address in current_workers):
            employeeStatus = 1
        balance = myweb3.eth.getBalance(address)
        strkey = str(account.privateKey.hex())
        token = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(20))
        conn = sqlite3.connect("tokens.db")
        query = conn.execute("select * from tokens where privateKey=?", [strkey])
        query = query.fetchall()
        if (len(query) == 0):
            query = conn.execute("insert into tokens (privateKey, address, balance, employee, token) values (?, ?, ?, ?, ?)", [strkey, address, balance, employeeStatus, token])
            conn.commit()
        else:
            balance = query[0][3]
            query = conn.execute("update tokens set token = ? where privateKey = ?", [token, strkey])
            conn.commit()
    except Exception as e:
        return render_template("login.html", error=str(e))

    conn.close()
    return render_template("control_panel.html", token=token, balance=myweb3.fromWei(balance, 'ether'), employeeStatus="Become Employee" if employeeStatus==0 else "Stop Working")

@app.route("/pay", methods=["POST"])
def pay():
    token = request.form.get("token")
    try:
        conn = sqlite3.connect("tokens.db")
        query = conn.execute("select * from tokens where token=?", [token])
        query = query.fetchall()
        assert len(query) == 1, "authentication error"
        address = query[0][2]
        bal = myweb3.fromWei(query[0][3], 'ether')
        current_workers = getEmployees()
        employeeStatus = 0
        if (address in current_workers):
            employeeStatus = 1
        assert float(bal) > 0.015, "not enough balance"
        currentBal = float(bal) - float(0.015)
        query = conn.execute("UPDATE tokens set balance = ? where token = ?", [myweb3.toWei(currentBal, "ether"), token])
        conn.commit()
        conn.close()
        return render_template("control_panel.html", token=token, balance=currentBal, employeeStatus="Become Employee" if employeeStatus==0 else "Stop Working")
    except Exception as e:
        return render_template("result.html", message="Error paying: "+str(e), token=token)

@app.route("/becomeEmployee", methods=["POST"])
def toggleEmployee():
    token = request.form.get("token")
    try:
        conn = sqlite3.connect("tokens.db")
        query = conn.execute("select * from tokens where token = ?", [token])
        query = query.fetchall()
        assert len(query) == 1, "authentication error"
        balance = query[0][3]
        address = query[0][2]
        pkey = query[0][1]
        current_workers = getEmployees()
        employeeStatus = 0
        if (address in current_workers):
            employeeStatus = 1
        if (employeeStatus == 0):
            # become an employee
            nonce = myweb3.eth.getTransactionCount(address)
            t = contract.functions.become_employee().buildTransaction({'from':address, 'nonce':nonce})
            t['gas'] += 2000
            t['gasPrice'] = myweb3.toWei(3, 'gwei')
            signed = myweb3.eth.account.signTransaction(t, pkey)
            tx = myweb3.eth.sendRawTransaction(signed['rawTransaction'])
            r = get_receipt(str(tx.hex()))
            if not (r == 0):
                if (r['status'] == 1):
                    return render_template("result.html", message="succesfully became employee", token=token)
                else:
                    return render_template("result.html", message="r['status'] wasn't 1: "+str(r), token=token)
            else:
                return render_template("result.html", message="failed to start working", token=token)
        elif (employeeStatus == 1):
            # Quit
            nonce = myweb3.eth.getTransactionCount(address)
            t = contract.functions.quit().buildTransaction({'from':address, 'nonce':nonce})
            t['gas'] += 2000
            t['gasPrice'] = myweb3.toWei(3, 'gwei')
            signed = myweb3.eth.account.signTransaction(t, pkey)
            tx = myweb3.eth.sendRawTransaction(signed['rawTransaction'])
            r = get_receipt(str(tx.hex()))
            if not (r == 0):
                if (r['status'] == 1):
                    return render_template("result.html", message="succesfully quit", token=token)
                else:
                    return render_template("result.html", message="r['status'] wasn't 1: "+str(r), token=token)
            else:
                return render_template("result.html", message="failed to quit", token=token)
        else:
            #there is an error
            return render_template("result.html", message="Employee status unknown", token=token)
    except Exception as e:
        return "error son"

@app.route("/reauth", methods=["POST"])
def reauth():
    token = request.form.get("token")
    try:
        conn = sqlite3.connect("tokens.db")
        query = conn.execute("select * from tokens where token = ?", [token])
        query = query.fetchall()
        assert len(query) == 1, "authentication error"
        address = query[0][2]
        balance = query[0][3]
        current_workers = getEmployees()
        if (address in current_workers):
            employeeStatus = 1
        else:
            employeeStatus = 0
        return render_template("control_panel.html", token=token, balance=myweb3.fromWei(balance, 'ether'), employeeStatus="Become Employee" if employeeStatus==0 else "Stop Working")
    except Exception as e:
        return render_template("login.html", error="error: " + str(e))

def getEmployees():
    addrs = []
    addrs.append(str(contract.functions.get_num_employees(0).call()))
    addrs.append(str(contract.functions.get_num_employees(1).call()))
    return addrs

def get_receipt(signedTrans):
    time.sleep(10)
    attempts = 0
    while (attempts < 4):
        try:
            print("attempting...")
            print("number of attempts: " + str(attempts))
            r = myweb3.eth.getTransactionReceipt(signedTrans)
            assert not r == None, "r was None"
            return r
        except Exception as e:
            attempts += 1
            print(str(e))
    return 0

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
