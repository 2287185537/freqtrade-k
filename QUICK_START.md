# Freqtrade-K 快速开始指南 / Quick Start Guide

> 合约回测专用版 / Contract Backtesting Only Version

---

## ✅ 运行状态确认 / Run Status Confirmed

**代码已验证可以成功运行！** ✓

**Code verified to run successfully!** ✓

---

## 快速验证 / Quick Verification

### 1. 检查版本 / Check Version

```bash
$ freqtrade --version

Operating System:Linux-6.11.0-1018-azure-x86_64-with-glibc2.39
Python Version:Python 3.12.3
CCXT Version:4.5.35
Freqtrade Version:freqtrade 2026.2-dev
```

✅ **工作正常** / Working

---

### 2. 查看可用命令 / View Available Commands

```bash
$ freqtrade --help
```

**核心命令** / Core Commands:
- ✅ `backtesting` - 运行回测
- ✅ `download-data` - 下载数据
- ✅ `list-strategies` - 列出策略
- ✅ `list-exchanges` - 列出交易所
- ✅ `new-config` - 创建配置
- ✅ `hyperopt` - 超参数优化

---

### 3. 验证交易所支持 / Verify Exchange Support

```bash
$ freqtrade list-exchanges
```

**支持的交易所** / Supported Exchanges:
- ✅ Binance (Spot + Futures)
- ✅ Binance US (Spot)
- ✅ Binance USD-M Futures

---

### 4. 查看时间周期 / View Timeframes

```bash
$ freqtrade list-timeframes --exchange binance
```

**可用时间周期** / Available Timeframes:
`1s, 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M`

✅ **16 个时间周期** / 16 timeframes available

---

## 安装步骤 / Installation Steps

### 前置要求 / Prerequisites

- Python 3.11+
- pip

### 安装 / Installation

```bash
# 1. 克隆仓库 / Clone repository
git clone https://github.com/2287185537/freqtrade-k.git
cd freqtrade-k

# 2. 安装依赖 / Install dependencies
pip install -r requirements.txt

# 3. 安装包 / Install package
pip install -e .

# 4. 验证安装 / Verify installation
freqtrade --version
```

---

## 使用示例 / Usage Examples

### 示例 1: 下载数据 / Example 1: Download Data

```bash
freqtrade download-data \
  --exchange binance \
  --pairs BTC/USDT:USDT ETH/USDT:USDT \
  --timeframe 1h \
  --trading-mode futures \
  --days 30
```

### 示例 2: 创建配置 / Example 2: Create Config

```bash
freqtrade new-config --config user_data/config.json
```

按照提示输入配置信息 / Follow prompts to enter configuration

### 示例 3: 运行回测 / Example 3: Run Backtesting

```bash
freqtrade backtesting \
  --strategy YourStrategy \
  --config user_data/config.json \
  --timeframe 1h \
  --timerange 20240101-20240131
```

### 示例 4: 查看回测结果 / Example 4: View Backtest Results

```bash
freqtrade backtesting-show
```

---

## 配置文件示例 / Config File Example

创建 `config.json`:

```json
{
  "max_open_trades": 3,
  "stake_currency": "USDT",
  "stake_amount": 100,
  "trading_mode": "futures",
  "margin_mode": "isolated",
  "exchange": {
    "name": "binance",
    "key": "",
    "secret": "",
    "pair_whitelist": [
      "BTC/USDT:USDT",
      "ETH/USDT:USDT"
    ]
  }
}
```

---

## 创建策略 / Create Strategy

在 `user_data/strategies/` 目录下创建策略文件：

```python
from freqtrade.strategy import IStrategy
from pandas import DataFrame

class MyStrategy(IStrategy):
    # 策略配置
    timeframe = '1h'
    
    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # 添加技术指标
        return dataframe
    
    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # 定义入场条件
        dataframe.loc[:, 'enter_long'] = 0
        return dataframe
    
    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # 定义出场条件
        dataframe.loc[:, 'exit_long'] = 0
        return dataframe
```

---

## 常见命令 / Common Commands

### 数据管理 / Data Management

```bash
# 列出已下载的数据
freqtrade list-data --datadir user_data/data/binance

# 转换数据格式
freqtrade convert-data --format-from json --format-to feather
```

### 策略管理 / Strategy Management

```bash
# 列出所有策略
freqtrade list-strategies --strategy-path user_data/strategies

# 更新策略到最新版本
freqtrade strategy-updater --strategy YourStrategy
```

### 分析工具 / Analysis Tools

```bash
# 回测分析
freqtrade backtesting-analysis

# 前瞻偏差检查
freqtrade lookahead-analysis --strategy YourStrategy

# 递归公式检查
freqtrade recursive-analysis --strategy YourStrategy
```

---

## 目录结构 / Directory Structure

```
freqtrade-k/
├── freqtrade/              # 核心代码
│   ├── optimize/           # 回测引擎
│   ├── exchange/           # 交易所集成（Binance）
│   ├── leverage/           # 杠杆和清算
│   ├── strategy/           # 策略接口
│   └── data/              # 数据管理
├── user_data/             # 用户数据
│   ├── strategies/        # 策略文件
│   ├── data/             # 市场数据
│   └── backtest_results/ # 回测结果
├── tests/                 # 测试文件
└── docs/                  # 文档
```

---

## 功能清单 / Feature Checklist

### ✅ 已实现 / Implemented

- ✅ 合约回测引擎
- ✅ Binance 交易所支持
- ✅ 数据下载和管理
- ✅ 策略系统
- ✅ 清算价格计算
- ✅ 技术指标库
- ✅ 超参数优化
- ✅ 回测分析工具

### ❌ 已移除 / Removed

- ❌ 实盘交易
- ❌ RPC 通知（Telegram、Discord）
- ❌ Web 界面
- ❌ FreqAI 机器学习
- ❌ 绘图功能
- ❌ 其他交易所

---

## 技术支持 / Technical Support

### 文档 / Documentation

- 📄 `README.md` - 项目说明
- 📄 `REFACTORING_SUMMARY.md` - 重构详情
- 📄 `RUN_VERIFICATION.md` - 运行验证
- 📄 `QUICK_START.md` - 本文档

### 问题反馈 / Issue Reporting

如遇到问题，请提供：
1. 命令输出
2. 错误信息
3. 系统环境
4. Python 版本

---

## 性能和限制 / Performance and Limitations

### 性能 / Performance

- ✅ 内存数据库模式，回测速度快
- ✅ 支持多线程数据下载
- ✅ 高效的数据缓存机制

### 限制 / Limitations

- ⚠️ 仅支持 Binance 交易所
- ⚠️ 无实盘交易功能
- ⚠️ 无 Web 界面
- ⚠️ 需要网络连接下载数据

---

## 更新日志 / Changelog

### 2026-02-05 - v1.0

- ✅ 完成重构，仅保留回测功能
- ✅ 移除 150+ 文件
- ✅ 精简依赖
- ✅ 修复运行时错误
- ✅ 完成运行验证

---

**最后更新** / Last Updated: 2026-02-05  
**版本** / Version: 2026.2-dev  
**状态** / Status: ✅ 稳定运行 / Stable
