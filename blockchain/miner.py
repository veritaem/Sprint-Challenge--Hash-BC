import hashlib
import requests
import sys
import json
from uuid import uuid4
from timeit import default_timer as timer
import random

def proof_of_work(last_proof):
    """...AE9123456, new hash 123456888...
    - p is the previous proof, and p' is the new proof
    - Use the same method to generate SHA-256 hashes as the examples in class
    - Note:  We are adding the hash of the last proof to a number/nonce for the new proof"""
    start = timer()
    print("Searching for next proof")
    proof = 200000
    block_string = json.dumps(last_proof, sort_keys=True)
    print(block_string, 'BS')
    while valid_proof(block_string, proof) is False:
        proof += 1
    print("Proof found: " + str(proof) + " in " + str(timer() - start))
    return proof


def valid_proof(last_hash, proof):
    """Validates the Proof:  Multi-ouroborus:  Do the last six characters of
    the hash of the last proof match the first six characters of the proof?
    IE:  last_hash: ...AE9123456, new hash 123456888..."""
    prove_hash = f'{last_hash}'.encode()
    prove_hash = hashlib.sha256(prove_hash).hexdigest()
    guess = f'{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    if guess_hash[:6] == prove_hash[-6:]:
        print(f'{guess_hash[:6]} == {prove_hash[-6:]}')
    return guess_hash[:6] == prove_hash[-6:]


if __name__ == '__main__':
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "https://lambda-coin.herokuapp.com/api"
    coins_mined = 0
    f = open("my_id.txt", "r")
    id = f.read()
    print("ID is", id)
    f.close()
    if id == 'NONAME\n':
        print("ERROR: You must change your name in `my_id.txt`!")
        exit()
    while True:
        # Get the last proof from the server
        r = requests.get(url=node + "/last_proof")
        data = r.json()
        new_proof = proof_of_work(data.get('proof'))
        post_data = {"proof": new_proof,
                    "id": id}
        r = requests.post(url=node + "/mine", json=post_data)
        print(r)
        data = r.json()
        if data.get('message') == 'New Block Forged':
            coins_mined += 1
            print("Total coins mined: " + str(coins_mined))
        else:
            print(data.get('message'))
