from web3 import Web3
import sys

provider = Web3.HTTPProvider("http://parity:8545", request_kwargs={'timeout':60})

myweb3 = Web3(provider)
