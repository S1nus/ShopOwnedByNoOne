from web3 import Web3
import sys

provider = Web3.HTTPProvider("http://parity:8545", request_kwargs={'timeout':60})

myweb3 = Web3(provider)

#print(sys.argv[1])

acct = myweb3.eth.account.create()
to_write = open(str(sys.argv[1]), "w")
to_write.write(str(acct.privateKey.hex()))

to_write = open(str(sys.argv[2]), "w")
to_write.write(str(acct.address))
