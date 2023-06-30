from block import Block
from transaction import Transaction
from ecdsa import VerifyingKey, SECP256k1


class Chain:
    def __init__(self):
        self.currentBlock = 1
        self.chain = []
        self.pendingTxs = []

 # To be called before initiating a transaction

    def genesisBlock(self, publicaddress):
        if len(self.chain) == 0:
            tx = Transaction("0x0", publicaddress, str(10000*10**18),
                             "print('The chain starts today')", 0)
            tx.success()
            block = Block("1", "0", [tx], 0)
            self.currentBlock = self.currentBlock + 1
            self.chain.append(block)

        else:
            print("invalid block")

# called by the wallet when tx is submited by user

    def submitTx(self, tx: Transaction, signature):
        tx.signature = signature
        self.pendingTxs.append(tx)
        print("Transaction submitted with hash "+tx.hash())

    def createBlock(self):
        if len(self.chain) != 0:
            if len(self.pendingTxs) != 0:
                txs = []
                gasUsed = 0
                i = 0
                while i < len(self.pendingTxs):
                    tx = self.pendingTxs[i]
                    sender = VerifyingKey.from_string(
                        bytes.fromhex(tx.sender), SECP256k1)
                    validation = sender.verify(
                        tx.signature, bytes.fromhex(tx.hash()))
                    if validation:
                        tx.success()
                        gasUsed = gasUsed + tx.gas
                        txs.append(tx)

                    else:
                        tx.decline()
                        txs.append(tx)

                    i = i + 1

                block = Block(str(self.currentBlock),
                              self.chain[len(self.chain) - 1].hash, txs, gasUsed)
                print("Block created with hash "+block.hash)
                return block

            else:
                print("No pending transactions")

        else:
            print("Chain not started")

    def mineBlock(self, block: Block, publicAddress):
        if len(self.chain) != 0:
            if block == None:
                print("No block to mine")
            elif int(block.index) == int(self.currentBlock):
                i = 0
                while i < len(self.pendingTxs):
                    p = 0
                    while p < len(block.transactions):
                        if block.transactions[p].hash == self.pendingTxs[i].hash:
                            del self.pendingTxs[i]

                        p = p + 1

                    i = i + 1

                reward = Transaction("0x0", publicAddress,
                                     str(block.gasUsed), "print('Reward')", 0)
                reward.success()
                block.transactions.append(reward)
                self.chain.append(block)
                print("Block mined with hash " + block.hash)
                return True

            else:
                print("Block not valid")

        else:
            print("Chain not started")

    def printChain(self):
        i = 0
        while i < len(self.chain):
            t = 0
            txs = []
            while t < len(self.chain[i].transactions):
                tx: Transaction = self.chain[i].transactions[t]
                txObject = {
                    "timestamp": tx.timestamp,
                    "sender": tx.sender,
                    "receiver": tx.receiver,
                    "value": tx.value,
                    "data": tx.data,
                    "gas": tx.gas,
                    "status": tx.status,
                    "hash": tx.hash()
                }
                txs.append(txObject)
                t = t + 1
            block = {
                "index": self.chain[i].index,
                "hash": self.chain[i].hash,
                "previousHash": self.chain[i].previousHash,
                "gasUsed": self.chain[i].gasUsed,
                "timestamp": self.chain[i].timestamp,
                "transactions": txs
            }
            print(block, end="\n,")

            i = i + 1

  # Executes the speicified smart contract

    def executeContract(self, blockIndex, txHash):
        block = self.chain[blockIndex - 1]
        tx: Transaction
        i = 0
        while i < len(block.transactions):
            if txHash == block.transactions[i].hash:
                tx = block.transactions[i]
                break

            i = i + 1

        exec(tx.data)
