import hashlib
import json
from fastecdsa import ecdsa, keys, curve, point

"""
double spend is still wrong
find balance
balance calculations wrong
"""

class ScroogeCoin(object):
	def __init__(self):
		self.private_key, self.public_key = self.KeyGen() # MUST USE secp256k1 curve from fastecdsa
		self.address =  self.get_addr([bytes(bin(self.public_key.x)[2:],'utf-8'),
						bytes(bin(self.public_key.y)[2:],'utf-8')]) # create the address using public key, and bitwise operation, may need hex(value).hexdigest()
		self.chain = [] # list of all the blocks
		self.current_transactions = [] # list of all the current transactions creating a block, the scrooge will keep up with the transactions
		self.senders = []


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

	def get_user_tx_positions(self, address):
		"""
		Scrooge adds value to some coins
		:param address: User.address
		:return: list of all transactions where address is funded
		[{"block":block_num, "tx":tx_num, "amount":amount}, ...]
		"""
		funded_transactions = []
		tx_index = 0
		for block in self.chain:
			for old_tx in block["transactions"]:
				for funded, amount in old_tx["receivers"].items():
					if address == funded:
						funded_transactions.append({"block":block["index"], "tx":tx_index, "amount":amount})
						tx_index += 1

		return funded_transactions

	def validate_tx(self, tx, public_key):
		"""
		validates a single transaction

		:param tx = {
			"sender" : User.address,
				## a list of locations of previous transactions
				## look at
			"locations" : [{"block":block_num, "tx":tx_num, "amount":amount}, ...],
			"receivers" : {account:amount, account:amount, ...}
		}

		:param public_key: User.public_key

		:return: if tx is valid return tx
		"""
		is_correct_hash = False
		is_signed = False
		is_funded = False
		is_all_spent = False
		consumed_previous = False


		# Check for equal value
		balance = self.show_user_balance(tx['sender'], False)     #returns balance without printing
		sent_amt = 0
		remain_amt = 0
		# get len of previous trans to index final balance
		for usr, amount in tx['receivers'].items():
			# Check for consumed coins amount
			if usr == tx['sender']:
				remain_amt = amount
			else:
				sent_amt = amount

		# save remaining amount and sender address to senders to check for double spend
		remain_coins = {}
		remain_coins['sender'] = tx['sender']
		remain_coins['amount'] = remain_amt
		self.senders.append(remain_coins)

		# iterate through senders list and check for double spend
		# if sender is present with the same remaining balance twice in the same
		# block, it is a double spend 
		dup_test = []
		for i in self.senders:
			if i in dup_test:
				consumed_previous = True
			else:
				dup_test.append(i)


		# print('Balance :', balance)
		# print('last_location :', tx['locations'][num_trans-1]['amount'])
		#print('consumed coins : ', consumed_coins)

		if balance == remain_amt+sent_amt:
			is_all_spent=True
		# Check if consumed coins are valid

		# Check current balance
		if balance >= 0:
			is_funded = True


		test_hash = ['sender', 'locations', 'receivers']
		temp_tx = {}
		for item in test_hash:
			temp_tx[item] = tx[item]
		test_tx = self.hash(temp_tx)
		if test_tx == tx['hash']:
			is_correct_hash = True

		is_signed = ecdsa.verify(tx['signature'],tx['hash'],
			                    public_key,curve=curve.secp256k1,
			                    hashfunc=hashlib.sha256)

		# # print the errors
		if is_signed is not True:
			print('Invalid signature!!!')
		elif is_correct_hash  is not True:
			print("The hash is not valid!!")
		elif is_funded is not True:
			print('No balance!!!')
		elif is_all_spent is not True:
			print('Not all coins are spent!!!')
		elif consumed_previous is True:
			print('Invalid double spend!!!')

		if (is_correct_hash and is_signed and is_funded and is_all_spent and not consumed_previous):
			return tx


	def mine(self):
		"""
		mines a new block onto the chain
		"""
		prev_hash = ''
		try:
			prev_hash = self.chain[-1].get("hash")
		except IndexError:
			prev_hash = "0"*64     # Genesis block, very fist hash is just 64 0's

		block = {
			'previous_hash': prev_hash,# previous_hash,
			'index': len(self.chain), # index,
			'transactions': self.current_transactions,# transactions,
		}
		# hash and sign the block
		block["hash"] = self.hash(block)# hash of block
		block["signature"] = self.sign(block["hash"]) # signed hash of block

		self.chain.append(block)
		self.current_transactions = []
		self.senders = []

		return block

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
		tx_val = False
		validate = self.validate_tx(tx,public_key)
	
		if validate is None:
			print('Invalid Transaction')
		else:
			tx_val = True
			self.current_transactions.append(validate)

		return tx_val
		



	def show_user_balance(self, address, p):
		"""
		prints balance of address
		:param address: User.address
		"""
		# # Check for equal value
		# sent_amt = 0
		# remain_amt = 0
		# for usr, amount in tx['receivers'].items():
		# 	# Check for consumed coins amount
		# 	if usr == tx['sender']:
		# 		remain_amt = amount
		# 	else:
		# 		sent_amt = amount
		# 	if amount > 0 :
		# 		balance+= amount
		# print('address : ', address, '\n')
		tx_index = 0
		bal_lst = []
		start_bal = self.chain[0]["transactions"][0]['receivers'][address]
		bal = start_bal
		# print("start_bal : ", start_bal)
		for block in self.chain:
			for old_tx in block["transactions"]:
				sender = block['transactions'][0]['sender']
				# Skip first transaction, since its just creating coins
				if tx_index > 0:
					for funded, amount in old_tx["receivers"].items():
						# print("funded : ", funded, "amount : ", amount)
						if sender == funded == address:
							# print("this the new amount")
							#print("funded : ", funded, "amount : ", amount)
							bal = amount
						elif address == funded != sender:
							bal = bal+amount
				else:
					pass
				tx_index += 1
		if p is True:
			print("%s's balance is : %s"%(address, bal))
		return bal
				#print("index: ", tx_index)	
		# print(bal_lst)
		# balance = bal_lst[0]
		# i = 0
		# while len(bal_lst)>i:
		# 	print('index : ', i)
		# 	print(bal_lst[i])
		# 	print(balance)
		# 	try:
		# 		if bal_lst[i-1]>balance:
		# 			balance = balance - bal_lst[i]
		# 		else:
		# 			balance = bal_lst[i]+bal_lst[i-1]
		# 	except IndexError:
		# 		if bal_lst[0]>balance:
		# 			balance = balance - bal_lst[i]
		# 		else:
		# 			balance = bal_lst[i]+bal_lst[0]
		# 	i+=1
		#print("the balance is : ", balance)


	def show_block(self, block_num):
		"""
		prints out a single formated block
		:param block_num: index of the block to be printed
		"""
		b = self.chain[block_num]
		formatted_block = str("Index: %s\n\nHash:"+
			                  " %s\n\nPrevious hash:"+
			                  " %s\n\nTransactions:"+
			                  " %s\n\nSignature: %s\n\n")%(
			                  b["index"], b["hash"],
			                   b["previous_hash"], 
			                   b["transactions"], 
			                   b["signature"])
		print(formatted_block)

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
		addr = m.hexdigest()    #add x and y to hash and concatenate:20, users[3].address:50})
		
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
	Scrooge.mine()
	
	user_0_tx_locations = Scrooge.get_user_tx_positions(users[0].address)
	first_tx = users[0].send_tx({users[1].address: 2, users[0].address:8}, user_0_tx_locations)
	Scrooge.add_tx(first_tx, users[0].public_key)
	Scrooge.mine()
	#print(Scrooge.get_user_tx_positions(users[1].address))

	second_tx = users[1].send_tx({users[0].address:20, users[1].address:2}, Scrooge.get_user_tx_positions(users[1].address))
	user_0_tx_locations = Scrooge.get_user_tx_positions(users[0].address)
	second_tx = users[0].send_tx({users[1].address: 2, users[0].address:6}, user_0_tx_locations)
	Scrooge.add_tx(second_tx, users[0].public_key)
	Scrooge.mine()
	#print(Scrooge.get_user_tx_positions(users[1].address))

	user_0_tx_locations = Scrooge.get_user_tx_positions(users[0].address)
	third_tx = users[0].send_tx({users[1].address: 2, users[0].address:4}, user_0_tx_locations)
	Scrooge.add_tx(third_tx, users[0].public_key)
	Scrooge.mine()
	# usr_1_tx_locations = Scrooge.get_user_tx_positions(users[1].address)
	# print(usr_1_tx_locations)
	# print(user_0_tx_locations)
	# print(Scrooge.get_user_tx_positions(users[1].address))
	#Scrooge.show_user_balance(users[1].address)

	# Scrooge.create_coins({users[0].address:10, users[1].address:20, users[3].address:50})
	# Scrooge.mine()


	# Scrooge.show_block(0)
	# Scrooge.show_block(1)
	# Scrooge.show_block(2)
	# Scrooge.show_block(3)
	# Scrooge.show_block(4)

	Scrooge.show_user_balance(users[0].address,True)

	#Scrooge.get_user_tx_positions(users[1].address)
	#Scrooge.get_user_tx_positions(users[0].address)

	#Scrooge.show_user_balance(users[0].address)


if __name__ == '__main__':
   main()
