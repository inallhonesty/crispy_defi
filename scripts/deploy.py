from scripts.helpful_scripts import get_account
from brownie import MockWETH, GGWPToken, TokenFarm, config, network, interface, Wei
from web3 import Web3
import time

KEPT_BALANCE = Web3.toWei(50000, "ether")

def deploy_token_and_tokenfarm():
    account = get_account()
    gg_token = GGWPToken.deploy({"from": account})
    token_farm = TokenFarm.deploy(gg_token.address, {"from": account})
    tx = gg_token.transfer(token_farm.address, gg_token.totalSupply() - KEPT_BALANCE, {"from": account})
    time.sleep(2)
    tx2 = gg_token.transfer(account.address, KEPT_BALANCE, {"from": account})
    return gg_token, token_farm


    # add_allowed_tokens()


def add_allowed_tokens(token_farm):
    for token in config["networks"][network.show_active()]["tokens"]:
        tx = token_farm.addToApprovedList(config["networks"][network.show_active()]["tokens"][token])
        time.sleep(2)


def deploy_weth_and_fund_acc():
    account = get_account()
    weth_contract = MockWETH.deploy({"from": account})
    time.sleep(1)
    eth_to_convert = Wei("1 ether")
    tx = weth_contract.deposit({"from": account, "value": eth_to_convert})
    time.sleep(1)
    return weth_contract

def main():
    # gg_token, token_farm = deploy_token_and_tokenfarm()
    # add_allowed_tokens(token_farm)
    deploy_weth_and_fund_acc()
    