'''
    File name: bridge/judger.py
    Author: William Hale
    Date created: 11/25/2021
'''

from typing import List

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .game import BridgeGame

from .utils.action_event import PlayCardAction
from .utils.action_event import ActionEvent, BidAction, PassAction, DblAction, RdblAction
from .utils.move import MakeBidMove, MakeDblMove, MakeRdblMove
from .utils.bridge_card import BridgeCard

'''
Returns all possible legal actions for
    * Bidding phase
    * Card play phase
'''


class BridgeJudger:

    '''
        Judger decides legal actions for current player
    '''

    def __init__(self, game: 'BridgeGame'):
        ''' Initialize the class BridgeJudger
        :param game: BridgeGame
        '''
        self.game: BridgeGame = game

    def get_legal_actions(self) -> List[ActionEvent]:
        """
        :return: List[ActionEvent] of legal actions
        """
        legal_actions: List[ActionEvent] = []
        if not self.game.is_over():
            current_player = self.game.round.get_current_player()
            # 1. If phase = Bidding 
            if not self.game.round.is_bidding_over():
                
                # 1.1 Action = Pass
                legal_actions.append(PassAction())
                
                # 1.2 Action = Bidding (but should be greater then last bidding)
                ##    Steps:
                ##        1.2.1 Find highest bid till now (e.g.last_make_bid_move = 8 )
                last_make_bid_move: MakeBidMove or None = None
                for move in reversed(self.game.round.move_sheet):
                    if isinstance(move, MakeBidMove):
                        last_make_bid_move = move
                        break

                first_bid_action_id = ActionEvent.first_bid_action_id
                
                ##         1.2.2 legal actions = [9, 35]   ............ [last_make_bid_move.action.action_id + 1,   first_bid_action_id + 35]
                next_bid_action_id = last_make_bid_move.action.action_id + 1 if last_make_bid_move else first_bid_action_id
                for bid_action_id in range(next_bid_action_id, first_bid_action_id + 35):
                    action = BidAction.from_action_id(action_id=bid_action_id)
                    legal_actions.append(action)

            # 2. If phase = Card play
            else:
                trick_moves = self.game.round.get_trick_moves()
                hand = self.game.round.players[current_player.player_id].hand
                legal_cards = hand
                if trick_moves and len(trick_moves) < 4:
                    led_card: BridgeCard = trick_moves[0].card
                    cards_of_led_suit = [card for card in hand if card.suit == led_card.suit]
                    if cards_of_led_suit:
                        legal_cards = cards_of_led_suit
                for card in legal_cards:
                    action = PlayCardAction(card=card)
                    legal_actions.append(action)
        return legal_actions
