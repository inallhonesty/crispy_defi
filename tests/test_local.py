from brownie import accounts, network, config, exceptions
from scripts.deploy import deploy_token_and_tokenfarm, add_allowed_tokens, KEPT_BALANCE, deploy_weth_and_fund_acc
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
)
from web3 import Web3
import pytest, time



def test_deploy_and_initial_balance():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Arrange
    account = get_account()
    gg_token, token_farm = deploy_token_and_tokenfarm()
    # Act
    expected_contract_balance = gg_token.balanceOf(token_farm.address)
    expected_account_balance = gg_token.balanceOf(account.address)
    # Assert
    assert expected_contract_balance == 1 * 10 ** 6 * 10 ** 18 - KEPT_BALANCE
    assert expected_account_balance == KEPT_BALANCE


def test_add_approved_tokens():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Arrange
    weth_token = config["networks"][network.show_active()]["tokens"]["weth_token"]
    account = get_account()
    gg_token, token_farm = deploy_token_and_tokenfarm()
    # Act
    add_allowed_tokens(token_farm)
    expect_token_is_allowed = token_farm.tokenIsAllowed(weth_token)
    # Assert
    assert expect_token_is_allowed == True

def test_staking():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Arrange
    amount = 10 ** 10
    # weth_token = config["networks"][network.show_active()]["tokens"]["weth_token"]
    account = get_account()
    gg_token, token_farm = deploy_token_and_tokenfarm()
    weth_contract = deploy_weth_and_fund_acc()
    approve_weth = token_farm.addToApprovedList(weth_contract.address, {"from": account})
    time.sleep(1)
    print(token_farm.tokenIsAllowed(weth_contract.address))
    print(weth_contract.balanceOf(account))
    # Act
    stake_tx = token_farm.stakeTokens(amount, weth_contract.address, {"from": account})
    time.sleep(2)
    registered_staked = token_farm.stakingBalance[weth_contract.address][account.address]
    time.sleep(2)
    # Assert
    assert amount == registered_staked

    #Trebuie aprobat transferul intern   approve(address guy, uint wad)