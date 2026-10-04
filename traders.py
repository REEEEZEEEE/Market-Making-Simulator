import random


def generateTrade(book):
    """
    Generate a random NPC order.
    """

    price = book.returnPrice()

    # 0 = no trade
    # 1 = buy
    # 2 = sell
    trade_type = random.randint(0, 2)

    if trade_type == 0:
        return False

    if trade_type == 1:
        order_type = "buy"
    else:
        order_type = "sell"

    # 0 = market order
    # 1/2 = limit order
    order_style = random.randint(0, 2)

    quantity = random.randint(10, 50)

    if order_style == 0:

        stock_price = None

    else:

        buy_volume = book.totalBuyVolume()
        sell_volume = book.totalSellVolume()

        imbalance = (
            (buy_volume + 1)
            / (buy_volume + sell_volume + 1)
        )

        if order_type == "buy":

            stock_price = (
                price
                - round(random.random(), 2)
                + round(imbalance, 2)
            )

        else:

            imbalance = (
                (sell_volume + 1)
                / (buy_volume + sell_volume + 1)
            )

            stock_price = (
                price
                + round(random.random(), 2)
                - round(imbalance, 2)
            )

        # Don't allow zero/negative prices.
        stock_price = max(0.01, round(stock_price, 2))

    order = {
        "price": stock_price,
        "quant": quantity,
        "trader": None
    }

    if order_type == "buy":
        book.newBuyOrder(order)
    else:
        book.newSellOrder(order)

    return order