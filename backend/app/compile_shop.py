from web3 import Web3
from solc import compile_source

# Connect to Parity
# Docker container's hostnames are the name of the container!
provider = Web3.HTTPProvider('http://parity:8545', request_kwargs={'timeout':60})

if (provider.isConnected()):
    print("Connected to our Parity node")
else:
    print("Not connected to our Parity Node. WHY??!?!?!")

myweb3 = Web3(provider)
