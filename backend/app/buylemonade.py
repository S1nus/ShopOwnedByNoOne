from web3 import Web3
import sys

provider = Web3.HTTPProvider("http://parity:8545", request_kwargs={'timeout':60})

myweb3 = Web3(provider)

abi = open("shop.abi", "r").read()
bytecode = open("shop.bin", "r").read()
bytecode = int(bytecode[:-1], 16)

private_key = open("dev1.key", "r").read()
account = myweb3.eth.account.privateKeyToAccount(private_key)

