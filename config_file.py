"""
Configuration file for Advanced Trading System v2.0
Edit these parameters to customize your trading strategy
"""

# ============================================================================
# CAPITAL & RISK MANAGEMENT
# ============================================================================

START_CAPITAL = 100_000         # Starting capital in USD
RISK_PER_TRADE = 0.01          # Risk per trade (1% of capital)
VOL_TARGET = 0.10              # Target portfolio volatility (10% annual)
MAX_POSITIONS = 10             # Maximum concurrent positions
MAX_POSITION_SIZE = 0.20       # Max 20% of capital per position

# ============================================================================
# MACHINE LEARNING
# ============================================================================

# Model parameters
ML_MODEL_TYPE = 'RandomForest'  # 'RandomForest', 'XGBoost', 'LightGBM'
N_ESTIMATORS = 200             # Number of trees
MAX_DEPTH = 6                  # Maximum tree depth
MIN_SAMPLES_SPLIT = 20         # Min samples for split

# Training parameters
TRAIN_WINDOW = 252             # Training window (days) - 1 year
TEST_WINDOW = 60               # Testing window (days) - 3 months
RETRAIN_FREQUENCY = 60         # Retrain every N days
MIN_TRAIN_SAMPLES = 50         # Minimum samples for training

# Signal threshold
ML_PROB_THRESHOLD = 0.6        # Minimum probability for trade entry

# ============================================================================
# RISK PARITY
# ============================================================================

USE_RISK_PARITY = True         # Enable risk parity optimization
LOOKBACK_CORRELATION = 60      # Days for correlation calculation
MAX_WEIGHT_PER_ASSET = 0.50    # Maximum weight per asset (50%)
MIN_WEIGHT_PER_ASSET = 0.00    # Minimum weight per asset (0%)

# ============================================================================
# REGIME DETECTION
# ============================================================================

VOL_LOOKBACK = 20              # Lookback for volatility regime
TREND_LOOKBACK = 50            # Lookback for trend strength
VOL_PERCENTILE_HIGH = 0.7      # High volatility threshold
TREND_PERCENTILE_STRONG = 0.6  # Strong trend threshold

# Trading by regime
TRADE_IN_CHOPPY = False        # Trade in choppy markets?
REDUCE_SIZE_HIGH_VOL = True    # Reduce size in high vol?

# ============================================================================
# TECHNICAL INDICATORS
# ============================================================================

EMA_FAST = 50                  # Fast EMA period
EMA_SLOW = 200                 # Slow EMA period
ATR_PERIOD = 14                # ATR calculation period
MACD_FAST = 12                 # MACD fast period
MACD_SLOW = 26                 # MACD slow period
MACD_SIGNAL = 9                # MACD signal period

# ============================================================================
# STOP LOSS / TAKE PROFIT
# ============================================================================

STOP_LOSS_ATR = 2.0            # Stop loss = entry ± 2×ATR
TAKE_PROFIT_ATR = 4.0          # Take profit = entry ± 4×ATR
USE_TRAILING_STOP = False      # Enable trailing stops
TRAILING_STOP_ATR = 3.0        # Trailing stop distance

# ============================================================================
# COSTS
# ============================================================================

COMMISSION_RATE = 0.001        # Commission per side (0.1%)
SLIPPAGE_BPS = 5               # Slippage in basis points (0.05%)

# ============================================================================
# LIVE TRADING
# ============================================================================

LIVE_MODE = False              # Set to True for live trading
PAPER_TRADING = True           # Use paper trading first!
BROKER = 'IBKR'                # 'IBKR' or 'BINANCE'

# Update frequency
UPDATE_INTERVAL = 60           # Check for signals every N seconds
REBALANCE_INTERVAL = 3600      # Rebalance portfolio every N seconds

# ============================================================================
# INTERACTIVE BROKERS (IBKR)
# ============================================================================

