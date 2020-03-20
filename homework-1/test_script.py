import hashlib
import json
from time import sleep
from fastecdsa import ecdsa, keys, curve, point


#create mock get_usr_trans

#prev_funds = [{"block":0, "tx":0, "amount":10}] 
"""

spent = False
wallet_amount = 0
for coins in tx['locations']:
	wallet_amount += coins['amount']
print(wallet_amount)
print(wallet_amount - tx['receivers'][address])
"""
"""
tx_receivers = tx['receivers']
t_amount = 0
num_trans = len(tx['locations'])
for r, amount in tx_receivers.items():
	if amount >0:
		t_amount += amount
if t_amount == tx['locations'][num_trans-1]['amount']:
	spent = True

if spent is True:
	print("valid")
else:
	print("try again fam")
"""
"""
is_funded = False
if len(prev_funds) !=0:
	is_funded = True
else:
	print("Broke Bitch")
if is_funded is True:
	print("yuhh")
"""
"""
for usr,amount in tx['receivers'].items():
	print(usr, " ", amount)
	if usr == 'usr_0':
		pass
	else:
		consumed_coins = amount
	print(consumed_coins)
"""
def get_addr(pub):

		m = hashlib.sha256()
		for i in pub:
			m.update(i)
		addr = m.hexdigest()    #add x and y to hash and concatenate

		return addr

def test_valid(tx):

	if tx['sender'] == 'usr_0' and tx['hash'] == 'itsasecret':
		return tx
def sign(private_key, hash_):
		return ecdsa.sign(msg=hash_, 
		d=private_key,
		curve=curve.secp256k1,
		hashfunc=hashlib.sha256)


if __name__ == '__main__':

	# create mock tx
	"""
	public_key = {"X": 0xdc6de65763431bfe1b9a6fe03622b125fb5ccab08a883a076c2590150bdd8fe4,"Y": 0xfc38ff4f5b5b217b6a5d68e8ad526ec08cc79b10fb9c8dbbf2c0850a72e6b9c2}
	test_key = get_addr([bytes(bin(public_key['X'])[2:],'utf-8'),bytes(bin(public_key['Y'])[2:],'utf-8')])
	tx = {
		"sender" : "f42d934470c3ed83844968e92f59fc26d41353a9a5e35f7bc2d61228e74f95f5",
		"locations" : [{"block":0, "tx":0, "amount":10},{"block":1, "tx":3, "amount":11}],
		"receivers" : {"usr_1":3,"usr_0":8},
	}
	tx["hash"] = "itsasecret"
	tx["signature"] = "Zachy B"

	check = test_valid(tx)
	if test_key != tx['sender']:
		print('Consumed True')
	else:
		print('Consumed False')
	"""
	# test_hash = '507363fe1a5d39545ef4a69ebeacbe6498fc789f0e09ac659768a3fae17ec50e'
	# (priv, pub) = keys.gen_keypair(curve.secp256k1)
	# print(priv)
	# print(pub)


	# test_1 = sign(priv,test_hash)
	# sleep(1)
	# test_2 = sign(priv, test_hash)
	# print(test_1, '\n', test_2)

	senders = [{'sender': '79793f5077d3ed48006b78d248728463a54e138496d376caad89dec13d544da3', 'amount': 8},{'sender': '79793f5077d3ed48006b78d248728463a54e138496d376caad89dec13d544da3', 'amount': 8}]
	r = []
	for i in senders:
		if i in r:
			print("double spend!!!")
		else:
			r.append(i)