from ddcmaker.maker.human_hand.actions import normal
from ddcmaker.maker.human_hand.hand import Hand
from ddcmaker.maker.human_hand.actions.ai import AI_FEATURES


def init():
    normal_hand = Hand()
    normal_hand.run_action(normal.init_body)
