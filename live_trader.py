"""
Live trading script for Advanced Trading System v2.0
Run: python live_trader.py --broker ibkr --paper

⚠️  IMPORTANT: Always test on paper trading first!
"""

import argparse
import time
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Import local modules
import config
from trading_system import (
    build_features, build_labels, MLModel, Portfolio, Position,
    position_size, long_signal, short_signal, RegimeDetector,
    RiskParityOptimizer, MonitoringSystem, IBKRConnector, BinanceConnector
)
from data_loader import load_data

# ============================================================================
# LIVE TRADER CLASS
# ============================================================================

class LiveTrader:
    """Main live trading orchestrator"""
    
    def __init__(self, broker='ibkr', paper_trading=True):
        self.broker = broker.lower()
        self.paper_trading = paper_trading
        
        # Initialize components
        self.portfolio = Portfolio(
            config.START_CAPITAL,
            vol_target=config.VOL_TARGET,
            max_positions=config.MAX_POSITIONS
        )
        
        self.ml_model = MLModel()
        self.regime_detector = RegimeDetector()
        self.risk_parity = RiskParityOptimizer() if config.USE_RISK_PARITY else None
        self.monitor = MonitoringSystem(self.portfolio, config.ALERT_DRAWDOWN)
        
        # Initialize broker connection
        self.connector = None
        self.is_connected = False
        
        # State
        self.symbols = config.SYMBOLS
        self.last_update = None
        self.last_rebalance = None
        self.weights = {sym: 1/len(self.symbols) for sym in self.symbols}
        
        print("\n" + "="*70)
        print("🤖 LIVE TRADER INITIALIZED")
        print("="*70)
        print(f"Broker: {self.broker.upper()}")
        print(f"Mode: {'PAPER TRADING' if paper_trading else '⚠️  LIVE TRADING'}")
        print(f"Symbols: {', '.join(self.symbols)}")
        print(f"Capital: ${config.START_CAPITAL:,.0f}")
        print("="*70 + "\n")
    
    def connect_broker(self):
        """Connect to broker"""
        print(f"🔌 Connecting to {self.broker.upper()}...")
        
        if self.broker == 'ibkr':
            self.connector = IBKRConnector(
                host=config.IBKR_HOST,
                port=config.IBKR_PORT,
                client_id=config.IBKR_CLIENT_ID
            )
            self.connector.connect()
            self.is_connected = self.connector.connected
            
        elif self.broker == 'binance':
            self.connector = BinanceConnector(
                api_key=config.BINANCE_API_KEY,
                api_secret=config.BINANCE_API_SECRET,
                testnet=config.BINANCE_TESTNET
            )
            self.connector.connect()
            self.is_connected = self.connector.connected
            
        else:
            print(f"❌ Unknown broker: {self.broker}")
            return False
        
        if self.is_connected:
            print("✅ Connected to broker!")
        else:
            print("❌ Failed to connect to broker")
        
        return self.is_connected
    
    def train_model(self):
        """Train ML model on historical data"""
        print("\n🧠 Training ML model...")
        
        # Load historical data
        end_date = datetime.now()
        start_date = end_date - timedelta(days=config.TRAIN_WINDOW + 100)
        
        data_dict = load_data(
            self.symbols,
            start_date.strftime('%Y-%m-%d'),
            end_date.strftime('%Y-%m-%d'),
            source=config.DATA_SOURCE
        )
        
        if not data_dict:
            print("❌ Failed to load training data")
            return False
        
        # Build features and labels
        X_train_list, y_train_list = [], []
        
        for symbol, df in data_dict.items():
            df = build_features(df)
            df['label'] = build_labels(df)
            df = df.dropna()
            
            if len(df) > 100:
                X_train_list.append(df[config.FEATURES])
                y_train_list.append(df['label'])
                data_dict[symbol] = df  # Store for weights calculation
        
        if not X_train_list:
            print("❌ No training data available")
            return False
        
        X_train = pd.concat(X_train_list)
        y_train = pd.concat(y_train_list)
        
        # Train model
        self.ml_model.train(X_train, y_train)
        print(f"✅ Model trained on {len(y_train)} samples")
        
        # Calculate risk parity weights
        if self.risk_parity:
            returns_df = pd.DataFrame({
                sym: data_dict[sym]['ret_1d'].tail(config.LOOKBACK_CORRELATION)
                for sym in self.symbols if sym in data_dict
            })
            self.weights = self.risk_parity.calculate_weights(returns_df)
            print(f"✅ Risk parity weights calculated")
        
        return True
    
    def get_current_data(self):
        """Get current market data for all symbols"""
        # In real implementation, fetch from broker API
        # For now, fetch recent bars
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=100)
        
        data_dict = load_data(
            self.symbols,
            start_date.strftime('%Y-%m-%d'),
            end_date.strftime('%Y-%m-%d'),
            source=config.DATA_SOURCE
        )
        
        # Build features
        for symbol in data_dict:
            data_dict[symbol] = build_features(data_dict[symbol])
        
        return data_dict
    
    def check_signals(self, data_dict):
        """Check for entry/exit signals"""
        signals = []
        current_time = datetime.now()
        
        for symbol, df in data_dict.items():
            if len(df) < 50:
                continue
            
            # Get latest data
            row = df.iloc[-1]
            
            # Detect regime
            regime = self.regime_detector.detect_regime(df.tail(100)).iloc[-1]
            
            # Get ML probability
            try:
                prob = self.ml_model.predict_prob(row[config.FEATURES].to_frame().T)[0]
            except:
                prob = 0.5
            
            # Check for existing position
            has_position = any(p.symbol == symbol for p in self.portfolio.positions)
            
            # Entry signals
            if not has_position and len(self.portfolio.positions) < config.MAX_POSITIONS:
                
                # Long signal
                if long_signal(row, prob, regime):
                    weight = self.weights.get(symbol, 1/len(self.symbols))
                    size = position_size(
                        self.portfolio.capital,
                        row['atr'],
                        row['close'],
                        config.VOL_TARGET,
                        config.RISK_PER_TRADE,
                        weight
                    )
                    
                    if size > 0:
                        signals.append({
                            'symbol': symbol,
                            'action': 'OPEN_LONG',
                            'size': size,
                            'price': row['close'],
                            'stop': row['close'] - config.STOP_LOSS_ATR * row['atr'],
                            'tp': row['close'] + config.TAKE_PROFIT_ATR * row['atr'],
                            'prob': prob,
                            'regime': regime
                        })
                
                # Short signal
                elif short_signal(row, prob, regime):
                    weight = self.weights.get(symbol, 1/len(self.symbols))
                    size = position_size(
                        self.portfolio.capital,
                        row['atr'],
                        row['close'],
                        config.VOL_TARGET,
                        config.RISK_PER_TRADE,
                        weight
                    )
                    
                    if size > 0:
                        signals.append({
                            'symbol': symbol,
                            'action': 'OPEN_SHORT',
                            'size': size,
                            'price': row['close'],
                            'stop': row['close'] + config.STOP_LOSS_ATR * row['atr'],
                            'tp': row['close'] - config.TAKE_PROFIT_ATR * row['atr'],
                            'prob': prob,
                            'regime': regime
                        })
            
            # Exit signals (check stops)
            for pos in [p for p in self.portfolio.positions if p.symbol == symbol]:
                current_price = row['close']
                
                # Stop loss hit
                if (pos.side == 'long' and current_price <= pos.stop) or \
                   (pos.side == 'short' and current_price >= pos.stop):
                    signals.append({
                        'symbol': symbol,
                        'action': 'CLOSE',
                        'position': pos,
                        'price': current_price,
                        'reason': 'STOP_LOSS'
                    })
                
                # Take profit hit
                elif (pos.side == 'long' and current_price >= pos.tp) or \
                     (pos.side == 'short' and current_price <= pos.tp):
                    signals.append({
                        'symbol': symbol,
                        'action': 'CLOSE',
                        'position': pos,
                        'price': current_price,
                        'reason': 'TAKE_PROFIT'
                    })
        
        return signals
    
    def execute_signals(self, signals):
        """Execute trading signals"""
        for signal in signals:
            try:
                if signal['action'] == 'OPEN_LONG':
                    print(f"\n📈 LONG SIGNAL: {signal['symbol']}")
                    print(f"   Price: ${signal['price']:.2f}")
                    print(f"   Size: {signal['size']:.2f}")
                    print(f"   Stop: ${signal['stop']:.2f}")
                    print(f"   TP: ${signal['tp']:.2f}")
                    print(f"   Prob: {signal['prob']:.2%}")
                    print(f"   Regime: {signal['regime']}")
                    
                    if not self.paper_trading and self.connector:
                        self.connector.place_order(signal['symbol'], 'BUY', signal['size'])
                    
                    # Add to portfolio
                    self.portfolio.positions.append(
                        Position(
                            signal['symbol'],
                            'long',
                            signal['price'],
                            signal['size'],
                            signal['stop'],
                            signal['tp'],
                            datetime.now()
                        )
                    )
                
                elif signal['action'] == 'OPEN_SHORT':
                    print(f"\n📉 SHORT SIGNAL: {signal['symbol']}")
                    print(f"   Price: ${signal['price']:.2f}")
                    print(f"   Size: {signal['size']:.2f}")
                    print(f"   Stop: ${signal['stop']:.2f}")
                    print(f"   TP: ${signal['tp']:.2f}")
                    print(f"   Prob: {signal['prob']:.2%}")
                    print(f"   Regime: {signal['regime']}")
                    
                    if not self.paper_trading and self.connector:
                        self.connector.place_order(signal['symbol'], 'SELL', signal['size'])
                    
                    # Add to portfolio
                    self.portfolio.positions.append(
                        Position(
                            signal['symbol'],
                            'short',
                            signal['price'],
                            signal['size'],
                            signal['stop'],
                            signal['tp'],
                            datetime.now()
                        )
                    )
                
                elif signal['action'] == 'CLOSE':
                    pos = signal['position']
                    print(f"\n🔴 CLOSING: {pos.symbol} {pos.side.upper()}")
                    print(f"   Reason: {signal['reason']}")
                    print(f"   Entry: ${pos.entry:.2f}")
                    print(f"   Exit: ${signal['price']:.2f}")
                    
                    if not self.paper_trading and self.connector:
                        side = 'SELL' if pos.side == 'long' else 'BUY'
                        self.connector.place_order(pos.symbol, side, pos.size)
                    
                    # Close position
                    pnl = self.portfolio.close_position(pos, signal['price'], signal['reason'])
                    print(f"   P&L: ${pnl:,.2f}")
            
            except Exception as e:
                print(f"❌ Error executing signal: {e}")
    
    def run(self):
        """Main trading loop"""
        # Initial setup
        if not self.is_connected:
            if not self.connect_broker():
                print("❌ Cannot start without broker connection")
                return
        
        # Train model
        if not self.train_model():
            print("❌ Cannot start without trained model")
            return
        
        print("\n✅ System ready! Starting trading loop...")
        print(f"⏰ Update interval: {config.UPDATE_INTERVAL}s")
        print("Press Ctrl+C to stop\n")
        
        iteration = 0
        
        try:
            while True:
                iteration += 1
                current_time = datetime.now()
                
                print(f"\n{'='*70}")
                print(f"🔄 Iteration {iteration} - {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
                print('='*70)
                
                # Get current data
                data_dict = self.get_current_data()
                
                if not data_dict:
                    print("⚠️  No data available, skipping...")
                    time.sleep(config.UPDATE_INTERVAL)
                    continue
                
                # Update equity
                prices = {sym: df.iloc[-1]['close'] for sym, df in data_dict.items()}
                self.portfolio.update_equity(prices, current_time)
                
                # Check signals
                signals = self.check_signals(data_dict)
                
                if signals:
                    print(f"\n📊 Found {len(signals)} signals")
                    self.execute_signals(signals)
                else:
                    print("\n⏸️  No signals")
                
                # Print status
                print(f"\n💰 Portfolio Status:")
                print(f"   Capital: ${self.portfolio.capital:,.2f}")
                print(f"   Positions: {len(self.portfolio.positions)}")
                print(f"   Trades today: {len([t for t in self.portfolio.trades if t.get('timestamp', None) and t['timestamp'].date() == current_time.date()])}")
                
                if self.portfolio.positions:
                    print(f"\n📋 Open Positions:")
                    for pos in self.portfolio.positions:
                        unrealized = (prices[pos.symbol] - pos.entry) * pos.size if pos.side == 'long' else (pos.entry - prices[pos.symbol]) * pos.size
                        print(f"   {pos.symbol} {pos.side.upper()}: ${unrealized:+,.2f}")
                
                # Check alerts
                self.monitor.check_alerts()
                
                # Retrain model periodically
                if iteration % (config.RETRAIN_FREQUENCY // (config.UPDATE_INTERVAL // 60)) == 0:
                    print("\n🔄 Retraining model...")
                    self.train_model()
                
                # Sleep until next update
                time.sleep(config.UPDATE_INTERVAL)
        
        except KeyboardInterrupt:
            print("\n\n⚠️  Stopping trading system...")
            self.cleanup()
    
    def cleanup(self):
        """Cleanup before exit"""
        print("\n🧹 Cleaning up...")
        
        # Close all positions if needed
        if self.portfolio.positions:
            print(f"⚠️  {len(self.portfolio.positions)} positions still open")
            response = input("Close all positions before exit? (y/n): ")
            
            if response.lower() == 'y':
                data_dict = self.get_current_data()
                prices = {sym: df.iloc[-1]['close'] for sym, df in data_dict.items()}
                
                for pos in self.portfolio.positions[:]:
                    price = prices.get(pos.symbol, pos.entry)
                    pnl = self.portfolio.close_position(pos, price, 'MANUAL_CLOSE')
                    print(f"Closed {pos.symbol} {pos.side}: P&L ${pnl:,.2f}")
        
        # Print final stats
        print("\n" + "="*70)
        print("📊 FINAL STATISTICS")
        print("="*70)
        metrics = self.portfolio.get_metrics()
        for key, value in metrics.items():
            if isinstance(value, float):
                print(f"{key}: {value:.4f}")
            else:
                print(f"{key}: {value}")
        
        print("\n✅ System stopped successfully")

# ============================================================================
# COMMAND LINE INTERFACE
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description='Live trading system')
    parser.add_argument('--broker', type=str, default='ibkr', 
                       choices=['ibkr', 'binance'], help='Broker to use')
    parser.add_argument('--paper', action='store_true', 
                       help='Use paper trading (highly recommended!)')
    parser.add_argument('--live', action='store_true', 
                       help='⚠️  Use LIVE trading (use at your own risk!)')
    
    args = parser.parse_args()
    
    # Safety check
    if args.live and not args.paper:
        print("\n" + "⚠️ "*25)
        print("YOU ARE ABOUT TO START LIVE TRADING WITH REAL MONEY!")
        print("⚠️ "*25)
        response = input("\nType 'I UNDERSTAND THE RISKS' to continue: ")
        
        if response != 'I UNDERSTAND THE RISKS':
            print("\n✅ Wise choice! Starting paper trading instead...")
            args.paper = True
    
    # Create and run trader
    trader = LiveTrader(broker=args.broker, paper_trading=args.paper)
    trader.run()

if __name__ == "__main__":
    main()
