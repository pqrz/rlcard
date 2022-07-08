import numpy as np
from rlcard.games.bridge.utils.bridge_card import BridgeCard
from rlcard.games.bridge.utils.action_event import ActionEvent


class HumanAgentBridge(object):
	''' A random agent. Random agents is for running toy examples on the card games
	'''

	def __init__(self, num_actions, verbose=False):
		''' Initilize the random agent

		Args:
			num_actions (int): The size of the ouput action space
		'''
		self.use_raw = False
		self.num_actions = num_actions
		self.verbose = verbose

	#@staticmethod
	def step(self, state):
		''' Predict the action given the curent state in gerenerating training data.

		Args:
			state (dict): An dictionary that represents the current state

		Returns:
			action (int): The action predicted (randomly chosen) by the random agent
		'''
		#legal_actions = list(state['legal_actions'].keys())
		#print()
		#print('Legal actions:')
		#for idx, act in enumerate(legal_actions):
		#	print(f'{idx}. {act}')
		#user_inp = input('Enter your choice: ')
		#return legal_actions[int(user_inp)]
		#return np.random.choice()
		
		#print(state['raw_obs'])
		#import pdb; pdb.set_trace()
		if self.verbose:
			_print_state(state)
		action = int(input('>> You choose action (integer): '))
		while action < 0 or action >= len(state['legal_actions']):
			print('Action illegel...')
			action = int(input('>> Re-choose action (integer): '))
		choice = state['raw_legal_actions'][action]
		if self.verbose:
			print('Final Choice:', choice)
		return choice

	def eval_step(self, state):
		''' Predict the action given the current state for evaluation.
			Since the random agents are not trained. This function is equivalent to step function

		Args:
			state (dict): An dictionary that represents the current state

		Returns:
			action (int): The action predicted (randomly chosen) by the random agent
			probs (list): The list of action probabilities
		'''
		probs = [0 for _ in range(self.num_actions)]
		for i in state['legal_actions']:
			try:
				probs[i-1] = 1/len(state['legal_actions'])
			except:
				import pdb; pdb.set_trace()

		info = {}
		#if i > 36:
		#	import pdb; pdb.set_trace()
		'''
		info['probs'] = {state['raw_legal_actions'][i]: probs[list(state['legal_actions'].keys())[i]-1] 
							for i in range(len(state['legal_actions']))
						}
		'''
		try: 
			info['probs'] = {state['raw_legal_actions'][i]: probs[list(state['legal_actions'].keys())[i]] 
							for i in range(len(state['legal_actions']))
						}
		except:
			import pdb; pdb.set_trace()
		return self.step(state), info


def _print_state(state):
	try:
		l = state['obs']
		l1_hand_rep			  = l[0:208]
		l2_pile_rep			  = l[208:415+1]
		l3_otherplayer_rep	  = l[416:467+1]

		l4_highest_bidder	   = l[468:471+1]
		l5_current_player	  = l[472:475+1]

		l6_bidding_phase	  = l[476:476+1]
		l7_bidding_amount_rep = l[477:620+1]
		l8_last_bid_amt_rep	  = l[621:656+1]

		l9_contract_bid_rep	  = l[657:664+1]
		l10_contract_trump_rep= l[665:]

		suits = ['C', 'D', 'H', 'S']
		ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
		all_cards = [r+s for s in suits for r in ranks]
		print('\n-------------- STATE / Human Agent  --------------')
		#for pid, i in enumerate(range(0, len(l1_hand_rep), 52)):
		print(f'1. Your Hand Rep:	   ', [all_cards[idx%52] for idx, x in enumerate(l1_hand_rep) if x])
		# import pdb; pdb.set_trace()
		print('2. Pile Rep:			   ', [all_cards[idx%52] for idx, x in enumerate(l2_pile_rep) if x])
		print('3. Other Player Rep:	   ', [all_cards[idx] for idx, x in enumerate(l3_otherplayer_rep) if x])
		print('4. Highest Bidder:	   ', l4_highest_bidder)
		print('5. Current Player:	   ', l5_current_player)
		print('6. Is Bidding phase:	   ', l6_bidding_phase)
		print('7. Bidding amount Rep:  ', [idx for idx, x in enumerate(l7_bidding_amount_rep) if x])
		
		'''
		bids = ['7', '8', '9', '10', '11', '12', '13']
		suits = ['C', 'D', 'H', 'S', 'NT']
		all_bid = []
		for p in ['p0', 'p1', 'p2', 'p3']:
			all_bid += [p+'_'+'pass']
			for s in suits:
				for amt in bids:
					all_bid	 += [p+'_'+s+'_'+amt]
		'''
		print('8. Last bid amount rep: ', [idx for idx, x in enumerate(l8_last_bid_amt_rep) if x])
		print('9. Contract Bid rep:	   ', l9_contract_bid_rep)
		print('10. Contract Trump rep: ', l10_contract_trump_rep)
		
		print()
		#print('Possible Legal Actions:', state['legal_actions'])
		print('Possible Legal Actions:', [num_to_name(i) for i, j in state['legal_actions'].items()])
	except:
		import pdb; pdb.set_trace()
		
def num_to_name(action_id):
	#import pdb; pdb.set_trace()
	if ActionEvent.first_bid_action_id <= action_id <= ActionEvent.last_bid_action_id:
		#bid_amount = 7 + (action_id - 1) % 7
		#bid_suit_id = (action_id - 1) // 7

		bid_amount = 7 + (action_id) % 7
		bid_suit_id = (action_id) // 7
		bid_suit = BridgeCard.suits[bid_suit_id] if bid_suit_id < 4 else "nt"               # [c, d, s, h, nt]
		return f'{bid_amount}_{bid_suit}'
	elif action_id==35:
		return 'Pass'
	# If 37 <= action_id <= 88
	elif ActionEvent.first_play_card_action_id <= action_id <= ActionEvent.last_play_card_action_id:
		card_id = action_id - ActionEvent.first_play_card_action_id
		card = BridgeCard.card(card_id=card_id)
		return card
	return ''