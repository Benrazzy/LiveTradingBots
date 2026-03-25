# LiveTradingBots

_A simple automated trading bot library for live stock trading on Alpaca_

\
🛠️ Setup commands (virtual environment included)
-------------
> git clone https://github.com/RobotTraders/LiveTradingBots.git \
> bash LiveTradingBots/install.sh


\
⭐ Alpaca Heikin-Ashi Bot
-------------
A live trading bot using Heikin-Ashi candles for stock trading on **Alpaca Paper Account**. 

**Features:**
- Heikin-Ashi candle transformation for trend identification
- Risk-based position sizing (configurable % of equity)
- Stop loss and take profit automation
- Paper trading mode (no real money)
- Live market data streaming

**Setup:**
1. Get an [Alpaca account](https://alpaca.markets) (paper trading is free)
2. Generate API keys from your dashboard
3. Add keys to `secret.json` under `alpaca_heikin_ashi`:
   ```json
   {
       "alpaca_heikin_ashi": {
           "api_key": "YOUR_KEY_HERE",
           "secret_key": "YOUR_SECRET_HERE"
       }
   }
   ```
4. Run: `bash code/run_alpaca_heikin_ashi.sh`

**Usage:**
- Edit trading parameters in `code/strategies/alpaca_heikin_ashi/run.py` (symbol, risk %, leverage, etc.)
- Run manually: `bash code/run_alpaca_heikin_ashi.sh`
- Schedule on VPS via cron: `0 9 * * 1-5 bash /path/to/LiveTradingBots/code/run_alpaca_heikin_ashi.sh`

\
✅ Requirements
-------------
Python 3.10+
\
See [requirements.txt](requirements.txt) for specific packages. Install with:
```bash
bash install.sh
```

\
📊 Analysis
-------------
Use `code/analysis/run_pnl.ipynb` to analyze P&L from completed trades.

\
📃 License
-------------
This project is licensed under the [GNU General Public License](LICENSE) - see the LICENSE file for details.


\
⚠️ Disclaimer
-------------
This bot is for educational purposes. Paper trading means NO REAL MONEY is at risk. Use at your own risk. Robot Traders and its affiliates are not responsible for any losses. This is not financial advice. 
