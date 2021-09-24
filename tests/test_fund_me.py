from brownie import network, accounts, exceptions
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
from scripts.deploy import deploy_fund_me
import pytest

def test_can_fund_and_withdraw():
  account = get_account()
  fund_me = deploy_fund_me()
  entrance_fee = fund_me.getEntranceFee() + 100 # Add 100 just in case we need a little bit more fee

  tx = fund_me.fund({"from": account, "value": entrance_fee})
  tx.wait(1)

  # Check the amount funded against the amount at account.address
  assert fund_me.addressToAmountFunded(account.address) == entrance_fee

  tx2 = fund_me.withdraw({"from": account})
  tx2.wait(1)

  assert fund_me.addressToAmountFunded(account.address) == 0

def test_only_owner_can_withdraw():
  if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
    pytest.skip("only for local testing")

  account = get_account()
  fund_me = deploy_fund_me()

  # Gives us random account
  bad_actor = accounts.add()

  # Tells our test that if withdraw() reverts, then its expected result
  with pytest.raises(exceptions.VirtualMachineError):
    fund_me.withdraw({"from": bad_actor})
