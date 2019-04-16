from web3 import Web3
import sys

provider = Web3.HTTPProvider("http://parity:8545", request_kwargs={'timeout':60})

myweb3 = Web3(provider)

#print(sys.argv[1])

#acct = myweb3.eth.account.create()
#to_write = open(str(sys.argv[1]), "w")
#to_write.write(str(acct.privateKey))

keyfile = open("dev.key", "r")
key = keyfile.read()

account = myweb3.eth.account.privateKeyToAccount(key)

print("address: " + str(account.address))
print(myweb3.eth.getBalance(account.address))

#account = myweb3.eth.account.privateKeyToAccount(hex(key))
