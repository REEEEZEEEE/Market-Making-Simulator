import plotille
import sys

from book import Book, Player
from traders import generateTrade


# Create the market.
book = Book()
player = Player()


print(r"""
    $$$$$$$\  $$\                           
    $$  __$$\ $$ |                          
    $$ |  $$ |$$$$$$$\  $$\   $$\  $$$$$$$\ 
    $$$$$$$  |$$  __$$\ $$ |  $$ |$$  _____|
    $$  __$$< $$ |  $$ |$$ |  $$ |\$$$$$$\  
    $$ |  $$ |$$ |  $$ |$$ |  $$ | \____$$\ 
    $$ |  $$ |$$ |  $$ |\$$$$$$$ |$$$$$$$  |
    \__|  \__|\__|  \__| \____$$ |\_______/ 
                        $$\   $$ |          
                        \$$$$$$  |          
                        \______/           
      """)

while True:

    # Generate random market activity.
    for _ in range(15):
        generateTrade(book)

    print(
        f"You have ${player.usableCash:.2f} usable."
    )

    print(
        f"You have {player.inventory} shares."
    )

    print(
        f"Current Price is ${book.returnPrice():.2f}"
    )

    print(
        f"Your net worth is "
        f"${player.netWorth(book):.2f}"
    )

    # Display price chart.
    x, y = book.returnXY()

    print(
        plotille.plot(
            x,
            y,
            height=15,
            width=60
        )
    )

    try:

        order = input(
            "Buy order price "
            "(press Enter for market): "
        )

        quant = input(
            "Buy order amount "
            "(0 to skip): "
        )

        order2 = input(
            "Sell order price "
            "(press Enter for market): "
        )

        quant2 = input(
            "Sell order amount "
            "(0 to skip): "
        )

        # Advance simulation day.
        book.addDay()
        book.addPrice()

        # BUY
        if quant.strip() != "":

            buy_quantity = int(quant)

            if buy_quantity > 0:

                if order.strip() == "":
                    buy_price = None
                else:
                    buy_price = float(order)

                player.order(
                    buy_price,
                    buy_quantity,
                    "buy",
                    book
                )

        # SELL
        if quant2.strip() != "":

            sell_quantity = int(quant2)

            if sell_quantity > 0:

                if order2.strip() == "":
                    sell_price = None
                else:
                    sell_price = float(order2)

                player.order(
                    sell_price,
                    sell_quantity,
                    "sell",
                    book
                )

    except ValueError as e:

        print(f"Invalid order: {e}")

        input("Press Enter to continue...")

    # Move the terminal output up.
    for _ in range(27):
        sys.stdout.write("\x1b[1A")
        sys.stdout.write("\x1b[2K")

    sys.stdout.flush()
    