# 使用 python-binance 库下载数据指南 / Python-Binance Library Data Download Guide

## 概述 / Overview

本指南说明如何使用 `python-binance` 库作为替代数据源下载 Binance 历史数据。

This guide explains how to use the `python-binance` library as an alternative data source for downloading Binance historical data.

---

## 为什么使用 python-binance？/ Why Use python-binance?

### 优势 / Advantages

- ✅ **简单易用** / Easy to use - 不需要搭建镜像服务器
- ✅ **无需 API Key** / No API key needed - 公开市场数据免费访问
- ✅ **社区维护** / Community maintained - 活跃的开源项目
- ✅ **功能完整** / Feature complete - 封装了所有 Binance API
- ✅ **自动处理** / Auto handling - 自动处理分页和限流

### 适用场景 / Use Cases

1. **可以访问 Binance 但不想用 Vision 归档** / Can access Binance but prefer not using Vision
2. **需要更灵活的数据下载控制** / Need more flexible data download control
3. **不想搭建镜像服务器** / Don't want to setup mirror server
4. **开发测试环境** / Development and testing environment

---

## 安装 / Installation

### 方法 1: 使用 pip

```bash
pip install python-binance
```

### 方法 2: 添加到 requirements

取消注释 `requirements.txt` 中的对应行：

Uncomment the line in `requirements.txt`:

```text
python-binance==1.0.19
```

然后安装：

Then install:

```bash
pip install -r requirements.txt
```

---

## 配置 / Configuration

### 基础配置 / Basic Configuration

在配置文件中添加：

Add to your config file:

```json
{
    "exchange": {
        "name": "binance",
        "use_python_binance_client": true
    }
}
```

### 完整配置示例 / Complete Configuration Example

```json
{
    "max_open_trades": 3,
    "stake_currency": "USDT",
    "trading_mode": "futures",
    "exchange": {
        "name": "binance",
        "use_python_binance_client": true,
        "pair_whitelist": [
            "BTC/USDT:USDT",
            "ETH/USDT:USDT",
            "BNB/USDT:USDT"
        ]
    },
    "timeframe": "1h"
}
```

---

## 使用方法 / Usage

### 基本用法 / Basic Usage

```bash
# 1. 创建配置文件
cat > config_python_binance.json << 'CONF'
{
    "exchange": {
        "name": "binance",
        "use_python_binance_client": true
    }
}
CONF

# 2. 下载数据
freqtrade download-data \
  --config config_python_binance.json \
  --pairs BTC/USDT:USDT ETH/USDT:USDT \
  --timeframe 1h \
  --trading-mode futures \
  --days 30
```

### 现货数据 / Spot Data

```bash
# 下载现货数据
freqtrade download-data \
  --config config_python_binance.json \
  --pairs BTC/USDT ETH/USDT \
  --timeframe 1h \
  --trading-mode spot \
  --days 90
```

### 合约数据 / Futures Data

```bash
# 下载合约数据
freqtrade download-data \
  --config config_python_binance.json \
  --pairs BTC/USDT:USDT ETH/USDT:USDT \
  --timeframe 1h \
  --trading-mode futures \
  --days 90
```

---

## 数据源优先级 / Data Source Priority

当启用 `use_python_binance_client` 时，数据源选择优先级为：

When `use_python_binance_client` is enabled, data source priority is:

```
1. python-binance 库 / python-binance library (最高优先级 / Highest priority)
   ↓ (如果失败 / If fails)
2. Binance Vision 归档 / Binance Vision archive
   ↓ (如果失败 / If fails)
3. REST API 回退 / REST API fallback (如果未禁用 / If not disabled)
```

### 配置组合 / Configuration Combinations

#### 组合 1: 仅使用 python-binance（推荐）/ Only python-binance (Recommended)

```json
{
    "exchange": {
        "use_python_binance_client": true
    }
}
```

**行为** / Behavior:
- 优先使用 python-binance
- 失败时自动尝试其他方法
- 最灵活的配置

#### 组合 2: python-binance + 禁用回退 / python-binance + Disable Fallback

```json
{
    "exchange": {
        "use_python_binance_client": true,
        "disable_binance_api_fallback": true
    }
}
```

**行为** / Behavior:
- 只使用 python-binance
- 失败时不尝试其他方法
- 严格控制数据源

#### 组合 3: python-binance + 自定义镜像 / python-binance + Custom Mirror

```json
{
    "exchange": {
        "use_python_binance_client": true,
        "binance_data_mirror_url": "http://your-mirror.com"
    }
}
```

**行为** / Behavior:
- 首选 python-binance
- python-binance 失败时使用镜像
- 最全面的配置

---

## 支持的时间周期 / Supported Timeframes

python-binance 支持以下时间周期：

python-binance supports the following timeframes:

