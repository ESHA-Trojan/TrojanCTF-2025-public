# Python program to create Blockchain

# For timestamp
import datetime

# Calculating the hash
# in order to add digital
# fingerprints to the blocks
import hashlib

# To store data
# in our blockchain
import json

# Flask is for creating the web
# app and jsonify is for
# displaying the blockchain
from flask import Flask, jsonify, request

import requests

import copy

import numpy

import os

class APIError(Exception):
    code = 403
    description = "Authentication Error"

API_KEY = "zChWbFITvM4HSPFcshkQ"
SERVER = os.environ.get("FLASK_SERVER")


class Blockchain:

    def register_user(self, username, userID):
        if username == "admin":
            return {'error': "User is already registered."}
        if userID not in self.chains.keys():
            self.chains[userID] = [{'index': 1,
                        'amount': 200,
                        'sender': "admin",
                        'receiver': username,
                        'timestamp': str(datetime.datetime.now()),
                        'proof': 1,
                        'previous_hash': '0'}]
            self.users[username] = userID
            return {'message': "Registration successful."}
        else:
            return {'error': "User is already registered."}
        
    def get_balance(self, username, userID):
        if username not in self.users.keys():
            return {'error': "User does not exist."}
        if self.users[username] != userID:
            return {'error': "Username and userID do not match."}
        
        block_index = 0
        balance = 0

        while block_index < len(self.chains[userID]):
            block = self.chains[userID][block_index]
            if block['sender'] == username:
                balance -= block['amount']
            if block['receiver'] == username:
                balance += block['amount']
            block_index += 1

        return {'balance': balance}
    
    def get_chain(self, username, userID):
        if username not in self.users.keys():
            return {'error': "User does not exist."}
        if username == "admin" or username == "testing":
            return {'error': "External access to admin or testing blockchain is restricted"}
        if self.users[username] != userID:
            return {'error': "Username and userID do not match."}
        
        return {'chain': self.chains[userID]}


    # This function is created
    # to create the very first
    # block and set its hash to "0"
    def __init__(self):
        self.chains = {'Trojan{C01n_m45TeR_t0_4Dm1N}': [{'index': 1,
                        'amount': 10,
                        'sender': "admin",
                        'receiver': "admin",
                        'timestamp': str(datetime.datetime.now()),
                        'proof': 1,
                        'previous_hash': '0'}], "iPtstnMbztS6J9kTtWpm": [{'index': 1,
                        'amount': 10,
                        'sender': "admin",
                        'receiver': "testing",
                        'timestamp': str(datetime.datetime.now()),
                        'proof': 1,
                        'previous_hash': '0'}]}
        self.users = {"admin": "Trojan{C01n_m45TeR_t0_4Dm1N}", "testing": "iPtstnMbztS6J9kTtWpm"}

    # This function is created
    # to add further blocks
    # into the chain
    def create_block(self, amount, sender, sender_id, receiver):
        if sender not in self.users.keys():
            return {'error': "Sender is not registered"}
        if receiver not in self.users.keys():
            return {'error': "Receiver is not registered"}
        if self.users[sender] != sender_id:
            return {'error': "Sender userID is invalid"}  
        if sender == receiver:
            return {'error': "You can't transfer h4xcoins to yourself"}
        if receiver == 'admin' and amount < 100000:
            return {'error': "Please only send me >100000 h4xcoins per transfer. It simplifies accounting on my end. thx ;p"}
        
        force_overflow = amount & ((1 << 64) - 1)
        
        amount = numpy.uint64(force_overflow).view(numpy.int64)

        if amount > self.get_balance(sender, sender_id)['balance']:
            return {'error': "Not enough funds"}
        
        amount = int(amount)
        
        timestamp = str(datetime.datetime.now())
        
        previous_block_sender = self.print_previous_block(sender_id)
        previous_proof_sender = previous_block_sender['proof']
        proof_sender = self.proof_of_work(previous_proof_sender)
        previous_hash_sender = self.hash(previous_block_sender)
        
        block_sender = {'index': len(self.chains[sender_id]) + 1,
                        'amount': amount,
                        'sender': sender,
                        'receiver': receiver,
                        'timestamp': timestamp,
                        'proof': proof_sender,
                        'previous_hash': previous_hash_sender}
        
        self.chains[sender_id].append(block_sender)

        previous_block_receiver = self.print_previous_block(self.users[receiver])
        previous_proof_receiver = previous_block_receiver['proof']
        proof_receiver = self.proof_of_work(previous_proof_receiver)
        previous_hash_receiver = self.hash(previous_block_receiver)
        
        block_receiver = {'index': len(self.chains[self.users[receiver]]) + 1,
                        'amount': amount,
                        'sender': sender,
                        'receiver': receiver,
                        'timestamp': timestamp,
                        'proof': proof_receiver,
                        'previous_hash': previous_hash_receiver}

        self.chains[self.users[receiver]].append(block_receiver)

        result = copy.deepcopy(block_sender)

        result['debug'] = f"{sender} ({sender_id}) has transferred {receiver} ({self.users[receiver]}) {amount} h4xcoins"

        return result

    # This function is created
    # to display the previous block
    def print_previous_block(self, userID):
        return self.chains[userID][-1]

    # This is the function for proof of work
    # and used to successfully mine the block
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False

        while check_proof is False:
            hash_operation = hashlib.sha256(
                str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:5] == '00000':
                check_proof = True
            else:
                new_proof += 1

        return new_proof

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()