IBKR_HOST = '127.0.0.1'
IBKR_PORT = 7497               # 7497 = paper trading, 7496 = live
IBKR_CLIENT_ID = 1
IBKR_ACCOUNT = ''              # Leave empty for default account

# Order types
IBKR_ORDER_TYPE = 'MKT'        # 'MKT' or 'LMT'
IBKR_TIMEOUT = 10              # Order timeout in seconds

# ============================================================================
# BINANCE
# ============================================================================

BINANCE_API_KEY = ''           # Your Binance API key
BINANCE_API_SECRET = ''        # Your Binance API secret
BINANCE_TESTNET = True         # Use testnet (recommended!)

# Binance settings
BINANCE_RECV_WINDOW = 5000     # API receive window
BINANCE_ORDER_TYPE = 'MARKET'  # 'MARKET' or 'LIMIT'

# ============================================================================
# MONITORING & ALERTS
# ============================================================================

# Drawdown alerts
ALERT_DRAWDOWN = 0.05          # Alert at 5% drawdown
ALERT_DRAWDOWN_CRITICAL = 0.10 # Critical alert at 10%

# Capital alerts
ALERT_CAPITAL_LOW = 0.80       # Alert when capital < 80%
ALERT_CAPITAL_CRITICAL = 0.70  # Critical when capital < 70%

# Exposure alerts
ALERT_EXPOSURE_HIGH = 1.5      # Alert when exposure > 1.5x capital
ALERT_EXPOSURE_CRITICAL = 2.0  # Critical when exposure > 2x capital

# ============================================================================
# EMAIL NOTIFICATIONS
# ============================================================================

EMAIL_ENABLED = False          # Enable email alerts
EMAIL_FROM = 'system@trading.com'
EMAIL_TO = 'your@email.com'
EMAIL_SUBJECT_PREFIX = '[Trading System]'

# SMTP settings
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USERNAME = 'your@gmail.com'
SMTP_PASSWORD = 'your_app_password'
SMTP_USE_TLS = True

# ============================================================================
# TELEGRAM NOTIFICATIONS (Optional)
# ============================================================================

TELEGRAM_ENABLED = False       # Enable Telegram alerts
TELEGRAM_BOT_TOKEN = ''        # Your bot token
TELEGRAM_CHAT_ID = ''          # Your chat ID

# ============================================================================
# DATA SOURCES
# ============================================================================

# Symbols to trade
SYMBOLS = [
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA',
    'META', 'NVDA', 'JPM', 'V', 'WMT'
]

# Data parameters
DATA_TIMEFRAME = '1d'          # '1m', '5m', '15m', '1h', '1d'
DATA_START_DATE = '2020-01-01'
DATA_END_DATE = None           # None = today

# Data source
DATA_SOURCE = 'yahoo'          # 'yahoo', 'alpaca', 'binance', 'csv'
DATA_PATH = './data/'          # Path for CSV files

# ============================================================================
# BACKTEST SETTINGS
# ============================================================================

BACKTEST_START = '2020-01-01'
BACKTEST_END = '2023-12-31'
MONTE_CARLO_RUNS = 1000        # Number of MC simulations

# ============================================================================
# LOGGING
# ============================================================================

LOG_LEVEL = 'INFO'             # 'DEBUG', 'INFO', 'WARNING', 'ERROR'
LOG_FILE = 'trading_system.log'
LOG_TO_CONSOLE = True
LOG_TO_FILE = True

# ============================================================================
# PERFORMANCE
# ============================================================================

N_JOBS = -1                    # CPU cores for ML (-1 = all)
CACHE_DATA = True              # Cache processed data
RANDOM_SEED = 42               # For reproducibility

# ============================================================================
# FEATURES FOR ML MODEL
# ============================================================================

FEATURES = [
    'price_ema200',
    'ema_ratio',
    'macd_hist',
    'macd_delta',
    'atr_norm',
    'ret_1d',
    'ret_5d',
    'ret_20d',
    'volatility'
]

# Optional features (if volume data available)
OPTIONAL_FEATURES = [
    'volume_ratio'
]
