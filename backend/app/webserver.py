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

provider = Web3.HTTPProvider("http://parity:8545", request_kwargs={'timeout':60})
myweb3 = Web3(provider)
abi = open("shop.abi", "r").read()
contract = myweb3.eth.contract(abi=abi, address="0xfD6157428a210df574159b39e065A1bfC15023c8")
myweb3.eth.setGasPriceStrategy(rpc.rpc_gas_price_strategy)

@app.route("/auth", methods=['POST'])
def get_privkey():
    privkey = request.form.get("privkey")
        try:
            account = myweb3.eth.account.privateKeyToAccount(privkey)
                strkey = str(account.privateKey.hex())
                token = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(20))
                conn = sqlite3.connect("tokens.db")
                query = conn.execute("select * from tokens where privateKey=?", [strkey])
                query = query.fetchall()
                if (len(query) == 0):
                    query = conn.execute("insert into tokens (privateKey, token) values (?, ?)", [strkey, token])
                        conn.commit()
                else:
                    query = conn.execute("delete from tokens where privateKey=?", [strkey])
                        query = conn.execute("insert into tokens (privateKey, token) values (?, ?)", [strkey, token])
                        conn.commit()
                balance = myweb3.eth.getBalance(account.address)
                balance = myweb3.fromWei(balance, 'ether')
                conn.close()
                return render_template("control_panel.html", balance=balance, token=token)
        except Exception as e:
            return render_template("control_panel.html", balance=str(e))

@app.route("/auth2", methods=['POST'])
def get_privkey():
    token = request.form.get("token")
        try:
            conn = sqlite3.connect("tokens.db")
                query = conn.execute("select * from tokens where token=?", token=[token])
                query = conn.fetchall()
                if (len(query) != 1):
                    print("error: query = " + str(len(query)))
                    return render_template('control_panel.html', balance="error sry")
                else:
                    privkey = query[0][1]
                    account = myweb3.eth.account.privateKeyToAccount(privkey)
                    balance = myweb3.eth.getBalance(account.address)
                    return render_template("control_panel.html", balance=balance, token=token)
        except Exception as e:
            return render_template("control_panel.html", balance=str(e))

@app.route("/")
def homepage():
    return render_template("index.html")

@app.route("/pay", methods=['POST'])
def pay():
    token = request.form.get('token')
        conn = sqlite3.connect("tokens.db")
        query = conn.execute("select * from tokens where token=?", [token])
        query = query.fetchall()
        if (len(query) != 1):
            print("error: query = " + str(len(query)))
        else:
            privkey = query[0][1]
                account = myweb3.eth.account.privateKeyToAccount(privkey)
                balance = myweb3.eth.getBalance(account.address)
                print("balance: " + str(balance))
                if (balance >= .015):
                    nonce = myweb3.eth.getTransactionCount(account.address)
                        t = contract.functions.purchase().buildTransaction({'from':account.address, 'nonce':nonce, 'value':myweb3.toWei(0.015, 'ether')})
                        t['gas'] += 2000
                        t['gasPrice'] = myweb3.toWei(3, 'gwei')
                        signed = myweb3.eth.account.signTransaction(t, account.privateKey)
                        tx = myweb3.eth.sendRawTransaction(signed['rawTransaction'])
                        print(tx.hex())
                        time.sleep(10)
                        recpt = myweb3.eth.getTransactionReceipt(str(tx.hex()))
                        if (recpt['status'] == 1):
                            return render_template("result.html", message="Looks like your transaction succeeded.")
                        else:
                            return render_template("result.html", message="Looks like your transaction failed, but I am sometimes wrong.")
                else:
                    return "you don't have enough :("
        return "we paid"

@app.route("/amemployee", methods=["POST"])
def am_employee():
    token = request.form.get("token")
        conn = sqlite3.connect("tokens.db") 
        query = conn.execute("select * from tokens where token=?", [token])
        query = query.fetchall()
        if (len(query) != 1):
            print("error: query = " + str(len(query)))
        else:
            privkey = query[0][1]

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
