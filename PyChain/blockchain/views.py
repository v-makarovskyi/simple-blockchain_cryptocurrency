from django.shortcuts import render
import datetime
import hashlib
import json
from django.http import JsonResponse


class Blockchain:

    def __init__(self) -> None:
        self.chain = []
        self.create_block(nonce=1, previous_hash="0")

    def create_block(self, nonce, previous_hash):
        block = {
            "index": len(self.chain) + 1,
            "timestamp": str(datetime.datetime.now()),
            "nonce": nonce,
            "previous_hash": previous_hash,
        }
        self.chain.append(block)
        return block
    
    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_nonce):
        new_nonce = 1
        check_nonce = False
        
        while check_nonce is False:
            hash_operation = hashlib.sha256(str(new_nonce**2 - previous_nonce**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_nonce = True
            else:
                new_nonce += 1
        return new_nonce
    

    def hash(self, block):
        encoded_block = json.dumps(block, sort_key=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1

        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_nonce = previous_block['nonce']
            nonce = block['nonce']
            hash_operation = hashlib.sha256(str(nonce**2 - previous_nonce**2).encode()).hexdigest()

            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True

blockchain = Blockchain()

def mine_block(request):
    if request.method == 'GET':
        previous_block = blockchain.get_previous_block()
        previous_nonce = previous_block['nonce']
        nonce = blockchain.proof_of_work(previous_nonce)
        previous_hash = blockchain.hash(previous_block)
        block = blockchain.create_block(nonce, previous_hash)
        response = {
            'message': 'Поздравляем! Вы только что создали блок.',
            'index': block['index'],
            'timestamp': block['timestamp'],
            'nonce': block['nonce'],
            'previous_hash': block['previous_hash']
        }
    return JsonResponse(response)