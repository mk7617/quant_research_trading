# Risk Parity ETF Portfolio Strategy (UK ETFs + IBKR Fees)

This project implements a **risk parity investment strategy** using **UK-listed ETFs**, with **monthly rebalancing** and **realistic brokerage fees** (Interactive Brokers UK). The backtest simulates capital growth, allocates weights based on risk contribution, and visualizes key portfolio performance metrics.
---

## Output Visuals

- Portfolio value over time
- ETF performance comparison (normalized prices)
- Allocation weight dynamics
- Monthly return heatmap
- Annual return bar chart
- Performance summary statistics

---

## Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

---

##  How to Run

```bash
python risk_parity_portfolio.py
```

Make sure to modify the ETF tickers in the script to suit your portfolio preferences.

---

## Future Improvements

- Add more diversified ETFs (UK, global equities, bonds, REITs, etc.)
- Incorporate volatility targeting or dynamic risk budgeting
- Extend to multi-currency portfolios with FX hedging
- Export results to CSV or interactive dashboards

---

## License

This project is for educational and research purposes only. Use at your own risk. No investment advice is provided.

---

## Live Trading Bot (IBKR)

A live trading script is included to automate **monthly rebalancing** of the portfolio using **Interactive Brokers (IBKR)** via the `ib_insync` API.

### Features

- Connects to IBKR TWS or IB Gateway (`localhost:7497`)
- Pulls 1-year daily historical prices for selected tickers
- Computes risk-parity weights using recent return covariance
- Calculates target allocation and places market orders accordingly
- Logs all actions to both terminal and `ibkr_rebalance.log`

### Scheduling

The script includes a built-in scheduler to run **every Monday at 9:30 AM**, or it can be executed manually for immediate rebalancing.

### Running the Bot

```bash
python risk_parity_portfolio_in_etf.py
```

Ensure TWS or IB Gateway is running and connected to paper/live trading before execution. Run the script once a month to rebalace portfolio based on risk parity. 

### Disclaimer

This bot interacts with a live brokerage account. Use extreme caution. **Always test thoroughly on a paper account first.**
