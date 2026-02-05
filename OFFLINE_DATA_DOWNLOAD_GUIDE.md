# 离线数据下载指南 / Offline Data Download Guide

## 概述 / Overview

本指南说明如何在不直接访问 Binance API 的情况下下载数据，避免 Binance 访问失败的问题。

This guide explains how to download data without directly accessing Binance API, avoiding Binance connection failures.

---

## 方法对比 / Methods Comparison

| 方法 | 优点 | 缺点 | 网络需求 |
|------|------|------|----------|
| **标准 API** | 实时数据 | 可能被封锁 | 需要访问 Binance API |
| **Binance Vision** | 快速、稳定 | 2天延迟 | 需要访问 data.binance.vision |
| **自定义镜像** | 避免封锁 | 需要搭建 | 需要访问镜像服务器 |
| **纯离线模式** | 完全不需要网络 | 数据必须预先准备 | 不需要网络 |

---

## 方法 1: 使用自定义数据镜像（推荐）/ Method 1: Custom Data Mirror (Recommended)

### 什么是数据镜像？/ What is a Data Mirror?

数据镜像是 Binance Vision 数据的副本，部署在您可以访问的服务器上。

A data mirror is a copy of Binance Vision data deployed on a server you can access.

### 配置方法 / Configuration

在您的配置文件中添加以下设置：

Add the following settings to your config file:

```json
{
    "exchange": {
        "name": "binance",
        "binance_data_mirror_url": "https://your-mirror-server.com",
        "disable_binance_api_fallback": false
    }
}
```

### 配置选项说明 / Configuration Options

#### `binance_data_mirror_url` (可选 / Optional)

**用途**: 指定自定义的 Binance 数据镜像 URL

**Purpose**: Specify custom Binance data mirror URL

**默认值**: `https://data.binance.vision`

**示例** / Examples:
- `https://your-mirror-server.com`
- `http://192.168.1.100:8080`
- `https://mirror.example.com/binance-data`

**URL 格式要求** / URL Format Requirements:

镜像必须提供与 Binance Vision 相同的目录结构：

Mirror must provide the same directory structure as Binance Vision:

```
{base_url}/data/spot/daily/klines/{symbol}/{timeframe}/{symbol}-{timeframe}-{date}.zip
{base_url}/data/futures/um/daily/klines/{symbol}/{timeframe}/{symbol}-{timeframe}-{date}.zip
```

#### `disable_binance_api_fallback` (可选 / Optional)

**用途**: 禁用 API 回退，强制纯离线模式

**Purpose**: Disable API fallback, enforce pure offline mode

**默认值**: `false`

**值** / Values:
- `false`: 如果镜像下载失败，会回退到 Binance REST API（默认）
- `true`: 如果镜像下载失败，直接报错，不访问 Binance API

**使用场景** / Use Cases:
- ✅ 完全离线环境（无法访问 Binance）
- ✅ 需要确保不访问 Binance 的环境
- ✅ 测试镜像服务器配置

---

## 方法 2: 纯离线模式 / Method 2: Pure Offline Mode

### 配置 / Configuration

```json
{
    "exchange": {
        "name": "binance",
        "disable_binance_api_fallback": true
    }
}
```

### 使用说明 / Usage

1. **预先准备数据** / Pre-prepare Data

   在有网络的环境中下载数据：
   
   Download data in a network-enabled environment:

   ```bash
   # 使用标准方式下载数据
   freqtrade download-data \
     --exchange binance \
     --pairs BTC/USDT:USDT ETH/USDT:USDT \
     --timeframe 1h \
     --trading-mode futures \
     --days 90
   ```

2. **复制数据到离线环境** / Copy Data to Offline Environment

   ```bash
   # 复制整个数据目录
   cp -r user_data/data/binance /path/to/offline/freqtrade/user_data/data/
   ```

3. **在离线环境中回测** / Backtest in Offline Environment

   ```bash
   # 完全离线回测（使用本地数据）
   freqtrade backtesting \
     --strategy MyStrategy \
     --timeframe 1h \
     --timerange 20240101-20240331
   ```

### 注意事项 / Notes

- ⚠️ 启用 `disable_binance_api_fallback` 后，如果镜像数据不完整，会直接报错
- ⚠️ 确保本地数据覆盖回测所需的时间范围
- ⚠️ 数据需要定期更新

---

## 方法 3: 搭建 Binance 数据镜像 / Method 3: Setup Binance Data Mirror

### 为什么要搭建镜像？/ Why Setup a Mirror?

- ✅ 避免 Binance 封锁
- ✅ 提高下载速度
- ✅ 多人团队共享
- ✅ 内网部署，安全可控

### 镜像搭建方案 / Mirror Setup Options

#### 方案 A: 使用 Nginx 静态文件服务

**步骤** / Steps:

