import time
import json
from hashlib import sha256
from transaction import Transaction
import sys


class Block:
    def __init__(self, index, previousHash, transactions, gasUsed):
        self.timestamp = time.ctime(time.time())
        self.index = index
        self.previousHash = previousHash
        self.transactions: list(Transaction) = transactions
        self.gasUsed = str(gasUsed)
        self.size = str(self.calculateSize())+" B"
        self.hash = self.calculateHash()

    def calculateHash(self):
        i = 0
        txHash = ""
        while i < len(self.transactions):
            txHash = txHash+self.transactions[i].sender
            i = i+1
        str = json.dumps(self.timestamp+self.index+self.previousHash +
                         txHash + self.gasUsed)
        return sha256(str.encode("utf-8")).hexdigest()

    def calculateSize(self):
        return sys.getsizeof(self)
