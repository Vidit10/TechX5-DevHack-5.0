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

# Example participant key pairs
participant1_private_key = RSA.generate(2048).export_key()
participant1_public_key = RSA.import_key(participant1_private_key).publickey().export_key()

participant2_private_key = RSA.generate(2048).export_key()
participant2_public_key = RSA.import_key(participant2_private_key).publickey().export_key()

# Create the blockchain and add some blocks
blockchain = [create_genesis_block()]
previous_block = blockchain[0]

# Simulate votes on the website with public keys included
votes = [
    {"username": "user1", "candidate": "Candidate A", "private_key": participant1_private_key, "public_key": participant1_public_key, "signature": ""},
    {"username": "user2", "candidate": "Candidate B", "private_key": participant2_private_key, "public_key": participant2_public_key, "signature": ""},
    # Add more votes as needed
]


# Create blocks for each vote and validate before adding to the blockchain
for vote in votes:
    vote_data = f"Vote: {vote['username']} for {vote['candidate']}"

    # Sign the data using the participant's private key
    vote['signature'] = sign_data(vote_data, vote['private_key'])

    # Verify the signature using the participant's public key
    if verify_signature(vote_data, vote['signature'], vote['public_key']):
        new_block = create_new_block(previous_block, vote_data, vote['private_key'])
        blockchain.append(new_block)
        previous_block = new_block
        print(f"Block #{new_block.index} has been added to the blockchain!")
        print(f"Hash: {new_block.hash}\n")
    else:
        print(f"Vote from {vote['username']} is not valid. Signature verification failed.\n")