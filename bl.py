from bitkub import Bitkub
import os
import requests
from dotenv import load_dotenv

load_dotenv()

url = os.environ.get('DATAAPIURL')

# initial obj non-secure and secure
bitkub = Bitkub(api_key=os.environ.get('KEY'),
                api_secret=os.environ.get('SECRET'))


def GetPrice(name):
    result = bitkub.ticker(sym=name)
    price = float(result[name]['last'])
    return price


def GetMyBalances():
    return bitkub.balances()


def GetMyWallet():
    return bitkub.wallet()


def GetMyOrder(name):
    return bitkub.my_open_orders(name)


def CancelOrder(hash):
    result = bitkub.cancel_order(hash=hash)
    return float(result['error'])


def SellOrder(name, amt, rat):
    result = bitkub.place_ask(sym=name, amt=amt, rat=rat, typ='limit')
    return float(result['error'])


def BuyOrder(name, amt, rat):
    result = bitkub.place_bid(sym=name, amt=amt, rat=rat, typ='limit')
    return float(result['error'])


def Authenticate(user, password):
    res = requests.post(
        url + '/user', json={'UserName': user, 'PassWord': password})
    data = res.json()
    return data


def Trading(name):
    # Get Target Price,Trade
    targetprofit = 2
    targetlost = 4
    profitcal = 0
    targetname = 'THB_' + name
    latestprice = GetPrice(targetname)
    print(f'{targetname} Lastest price = {latestprice}')
    rate = latestprice - 2
    print(f'Rate = {rate}')
    # Get MyWallet
    wallet = GetMyWallet()
    amt = float(wallet['result'][name])
    print(f'{targetname} in my wallet amount = {amt}')
    balance = float(wallet['result']['THB'])
    print(f'My wallet THB balance = {balance}')

    # CalProfit
    if(amt > 0):
        profitcal = latestprice + targetprofit
        print(f'ProfitCal = {profitcal}')
    # Get Pending Order
    orders = GetMyOrder(targetname)
    print(f'My pending order = {orders}')
    if(any(orders['result'])):
        for order in orders['result']:
            hashkey = order['hash']
            orderRate = float(order['rate'])
            ordertype = order['side']
            profitcal = (orderRate*targetprofit) / 100
            diff = orderRate - latestprice
            print(f'ProfitCal = {profitcal} Different = {diff}')
            if(ordertype == 'SELL'):
                if(diff >= targetprofit):
                    # Cancel Order
                    CancelOrder(hashkey)
                    print(f'Order {hashkey} Was Cancel Sell')
            if(ordertype == 'BUY'):
                if(diff <= targetlost):
                    # Cancel Order
                    CancelOrder(hashkey)
                    print(f'Order {hashkey} Was Cancel Buy')

    # balance > 0 place order
    if(balance > 0):
        BuyOrder(targetname, balance, rate)
        print(f'Create Buy Order with rate = {rate} balance = {balance}')
    elif (not orders['result']):
        # Create SELL Order
        SellOrder(targetname, amt, profitcal)
        requests.post(
            url+'/insertcryptohistory', json={"CryptoName": name,
                                              "Amt": amt,
                                              "Rate": profitcal})
        print(f'Create Sell Order with rate = {profitcal} balance = {balance}')
    return "OK"
