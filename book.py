class Book:
    def __init__(self):
        self.buyOrders = []
        self.sellOrders = []

        self.priceHistoryDays = [1]
        self.priceHistoryPrice = [100]

        self.price = 100

    def addDay(self):
        next_day = self.priceHistoryDays[-1] + 1
        self.priceHistoryDays.append(next_day)

    def addPrice(self):
        self.priceHistoryPrice.append(self.price)

    def returnPrice(self):
        return self.price

    def returnXY(self):
        return self.priceHistoryDays, self.priceHistoryPrice

    def totalSellVolume(self):
        return sum(order["quant"] for order in self.sellOrders)

    def totalBuyVolume(self):
        return sum(order["quant"] for order in self.buyOrders)

    def newBuyOrder(self, order):

        # MARKET BUY
        if order["price"] is None:

            for trade in self.sellOrders[:]:

                if order["quant"] <= 0:
                    break

                quantity = min(
                    trade["quant"],
                    order["quant"]
                )

                price = trade["price"]

                self.executeTrade(
                    sell=trade,
                    buy=order,
                    price=price,
                    quant=quantity
                )

                trade["quant"] -= quantity
                order["quant"] -= quantity

                if trade["quant"] <= 0:
                    self.sellOrders.remove(trade)

            # Any unfilled market order disappears.
            return

        # LIMIT BUY

        for trade in self.sellOrders[:]:

            if order["quant"] <= 0:
                break

            if trade["price"] <= order["price"]:

                quantity = min(
                    trade["quant"],
                    order["quant"]
                )

                price = trade["price"]

                self.executeTrade(
                    sell=trade,
                    buy=order,
                    price=price,
                    quant=quantity
                )

                trade["quant"] -= quantity
                order["quant"] -= quantity

                if trade["quant"] <= 0:
                    self.sellOrders.remove(trade)

        # Remaining limit order goes onto the book.
        if order["quant"] > 0:

            self.buyOrders.append(order)

            self.buyOrders.sort(
                key=lambda x: x["price"],
                reverse=True
            )

    def newSellOrder(self, order):

        # MARKET SELL
        if order["price"] is None:

            for trade in self.buyOrders[:]:

                if order["quant"] <= 0:
                    break

                quantity = min(
                    trade["quant"],
                    order["quant"]
                )

                price = trade["price"]

                self.executeTrade(
                    sell=order,
                    buy=trade,
                    price=price,
                    quant=quantity
                )

                trade["quant"] -= quantity
                order["quant"] -= quantity

                if trade["quant"] <= 0:
                    self.buyOrders.remove(trade)

            # Any unfilled market order disappears.
            return

        # LIMIT SELL

        for trade in self.buyOrders[:]:

            if order["quant"] <= 0:
                break

            if trade["price"] >= order["price"]:

                quantity = min(
                    trade["quant"],
                    order["quant"]
                )

                price = trade["price"]

                self.executeTrade(
                    sell=order,
                    buy=trade,
                    price=price,
                    quant=quantity
                )

                trade["quant"] -= quantity
                order["quant"] -= quantity

                if trade["quant"] <= 0:
                    self.buyOrders.remove(trade)

        # Remaining limit order goes onto the book.
        if order["quant"] > 0:

            self.sellOrders.append(order)

            self.sellOrders.sort(
                key=lambda x: x["price"]
            )

    def executeTrade(self, sell, buy, price, quant):

        seller = sell["trader"]
        buyer = buy["trader"]

        value = price * quant

        # PLAYER SELLER
        if seller is not None:
            seller.addCash(value)
            seller.addUsableCash(value)
            seller.removeInventory(quant)

        # PLAYER BUYER
        if buyer is not None:
            buyer.removeCash(value)
            buyer.addInventory(quant)
            buyer.addUsableInventory(quant)

        # Last transaction determines market price.
        self.price = price


class Player:

    def __init__(self):
        self.inventory = 0
        self.usableInventory = 0

        self.cash = 100000
        self.usableCash = 100000

        self.activeOrders = []

    def netWorth(self, book):
        return self.cash + self.inventory * book.returnPrice()

    def addCash(self, amount):
        self.cash += amount

    def removeCash(self, amount):
        self.cash -= amount

    def addUsableCash(self, amount):
        self.usableCash += amount

    def addInventory(self, amount):
        self.inventory += amount

    def removeInventory(self, amount):
        self.inventory -= amount

    def addUsableInventory(self, amount):
        self.usableInventory += amount

    def order(self, price, quant, orderType, book):

        if quant <= 0:
            raise ValueError("Quantity must be greater than 0")

        if orderType not in ("buy", "sell"):
            raise ValueError("Order type must be 'buy' or 'sell'")

        # BUY
        if orderType == "buy":

            # Estimate required cash.
            estimatedPrice = (
                book.returnPrice()
                if price is None
                else price
            )

            requiredCash = estimatedPrice * quant

            if self.usableCash < requiredCash:
                return

            # Reserve cash.
            self.usableCash -= requiredCash

        # SELL
        else:

            if self.usableInventory < quant:
                return

            # Reserve shares.
            self.usableInventory -= quant

        order = {
            "price": price,
            "quant": quant,
            "trader": self
        }

        self.activeOrders.append(order)

        if orderType == "buy":
            book.newBuyOrder(order)

        else:
            book.newSellOrder(order)

        return order