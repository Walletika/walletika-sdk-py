import os
import json


TOKEN_ABI_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'token.json'
)
STAKE_ABI_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'stake.json'
)
WNS_ABI_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'wns.json'
)


with open(TOKEN_ABI_PATH) as file:
    tokenABI = json.load(file)


with open(STAKE_ABI_PATH) as file:
    stakeABI = json.load(file)


with open(WNS_ABI_PATH) as file:
    wnsABI = json.load(file)


__all__ = ['TOKEN_ABI_PATH', 'STAKE_ABI_PATH', 'WNS_ABI_PATH', 'tokenABI', 'stakeABI', 'wnsABI']
