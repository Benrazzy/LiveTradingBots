#!/usr/bin/env python3
# Heikin-Ashi Live Trading Bot for Alpaca Paper Account - Fixed Version
# Original backtest: https://github.com/je-suis-tm/quant-trading/blob/master/Heikin-Ashi backtest.py
# Adapted for live trading. PAPER ONLY. FOR NOVICE USERS.
# Run: pip install alpaca-py pandas numpy yfinance first
# Edit keys below. Ctrl+C to stop.

import os
import sys
import json
import time
import pandas as pd
import numpy as np
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest, GetOrdersRequest
from alpaca.trading.enums import OrderSide, TimeInForce, QueryOrderStatus
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
import yfinance as yf  # fallback

# ========== USER CONFIG - EDIT HERE ==========
# Find secret.json relative to repo root (2 levels up from this script)
script_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.join(script_dir, '..', '..', '..')
key_path = os.path.join(repo_root, 'secret.json')
key_name = 'alpaca_heikin_ashi'

SYMBOL = "NVDA"
TIMEFRAME = TimeFrame.Minute  # 1min bars
LOOKBACK_BARS = 100  # Recent bars for HA calculation
MAX_POSITIONS = 3
RISK_PCT = 0.10  # 10% equity per trade
STOP_LOSS_PCT = 0.05  # 5% stop loss
TAKE_PROFIT_PCT = 0.10  # 10% take profit
DRY_RUN = False  # True: simulate orders, False: live submit
SLEEP_SEC = 60  # Check every minute
# ============================================

# Load API keys
try:
    with open(key_path, "r") as f:
        api_setup = json.load(f)[key_name]
    API_KEY = api_setup['api_key']
    API_SECRET = api_setup['secret_key']
    print(f"✓ Loaded API keys from {key_path}")
except FileNotFoundError:
    print(f"✗ ERROR: {key_path} not found. Did you run install.sh and add keys to secret.json?")
    sys.exit(1)
except KeyError:
    print(f"✗ ERROR: '{key_name}' key not found in secret.json")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"✗ ERROR: {key_path} is not valid JSON")
    sys.exit(1)

# Initialize Alpaca clients
try:
    trading_client = TradingClient(API_KEY, API_SECRET, paper=True)
    data_client = StockHistoricalDataClient(API_KEY, API_SECRET)
    # Test connection
    account = trading_client.get_account()
    print(f"✓ Connected to Alpaca (Paper: {account.account_number})")
except Exception as e:
    print(f"✗ ERROR: Failed to connect to Alpaca: {e}")
    sys.exit(1)

mode = "DRY RUN (SIMULATION)" if DRY_RUN else "LIVE PAPER TRADING"
print(f"{mode} MODE")
print("Symbol: %s, Risk: %.0f%%, Max Pos: %d" % (SYMBOL, RISK_PCT*100, MAX_POSITIONS))
print("Press Ctrl+C to stop.")

def heikin_ashi(df):
    """HA transformation from original script"""
    df = df.copy()
    df.reset_index(inplace=True)
    df['HA_close'] = (df['open'] + df['close'] + df['high'] + df['low']) / 4
    df['HA_open'] = 0.0
    df.loc[0, 'HA_open'] = df.loc[0, 'open']
    for n in range(1, len(df)):
        df.loc[n, 'HA_open'] = (df.loc[n-1, 'HA_open'] + df.loc[n-1, 'HA_close']) / 2
    temp = pd.concat([df['HA_open'], df['HA_close'], df['low'], df['high']], axis=1)
    df['HA_high'] = temp.max(axis=1)
    df['HA_low'] = temp.min(axis=1)
    return df

def generate_signal(df):
    """Signal logic from original (simplified for last bar)"""
    ha_df = heikin_ashi(df)
    n = len(ha_df) - 1
    if n < 1:
        return 0
    # Long trigger (bearish marubozu continuation)
    if (ha_df.loc[n, 'HA_open'] > ha_df.loc[n, 'HA_close'] and 
        ha_df.loc[n, 'HA_open'] == ha_df.loc[n, 'HA_high'] and
        abs(ha_df.loc[n, 'HA_open'] - ha_df.loc[n, 'HA_close']) > abs(ha_df.loc[n-1, 'HA_open'] - ha_df.loc[n-1, 'HA_close']) and
        ha_df.loc[n-1, 'HA_open'] > ha_df.loc[n-1, 'HA_close']):
        return 1  # Long
    # Exit long
    elif (ha_df.loc[n, 'HA_open'] < ha_df.loc[n, 'HA_close'] and 
          ha_df.loc[n, 'HA_open'] == ha_df.loc[n, 'HA_low'] and
          ha_df.loc[n-1, 'HA_open'] < ha_df.loc[n-1, 'HA_close']):
        return -1  # Exit
    return 0

