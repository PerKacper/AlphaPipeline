# 🚀 Advanced Trading System v2.0

Zaawansowany system tradingowy z Machine Learning, Risk Parity i obsługą live tradingu na IBKR/Binance.

## 📋 Spis treści

- [Funkcje](#-funkcje)
- [Instalacja](#-instalacja)
- [Szybki start](#-szybki-start)
- [Konfiguracja](#-konfiguracja)
- [Architektura](#-architektura)
- [Live Trading](#-live-trading)
- [Parametry](#-parametry)
- [Troubleshooting](#-troubleshooting)

---

## ✨ Funkcje

### Core Features
- ✅ **Long & Short positions** - pełna obsługa dwukierunkowego tradingu
- ✅ **Multi-asset portfolio** - handel na wielu instrumentach jednocześnie
- ✅ **Machine Learning filter** - Random Forest do filtrowania sygnałów
- ✅ **Walk-forward optimization** - retraining modelu co N okresów
- ✅ **Commission & slippage** - realistyczne koszty (0.2% total)

### Advanced Features
- 🎯 **True Risk Parity** - dynamiczne wagi oparte na macierzy kowariancji
- 📊 **Regime Detection** - 4 reżimy rynkowe (trending/choppy × low/high vol)
- 🔴 **Volatility Targeting** - dostosowanie wielkości pozycji do zmienności
- 📈 **Monte Carlo simulation** - bootstrap equity curves
- ⚡ **Live trading** - IBKR & Binance connectors

### Monitoring
- 🔔 **Real-time alerts** - drawdown, exposure, capital warnings
- 📧 **Email notifications** - gotowe pod SMTP
- 📊 **Performance metrics** - win rate, profit factor, Sharpe ratio
- 📉 **Drawdown tracking** - continuous monitoring

---

## 🔧 Instalacja

### 1. Wymagania systemowe
```bash
Python 3.8+
pip
```

### 2. Podstawowe biblioteki
```bash
pip install numpy pandas scikit-learn scipy matplotlib
```

### 3. Live Trading (opcjonalne)

**Dla Interactive Brokers:**
```bash
pip install ib_insync
```

**Dla Binance:**
```bash
pip install python-binance
```

### 4. Pobierz pliki
```bash
git clone https://github.com/your-repo/trading-system.git
cd trading-system
```

**Struktura plików:**
```
trading-system/
├── trading_system.py          # Główny kod systemu
├── config.py                  # Konfiguracja
├── data_loader.py             # Ładowanie danych
├── backtest_runner.py         # Skrypt do backtestów
├── live_trader.py             # Skrypt live trading
├── requirements.txt           # Zależności
└── README.md                  # Ta dokumentacja
```

---

## 🚀 Szybki start

### Backtest na danych historycznych

```python
from trading_system import walk_forward_backtest, build_features, build_labels
import pandas as pd

# 1. Załaduj dane
data_dict = {}
for symbol in ['AAPL', 'MSFT', 'GOOGL']:
    df = pd.read_csv(f'data/{symbol}.csv', index_col=0, parse_dates=True)
    df = build_features(df)
    df['label'] = build_labels(df)
    data_dict[symbol] = df

# 2. Uruchom backtest
portfolio = walk_forward_backtest(
    data_dict,
    start_capital=100_000,
    train_window=252,      # 1 rok trenowania
    test_window=60,        # 3 miesiące testowania
    risk_pct=0.01,         # 1% ryzyka per trade
    use_risk_parity=True   # Włącz risk parity
)

# 3. Zobacz wyniki
print(portfolio.get_metrics())
```

### Live Trading - IBKR

```python
from trading_system import IBKRConnector

# 1. Połącz z TWS
ibkr = IBKRConnector(
    host='127.0.0.1',
    port=7497,        # Paper trading
    client_id=1
)
ibkr.connect()

# 2. Złóż zlecenie
ibkr.place_order('AAPL', 'BUY', 100)
```

### Live Trading - Binance

```python
from trading_system import BinanceConnector

# 1. Połącz z Binance
binance = BinanceConnector(
    api_key='YOUR_API_KEY',
    api_secret='YOUR_API_SECRET',
    testnet=True  # Użyj testnetu!
)
binance.connect()

# 2. Złóż zlecenie
binance.place_order('BTCUSDT', 'BUY', 0.01)
```

---

## ⚙️ Konfiguracja

### config.py

```python
# Capital & Risk
START_CAPITAL = 100_000
RISK_PER_TRADE = 0.01      # 1% kapitału per trade
VOL_TARGET = 0.10           # 10% target volatility
MAX_POSITIONS = 10

# ML Training
TRAIN_WINDOW = 252          # Dni do trenowania
TEST_WINDOW = 60            # Dni do testowania
RETRAIN_FREQUENCY = 60      # Co ile dni retrenować

# Risk Parity
USE_RISK_PARITY = True
LOOKBACK_CORRELATION = 60   # Dni do kalkulacji korelacji

# Regime Detection
VOL_LOOKBACK = 20
TREND_LOOKBACK = 50

# Live Trading
LIVE_MODE = False           # Ustaw True dla live
BROKER = 'IBKR'             # 'IBKR' lub 'BINANCE'

# IBKR Settings
IBKR_HOST = '127.0.0.1'
IBKR_PORT = 7497            # 7497=paper, 7496=live
IBKR_CLIENT_ID = 1

# Binance Settings
BINANCE_API_KEY = 'your_key'
BINANCE_API_SECRET = 'your_secret'
BINANCE_TESTNET = True

# Alerts
ALERT_DRAWDOWN = 0.05       # Alert przy 5% DD
ALERT_EMAIL = 'your@email.com'
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
```

---

## 🏗️ Architektura

### 1. Data Pipeline
```
Raw Data → build_features() → build_labels() → ML Training
```

### 2. ML Model
- **Algorithm:** Random Forest Classifier
- **Purpose:** Filtrowanie sygnałów (nie generowanie!)
- **Features:** 9 wskaźników technicznych
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

1. **Zainstaluj TWS lub IB Gateway**
   - Download: https://www.interactivebrokers.com/

2. **Włącz API**
   - TWS → File → Global Configuration → API → Settings
   - Enable ActiveX and Socket Clients
   - Socket port: 7497 (paper) / 7496 (live)

3. **Uruchom system**
```bash
python live_trader.py --broker ibkr --paper
```

### Binance Setup

1. **Stwórz API keys**
   - https://www.binance.com/en/my/settings/api-management

2. **Włącz testnet (opcjonalne)**
   - https://testnet.binance.vision/

3. **Uruchom system**
```bash
python live_trader.py --broker binance --testnet
```

---

## 🎛️ Parametry

### Podstawowe

| Parameter | Default | Description |
|-----------|---------|-------------|
| `start_capital` | 100,000 | Kapitał początkowy |
| `risk_pct` | 0.01 | Ryzyko per trade (1%) |
| `vol_target` | 0.10 | Target volatility (10%) |
| `max_positions` | 10 | Max otwartych pozycji |

### ML Model

| Parameter | Default | Description |
|-----------|---------|-------------|
| `n_estimators` | 200 | Liczba drzew RF |
| `max_depth` | 6 | Głębokość drzew |
| `train_window` | 252 | Okno trenowania (dni) |
| `test_window` | 60 | Okno testowania (dni) |

### Risk Parity

| Parameter | Default | Description |
|-----------|---------|-------------|
| `lookback` | 60 | Okno korelacji (dni) |
| `max_weight` | 0.5 | Max waga na instrument |

### Stop Loss / Take Profit

| Parameter | Default | Description |
|-----------|---------|-------------|
| `stop_loss` | 2 × ATR | Stop loss distance |
| `take_profit` | 4 × ATR | Take profit distance |

---

## 🔍 Troubleshooting

### Problem: "Model not trained"
**Rozwiązanie:** Zwiększ `train_window` lub zmniejsz liczbę symboli

### Problem: "IBKR connection failed"
**Rozwiązanie:**
1. Sprawdź czy TWS/Gateway jest uruchomiony
2. Zweryfikuj port (7497/7496)
3. Włącz API w ustawieniach TWS

### Problem: "Binance API error"
**Rozwiązanie:**
1. Sprawdź API key & secret
2. Włącz spot trading w ustawieniach API
3. Dodaj whitelist IP (opcjonalne)

### Problem: "No trades executed"
**Rozwiązanie:**
1. Zmniejsz `ML_prob` threshold (np. 0.5)
2. Sprawdź czy dane mają poprawne kolumny (OHLCV)
3. Zwiększ liczbę symboli w portfolio

### Problem: "High drawdown"
**Rozwiązanie:**
1. Zmniejsz `risk_pct` (np. 0.005)
2. Zwiększ `train_window` dla lepszego ML
3. Włącz `use_risk_parity=True`

---

## 📊 Performance Metrics

System generuje następujące metryki:

- **Total Return** - całkowity zwrot
- **Win Rate** - % zyskownych transakcji
- **Profit Factor** - avg_win / avg_loss
- **Max Drawdown** - największy spadek equity
- **Sharpe Ratio** - risk-adjusted returns
- **Number of Trades** - liczba wykonanych transakcji

---

## ⚠️ Disclaimer

**Ten system jest narzędziem edukacyjnym.**

- Trading wiąże się z ryzykiem utraty kapitału
- Zawsze testuj na paper trading przed live
- Nie inwestuj więcej niż możesz stracić
- Autor nie ponosi odpowiedzialności za straty

---

## 📝 TODO

- [ ] Telegram bot integration
- [ ] Real-time dashboard (Streamlit)
- [ ] More ML models (LightGBM, XGBoost)
- [ ] Options trading support
- [ ] Advanced portfolio optimization (Black-Litterman)

---

## 📞 Support

- **Issues:** GitHub Issues
- **Email:** support@tradingsystem.com
- **Discord:** [Join our community]

---

## 📄 License

MIT License - użyj swobodnie, na własną odpowiedzialność.

---

**Made with ❤️ for algorithmic traders**

*Last updated: December 2025*