1. **下载 Binance Vision 数据**

   ```bash
   # 创建数据目录
   mkdir -p /var/www/binance-mirror/data
   
   # 下载数据（使用官方脚本或自定义脚本）
   # 示例：下载特定交易对的数据
   wget -r -np -nH --cut-dirs=1 \
     https://data.binance.vision/data/spot/daily/klines/BTCUSDT/1h/
   ```

2. **配置 Nginx**

   ```nginx
   server {
       listen 80;
       server_name binance-mirror.local;
       
       location /data {
           root /var/www/binance-mirror;
           autoindex on;
           add_header Access-Control-Allow-Origin *;
       }
   }
   ```

3. **启动服务**

   ```bash
   nginx -t
   systemctl restart nginx
   ```

4. **测试访问**

   ```bash
   curl http://your-server/data/spot/daily/klines/BTCUSDT/1h/BTCUSDT-1h-2024-01-01.zip
   ```

#### 方案 B: 使用 Python Simple HTTP Server

**适合**: 快速测试、个人使用

```bash
# 进入数据目录
cd /path/to/binance-data

# 启动 HTTP 服务器（Python 3）
python -m http.server 8080
```

**访问**: `http://localhost:8080`

#### 方案 C: 使用 Docker

创建 `docker-compose.yml`:

```yaml
version: '3'
services:
  binance-mirror:
    image: nginx:alpine
    ports:
      - "8080:80"
    volumes:
      - ./binance-data:/usr/share/nginx/html/data:ro
    restart: unless-stopped
```

启动服务：

```bash
docker-compose up -d
```

---

## 完整配置示例 / Complete Configuration Examples

### 示例 1: 使用本地镜像 / Example 1: Local Mirror

```json
{
    "exchange": {
        "name": "binance",
        "binance_data_mirror_url": "http://192.168.1.100:8080",
        "disable_binance_api_fallback": false
    },
    "pairs": ["BTC/USDT:USDT", "ETH/USDT:USDT"],
    "timeframe": "1h",
    "trading_mode": "futures"
}
```

### 示例 2: 纯离线模式 / Example 2: Pure Offline Mode

```json
{
    "exchange": {
        "name": "binance",
        "disable_binance_api_fallback": true
    },
    "pairs": ["BTC/USDT:USDT"],
    "timeframe": "1h",
    "trading_mode": "futures",
    "datadir": "user_data/data/binance"
}
```

### 示例 3: 外部镜像 + API 回退 / Example 3: External Mirror + API Fallback

```json
{
    "exchange": {
        "name": "binance",
        "binance_data_mirror_url": "https://mirror.example.com/binance",
        "disable_binance_api_fallback": false
    }
}
```

---

## 使用场景 / Use Cases

### 场景 1: 公司内网环境

**问题**: 公司防火墙封锁了 Binance

**解决方案**:
1. 在可以访问 Binance 的服务器上搭建镜像
2. 内网用户配置使用内部镜像
3. 定期更新镜像数据

**配置**:
```json
{
    "exchange": {
        "binance_data_mirror_url": "http://internal-mirror.company.com"
    }
}
```

### 场景 2: 中国大陆用户

**问题**: Binance 在中国大陆被封锁

**解决方案**:
1. 使用 VPS 搭建镜像（香港、新加坡等）
2. 或使用 VPN 下载数据后离线使用
3. 启用纯离线模式

**配置**:
```json
{
    "exchange": {
        "binance_data_mirror_url": "https://hk-mirror.example.com",
        "disable_binance_api_fallback": true
    }
}
```

### 场景 3: 完全离线开发

**问题**: 需要在没有网络的环境中开发策略

**解决方案**:
1. 一次性下载所需的所有数据
2. 复制到离线环境
3. 启用 `disable_binance_api_fallback`

**配置**:
```json
{
    "exchange": {
        "disable_binance_api_fallback": true
    }
}
```

---

## 数据同步脚本 / Data Sync Script

### 自动同步镜像数据

创建 `sync_binance_data.sh`:

