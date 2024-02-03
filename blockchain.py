import hashlib
import time
import json
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash, signature):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash
        self.signature = signature

def calculate_hash(index, previous_hash, timestamp, data):
    value = str(index) + str(previous_hash) + str(timestamp) + str(data)
    return hashlib.sha256(value.encode('utf-8')).hexdigest()

def create_genesis_block():
    return Block(0, "0", time.time(), "Genesis Block", calculate_hash(0, "0", time.time(), "Genesis Block"), "")

def create_new_block(previous_block, data, private_key):
    index = previous_block.index + 1
    timestamp = time.time()
    hash = calculate_hash(index, previous_block.hash, timestamp, data)

    # Sign the block's hash with the private key
    signature = sign_data(hash, private_key)

    return Block(index, previous_block.hash, timestamp, data, hash, signature)

def sign_data(data, private_key):
    key = RSA.import_key(private_key)
    h = SHA256.new(data.encode('utf-8'))
    signature = pkcs1_15.new(key).sign(h)
    return signature

def verify_signature(data, signature, public_key):
    key = RSA.import_key(public_key)
    h = SHA256.new(data.encode('utf-8'))
    try:
        pkcs1_15.new(key).verify(h, signature)
        return True
    except (ValueError, pkcs1_15.VerificationError):
        return False

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Create the genesis block
        self.new_block(previous_hash='1')

    def new_block(self, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'transactions': self.current_transactions,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

    def verify_transaction(self, transaction, public_key):
        """
        Verifies the signature of a transaction using the participant's public key.
        :param transaction: <dict> Transaction data
        :param public_key: <str> Participant's public key
        :return: <bool> True if the signature is valid, False otherwise
        """
        data = transaction['data']
        signature = transaction['signature']
        try:
            key = RSA.import_key(public_key)
            h = SHA256.new(data.encode('utf-8'))
            pkcs1_15.new(key).verify(h, signature)
            return True
        except (ValueError, pkcs1_15.VerificationError):
            return False
