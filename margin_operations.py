from binance.client import Client


def isolated_margin_balance(client=Client()):
    info = client.get_isolated_margin_account()
    pair_info = ''
    for i in info['assets']:

        if float(i["baseAsset"]["totalAsset"]) + float(i["quoteAsset"]["totalAsset"]) == 0:
            continue

        symbol1 = str(i['baseAsset']['asset']) + 'USDT'
        symbol2 = str(i['quoteAsset']['asset']) + 'USDT'

        if symbol1 != 'USDTUSDT':
            price1 = float(i["baseAsset"]["totalAsset"]) * float(client.get_margin_price_index(symbol=symbol1)['price'])
            borrow_price1= float(i["baseAsset"]["borrowed"]) * float(client.get_margin_price_index(symbol=symbol1)['price'])
        else:
            price1 = float(i["baseAsset"]["totalAsset"])
            borrow_price1 = float(i["baseAsset"]["borrowed"])

        if symbol2 != 'USDTUSDT':
            price2 = float(i["quoteAsset"]["totalAsset"]) * float(client.get_margin_price_index(symbol=symbol2)['price'])
            borrow_price2 = float(i["quoteAsset"]["borrowed"]) * float(
                client.get_margin_price_index(symbol=symbol2)['price'])
        else:
            price2 = float(i["quoteAsset"]["totalAsset"])
            borrow_price2 = float(i["quoteAsset"]["borrowed"])

        worth = price1 + price2
        personal_money = worth - borrow_price1 - borrow_price2
        total_borrowed = borrow_price1 + borrow_price2

        pair_info += i['baseAsset']['asset'] + i['quoteAsset']['asset'] + '. '
        pair_info += f'Current balance: {i["baseAsset"]["totalAsset"]} {i["baseAsset"]["asset"]}, {i["quoteAsset"]["totalAsset"]} {i["quoteAsset"]["asset"]}. '
        pair_info += f'Total worth: {format(worth, ".2f")} USD. '
        pair_info += f'Borrowed: {i["baseAsset"]["borrowed"]} {i["baseAsset"]["asset"]}, {i["quoteAsset"]["borrowed"]} {i["quoteAsset"]["asset"]}. Total borrowed {format(total_borrowed, ".2f")} USDT. '
        pair_info += f'Personal money: {format(personal_money, ".2f")} USD.\n\n'

    pair_info = pair_info[:-1]  # убрал лишний \n
    return pair_info

