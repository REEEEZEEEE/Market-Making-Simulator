# Terminal Stock Market Simulator

A text-based Python application that simulates a dynamic stock market environment directly within the terminal. Users can interact with a live order book, place market or limit orders, and track their portfolio's net worth over time against algorithmic market activity.

## Features

* **Live Terminal Charting:** Visualizes stock price history directly in the command line using the `plotille` library.

* **Order Book Management:** Features a fully functional matching engine that handles both market and limit orders for buying and selling.

* **Algorithmic Trading Bots:** Simulates market activity using NPC traders whose behavior is influenced by current order book volume imbalances.

* **Portfolio Tracking:** Calculates and displays real-time statistics, including usable cash, held shares (inventory), and total net worth.

* **Dashboard Interface:** Continuously refreshes the terminal output to provide a clean, static dashboard experience.

## Prerequisites

This project requires Python 3.x and the following external dependency:

* `plotille` (for rendering terminal-based graphs)

You can install the required dependency using pip:

```
pip install plotille

```

## Project Structure

Based on the source code, the project is divided into three main components:

* `marketMakingEngine.py` (or your execution script): Contains the primary game loop, handles user input, prints the terminal UI, and coordinates the simulation turns.

* `book.py`: Contains the `Book` class (the market matching engine and price tracker) and the `Player` class (manages user balances, inventory, and order validation).

* `traders.py`: Contains the `generateTrade` function, which creates randomized, algorithmic market activity to simulate a live trading environment.

## Usage

1. Ensure all files (`marketMakingEngine.py`, `book.py`, `traders.py`) are in the same directory.

2. Run the main script from your terminal:

```
python marketMakingEngine.py

```

3. Follow the on-screen prompts to place orders:

   * **Buy/Sell order price:** Enter a specific price for a limit order. Press `Enter` without typing a number to execute a market order at the current price.

   * **Buy/Sell order amount:** Enter the quantity of shares you wish to trade. Enter `0` to skip placing that specific type of order for the current turn.

The simulation advances by one "day" after each round of inputs, updating the chart and your portfolio statistics accordingly.

## Technical Details

* **Market Orders:** Executed immediately against the available liquidity in the order book. Unfilled portions of market orders are discarded.

* **Limit Orders:** Placed onto the order book and executed only when the target price is met by opposing market or limit orders.

* **Imbalance Pricing:** The NPC generation algorithm calculates the ratio of buy volume to sell volume on the book, slightly adjusting the random prices it submits to simulate basic supply and demand mechanics.