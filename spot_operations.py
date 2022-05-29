from binance.client import Client


def spot_balance(client=Client()):
    info = client.get_account()
    answer = ''
    for i in info["balances"]:
        if float(i["free"]) + float(i["locked"]) > 0:
            answer += f'{i["asset"]}: free {i["free"]}, locked {i["locked"]}\n'

    return answer


def get_spot_asset(asset, client=Client()):
    info = client.get_asset_balance(asset)
    asset_message = f'{info["asset"]}: free {info["free"]}, locked {info["locked"]}'
    return asset_message