| 时间周期 / Timeframe | 说明 / Description |
|---------------------|-------------------|
| 1m | 1 分钟 / 1 minute |
| 3m | 3 分钟 / 3 minutes |
| 5m | 5 分钟 / 5 minutes |
| 15m | 15 分钟 / 15 minutes |
| 30m | 30 分钟 / 30 minutes |
| 1h | 1 小时 / 1 hour |
| 2h | 2 小时 / 2 hours |
| 4h | 4 小时 / 4 hours |
| 6h | 6 小时 / 6 hours |
| 8h | 8 小时 / 8 hours |
| 12h | 12 小时 / 12 hours |
| 1d | 1 天 / 1 day |
| 3d | 3 天 / 3 days |
| 1w | 1 周 / 1 week |
| 1M | 1 月 / 1 month |

---

## 与用户提供的脚本对比 / Comparison with User's Script

### 用户的脚本 / User's Script

```python
from binance.client import Client
import pandas as pd

client = Client()
klines = client.get_historical_klines(symbol, interval, start_str, end_str)
df = pd.DataFrame(klines, columns=[...])
```

### Freqtrade 集成 / Freqtrade Integration

```json
{
    "exchange": {
        "use_python_binance_client": true
    }
}
```

### 主要区别 / Key Differences

| 特性 / Feature | 用户脚本 / User Script | Freqtrade 集成 / Integration |
|---------------|----------------------|----------------------------|
| 编程方式 / Programming | ✅ 需要写代码 | ❌ 配置即用 |
| 数据格式 / Data Format | ⚠️ 需要手动转换 | ✅ 自动转换 |
| 错误处理 / Error Handling | ⚠️ 需要自己实现 | ✅ 内置处理 |
| 多数据源 / Multiple Sources | ❌ 不支持 | ✅ 自动切换 |
| 回测集成 / Backtest Integration | ❌ 需要手动集成 | ✅ 无缝集成 |
| 持续使用 / Continuous Use | ⚠️ 每次都要运行脚本 | ✅ 配置一次永久使用 |

### 优势总结 / Advantage Summary

Freqtrade 集成提供：

1. **配置驱动** / Configuration-driven - 无需编程
2. **自动化** / Automated - 无需手动运行脚本
3. **容错性** / Fault-tolerant - 自动回退到其他数据源
4. **标准化** / Standardized - 数据格式统一
5. **可维护** / Maintainable - 配置管理更简单

---

## 实际示例 / Practical Examples

### 示例 1: 下载多个交易对 / Download Multiple Pairs

```bash
# 配置
cat > config.json << 'CONF'
{
    "exchange": {
        "name": "binance",
        "use_python_binance_client": true
    }
}
CONF

# 下载
freqtrade download-data \
  --config config.json \
  --pairs BTC/USDT:USDT ETH/USDT:USDT BNB/USDT:USDT SOL/USDT:USDT \
  --timeframe 1h 4h 1d \
  --trading-mode futures \
  --days 90

# 查看结果
freqtrade list-data --exchange binance
```

### 示例 2: 定期更新数据 / Regular Data Updates

```bash
#!/bin/bash
# 数据更新脚本 / Data update script
# 文件名: update_data.sh

CONFIG="config_python_binance.json"
PAIRS="BTC/USDT:USDT ETH/USDT:USDT"
TIMEFRAMES="1h 4h"
DAYS=7  # 只更新最近7天

freqtrade download-data \
  --config $CONFIG \
  --pairs $PAIRS \
  --timeframe $TIMEFRAMES \
  --trading-mode futures \
  --days $DAYS

echo "Data updated: $(date)"
```

添加到 crontab（每天更新）：

```bash
# 每天凌晨 2 点更新
0 2 * * * /path/to/update_data.sh >> /var/log/freqtrade-update.log 2>&1
```

### 示例 3: 完整工作流程 / Complete Workflow

```bash
# 1. 安装 python-binance
pip install python-binance

# 2. 创建配置
cat > my_config.json << 'CONF'
{
    "max_open_trades": 3,
    "stake_currency": "USDT",
    "trading_mode": "futures",
    "exchange": {
        "name": "binance",
        "use_python_binance_client": true
    },
    "timeframe": "1h"
}
CONF

# 3. 下载数据
freqtrade download-data \
  --config my_config.json \
  --pairs BTC/USDT:USDT \
  --timeframe 1h \
  --days 90

# 4. 运行回测
freqtrade backtesting \
  --config my_config.json \
  --strategy MyStrategy \
  --timerange 20240101-20240331

# 5. 查看结果
freqtrade backtesting-show
```

---

## 故障排查 / Troubleshooting

### 问题 1: 库未安装 / Library Not Installed

**错误信息** / Error:
```
python-binance library is not installed
```

**解决方案** / Solution:
```bash
pip install python-binance
```

### 问题 2: 连接超时 / Connection Timeout

**错误信息** / Error:
```
ReadTimeout: HTTPSConnectionPool
```

**解决方案** / Solution:
1. 检查网络连接
2. 检查是否可以访问 Binance
3. 尝试使用 VPN
4. 或切换到镜像模式

```json
{
    "exchange": {
        "use_python_binance_client": false,
        "binance_data_mirror_url": "http://your-mirror.com"
    }
}
```

### 问题 3: API 限流 / Rate Limit

**错误信息** / Error:
```
429 Too Many Requests
```

**解决方案** / Solution:
- 减少并发下载
- 分批下载
- 等待后重试

