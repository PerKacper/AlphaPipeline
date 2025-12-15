# 📖 Usage Examples

Complete examples for common use cases.

---

## 🎯 Example 1: Basic Backtest

Test the strategy on Apple stock:

```python
from trading_system import walk_forward_backtest, build_features, build_labels
from data_loader import load_data
import config

# Load data
data_dict = load_data(
    symbols=['AAPL'],
    start_date='2020-01-01',
    end_date='2023-12-31',
    source='yahoo'
)

# Build features
for symbol in data_dict:
    df = data_dict[symbol]
    df = build_features(df)
    df['label'] = build_labels(df)
    data_dict[symbol] = df

# Run backtest
portfolio = walk_forward_backtest(
    data_dict,
    start_capital=100_000,
    train_window=252,
    test_window=60,
    risk_pct=0.01,
    use_risk_parity=False  # Single asset
)

# Print results
print(portfolio.get_metrics())
```

---

## 🎯 Example 2: Multi-Asset Portfolio

Test on tech stocks with risk parity:

```python
from trading_system import walk_forward_backtest, build_features, build_labels
from data_loader import load_data

# Tech portfolio
symbols = ['AAPL', 'MSFT', 'GOOGL', 'NVDA', 'META']

data_dict = load_data(symbols, '2020-01-01', '2023-12-31', source='yahoo')

# Process all symbols
for symbol in data_dict:
    df = data_dict[symbol]
    df = build_features(df)
    df['label'] = build_labels(df, horizon=10, tp=0.05, sl=0.025)
    data_dict[symbol] = df

# Run with risk parity
portfolio = walk_forward_backtest(
    data_dict,
    start_capital=100_000,
    train_window=252,
    test_window=60,
    risk_pct=0.008,  # Slightly lower for diversification
    use_risk_parity=True
)

# Results
metrics = portfolio.get_metrics()
print(f"Return: {metrics['total_return']:.2%}")
print(f"Max DD: {metrics['max_drawdown']:.2%}")
print(f"Win Rate: {metrics['win_rate']:.2%}")
```

---

## 🎯 Example 3: Conservative Trading

Low-risk, conservative parameters:

```python
# Conservative config
config.RISK_PER_TRADE = 0.005      # 0.5% per trade
config.VOL_TARGET = 0.08            # 8% target vol
config.MAX_POSITIONS = 5            # Fewer positions
config.ML_PROB_THRESHOLD = 0.65     # Higher threshold
config.STOP_LOSS_ATR = 1.5          # Tighter stop
config.TAKE_PROFIT_ATR = 3.0        # Closer TP

portfolio = walk_forward_backtest(
    data_dict,
    start_capital=100_000,
    train_window=500,  # Longer training
    test_window=40,    # Shorter testing
    risk_pct=config.RISK_PER_TRADE,
    use_risk_parity=True
)
```

---

## 🎯 Example 4: Aggressive Trading

Higher risk, more frequent trades:

```python
# Aggressive config
config.RISK_PER_TRADE = 0.02        # 2% per trade
config.VOL_TARGET = 0.15            # 15% target vol
config.MAX_POSITIONS = 15           # More positions
config.ML_PROB_THRESHOLD = 0.55     # Lower threshold
config.STOP_LOSS_ATR = 3.0          # Wider stop
config.TAKE_PROFIT_ATR = 6.0        # Further TP

portfolio = walk_forward_backtest(
    data_dict,
    start_capital=100_000,
    train_window=252,
    test_window=60,
    risk_pct=config.RISK_PER_TRADE,
    use_risk_parity=True
)
```

---

## 🎯 Example 5: Custom Features

Add your own indicators:

```python
from trading_system import build_features
import pandas as pd

def build_custom_features(df):
    """Add custom features"""
    # Start with standard features
    df = build_features(df)
    
    # Add Bollinger Bands
    sma20 = df['close'].rolling(20).mean()
    std20 = df['close'].rolling(20).std()
    df['bb_upper'] = sma20 + 2 * std20
    df['bb_lower'] = sma20 - 2 * std20
    df['bb_width'] = (df['bb_upper'] - df['bb_lower']) / sma20
    
    # Add RSI
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss
    df['rsi'] = 100 - (100 / (1 + rs))
    
    # Add to features list
    return df

# Update FEATURES in config
config.FEATURES = config.FEATURES + ['bb_width', 'rsi']

# Use custom feature builder
for symbol in data_dict:
    data_dict[symbol] = build_custom_features(data_dict[symbol])
```

---

## 🎯 Example 6: Different ML Models

Use XGBoost instead of Random Forest:

```python
from trading_system import MLModel
import xgboost as xgb

class XGBoostModel(MLModel):
    def __init__(self):
        self.model = xgb.XGBClassifier(
            n_estimators=200,
            max_depth=6,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42
        )
        self.is_trained = False

# Use in backtest (modify walk_forward_backtest to accept custom model)
```

---

## 🎯 Example 7: CSV Data Loading

Use your own CSV files:

```python
from data_loader import load_csv_data
from trading_system import build_features, build_labels

# Load from CSV
data_dict = load_csv_data(
    symbols=['SPY', 'QQQ', 'DIA'],
    data_path='./my_data/'
)

# CSV format should be:
# date,open,high,low,close,volume
# 2020-01-01,100,102,99,101,1000000

# Process and run backtest
for symbol in data_dict:
    df = data_dict[symbol]
    df = build_features(df)
    df['label'] = build_labels(df)
    data_dict[symbol] = df

portfolio = walk_forward_backtest(data_dict, ...)
```

---

## 🎯 Example 8: Crypto Trading

Trade cryptocurrencies on Binance:

```python
from data_loader import load_binance_data
from trading_system import walk_forward_backtest, build_features, build_labels

# Load crypto data
symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT']

data_dict = load_binance_data(
    symbols,
    start_date='2022-01-01',
    end_date='2023-12-31',
    interval='1d'
)

# Process features
for symbol in data_dict:
    df = data_dict[symbol]
    df = build_features(df)
    df['label'] = build_labels(df, horizon=5, tp=0.08, sl=0.04)  # Wider targets for crypto
    data_dict[symbol] = df

# Run backtest with crypto-specific settings
portfolio = walk_forward_backtest(
    data_dict,
    start_capital=10_000,
    train_window=180,
    test_window=30,
    risk_pct=0.015,  # Slightly higher risk for crypto
    use_risk_parity=True
)
```

---

## 🎯 Example 9: Monte Carlo Analysis

Analyze strategy robustness:

```python
from trading_system import monte_carlo
import numpy as np
import matplotlib.pyplot as plt

# After running backtest
trades = portfolio.trades
initial_capital = portfolio.initial_capital

# Run Monte Carlo
curves = monte_carlo(trades, initial_capital, n=1000)

# Calculate statistics
final_values = curves[:, -1]
percentiles = np.percentile(final_values, [5, 25, 50, 75, 95])

print(f"5th percentile: ${percentiles[0]:,.0f}")
print(f"25th percentile: ${percentiles[1]:,.0f}")
print(f"Median: ${percentiles[2]:,.0f}")
print(f"75th percentile: ${percentiles[3]:,.0f}")
print(f"95th percentile: ${percentiles[4]:,.0f}")

# Probability of profit
prob_profit = (final_values > initial_capital).mean()
print(f"\nProbability of profit: {prob_profit:.1%}")

# Expected value
expected_value = final_values.mean()
print(f"Expected final capital: ${expected_value:,.0f}")
```

---

## 🎯 Example 10: Live Paper Trading

Run paper trading with monitoring:

```python
from live_trader import LiveTrader
import config

# Set paper trading mode
config.LIVE_MODE = False
config.PAPER_TRADING = True

# Configure symbols
config.SYMBOLS = ['AAPL', 'MSFT', 'GOOGL']

# Create trader
trader = LiveTrader(broker='ibkr', paper_trading=True)

# Connect
if trader.connect_broker():
    # Train model
    trader.train_model()
    
    # Start trading loop
    trader.run()
```

---

## 🎯 Example 11: Custom Signal Logic

Override signal functions:

```python
def my_long_signal(row, prob, regime):
    """Custom long signal with additional filters"""
    base_conditions = (
        row['close'] > row['ema200'] and
        row['ema50'] > row['ema200'] and
        prob > 0.6
    )
    
    # Add custom filters
    volume_ok = row.get('volume', 1) > row.get('volume_ma', 1) * 1.2
    volatility_ok = row['volatility'] < 0.3
    
    return base_conditions and volume_ok and volatility_ok and regime.startswith('trending')

# Use in backtest by modifying walk_forward_backtest function
# or creating a custom strategy class
```

---

## 🎯 Example 12: Performance Comparison

Compare multiple configurations:

```python
from trading_system import walk_forward_backtest
import pandas as pd

configs = [
    {'risk': 0.005, 'vol_target': 0.08, 'name': 'Conservative'},
    {'risk': 0.01, 'vol_target': 0.10, 'name': 'Balanced'},
    {'risk': 0.02, 'vol_target': 0.15, 'name': 'Aggressive'}
]

results = []

for cfg in configs:
    portfolio = walk_forward_backtest(
        data_dict,
        start_capital=100_000,
        risk_pct=cfg['risk'],
        use_risk_parity=True
    )
    
    metrics = portfolio.get_metrics()
    metrics['config'] = cfg['name']
    results.append(metrics)

# Compare
df_results = pd.DataFrame(results)
print(df_results[['config', 'total_return', 'max_drawdown', 'win_rate']])
```

---

## 💡 Tips & Best Practices

1. **Start simple** - test with 1-3 symbols first
2. **Validate thoroughly** - run multiple backtests with different periods
3. **Monitor regime detection** - adjust trading based on market conditions
4. **Use risk parity** - for portfolios with 5+ assets
5. **Keep ML simple** - Random Forest works well, don't overcomplicate
6. **Paper trade first** - always test live system in paper mode
7. **Log everything** - enable detailed logging for debugging

---

## 🆘 Need Help?

- Check [README.md](README.md) for full documentation
- See [QUICKSTART.md](QUICKSTART.md) for setup guide
- Open GitHub issue for bugs
- Email support@tradingsystem.com for questions

---

**Happy Trading! 📈**