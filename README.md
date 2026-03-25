# LiveTradingBots

_A simple automated trading bot library for live stock trading on Alpaca_

\
� Quick Start (5 minutes)
-------------

### 1️⃣ Clone Repository
```bash
git clone https://github.com/RobotTraders/LiveTradingBots.git
cd LiveTradingBots
```

### 2️⃣ Set Up Credentials
```bash
# Copy template to create your own secret.json
cp secret.template.json secret.json

# Edit secret.json and add your Alpaca API keys
# Get keys from: https://app.alpaca.markets/brokerage/account/api-keys
```

### 3️⃣ Install & Run
```bash
# Linux/macOS:
bash install.sh
bash code/run_alpaca_heikin_ashi.sh

# Windows (requires WSL or Git Bash):
# Run the same commands above
```

\
⭐ Alpaca Heikin-Ashi Bot
-------------
A live trading bot using **Heikin-Ashi price action** for stock trading on **Alpaca Paper Account** (NO REAL MONEY).

**Features:**
- Heikin-Ashi candle transformation for trend identification
- Risk-based position sizing (configurable % of equity)
- Stop loss and take profit automation
- Paper trading mode (simulated only)
- Live 1-minute market data streaming
- Comprehensive error handling & monitoring

**Requirements:**
- Python 3.10+
- Alpaca account ([free paper trading](https://alpaca.markets))
- Linux/macOS, WSL, or Git Bash (Windows)

**Setup Process:**

1. **Create Alpaca Account**
   - Sign up: https://alpaca.markets
   - Enable paper trading (default)
   - Generate API keys: Account → API Keys

2. **Configure Bot**
   - Copy template: `cp secret.template.json secret.json`
   - Edit `secret.json` with your API keys
   - Example:
     ```json
     {
         "alpaca_heikin_ashi": {
             "api_key": "YOUR_API_KEY",
             "secret_key": "YOUR_SECRET_KEY"
         }
     }
     ```

3. **Customize Trading (Optional)**
   - Edit `code/strategies/alpaca_heikin_ashi/run.py`
   - Change: `SYMBOL` (default: NVDA), `RISK_PCT` (10%), `MAX_POSITIONS` (3)
   - DRY_RUN is already set to False (live paper trading)

4. **Run Bot**
   ```bash
   # One-time run:
   bash code/run_alpaca_heikin_ashi.sh
   
   # Schedule on Linux/macOS (runs at 9 AM weekdays):
   crontab -e
   # Add: 0 9 * * 1-5 bash /path/to/LiveTradingBots/code/run_alpaca_heikin_ashi.sh
   ```

\
📁 File Structure
-------------
```
code/
├── run_alpaca_heikin_ashi.sh          # Bot launcher
├── strategies/
│   └── alpaca_heikin_ashi/
│       ├── run.py                     # Main bot code
│       └── credentials.template.json  # Reference (see root template instead)
└── analysis/
    └── run_pnl.ipynb                  # P&L visualization
```

\
✅ Requirements
-------------
Python 3.10+

Install dependencies:
```bash
bash install.sh
```

Or manually:
```bash
python3 -m venv code/.venv
source code/.venv/bin/activate  # Linux/macOS
code\.venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

\
📊 Analysis
-------------
After trading, analyze P&L:
```bash
jupyter notebook code/analysis/run_pnl.ipynb
```

\
🔐 Security
-------------
- **Never commit** `secret.json` (it's gitignored)
- API keys are loaded from `secret.json` only
- Use strong, unique API keys from Alpaca
- Monitor account activity regularly

\
📝 Bot Parameters
-------------
Edit `code/strategies/alpaca_heikin_ashi/run.py`:

| Parameter | Current | Notes |
|-----------|---------|-------|
| SYMBOL | NVDA | Stock to trade (e.g., AAPL, SPY) |
| RISK_PCT | 10% | Risk per trade (% of account) |
| MAX_POSITIONS | 3 | Max open positions |
| STOP_LOSS_PCT | 5% | Stop loss distance |
| TAKE_PROFIT_PCT | 10% | Take profit distance |
| DRY_RUN | False | Set to True for simulation |
| SLEEP_SEC | 60 | Check interval (seconds) |

\
❓ Troubleshooting
-------------

**"KeyError: 'alpaca_heikin_ashi'"**
- Ensure `secret.json` exists and has correct format
- Copy template: `cp secret.template.json secret.json`

**"ERROR: Failed to connect to Alpaca"**
- Verify API keys are correct
- Check internet connection
- Ensure Alpaca API is operational

**"No bars data. Retrying..."**
- Market may be closed (trading happens 9:30 AM - 4:00 PM ET on weekdays)
- Check Alpaca trading hours

\
📃 License
-------------
GNU General Public License (see [LICENSE](LICENSE))

\
⚠️ Disclaimer
-------------
**Educational use only.** Paper trading = simulated funds, NO REAL MONEY. This bot is not financial advice. User assumes all responsibility for trading decisions. Robot Traders and affiliates are not liable for losses. 