```bash
# 分批下载
freqtrade download-data --pairs BTC/USDT:USDT --timeframe 1h --days 30
# 等待 60 秒
sleep 60
freqtrade download-data --pairs ETH/USDT:USDT --timeframe 1h --days 30
```

### 问题 4: 数据不完整 / Incomplete Data

**症状** / Symptom:
下载的数据有缺失

Downloaded data has gaps

**解决方案** / Solution:
1. 使用 `--erase` 重新下载

```bash
freqtrade download-data \
  --config config.json \
  --pairs BTC/USDT:USDT \
  --timeframe 1h \
  --days 90 \
  --erase
```

2. 或启用回退到其他数据源

```json
{
    "exchange": {
        "use_python_binance_client": true,
        "disable_binance_api_fallback": false
    }
}
```

---

## 性能对比 / Performance Comparison

### 下载速度 / Download Speed

| 方法 / Method | 速度 / Speed | 可靠性 / Reliability |
|--------------|-------------|---------------------|
| python-binance | 中等 / Medium | 高 / High |
| Binance Vision | 快 / Fast | 中等 / Medium |
| REST API | 慢 / Slow | 低 / Low |
| 自定义镜像 / Mirror | 很快 / Very Fast | 高 / High |

### 推荐配置 / Recommended Configuration

**最佳配置** / Best Configuration:
```json
{
    "exchange": {
        "use_python_binance_client": true,
        "binance_data_mirror_url": "http://your-mirror.com"
    }
}
```

**说明** / Explanation:
- 优先使用 python-binance（简单、可靠）
- python-binance 失败时自动切换到镜像
- 提供最佳的可靠性和灵活性

---

## 最佳实践 / Best Practices

### 1. 合理选择时间范围 / Choose Reasonable Time Range

```bash
# 推荐：分批下载大数据
# 第一次下载历史数据（大量）
freqtrade download-data --pairs BTC/USDT:USDT --timeframe 1h --days 365

# 后续定期更新（少量）
freqtrade download-data --pairs BTC/USDT:USDT --timeframe 1h --days 7
```

### 2. 使用配置文件 / Use Configuration Files

```bash
# 不推荐：命令行参数太多
freqtrade download-data --exchange binance --pairs ... --timeframe ...

# 推荐：使用配置文件
freqtrade download-data --config my_config.json
```

### 3. 定期更新 / Regular Updates

```bash
# 创建定时任务
0 2 * * * /path/to/update_data.sh
```

### 4. 监控日志 / Monitor Logs

```bash
# 查看下载日志
tail -f user_data/logs/freqtrade.log | grep "python-binance"
```

---

## 与其他方法对比 / Comparison with Other Methods

### 方法对比表 / Method Comparison Table

| 特性 / Feature | python-binance | 自定义镜像 / Mirror | Binance Vision | 纯离线 / Offline |
|---------------|----------------|-------------------|----------------|-----------------|
| 设置难度 / Setup | 简单 / Easy | 中等 / Medium | 简单 / Easy | 简单 / Easy |
| 网络要求 / Network | Binance 可达 | 镜像可达 | Vision 可达 | 不需要 / None |
| 维护成本 / Maintenance | 低 / Low | 中等 / Medium | 低 / Low | 低 / Low |
| 速度 / Speed | 中等 / Medium | 快 / Fast | 快 / Fast | 很快 / Very Fast |
| 灵活性 / Flexibility | 高 / High | 高 / High | 中等 / Medium | 低 / Low |
| 推荐场景 / Use Case | 一般使用 / General | 团队/企业 / Team | 个人 / Personal | 开发 / Dev |

---

## 总结 / Summary

### 何时使用 python-binance？/ When to Use python-binance?

✅ **推荐使用** / Recommended:
- 可以访问 Binance
- 不想搭建镜像服务器
- 需要简单的设置
- 个人或小团队使用

❌ **不推荐** / Not Recommended:
- Binance 被封锁（改用镜像）
- 需要最快速度（改用镜像）
- 大规模团队使用（改用镜像）
- 完全离线环境（改用离线模式）

### 快速决策树 / Quick Decision Tree

```
需要下载数据？
├─ 可以访问 Binance？
│  ├─ 是 → 使用 python-binance ✅
│  └─ 否 → 使用自定义镜像
├─ 有服务器？
│  ├─ 是 → 搭建镜像（长期更好）
│  └─ 否 → 使用 python-binance ✅
└─ 完全离线？
   └─ 使用预下载数据 + 离线模式
```

---

## 相关文档 / Related Documentation

- [OFFLINE_DATA_DOWNLOAD_GUIDE.md](OFFLINE_DATA_DOWNLOAD_GUIDE.md) - 离线数据下载完整指南
- [OFFLINE_DOWNLOAD_SUMMARY.md](OFFLINE_DOWNLOAD_SUMMARY.md) - 快速参考
- [BACKTESTING_OFFLINE_GUIDE.md](BACKTESTING_OFFLINE_GUIDE.md) - 离线回测指南

---

**版本** / Version: 1.0  
**最后更新** / Last Updated: 2026-02-05  
**状态** / Status: ✅ 可用 / Available
