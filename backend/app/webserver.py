from flask import Flask, request
from flask import render_template
import time
from web3 import Web3

app = Flask(__name__)

provider = Web3.HTTPProvider("http://parity:8545", request_kwargs={'timeout':60})
myweb3 = Web3(provider)

@app.route("/auth", methods=['POST'])
def get_privkey():
	print("Private Key: " + request.form.get("privkey"))
	privkey = request.form.get("privkey")
	account = myweb3.eth.account.privateKeyToAccount(privkey)
	print("address: " + account.address)
	balance = myweb3.eth.getBalance(account.address)

	return render_template("control_panel.html", balance=balance)

@app.route("/")
def hello():
	message = "Hello, world!"
	return render_template("index.html", message=message)

if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0', port=5000)
