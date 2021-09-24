from brownie import accounts, config, network, MockV3Aggregator
# from web3 import Web3

DECIMALS = 8
STARTING_PRICE = 200000000000
LOCAL_BLOCKCHAIN_ENVIRONMENTS = [
  "development",
  "ganache-local"
]
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork-dev"]


def get_account():
  if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS or network.show_active() in FORKED_LOCAL_ENVIRONMENTS:
    return accounts[0]
  else:
    return accounts.add(config["wallets"]["from_key"])


def deploy_mocks():
    print("The active network is {}".format(network.show_active()))
    print("Deploying Mocks...")

    # Remember we can check the length of MockV3Aggregator to see if we've already deployed this contract
    if len(MockV3Aggregator) <= 0:
      # MockV3Agreggator constructor arguments _decimals, _initialAnswer
      # MockV3Aggregator.deploy(DECIMALS, Web3.toWei(STARTING_PRICE, "ether"), {"from": get_account()})
       MockV3Aggregator.deploy(DECIMALS, STARTING_PRICE, {"from": get_account()})

    print("Mocks Deployed...")