# Creating the Web
# App using flask
app = Flask(__name__)

# Create the object
# of the class blockchain
blockchain = Blockchain()

# Mining a new block
@app.route('/transfer', methods=['POST'])
def transfer():
    if "api_key" not in request.json:
        raise APIError('Missing api_key')
    api_key = request.json['api_key']
    if api_key != API_KEY:
        raise APIError('Incorrect api_key')
    if "sender" not in request.json:
        raise APIError('Missing sender username')
    if "senderID" not in request.json:
        raise APIError('Missing sender userID')
    if "receiver" not in request.json:
        raise APIError('Missing receiver username')
    if "amount" not in request.json:
        raise APIError('Missing amount')
    
    sender = request.json['sender']
    senderID = request.json['senderID']
    receiver = request.json['receiver']
    amount = request.json['amount']

    if not str(amount).isdigit():
        raise APIError('Amount should be a positive number')

    block = blockchain.create_block(int(amount), sender, senderID, receiver)

    return jsonify(block), 200

@app.route('/get-chain', methods=['POST'])
def display_chain():
    if "api_key" not in request.json:
        raise APIError('Missing api_key')
    
    api_key = request.json['api_key']
    if api_key != API_KEY:
        raise APIError('Incorrect api_key')
    
    if "username" not in request.json:
        raise APIError('Missing username')
    if "userID" not in request.json:
        raise APIError('Missing userID')
    
    result = blockchain.get_chain(request.json['username'], request.json['userID'])

    return jsonify(result), 200

@app.route('/register', methods=['POST'])
def register():
    if "api_key" not in request.json:
        raise APIError('Missing api_key')
    api_key = request.json['api_key']
    if api_key != API_KEY:
        raise APIError('Incorrect api_key')
    if "username" not in request.json:
        raise APIError('Missing username')
    if "userID" not in request.json:
        raise APIError('Missing userID')
    
    username = str(request.json['username'])
    userID = str(request.json['userID'])
    
    r = requests.post(SERVER + '/api/check-id', json={"userID": userID})

    if (r.json()["result"] == "true"):
        return jsonify(blockchain.register_user(username, userID)), 200
    else:
        raise APIError("userID does not exist")

@app.route('/info', methods=['GET'])
def info():
    response = {'How does this work?': 'Send POST requested to these endpoints. Also include the parameters needed as json.',
                'format': 'endpoint: parameters; description',
                '/info': "; get information on api endpoints",
                '/register': "api_key, username, userID; register a user on the h4xcoin blockchainchain, use your userID from the forums",
                '/transfer': "api_key, sender, senderID, receiver, amount; transfer an amount of h4xcoins from sender to receiver",
                '/get-chain': "api_key, username, userID; get the blockchain of a user",
                '/get-balance': "api_key, username, userID; get the balance of a user"}

    return jsonify(response), 200

@app.route('/get-balance', methods=['POST'])
def balance():
    if "api_key" not in request.json:
        raise APIError('Missing api_key')
    api_key = request.json['api_key']
    if api_key != API_KEY:
        raise APIError('Incorrect api_key')

    if "username" not in request.json:
        raise APIError('Missing username')
    if "userID" not in request.json:
        raise APIError('Missing userID')
    
    result = blockchain.get_balance(request.json['username'], request.json['userID'])

    return jsonify(result), 200

@app.errorhandler(APIError)
def handle_exception(err):
    response = {
      "error": "API error" 
    }
    if len(err.args) > 0:
        response["message"] = err.args[0]
    return jsonify(response), err.code



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, threaded=True)
