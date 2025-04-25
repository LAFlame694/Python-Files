from binance.client import Client
import numpy as np
import time
import requests
import logging
import smtplib
from email.message import EmailMessage
from decimal import Decimal, ROUND_DOWN
import os
from dotenv import load_dotenv
from binance.exceptions import BinanceAPIException
from datetime import datetime, timedelta

# === Load environment variables ===
load_dotenv()

API_KEY = os.getenv('BINANCE_API_KEY')
SECRET_KEY = os.getenv('BINANCE_SECRET_KEY')
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

# === Validation Step: Ensure all credentials are loaded ===
if not API_KEY or not SECRET_KEY:
    raise ValueError("⚠️ Binance API key and/or secret key are not set in the environment variables. Exiting...")

if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
    raise ValueError("⚠️ Email credentials are not set in the environment variables. Exiting...")

# === Global variables for Trading Signal Cooldown ===
last_buy_time = None
last_sell_time = None
trade_cooldown = timedelta(minutes=5) # Cooldown period for trades (e.g., 5 minutes)

# === Global variables for Email alerts cooldown ===
last_buy_alert_time = None
last_sell_alert_time = None
alert_cooldown = timedelta(minutes = 15) # Cooldown period for email alerts (15 minutes)

# === Email Alerts ===
def send_email(subject, body, signal_type):
    global last_buy_alert_time, last_sell_alert_time

    now = datetime.now()

    # check cooldown for buy or sell signals
    if signal_type == "buy":
        if last_buy_alert_time and now - last_buy_alert_time < alert_cooldown:
            print("⚠️ Buy alert skipped due to cooldown.")
            logging.info("Buy alert skipped due to cooldown.")
            return
        last_buy_alert_time = now

    elif signal_type == "sell":
        if last_sell_alert_time and now - last_sell_alert_time < alert_cooldown:
            print("⚠️ Sell alert skipped due to cooldown.")
            logging.info("Sell alert skipped due to cooldown.")
            return
        last_sell_alert_time = now

    # Prepare and send the email
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS
    msg.set_content(body)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print(f"Email alert sent: {subject}")
        logging.info(f"Email alert sent: {subject}")

    except Exception as e:
        print(f"⚠️ Failed to send email: {e}")
        logging.error(f"Failed to send email: {e}")

