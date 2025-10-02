# Risk Parity ETF Portfolio Strategy (UK ETFs + IBKR Fees)

This project implements a **risk parity investment strategy** using **UK-listed ETFs**, with **monthly rebalancing** and **realistic brokerage fees** (Interactive Brokers UK). The backtest simulates capital growth, allocates weights based on risk contribution, and visualizes key portfolio performance metrics.
---

## Strategy Summary

- **Portfolio Assets (default)**:
  - `SGLN.L`  iShares Physical Gold ETC (Gold)
  - `VUSA.L`  Vanguard S&P 500 UCITS ETF (US Equities)
  - *(Replace with your own ETF basket as desired)*

- **Initial Capital**: £1,000,000  
- **Backtest Period**: Jan 2015 – Aug 2025  
- **Rebalancing Frequency**: Monthly  
- **Max Asset Weight**: 70%  
- **Fee Model (IBKR UK)**: `max(£6, 0.05% of trade value)`  
- **Risk Model**: Minimum-variance optimization with equal risk contribution

---

## Output Visuals

- Portfolio value over time
- ETF performance comparison (normalized prices)
- Allocation weight dynamics
- Monthly return heatmap
- Annual return bar chart
- Performance summary statistics

---

## Performance Metrics (Example)

```
Sharpe Ratio (annualized): 4.69
Cumulative Return: 86.34%
CAGR: 6.41%
Max Drawdown: -13.45%
Win Rate: 61.5%
Total IBKR Fees Paid: £2,674.00

Final Portfolio Weights:
VUSA.L    70.00%
SGLN.L    30.00%
```

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
python ibkr_trading_bot.py
```

Ensure TWS or IB Gateway is running and connected to paper/live trading before execution. Run the script once a month to rebalace portfolio based on risk parity. 

### Disclaimer

This bot interacts with a live brokerage account. Use extreme caution. **Always test thoroughly on a paper account first.**