def get_qty(equity, price):
    """Risk-based qty"""
    risk_amount = equity * RISK_PCT
    qty = int(risk_amount / price)
    return min(qty, equity // price)  # Whole shares

def close_all_positions():
    """Market close all NVDA positions"""
    positions = trading_client.get_all_positions()
    for pos in positions:
        if pos.symbol == SYMBOL:
            side = OrderSide.SELL if pos.qty > '0' else OrderSide.BUY
            qty = abs(int(pos.qty))
            if qty > 0 and not DRY_RUN:
                order = MarketOrderRequest(symbol=SYMBOL, qty=str(qty), side=side, time_in_force=TimeInForce.GTC)
                trading_client.submit_order(order)
            print(f"Closed {qty} {SYMBOL} {side}")

try:
    while True:
        try:
            # Get account equity
            account = trading_client.get_account()
            equity = float(account.equity)
            print(f"\n--- {time.strftime('%Y-%m-%d %H:%M:%S')} | Equity: ${equity:.2f} ---")

            # Get NVDA positions
            positions = trading_client.get_all_positions()
            nvda_pos = [p for p in positions if p.symbol == SYMBOL]
            current_qty = sum(int(p.qty) for p in nvda_pos) if nvda_pos else 0
            print(f"Current {SYMBOL} qty: {current_qty}")

            if abs(current_qty) >= MAX_POSITIONS:
                print(f"Max positions reached ({MAX_POSITIONS}). Skipping.")
                time.sleep(SLEEP_SEC)
                continue

            # Fetch recent 1min bars
            try:
                request = StockBarsRequest(symbol_or_symbols=[SYMBOL], timeframe=TIMEFRAME, limit=LOOKBACK_BARS)
                bars = data_client.get_stock_bars(request)
                if not bars or len(bars.df) == 0:
                    print("No bars data. Retrying...")
                    time.sleep(SLEEP_SEC)
                    continue
                df = bars.df
                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = [col[0] for col in df.columns]
                
                # Ensure required columns
                required_cols = ['open', 'close', 'high', 'low']
                if not all(col in df.columns for col in required_cols):
                    print(f"Missing columns. Got: {list(df.columns)}")
                    time.sleep(SLEEP_SEC)
                    continue
                    
                latest_price = float(df['close'].iloc[-1])
                print(f"Latest {SYMBOL}: ${latest_price:.2f}")
            except Exception as e:
                print(f"Error fetching bars: {e}")
                time.sleep(SLEEP_SEC)
                continue

            # Generate signal
            signal = generate_signal(df)
            print(f"HA Signal: {signal}")

            if signal == 1 and current_qty < MAX_POSITIONS:  # New long
                qty = get_qty(equity, latest_price)
                if qty > 0:
                    stop_price = latest_price * (1 - STOP_LOSS_PCT)
                    profit_price = latest_price * (1 + TAKE_PROFIT_PCT)
                    if not DRY_RUN:
                        try:
                            entry_order = MarketOrderRequest(symbol=SYMBOL, qty=str(qty), side=OrderSide.BUY, time_in_force=TimeInForce.GTC)
                            trading_client.submit_order(entry_order)
                            print(f"✓ Submitted BUY {qty} {SYMBOL} @market")
                        except Exception as e:
                            print(f"✗ Failed to place order: {e}")
                    else:
                        print(f"DRY: Would BUY {qty} {SYMBOL} @${latest_price:.2f}, stop ${stop_price:.2f}, TP ${profit_price:.2f}")

            elif signal == -1 and current_qty > 0:  # Exit long
                close_all_positions()

            time.sleep(SLEEP_SEC)
            
        except Exception as e:
            print(f"✗ Loop error: {e}")
            time.sleep(SLEEP_SEC)
            continue

except KeyboardInterrupt:
    print("\n✓ Bot stopped by user.")
    close_all_positions()