# === ✅ Configure logging ===
logging.basicConfig(
    filename="trading_bot_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

try:
    client = Client(API_KEY, SECRET_KEY)
    client.API_URL = "https://testnet.binance.vision/api"
    print("Binance connection established.")
    logging.info("Binance connection established.")
except requests.exceptions.ConnectionError:
    print("⚠️ No internet connection. Binance API not available.")
    logging.warning("No internet connection. Binance API not available.")
    client = None

# === trading pairs ===
symbols = ["ETHUSDT", "BTCUSDT", "BNBUSDT"]

risk_percent = 0.01 # 1% of balance
min_signal_strength = 0.005  # 0.5% of current price
stop_loss_percent = 0.01
take_profit_percent = 0.02
entry_price = None

# === Connectivity Check ===
def is_connected():
    try:
        requests.get("https://www.google.com/", timeout=3)

        return True

    except requests.ConnectionError:

        return False

# === fetch price and SMA together
def get_price_and_sma(symbol, interval = '15m', limit = 20, retries = 5):
    for attempt in range(retries):
        try:
            # fetch candlestick data
            candles = client.get_klines(symbol = symbol, interval = interval, limit = limit)
            closes = [float(candle[4]) for candle in candles] # Closing prices

            # calculate the current price as the latest closing price
            current_price = closes[-1]

            # calculate short and long SMAs
            short_sma = np.mean(closes[-5:])
            long_sma = np.mean(closes[-10:])

            return current_price, short_sma, long_sma

        except BinanceAPIException as e:
            if e.status_code == 429: # HTTP 429: Too many requests
                wait_time = 2 ** attempt # Exponential backoff
                print(f"⚠️ Rate limit exceeded. Retrying in {wait_time} seconds...")
                logging.warning(f"Rate limit exceeded. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print(f"Binance API Exception: {e}")
                logging.error(f"Binance API Exception: {e}")
                break

        except Exception as e:
            print(f"Error fetching price and SMAs: {e}")
            logging.error(f"Error fetching price and SMAs: {e}")

    return None, None, None


# === Calculate Quantity ===
def calculate_quantity(symbol, price):
    try:
        # fetch balance
        balance = client.get_asset_balance('USDT')
        free_balance = float(balance['free'])
        risk_amount = free_balance * risk_percent

        # calculate raw quantity
        raw_quantity = risk_amount / price # Divide the risk_amount by the current asset price to get how many units of ETH you can buy

        # fetch symbol info
        info = client.get_symbol_info(symbol)
        if not info:
            print(f"⚠️ Unable to fetch symbol info for {symbol}. Skipping trade.")
            logging.warning(f"Unable to fetch symbol info for {symbol}. Skipping trade.")

            return None

        # Extract filters
        step_size = 0.0001 # Default step size
        min_notional = 5 # Default minimum notional value
        for f in info['filters']:
            if f['filterType'] == 'LOT_SIZE':
                step_size = float(f['stepSize'])
            elif f['filterType'] == 'MIN_NOTIONAL':
                min_notional = float(f['minNotional'])

        # Adjust quantity based on step size
        precision = int(round(-np.log10(step_size)))
        quantity = float(Decimal(str(raw_quantity)).quantize(Decimal('1e-{0}'.format(precision)), rounding=ROUND_DOWN))

        # Validate notional value
        notional_value = quantity * price
        if notional_value < min_notional:
            print(f"⚠️ Quantity too small (${notional_value:.2f} < ${min_notional:.2f})")
            logging.warning(f"⚠️ Quantity too small (${notional_value:.2f} < ${min_notional:.2f})")
            logging.info(
                f"Available balance: ${free_balance:.2f}, Risk amount: ${risk_amount:.2f}, Price: ${price:.2f}")

            return None

        return quantity
    except BinanceAPIException as e:
        print(f"Binance API Exception: {e}")
        logging.error(f"Binance API Exception: {e}")

    except Exception as e:
        print(f"Error calculating quantity: {e}")
        logging.error(f"Error calculating quantity: {e}")
        return None

# === Place Buy Order ===
def place_buy_order(symbol, quantity):
    try:
        order = client.order_market_buy(symbol=symbol, quantity=quantity)
        print(f"Buy order done: {order}")

        price = float(order['fills'][0]['price'])
        cost = price * quantity
        fee = cost * 0.001  # 0.1% fee
        total_cost = cost + fee

        print(f"Buy Price: {price:.2f} | Fee: {fee:.4f} USDT | Total Cost: {total_cost:.4f} USDT")
        logging.info(f"BUY order at {price}, quantity: {quantity}, fee: {fee:.4f}, total cost: {total_cost:.4f}")

        return order  # Properly indented to be part of the try block

    except requests.exceptions.ConnectionError:
        print("No internet connection when placing buy order.")
        logging.warning("No internet connection when placing buy order.")
    except Exception as e:
        print(f"Error placing buy order: {e}")
        logging.error(f"Error placing buy order: {e}")

    return None  # None is returned if any exception occurs


# === Place Sell Order ===
def place_sell_order(symbol, quantity):
    try:
        order = client.order_market_sell(symbol=symbol, quantity=quantity)
        print(f"Sell order done: {order}")

        price = float(order['fills'][0]['price'])
        revenue = price * quantity
        fee = revenue * 0.001  # 0.1% fee
        net_revenue = revenue - fee

        print(f"Sell Price: {price:.2f} | Fee: {fee:.4f} USDT | Net Revenue: {net_revenue:.4f} USDT")
        logging.info(f"SELL order at {price}, quantity: {quantity}, fee: {fee:.4f}, net revenue: {net_revenue:.4f}")

        return order

    except requests.exceptions.ConnectionError:
        print("No internet connection when placing sell order.")
        logging.warning("No internet connection when placing sell order.")
    except Exception as e:
        print(f"Error placing sell order: {e}")
        logging.error(f"Error placing sell order: {e}")

    return None  # None is returned if any exception occurs

# == factor_stop_loss_and_take_profit ===
def calculate_stop_loss_and_take_profit(
        entry_price,
        stop_loss_percent,
        take_profit_percent,
        slippage_percent=0.001,
        fee_percent=0.001):
    """
    Calculating stop-loss and take-profit prices, factoring in slippage and fees.

    :param entry_price: The entry price of the trade.
    :param stop_loss_percent: The percentage for stop-loss (e.g., 0.01 for 1%).
    :param take_profit_percent: The percentage for take-profit (e.g., 0.02 for 2%).
    :param slippage_percent: The assumed slippage percentage (default is 0.1%).
    :param fee_percent: The trading fee percentage per trade (default is 0.1%).
    :return: Adjusted stop-loss and take-profit prices.
    """

    # adjust stop-loss for slippage and fees
    stop_loss_price = entry_price * (1 - stop_loss_percent) * (1 - slippage_percent - fee_percent)

    # adjust take_profit for slippage and fees
    take_profit_price = entry_price * (1 + take_profit_percent) * (1 - slippage_percent - fee_percent)

    return stop_loss_price, take_profit_price

def trading_bot():
    global entry_price, last_sell_time, last_buy_time
    in_position = {symbol: False for symbol in symbols} # track positions for each trading pair
    entry_prices = {symbol: None for symbol in symbols} # Track entry prices for each trading pair

    while True:
        try:
            if not is_connected():
                print("No internet connection. Waiting 60 seconds...")
                logging.warning("No internet connection. Retrying in 60 seconds.")
                time.sleep(60)
                continue

            for symbol in symbols: # loop through each trading pair
                print(f"processing {symbol}...")
                logging.info(f"processing {symbol}...")

                # Fetching price and SMA data for the trading pairs
                price, short_sma, long_sma = get_price_and_sma(symbol)

                if price is None or short_sma is None or long_sma is None:
                    print("Missing data. Skipping this cycle.")
                    logging.warning("Missing data. Skipping cycle.")
                    time.sleep(60)
                    continue

                required_sma_gap = min_signal_strength * price
                difference = abs(short_sma - long_sma)

                print(f"Current price: {price:.2f} | Short SMA: {short_sma:.2f} | Long SMA: {long_sma:.2f}")
                print(f"Difference: {difference:.4f} | Required SMA ga0p: {required_sma_gap:.4f}")
                logging.info(f"Price: {price:.2f}, Short SMA: {short_sma:.2f}, Long SMA: {long_sma:.2f}, Diff: {difference:.4f}")

                now = datetime.now()

                if in_position[symbol]:
                     # factoring in slippage and fees for stop-loss and take-profit
                    (stop_loss_price,
                     take_profit_price) = calculate_stop_loss_and_take_profit(
                        entry_price[symbol],
                        stop_loss_percent,
                        take_profit_percent
                    )

                    if price <= stop_loss_price:
                        # Check cooldown for sell signals
                        if last_sell_time and now - last_sell_time < trade_cooldown:
                            print("⚠️ Sell signal skipped due to cooldown.")
                            logging.info("Sell signal skipped due to cooldown.")
                            continue

                        print(f"Stop Loss Triggered! Selling at {price:.2f}")
                        logging.info(f"Stop Loss Triggered at {price:.2f}")
                        quantity = calculate_quantity(symbol, price)

                        if quantity:
                            place_sell_order(symbol, quantity)
                            last_sell_time = now # Update sell cooldown
                            in_position[symbol] = False
                            entry_price[symbol] = None

                    elif price >= take_profit_price:
                        # Check cooldown for sell signals
                        if last_sell_time and now - last_sell_time < trade_cooldown:
                            print("⚠️ Sell signal skipped due to cooldown.")
                            logging.info("Sell signal skipped due to cooldown.")
                            continue

                        print(f"Take Profit Triggered! Selling at {price:.2f}")
                        logging.info(f"Take Profit Triggered! Selling at {price:.2f}")
                        quantity = calculate_quantity(symbol, price)

                        if quantity:
                            place_sell_order(symbol, quantity)
                            last_sell_time = now  # Update sell cooldown
                            in_position[symbol] = False
                            entry_price[symbol] = None

                if not in_position and short_sma > long_sma and difference > required_sma_gap:
                    # Check cooldown for buy signals
                    if last_buy_time and now - last_buy_time < trade_cooldown:
                        print("⚠️ Buy signal skipped due to cooldown.")
                        logging.info("Buy signal skipped due to cooldown.")
                        continue

                    print("Buy signal! Short SMA crossed above Long SMA.")
                    logging.info("Buy signal detected. Executing buy.")
                    email_content = (
                        f"Buy Signal 🚀\n"
                        f"Trading Pair: {symbol}\n"
                        f"Price: {price:.2f}\n"
                        f"Short SMA: {short_sma:.2f}\n"
                        f"Long SMA: {long_sma:.2f}\n"
                        f"SMA Gap: {difference:.4f}"
                    )
                    send_email("Buy Alert 🚀", email_content, "buy")
                    quantity = calculate_quantity(symbol, price)

                    if quantity:
                        order = place_buy_order(symbol, quantity)

                        if order:
                            entry_price[symbol] = float(order['fills'][0]['price'])
                            last_buy_time = now  # Update buy cooldown
                            in_position[symbol] = True
                            logging.info(f"Buy order filled at {entry_price[symbol]:.2f}")

                elif in_position and short_sma < long_sma and difference > required_sma_gap:
                    # Check cooldown for sell signals
                    if last_sell_time and now - last_sell_time < trade_cooldown:
                        print("⚠️ Sell signal skipped due to cooldown.")
                        logging.info("Sell signal skipped due to cooldown.")
                        continue

                    print("Sell signal! Short SMA crossed below Long SMA.")
                    logging.info("Sell signal detected. Executing sell.")
                    email_content = (
                        f"Sell Signal 💸\n"
                        f"Trading Pair: {symbol}\n"
                        f"Price: {price:.2f}\n"
                        f"Short SMA: {short_sma:.2f}\n"
                        f"Long SMA: {long_sma:.2f}\n"
                        f"SMA Gap: {difference:.4f}"
                    )
                    send_email("Sell Alert 💸", email_content, "sell")
                    quantity = calculate_quantity(symbol, price)

                    if quantity:
                        place_sell_order(symbol, quantity)
                        last_sell_time = now  # Update sell cooldown
                        in_position[symbol] = False
                        entry_price[symbol] = None
                        logging.info(f"Sell order placed due to SMA crossover at {price:.2f}")

                else:
                    print("No strong signal. Holding position...")
                    logging.info("No trade signal. Holding...")

            time.sleep(60)

        except Exception as e:
                print(f"Unexpected error in trading loop: {e}")
                logging.error(f"Unexpected error in trading loop: {e}")
                time.sleep(60)

if __name__ == "__main__":
    trading_bot()
