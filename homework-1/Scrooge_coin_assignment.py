import hashlib
import json
from fastecdsa import ecdsa, keys, curve, point


class ScroogeCoin(object):
    def __init__(self):
        self.private_key, self.public_key = self.KeyGen() # MUST USE secp256k1 curve from fastecdsa
        self.address =  self.get_addr([bytes(bin(self.public_key.x)[2:],'utf-8'),
                        bytes(bin(self.public_key.y)[2:],'utf-8')]) # create the address using public key, and bitwise operation, may need hex(value).hexdigest()
        self.chain = [] # list of all the blocks
        self.current_transactions = [] # list of all the current transactions creating a block, the scrooge will keep up with the transactions

    def KeyGen(self):
        return keys.gen_keypair(curve.secp256k1)

    
    def create_coins(self, receivers: dict):
        """
        Scrooge adds value to some coins
        :param receivers: {account:amount, account:amount, ...}
        """
        
        tx = {
            "sender" :self.address, # address,
            # coins that are created do not come from anywhere
            #TODO: the value for block, tx, and amount should correspond to the transaction number?
            "locations": {"block": -1, "tx": -1, "amount":-1},
            "receivers" : receivers,
        }
        tx["hash"] = self.hash(tx)# hash of tx, sends an ordered dictionary to has funciton
        tx["signature"] = self.sign(tx["hash"]) # signed hash of tx


        self.current_transactions.append(tx)
        print(self.public_key, '\n\n')

        print(tx)


    def hash(self, blob):
        """
        Creates a SHA-256 hash of a Block
        iterates through dictionary and concatenates together to create hash
        :param block: Block
        """
        h = hashlib.sha256()
        h.update(json.dumps(blob, sort_keys=True).encode())

        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        # use json.dumps().encode() and specify the corrent parameters
        # use hashlib to hash the output of json.dumps()
        return h.hexdigest()


    def get_addr(self, pub):

        m = hashlib.sha256()
        for i in pub:
            m.update(i)
        addr = m.hexdigest()    #add x and y to hash and concatenate

        return addr
        


    def sign(self, hash_):
        return ecdsa.sign(msg=hash_, 
        d=self.private_key,
        curve=curve.secp256k1,
        hashfunc=hashlib.sha256)# use fastecdsa library

    def add_tx(self, tx, public_key):
        """
        checks that tx is valid
        adds tx to current_transactions
        

        :param tx = {
            "sender" : User.address,
                ## a list of locations of previous transactions
                ## look at 
            "locations" : [{"block":block_num, "tx":tx_num, "amount":amount}, ...], 
            "receivers" : {account:amount, account:amount, ...}
        }


        
        :param public_key: User.public_key
        :return: True if the tx is added to current_transactions
        """
        self.current_transactions.append(tx)


class User(object):
    def __init__(self):
        self.private_key, self.public_key = self.KeyGen()# MUST USE secp256k1 curve from fastecdsa
        self.address = self.get_addr([bytes(bin(self.public_key.x)[2:],'utf-8'),
                        bytes(bin(self.public_key.y)[2:],'utf-8')])
    def KeyGen(self):
        return keys.gen_keypair(curve.secp256k1)

    def hash(self, blob):
        """
        Creates a SHA-256 hash of a Block
        :param block: Block
        :return: the hash of the blob
        """
        h = hashlib.sha256()
        h.update(json.dumps(blob, sort_keys=True).encode())

        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        # use json.dumps().encode() and specify the corrent parameters
        # use hashlib to hash the output of json.dumps()
        return h.hexdigest()   # hash_of_blob

    def get_addr(self, pub):

        m = hashlib.sha256()
        for i in pub:
            m.update(i)
        addr = m.hexdigest()    #add x and y to hash and concatenate

        return addr

    def sign(self, hash_):
        return ecdsa.sign(msg=hash_, 
        d=self.private_key,
        curve=curve.secp256k1,
        hashfunc=hashlib.sha256)# use fastecdsa library

    def send_tx(self, receivers, previous_tx_locations):
        """
        creates a TX to be sent
        :param receivers: {account:amount, account:amount, ...}
        :param previous_tx_locations 
        """

        tx = {
                "sender" : self.address,  # address,
                "locations" : previous_tx_locations,
                "receivers" : receivers 
            }

        tx["hash"] = self.hash(tx)# hash of TX
        tx["signature"] = self.sign(tx["hash"])# signed hash of TX

        return tx
     



def main():

    # dict - defined using {key:value, key:value, ...} or dict[key] = value
        # they are used in this code for blocks, transactions, and receivers
        # can be interated through using dict.items()
        # https://docs.python.org/3/tutorial/datastructures.html#dictionaries

    # lists -defined using [item, item, item] or list.append(item) as well as other ways
        # used to hold lists of blocks aka the blockchain
        # https://docs.python.org/3/tutorial/datastructures.html#more-on-lists

    # fastecdsa - https://pypi.org/project/fastecdsa/
    # hashlib - https://docs.python.org/3/library/hashlib.html
    # json - https://docs.python.org/3/library/json.html

    # Example of how the code will be run
    Scrooge = ScroogeCoin()
    users = [User() for i in range(10)]
    Scrooge.create_coins({users[0].address:10, users[1].address:20, users[3].address:50})


if __name__ == '__main__':
   main()
    