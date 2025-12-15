#!/bin/bash

# Advanced Trading System v2.0 - Installation Script
# Run: bash install.sh

echo "======================================================================"
echo "🚀 Advanced Trading System v2.0 - Installation"
echo "======================================================================"
echo ""

# Check Python version
echo "📋 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "   Found: Python $python_version"

# Check if Python 3.8+
required_version="3.8"
if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python 3.8+ required (found $python_version)"
    exit 1
fi
echo "✅ Python version OK"
echo ""

# Create virtual environment (optional)
read -p "📦 Create virtual environment? (recommended) [y/N]: " create_venv
if [[ $create_venv =~ ^[Yy]$ ]]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
    echo "💡 Activate with: source venv/bin/activate (Linux/Mac) or venv\\Scripts\\activate (Windows)"
    
    # Activate venv
    source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null
    echo ""
fi

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip -q
echo "✅ pip upgraded"
echo ""

# Install core dependencies
echo "📦 Installing core dependencies..."
echo "   This may take a few minutes..."
pip install numpy pandas scikit-learn scipy matplotlib -q
if [ $? -eq 0 ]; then
    echo "✅ Core dependencies installed"
else
    echo "❌ Failed to install core dependencies"
    exit 1
fi
echo ""

# Install data sources
echo "📦 Installing data sources..."
pip install yfinance -q
echo "✅ Yahoo Finance support installed"
echo ""

# Optional: Live trading dependencies
read -p "📡 Install live trading dependencies? (IBKR, Binance) [y/N]: " install_live
if [[ $install_live =~ ^[Yy]$ ]]; then
    echo "Installing live trading libraries..."
    pip install ib_insync python-binance -q
    echo "✅ Live trading support installed"
fi
echo ""

# Optional: Advanced ML models
read -p "🧠 Install advanced ML models? (XGBoost, LightGBM) [y/N]: " install_ml
if [[ $install_ml =~ ^[Yy]$ ]]; then
    echo "Installing ML libraries..."
    pip install xgboost lightgbm -q
    echo "✅ Advanced ML models installed"
fi
echo ""

# Create data directory
echo "📁 Creating directories..."
mkdir -p data
mkdir -p logs
mkdir -p results
echo "✅ Directories created"
echo ""

# Download sample data
read -p "📥 Download sample data for testing? [y/N]: " download_data
if [[ $download_data =~ ^[Yy]$ ]]; then
    echo "Downloading sample data..."
    python3 -c "
import yfinance as yf
import pandas as pd

symbols = ['AAPL', 'MSFT', 'GOOGL']
print('Downloading sample data for:', ', '.join(symbols))

for symbol in symbols:
    print(f'  Downloading {symbol}...')
    df = yf.download(symbol, start='2020-01-01', end='2023-12-31', progress=False)
    df.to_csv(f'data/{symbol}.csv')
    print(f'  ✅ {symbol} saved to data/{symbol}.csv')

print('✅ Sample data downloaded')
"
fi
echo ""

# Verify installation
echo "🔍 Verifying installation..."
python3 -c "
import numpy
import pandas
import sklearn
import scipy
import matplotlib
print('✅ All core packages imported successfully')
" 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✅ Installation verified"
else
    echo "⚠️  Some packages may not have installed correctly"
fi
echo ""

# Create .env file
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file for credentials..."
    cat > .env << EOF
# IBKR Configuration
IBKR_HOST=127.0.0.1
IBKR_PORT=7497
IBKR_CLIENT_ID=1

# Binance Configuration
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
BINANCE_TESTNET=True

# Email Notifications
EMAIL_FROM=system@trading.com
EMAIL_TO=your@email.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your@gmail.com
SMTP_PASSWORD=your_app_password
EOF
    echo "✅ .env file created (edit with your credentials)"
fi
echo ""

# Print summary
echo "======================================================================"
echo "✅ Installation Complete!"
echo "======================================================================"
echo ""
echo "📚 Next Steps:"
echo ""
echo "1. Review configuration:"
echo "   nano config.py"
echo ""
echo "2. Run your first backtest:"
echo "   python backtest_runner.py"
echo ""
echo "3. For paper trading:"
echo "   python live_trader.py --broker ibkr --paper"
echo ""
echo "4. Read documentation:"
echo "   cat README.md"
echo "   cat QUICKSTART.md"
echo ""
echo "======================================================================"
echo "⚠️  Important Reminders:"
echo "======================================================================"
echo "• Always test strategies with backtests first"
echo "• Use paper trading before going live"
echo "• Never risk more than you can afford to lose"
echo "• Monitor your system regularly"
echo ""
echo "📧 Support: support@tradingsystem.com"
echo "📖 Docs: https://github.com/your-repo/trading-system"
echo ""
echo "Good luck with your trading! 🚀"
echo ""
