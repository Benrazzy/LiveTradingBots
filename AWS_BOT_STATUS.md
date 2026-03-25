# AWS Trading Bot Status Report\n\n**Date:** $(date)\n**Instance:** 52.91.54.126 (ubuntu)\n\n## Status\n- **Active**: Yes\n- **PID**: 51107\n- **Script**: ~/LiveTradingBots/code/strategies/alpaca_heikin_ashi/run.py\n- **Log**: No ~/bot_log.txt found\n\n## Strategy\n- Symbol: NVDA\n- Heikin-Ashi signals (1min bars)\n- Paper account\n- 10% risk per trade, max 3 positions\n\n## Commands\n```
ps -fp 51107
tail -f ~/heikin_bot.log || tail -f nohup.out
pkill -f run.py  # stop
```\n\n**Checked:** Processes, sessions, logs.
