import hashlib
import json
from fastecdsa import ecdsa, keys, curve, point


# create mock tx
address = 'usr_0'
tx = {
	"sender" : "usr_0",
	"locations" : [{"block":0, "tx":0, "amount":10},{"block":1, "tx":3, "amount":11}],
	"receivers" : {"usr_1":3,"usr_0":8},
}
tx["hash"] = "itsasecret"
tx["signature"] = "Zachy B"

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
build_hash = ['sender', 'locations', 'receivers']
print(tx['hash'])
test_tx = {}
for item in build_hash:
	test_tx[item] = tx[item]
print(test_tx)
