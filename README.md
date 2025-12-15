# 🚀 AlphaPipeline - Advanced Trading System

Advanced trading system with Machine Learning, Risk Parity, and live trading support for IBKR/Binance.

## 📋 Table of Contents

- [Features](#-features)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Configuration](#-configuration)
- [Architecture](#-architecture)
- [Live Trading](#-live-trading)
- [Parameters](#-parameters)
- [Troubleshooting](#-troubleshooting)

---

## ✨ Features

### Core Features
- ✅ **Long & Short positions** - full bidirectional trading support
- ✅ **Multi-asset portfolio** - trade multiple instruments simultaneously
- ✅ **Machine Learning filter** - Random Forest for signal filtering
- ✅ **Walk-forward optimization** - model retraining every N periods
- ✅ **Commission & slippage** - realistic costs (0.2% total)

### Advanced Features
- 🎯 **True Risk Parity** - dynamic weights based on covariance matrix
- 📊 **Regime Detection** - 4 market regimes (trending/choppy × low/high vol)
- 🔴 **Volatility Targeting** - position sizing adjusted to volatility
- 📈 **Monte Carlo simulation** - bootstrap equity curves
- ⚡ **Live trading** - IBKR & Binance connectors

### Monitoring
- 🔔 **Real-time alerts** - drawdown, exposure, capital warnings
- 📧 **Email notifications** - SMTP-ready
- 📊 **Performance metrics** - win rate, profit factor, Sharpe ratio
- 📉 **Drawdown tracking** - continuous monitoring

---

## 🔧 Installation

### 1. System Requirements
```bash
Python 3.8+
pip
```

### 2. Core Libraries
```bash
pip install numpy pandas scikit-learn scipy matplotlib
```

### 3. Live Trading (optional)

**For Interactive Brokers:**
```bash
pip install ib_insync
```

**For Binance:**
```bash
pip install python-binance
```

### 4. Download Files
```bash
git clone https://github.com/your-repo/alphapipeline.git
cd alphapipeline
```

**File Structure:**
```
alphapipeline/
├── trading_system.py          # Main system code
├── config.py                  # Configuration
├── data_loader.py             # Data loading
├── backtest_runner.py         # Backtest script
├── live_trader.py             # Live trading script
├── requirements.txt           # Dependencies
└── README.md                  # This documentation
```

---

## 🚀 Quick Start

### Backtest on Historical Data

```python
from trading_system import walk_forward_backtest, build_features, build_labels
import pandas as pd

# 1. Load data
data_dict = {}
for symbol in ['AAPL', 'MSFT', 'GOOGL']:
    df = pd.read_csv(f'data/{symbol}.csv', index_col=0, parse_dates=True)
    df = build_features(df)
    df['label'] = build_labels(df)
    data_dict[symbol] = df

# 2. Run backtest
portfolio = walk_forward_backtest(
    data_dict,
    start_capital=100_000,
    train_window=252,      # 1 year training
    test_window=60,        # 3 months testing
    risk_pct=0.01,         # 1% risk per trade
    use_risk_parity=True   # Enable risk parity
)

# 3. View results
print(portfolio.get_metrics())
```

### Live Trading - IBKR

```python
from trading_system import IBKRConnector

# 1. Connect to TWS
ibkr = IBKRConnector(
    host='127.0.0.1',
    port=7497,        # Paper trading
    client_id=1
)
ibkr.connect()

# 2. Place order
ibkr.place_order('AAPL', 'BUY', 100)
```

### Live Trading - Binance

```python
from trading_system import BinanceConnector

# 1. Connect to Binance
binance = BinanceConnector(
    api_key='YOUR_API_KEY',
    api_secret='YOUR_API_SECRET',
    testnet=True  # Use testnet!
)
binance.connect()

# 2. Place order
binance.place_order('BTCUSDT', 'BUY', 0.01)
```

---

## ⚙️ Configuration

### config.py

```python
# Capital & Risk
START_CAPITAL = 100_000
RISK_PER_TRADE = 0.01      # 1% capital per trade
VOL_TARGET = 0.10           # 10% target volatility
MAX_POSITIONS = 10

# ML Training
TRAIN_WINDOW = 252          # Days for training
TEST_WINDOW = 60            # Days for testing
RETRAIN_FREQUENCY = 60      # Retrain every N days

# Risk Parity
USE_RISK_PARITY = True
LOOKBACK_CORRELATION = 60   # Days for correlation calculation

# Regime Detection
VOL_LOOKBACK = 20
TREND_LOOKBACK = 50

# Live Trading
LIVE_MODE = False           # Set True for live
BROKER = 'IBKR'             # 'IBKR' or 'BINANCE'

# IBKR Settings
IBKR_HOST = '127.0.0.1'
IBKR_PORT = 7497            # 7497=paper, 7496=live
IBKR_CLIENT_ID = 1

# Binance Settings
BINANCE_API_KEY = 'your_key'
BINANCE_API_SECRET = 'your_secret'
BINANCE_TESTNET = True

# Alerts
ALERT_DRAWDOWN = 0.05       # Alert at 5% DD
ALERT_EMAIL = 'your@email.com'
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
```

---

## 🏗️ Architecture

### 1. Data Pipeline
```
Raw Data → build_features() → build_labels() → ML Training
```

### 2. ML Model
- **Algorithm:** Random Forest Classifier
- **Purpose:** Signal filtering (not generation!)
- **Features:** 9 technical indicators
- **Output:** Probability score (0-1)

### 3. Risk Management

**Position Sizing:**
```python
size = (capital × risk_pct × rp_weight) / ATR
```

**Risk Parity:**
```python
minimize: variance(risk_contributions)
constraint: sum(weights) = 1
bounds: 0 ≤ weight ≤ 0.5
```

### 4. Regime Detection

| Regime | Vol | Trend | Action |
|--------|-----|-------|--------|
| Trending Low Vol | ✅ Low | ✅ Strong | **TRADE** |
| Trending High Vol | ⚠️ High | ✅ Strong | Trade cautiously |
| Choppy Low Vol | ✅ Low | ❌ Weak | Avoid |
| Choppy High Vol | ❌ High | ❌ Weak | **STOP** |

### 5. Signal Generation

**Long Signal:**
```
price > EMA200 AND
ema50 > ema200 AND
ML_prob > 0.6 AND
regime = trending
```

**Short Signal:**
```
price < EMA200 AND
ema50 < ema200 AND
ML_prob > 0.6 AND
regime = trending
```

---

## 📡 Live Trading

### IBKR Setup

1. **Install TWS or IB Gateway**
   - Download: https://www.interactivebrokers.com/

2. **Enable API**
   - TWS → File → Global Configuration → API → Settings
   - Enable ActiveX and Socket Clients
   - Socket port: 7497 (paper) / 7496 (live)

3. **Run system**
```bash
python live_trader.py --broker ibkr --paper
```

### Binance Setup

1. **Create API keys**
   - https://www.binance.com/en/my/settings/api-management

2. **Enable testnet (optional)**
   - https://testnet.binance.vision/

3. **Run system**
```bash
python live_trader.py --broker binance --testnet
```

---

## 🎛️ Parameters

### Basic

| Parameter | Default | Description |
|-----------|---------|-------------|
| `start_capital` | 100,000 | Starting capital |
| `risk_pct` | 0.01 | Risk per trade (1%) |
| `vol_target` | 0.10 | Target volatility (10%) |
| `max_positions` | 10 | Max open positions |

### ML Model

| Parameter | Default | Description |
|-----------|---------|-------------|
| `n_estimators` | 200 | Number of RF trees |
| `max_depth` | 6 | Tree depth |
| `train_window` | 252 | Training window (days) |
| `test_window` | 60 | Testing window (days) |

### Risk Parity

| Parameter | Default | Description |
|-----------|---------|-------------|
| `lookback` | 60 | Correlation window (days) |
| `max_weight` | 0.5 | Max weight per instrument |

### Stop Loss / Take Profit

| Parameter | Default | Description |
|-----------|---------|-------------|
| `stop_loss` | 2 × ATR | Stop loss distance |
| `take_profit` | 4 × ATR | Take profit distance |

---

## 🔍 Troubleshooting

### Problem: "Model not trained"
**Solution:** Increase `train_window` or decrease number of symbols

### Problem: "IBKR connection failed"
**Solution:**
1. Check if TWS/Gateway is running
2. Verify port (7497/7496)
3. Enable API in TWS settings

### Problem: "Binance API error"
**Solution:**
1. Check API key & secret
2. Enable spot trading in API settings
3. Add IP whitelist (optional)

### Problem: "No trades executed"
**Solution:**
1. Lower `ML_prob` threshold (e.g., 0.5)
2. Check if data has correct columns (OHLCV)
3. Increase number of symbols in portfolio

### Problem: "High drawdown"
**Solution:**
1. Decrease `risk_pct` (e.g., 0.005)
2. Increase `train_window` for better ML
3. Enable `use_risk_parity=True`

---

## 📊 Performance Metrics

The system generates the following metrics:

- **Total Return** - overall return
- **Win Rate** - % of profitable trades
- **Profit Factor** - avg_win / avg_loss
- **Max Drawdown** - largest equity decline
- **Sharpe Ratio** - risk-adjusted returns
- **Number of Trades** - total trades executed

---

## ⚠️ Disclaimer

**This system is an educational tool.**

- Trading involves risk of capital loss
- Always test on paper trading before live
- Don't invest more than you can afford to lose
- The author is not responsible for losses

---

## 📝 TODO

- [ ] Telegram bot integration
- [ ] Real-time dashboard (Streamlit)
- [ ] More ML models (LightGBM, XGBoost)
- [ ] Options trading support
- [ ] Advanced portfolio optimization (Black-Litterman)

---

## 📄 License

Apache-2.0 license

---

**Made with ❤️ for algorithmic traders**

*Last updated: December 2025*
