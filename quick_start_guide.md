# 🚀 Quick Start Guide

Get up and running with the Advanced Trading System in 5 minutes!

---

## 📦 Step 1: Installation (2 min)

### Clone repository
```bash
git clone https://github.com/your-repo/trading-system.git
cd trading-system
```

### Install dependencies
```bash
pip install -r requirements.txt
```

**Minimum requirements:**
```bash
pip install numpy pandas scikit-learn scipy matplotlib yfinance
```

---

## 🎯 Step 2: First Backtest (2 min)

### Run with default settings
```bash
python backtest_runner.py
```

This will:
- Download data for AAPL, MSFT, GOOGL
- Run backtest from 2020-2023
- Generate performance charts
- Show metrics in terminal

### Custom backtest
```bash
python backtest_runner.py --symbols TSLA NVDA AMD --start 2021-01-01 --capital 50000
```

---

## 📊 Step 3: View Results (<1 min)

After backtest completes, you'll see:

### Terminal output:
```
📊 PERFORMANCE REPORT
════════════════════════════════════════════════════════════════════
💰 CAPITAL METRICS
Initial Capital:                     $100,000.00
Final Capital:                       $125,432.10
Total Return:                              25.43%
Max Drawdown:                               8.23%

📈 TRADE METRICS
Number of Trades:                             143
Win Rate:                                   58.74%
Profit Factor:                                1.85
```

### Generated charts:
- `backtest_equity.png` - Equity curve + drawdown
- `backtest_trades.png` - Trade distribution
- `backtest_montecarlo.png` - Monte Carlo simulation

---

## ⚙️ Step 4: Configuration (optional)

Edit `config.py` to customize:

```python
# Quick tweaks
START_CAPITAL = 50_000          # Your capital
RISK_PER_TRADE = 0.005          # 0.5% risk per trade (conservative)
SYMBOLS = ['AAPL', 'MSFT']      # Your symbols
```

---

## 🔴 Step 5: Paper Trading (when ready)

### For IBKR:

1. **Install TWS/Gateway**
   - Download from interactivebrokers.com
   - Enable API in settings (port 7497)

2. **Run paper trader**
```bash
python live_trader.py --broker ibkr --paper
```

### For Binance:

1. **Get testnet API keys**
   - Visit testnet.binance.vision
   - Generate API key + secret

2. **Edit config.py**
```python
BINANCE_API_KEY = 'your_key'
BINANCE_API_SECRET = 'your_secret'
BINANCE_TESTNET = True
```

3. **Run paper trader**
```bash
python live_trader.py --broker binance --paper
```

---

## 🎓 Next Steps

### Improve performance:
1. **Tune ML model** - edit `config.py`:
   ```python
   ML_PROB_THRESHOLD = 0.55  # Lower = more trades
   N_ESTIMATORS = 300        # More trees = better accuracy
   ```

2. **Optimize risk** - edit `config.py`:
   ```python
   RISK_PER_TRADE = 0.01     # Increase for more aggressive
   VOL_TARGET = 0.15         # Higher target volatility
   ```

3. **Add more symbols**:
   ```python
   SYMBOLS = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 
              'META', 'NVDA', 'JPM', 'V', 'WMT']
   ```

### Study the code:
- `trading_system.py` - Core logic
- `config.py` - All parameters
- `backtest_runner.py` - Backtest workflow

---

## ⚠️ Common Issues

### "No module named 'yfinance'"
```bash
pip install yfinance
```

### "Failed to load data"
- Check internet connection
- Try different symbols
- Use `--source csv` if you have local data

### "IBKR connection failed"
- Ensure TWS/Gateway is running
- Check port (7497 for paper)
- Enable API in TWS settings

### "Model not trained"
- Increase `TRAIN_WINDOW` in config
- Ensure sufficient data (252+ days)

---

## 📚 Full Documentation

For detailed docs, see [README.md](README.md)

---

## 🆘 Support

- **Issues**: GitHub Issues
- **Email**: support@tradingsystem.com
- **Docs**: Full README.md

---

## ⚡ Pro Tips

1. **Always start with backtest** - validate before live trading
2. **Use paper trading first** - test for at least 2 weeks
3. **Start small** - use minimum position sizes initially
4. **Monitor closely** - check system daily for first month
5. **Keep it simple** - don't over-optimize parameters

---

**Ready? Start with a backtest!**

```bash
python backtest_runner.py
```

Good luck! 📈