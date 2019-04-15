from python:3.6
run apt-get update
run apt-get install python-pip -y
run apt-get install libssl-dev -y
run pip3 install requests==2.4.3 flask flask_cors flask-mysql twilio bcrypt blockcypher flask_api py-solc
run apt-get install build-essential libffi-dev -y;
run python -c "from solc import install_solc; install_solc('v0.4.16');"
run echo 'export PATH="$PATH:/root/.py-solc/solc-v0.4.16/bin"' >> /root/.bashrc

copy web3py/requirements-dev.txt ./web3/
copy web3py/web3 ./web3/web3/
COPY web3py/tests ./web3/tests/
COPY web3py/ens ./web3/ens/
COPY web3py/setup.py ./web3/
COPY web3py/README.md ./web3/
workdir ./web3/
run pip3 install -r requirements-dev.txt
run pip3 install -e ./
workdir /

CMD /bin/bash
