# Freqtrade - Contract Backtesting Only (合约回测专用版)

[![Freqtrade CI](https://github.com/freqtrade/freqtrade/actions/workflows/ci.yml/badge.svg?branch=develop)](https://github.com/freqtrade/freqtrade/actions/workflows/ci.yml)

**This is a streamlined version of Freqtrade focused exclusively on contract (futures) backtesting.**

## 概述 (Overview)

本版本是 Freqtrade 的精简版，专注于合约（期货）回测功能。已删除实盘交易、RPC 通知、FreqAI 机器学习、Web 界面等非核心功能。

This version is a streamlined Freqtrade focused on contract (futures) backtesting. Live trading, RPC notifications, FreqAI machine learning, Web interface and other non-core features have been removed.

## 核心功能 (Core Features)

### 保留的功能 (Retained Features)
- ✅ **回测引擎** (Backtesting Engine) - 完整的回测功能
- ✅ **Binance 支持** (Binance Support) - 仅保留 Binance 交易所
- ✅ **合约/期货** (Futures/Contracts) - 完整的合约交易回测
- ✅ **清算价格计算** (Liquidation Price Calculation)
- ✅ **策略系统** (Strategy System) - 完整的策略接口
- ✅ **数据管理** (Data Management) - 数据下载和转换
- ✅ **内存数据库** (In-Memory Database) - 回测使用内存模式

### 已删除功能 (Removed Features)
- ❌ 实盘交易 (Live Trading)
- ❌ RPC 通知 (Telegram、Discord、Webhook)
- ❌ FreqAI 机器学习 (FreqAI Machine Learning)
- ❌ Web 界面 (Web Interface)
- ❌ 绘图功能 (Plotting)
- ❌ 其他交易所 (Other Exchanges - only Binance retained)

## Disclaimer

This software is for educational purposes only. Do not risk money which
you are afraid to lose. USE THE SOFTWARE AT YOUR OWN RISK. THE AUTHORS
AND ALL AFFILIATES ASSUME NO RESPONSIBILITY FOR YOUR TRADING RESULTS.

## Supported Exchange

### Binance (币安)

Only Binance exchange is supported in this version:

- [X] [Binance](https://www.binance.com/) - Spot & Futures
- [X] [Binance US](https://www.binance.us/) - Spot
- [X] [Binance USDⓈ-M Futures](https://www.binance.com/en/futures/BTCUSDT) - Futures
- [X] [Bybit](https://bybit.com/)

Please make sure to read the [exchange specific notes](docs/exchanges.md), as well as the [trading with leverage](docs/leverage.md) documentation before diving in.

## Installation (安装)

### Requirements (要求)

- Python 3.11+
- pip

### Install (安装步骤)

```bash
# Clone the repository
git clone https://github.com/2287185537/freqtrade-k.git
cd freqtrade-k

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

## Quick Start (快速开始)

### Download Data (下载数据)

```bash
# Download Binance USDT futures data
freqtrade download-data --exchange binance --pairs BTC/USDT ETH/USDT --timeframe 1h --trading-mode futures --days 30
```

### Run Backtesting (运行回测)

```bash
# Run backtesting with your strategy
freqtrade backtesting --strategy YourStrategy --timeframe 1h --timerange 20240101-20240131
```

## Available Commands (可用命令)

```
usage: freqtrade [-h] [-V]
                 {new-config,show-config,download-data,convert-data,
                  convert-trade-data,trades-to-ohlcv,list-data,backtesting,
                  backtesting-show,backtesting-analysis,edge,hyperopt,
                  list-exchanges,list-markets,list-pairs,list-strategies,
                  list-hyperoptloss,list-timeframes,show-trades,convert-db,
                  strategy-updater,lookahead-analysis,recursive-analysis}
                 ...
```

### Key Commands (核心命令)

- `backtesting` - Run backtesting (运行回测)
- `download-data` - Download historical data (下载历史数据)
- `list-strategies` - List available strategies (列出可用策略)
- `new-config` - Create new configuration file (创建新配置文件)
- `show-config` - Show current configuration (显示当前配置)

## Features (功能特性)

- [x] **Contract Backtesting** (合约回测): Complete futures/margin backtesting support
- [x] **Binance Integration** (币安集成): Full Binance spot and futures support
- [x] **Liquidation Calculation** (清算计算): Accurate liquidation price calculation
- [x] **In-Memory Database** (内存数据库): Fast backtesting with in-memory mode
- [x] **Strategy System** (策略系统): Full strategy interface and framework
- [x] **Data Management** (数据管理): Download and convert historical data

## What's Removed (已删除功能)
    list-freqaimodels   Print available freqAI models.
## What's Removed (已删除功能)

This streamlined version has removed the following features:

- ❌ **Live Trading** (实盘交易): freqtradebot.py, worker.py removed
- ❌ **RPC Notifications** (RPC 通知): Telegram, Discord, Webhook removed  
- ❌ **Web Interface** (Web 界面): API server, WebUI removed
- ❌ **FreqAI** (机器学习): All machine learning features removed
- ❌ **Plotting** (绘图): Plot dataframe and profit visualization removed
- ❌ **Other Exchanges** (其他交易所): Only Binance retained, 18+ exchanges removed
- ❌ **Hyperopt List/Show** (超参数优化列表): Hyperopt list and show commands removed
- ❌ **Pairlist Testing** (交易对列表测试): Test pairlist command removed

## Original Documentation (原始文档)

For the full Freqtrade documentation (with all features), please visit the [official Freqtrade website](https://www.freqtrade.io).

本版本仅保留回测功能。完整文档请访问 [Freqtrade 官方网站](https://www.freqtrade.io)。

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

--Maintain github's [community policy](https://docs.github.com/en/site-policy/github-terms/github-community-code-of-conduct)--

### [Feature Requests](https://github.com/freqtrade/freqtrade/labels/enhancement)

Have you a great idea to improve the bot you want to share? Please,
first search if this feature was not [already discussed](https://github.com/freqtrade/freqtrade/labels/enhancement).
If it hasn't been requested, please
[create a new request](https://github.com/freqtrade/freqtrade/issues/new/choose)
and ensure you follow the template guide so that it does not get lost
in the bug reports.

### [Pull Requests](https://github.com/freqtrade/freqtrade/pulls)

Feel like the bot is missing a feature? We welcome your pull requests!

Please read the
[Contributing document](https://github.com/freqtrade/freqtrade/blob/develop/CONTRIBUTING.md)
to understand the requirements before sending your pull-requests.

Coding is not a necessity to contribute - maybe start with improving the documentation?
Issues labeled [good first issue](https://github.com/freqtrade/freqtrade/labels/good%20first%20issue) can be good first contributions, and will help get you familiar with the codebase.

**Note** before starting any major new feature work, *please open an issue describing what you are planning to do* or talk to us on [discord](https://discord.gg/p7nuUNVfP7) (please use the #dev channel for this). This will ensure that interested parties can give valuable feedback on the feature, and let others know that you are working on it.

**Important:** Always create your PR against the `develop` branch, not `stable`.

## Requirements

### Up-to-date clock

The clock must be accurate, synchronized to a NTP server very frequently to avoid problems with communication to the exchanges.

### Minimum hardware required

To run this bot we recommend you a cloud instance with a minimum of:

- Minimal (advised) system requirements: 2GB RAM, 1GB disk space, 2vCPU

### Software requirements

- [Python >= 3.11](http://docs.python-guide.org/en/latest/starting/installation/)
- [pip](https://pip.pypa.io/en/stable/installing/)
- [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- [TA-Lib](https://ta-lib.github.io/ta-lib-python/)
- [virtualenv](https://virtualenv.pypa.io/en/stable/installation.html) (Recommended)
- [Docker](https://www.docker.com/products/docker) (Recommended)
