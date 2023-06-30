import time
import json
from hashlib import sha256


class Transaction:
    def __init__(self, sender, receiver, value, data, gas, signature=""):
        self.timestamp = time.ctime(time.time())
        self.sender = sender
        self.receiver = receiver
        self.value = value
        self.data = data
        self.gas = gas
        self.signature = signature
        self.status = "Pending"

    def hash(self):
        str = json.dumps(self.sender+self.receiver +
                         self.data+self.value+self.timestamp)
        return sha256(str.encode("utf-8")).hexdigest()

    def success(self):
        self.status = "Verified"

    def decline(self):
        self.status = "Declined"
