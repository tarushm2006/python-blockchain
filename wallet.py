import sys
from chain import Chain
from ecdsa import SECP256k1, SigningKey
from transaction import Transaction


class Wallet:
    def __init__(self, chain: Chain = [], privateKey=""):
        self.chain = chain
        self.updatedTill = 0
        self.balance = 0
        if (privateKey != ""):
            self.privateKey = SigningKey.from_string(
                bytes.fromhex(privateKey), SECP256k1)
            self.publicKey = self.privateKey.verifying_key

    def publicAddress(self):
        address = self.publicKey.to_string()
        return address.hex()

    def privateAddress(self):
        address = self.privateKey.to_string()
        return address.hex()

    def generatewallet(self):
        self.privateKey = SigningKey.generate(curve=SECP256k1)
        self.publicKey = self.privateKey.verifying_key

    def broadcastTx(self, reciever, value, data):

        if int(value) <= self.balance:
            gas = sys.getsizeof(data)
            tx: Transaction = Transaction(
                self.publicAddress(), reciever, value, data, gas * 10 ** 10)
            signature = self.privateKey.sign(bytes.fromhex(tx.hash()))
            if (self.balance - int(value)) >= gas:
                self.balance = self.balance - (gas * 10 ** 10)
                print("Transaction broadcasted")
                self.chain.submitTx(tx, signature)

            else:
                print("Insufficient balance")

        else:
            print("Insufficient balance")

    def sync(self):
        b = self.updatedTill
        while b < len(self.chain.chain):
            t = 0
            while t < len(self.chain.chain[b].transactions):
                tx: Transaction = self.chain.chain[b].transactions[t]
                if tx.sender == self.publicAddress():
                    self.balance = self.balance - int(tx.value)

                elif tx.receiver == self.publicAddress():
                    self.balance = self.balance + int(tx.value)

                t = t + 1

            b = b + 1

        self.updatedTill = b
