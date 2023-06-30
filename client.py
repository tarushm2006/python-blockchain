from chain import Chain
from wallet import Wallet
from codeParser import parse

chain = Chain()

data = parse()

wallet = Wallet(chain)
wallet.generatewallet()

chain.genesisBlock(wallet.publicAddress())

wallet.sync()

wallet.broadcastTx(
    "55d660560443f0a47f989229e36d5db5ed929ff17ad08c65f94964ffc632924e91e7852349aa4cc0e0bc17a92667f28c0e0f456c3f835449af8e97c3600e4898", str(
        5000*10**18),
    data
)

block = chain.createBlock()
chain.mineBlock(block, wallet.publicAddress())

chain.printChain()
wallet.sync()

chain.executeContract(2, chain.chain[1].transactions[0].hash)
