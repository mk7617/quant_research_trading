from ib_insync import *
import numpy as np
import pandas as pd
from scipy.optimize import minimize
import time
from datetime import datetime
import logging

# --- Logging Setup ---
logging.basicConfig(
    filename='ibkr_rebalance.log',
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


# Using leveraged tickers = ["TQQQ", "SVXY", "VXZ", "TMF", "EDZ", "UGL"] // make sure its rebalaced on weekly basis

console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger('').addHandler(console)

ib = IB()
try:
    ib.connect('127.0.0.1', 7497, clientId=1)
    logging.info("Connected to Interactive Brokers.")
except Exception as e:
    logging.error(f"Failed to connect to IBKR: {e}")
    exit()


tickers =  ["SGLN","VUSA"]
contracts = {ticker: Stock(ticker, 'SMART', 'GBP') for ticker in tickers}

for ticker, contract in contracts.items():
    try:
        ib.qualifyContracts(contract)
        logging.info(f"Qualified contract: {ticker}")
    except Exception as e:
        logging.warning(f"Could not qualify {ticker}: {e}")


def fetch_price_history(contract, duration='1 Y', bar_size='1 day'):
    try:
        bars = ib.reqHistoricalData(
            contract,
            endDateTime='',
            durationStr=duration,
            barSizeSetting=bar_size,
            whatToShow='TRADES',
            useRTH=True,
            formatDate=1
        )
        df = util.df(bars)
        df.set_index('date', inplace=True)
        return df['close']
    except Exception as e:
        logging.error(f"Error fetching history for {contract.symbol}: {e}")
        return pd.Series()

def get_returns():
    price_data = {}
    for ticker, contract in contracts.items():
        logging.info(f"Fetching price history for {ticker}")
        data = fetch_price_history(contract)
        if not data.empty:
            price_data[ticker] = data
        time.sleep(1)  # IBKR rate limiting
    df = pd.DataFrame(price_data)
    returns = df.pct_change().dropna()
    return returns

def optimize_weights(cov_matrix):
    n = cov_matrix.shape[0]
    x0 = np.ones(n) / n
    bounds = [(0, 1)] * n
    constraints = {'type': 'eq', 'fun': lambda w: np.sum(w) - 1}
    try:
        result = minimize(lambda w: 0.5 * w.T @ cov_matrix @ w, x0, bounds=bounds, constraints=constraints)
        if result.success:
            logging.info("Optimization successful.")
            return result.x
        else:
            logging.warning("Optimization failed, using equal weights.")
            return np.ones(n) / n
    except Exception as e:
        logging.error(f"Error during optimization: {e}")
        return np.ones(n) / n

def rebalance():
    logging.info("Starting rebalance routine...")
    returns = get_returns()
    if returns.empty:
        logging.warning("No returns data available. Skipping rebalance.")
        return

    cov = returns.cov().values
    weights = optimize_weights(cov)

    try:
        acct_summary = ib.accountSummary()
        net_liq = next((item.value for item in acct_summary if item.tag == 'NetLiquidation'), None)
        if net_liq is None:
            logging.error("Net Liquidation value not found.")
            return
        portfolio_value = float(net_liq)
        logging.info(f"Net Liquidation Value: ${portfolio_value:.2f}")
    except Exception as e:
        logging.error(f"Could not fetch account value: {e}")
        return

    for i, ticker in enumerate(returns.columns):
        try:
            contract = contracts[ticker]
            market_data = ib.reqMktData(contract, '', False, False)
            ib.sleep(2)

            price = market_data.last if market_data.last else market_data.close
            if price is None or price <= 0:
                logging.warning(f"Price unavailable for {ticker}. Skipping.")
                continue

            target_value = weights[i] * portfolio_value
            quantity = int(target_value / price)
            logging.info(f"{ticker}: Price=${price:.2f}, Target=${target_value:.2f}, Qty={quantity}, Weight={weights[i]:.2%}")

            # Place Market Order
            order = MarketOrder('BUY', quantity)
            trade = ib.placeOrder(contract, order)
            logging.info(f"Order placed for {ticker}: BUY {quantity} @ ${price:.2f}")
            ib.sleep(1)

        except Exception as e:
            logging.error(f"Error placing order for {ticker}: {e}")

    logging.info("Rebalance complete.\n")

def run_scheduler():
    logging.info("Scheduler started.")
    while True:
        now = datetime.now()
        if now.weekday() == 0 and now.hour == 9 and now.minute == 30:
            rebalance()
            time.sleep(3600) 
        else:
            time.sleep(30)


# --- Run Immediately ---
if __name__ == '__main__':
    rebalance()