```bash
#!/bin/bash
# Binance Vision 数据同步脚本

MIRROR_DIR="/var/www/binance-mirror/data"
BASE_URL="https://data.binance.vision/data"

# 交易对列表
PAIRS=("BTCUSDT" "ETHUSDT" "BNBUSDT")
# 时间周期
TIMEFRAMES=("1h" "4h" "1d")
# 下载最近N天的数据
DAYS=90

sync_data() {
    local pair=$1
    local timeframe=$2
    local market_type=$3  # spot or futures/um
    
    echo "Syncing $pair $timeframe data..."
    
    # 计算日期范围
    end_date=$(date +%Y-%m-%d)
    start_date=$(date -d "$DAYS days ago" +%Y-%m-%d)
    
    # 下载数据
    current_date=$start_date
    while [ "$current_date" != "$end_date" ]; do
        filename="${pair}-${timeframe}-${current_date}.zip"
        url="$BASE_URL/$market_type/daily/klines/$pair/$timeframe/$filename"
        dest="$MIRROR_DIR/$market_type/daily/klines/$pair/$timeframe/$filename"
        
        # 创建目录
        mkdir -p "$(dirname "$dest")"
        
        # 下载（如果不存在）
        if [ ! -f "$dest" ]; then
            wget -q "$url" -O "$dest" 2>/dev/null
            if [ $? -eq 0 ]; then
                echo "Downloaded: $filename"
            fi
        fi
        
        # 下一天
        current_date=$(date -I -d "$current_date + 1 day")
    done
}

# 同步现货数据
for pair in "${PAIRS[@]}"; do
    for timeframe in "${TIMEFRAMES[@]}"; do
        sync_data "$pair" "$timeframe" "spot"
    done
done

# 同步合约数据
for pair in "${PAIRS[@]}"; do
    for timeframe in "${TIMEFRAMES[@]}"; do
        sync_data "$pair" "$timeframe" "futures/um"
    done
done

echo "Sync completed!"
```

使用定时任务自动更新：

```bash
# 添加到 crontab（每天凌晨2点执行）
0 2 * * * /path/to/sync_binance_data.sh >> /var/log/binance-sync.log 2>&1
```

---

## 故障排查 / Troubleshooting

### 问题 1: 镜像连接失败

**错误信息**:
```
Failed to download from archive source. API fallback is disabled.
```

**解决方案**:
1. 检查镜像 URL 是否正确
2. 检查镜像服务器是否运行
3. 检查网络连接
4. 检查防火墙设置

```bash
# 测试镜像连接
curl -I http://your-mirror/data/spot/daily/klines/BTCUSDT/1h/
```

### 问题 2: 数据格式不正确

**错误信息**:
```
Error parsing ZIP file
```

**解决方案**:
- 确保镜像数据与 Binance Vision 格式完全一致
- 检查 ZIP 文件是否完整
- 重新下载损坏的文件

### 问题 3: 数据时间范围不足

**错误信息**:
```
No data available in the time range
```

**解决方案**:
- 扩展镜像数据的时间范围
- 调整回测的 `--timerange` 参数
- 检查数据是否完整下载

---

## 性能优化 / Performance Optimization

### 1. 使用 CDN

将镜像数据部署到 CDN 以提高全球访问速度：

- Cloudflare
- AWS CloudFront
- Akamai

### 2. 数据压缩

镜像服务器启用 gzip 压缩：

```nginx
gzip on;
gzip_types application/zip;
gzip_comp_level 6;
```

### 3. 缓存优化

配置适当的缓存头：

```nginx
location ~* \.zip$ {
    expires 365d;
    add_header Cache-Control "public, immutable";
}
```

---

## 安全建议 / Security Recommendations

### 1. 访问控制

如果镜像仅供内部使用，配置访问限制：

```nginx
location /data {
    allow 192.168.1.0/24;  # 内网
    deny all;
}
```

### 2. HTTPS

使用 HTTPS 保护数据传输：

```bash
# 使用 Let's Encrypt 获取免费证书
certbot --nginx -d mirror.example.com
```

### 3. 数据完整性

定期验证数据完整性：

```bash
# 验证 ZIP 文件
find /var/www/binance-mirror -name "*.zip" -exec unzip -t {} \;
```

---

## 总结 / Summary

### 快速决策树 / Quick Decision Tree

```
需要下载数据？
├─ 可以访问 Binance？
│  ├─ 是 → 使用标准方法
│  └─ 否 → 继续
├─ 有自己的服务器？
│  ├─ 是 → 搭建镜像服务器
│  └─ 否 → 继续
├─ 可以使用公共镜像？
│  ├─ 是 → 配置镜像 URL
│  └─ 否 → 纯离线模式
```

### 配置对照表 / Configuration Reference

| 场景 | binance_data_mirror_url | disable_binance_api_fallback |
|------|------------------------|------------------------------|
| 标准模式 | 不配置 | false |
| 使用镜像 | 镜像URL | false |
| 纯离线 | 可选 | true |

---

## 相关文档 / Related Documentation

- [BACKTESTING_OFFLINE_GUIDE.md](BACKTESTING_OFFLINE_GUIDE.md) - 离线回测详细指南
- [OFFLINE_BACKTEST_FAQ.md](OFFLINE_BACKTEST_FAQ.md) - 常见问题解答
- [QUICK_START.md](QUICK_START.md) - 快速开始指南

---

**文档版本** / Document Version: 1.0  
**最后更新** / Last Updated: 2026-02-05  
**状态** / Status: ✅ 完整 / Complete
