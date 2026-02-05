# 离线数据下载功能总结 / Offline Data Download Feature Summary

## ✅ 已实现功能 / Implemented Features

### 1. 自定义数据镜像支持 / Custom Data Mirror Support

**配置选项** / Configuration Option:
```json
{
    "exchange": {
        "binance_data_mirror_url": "https://your-mirror-server.com"
    }
}
```

**功能说明** / Description:
- 支持配置自定义 Binance Vision 数据镜像 URL
- 兼容标准 Binance Vision 目录结构
- 适用于内网部署、CDN 加速等场景

### 2. 禁用 API 回退 / Disable API Fallback

**配置选项** / Configuration Option:
```json
{
    "exchange": {
        "disable_binance_api_fallback": true
    }
}
```

**功能说明** / Description:
- 禁用自动回退到 Binance REST API
- 强制纯离线模式
- 确保不访问 Binance 服务器

### 3. 组合使用 / Combined Usage

**配置示例** / Configuration Example:
```json
{
    "exchange": {
        "name": "binance",
        "binance_data_mirror_url": "http://192.168.1.100:8080",
        "disable_binance_api_fallback": true
    }
}
```

---

## 🎯 解决的问题 / Problems Solved

### 问题 1: Binance 访问被封锁 / Binance Access Blocked

**解决方案**:
- 使用自定义镜像绕过封锁
- 支持内网部署
- 支持第三方镜像服务

### 问题 2: 网络不稳定 / Network Instability

**解决方案**:
- 使用本地或近端镜像
- 减少对外部网络的依赖
- 提高下载可靠性

### 问题 3: 需要完全离线环境 / Fully Offline Environment Needed

**解决方案**:
- 启用 `disable_binance_api_fallback`
- 预先准备数据
- 完全离线运行

---

## 📖 使用指南 / Usage Guide

### 快速开始 / Quick Start

#### 场景 A: 使用公司内网镜像 / Corporate Intranet Mirror

```bash
# 1. 配置文件
cat > config.json << 'CONF'
{
    "exchange": {
        "name": "binance",
        "binance_data_mirror_url": "http://internal-mirror.company.com"
    }
}
CONF

# 2. 下载数据
freqtrade download-data \
  --config config.json \
  --pairs BTC/USDT:USDT \
  --timeframe 1h \
  --days 30
```

#### 场景 B: 纯离线模式 / Pure Offline Mode

```bash
# 1. 有网络时下载数据
freqtrade download-data \
  --exchange binance \
  --pairs BTC/USDT:USDT \
  --timeframe 1h \
  --days 90

# 2. 配置纯离线模式
cat > offline_config.json << 'CONF'
{
    "exchange": {
        "name": "binance",
        "disable_binance_api_fallback": true
    }
}
CONF

# 3. 离线回测（即使没有网络也可以运行）
freqtrade backtesting \
  --config offline_config.json \
  --strategy MyStrategy \
  --timeframe 1h
```

---

## 🛠️ 镜像服务器搭建 / Mirror Server Setup

### 方法 1: 使用 Nginx (推荐 / Recommended)

```bash
# 1. 安装 Nginx
sudo apt-get install nginx

# 2. 创建数据目录
sudo mkdir -p /var/www/binance-mirror/data

# 3. 下载 Binance Vision 数据
# (参考 OFFLINE_DATA_DOWNLOAD_GUIDE.md 中的同步脚本)

# 4. 配置 Nginx
cat > /etc/nginx/sites-available/binance-mirror << 'NGINX'
server {
    listen 80;
    server_name binance-mirror.local;
    
    location /data {
        root /var/www/binance-mirror;
        autoindex on;
    }
}
NGINX

# 5. 启用配置
sudo ln -s /etc/nginx/sites-available/binance-mirror /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 方法 2: 使用 Docker

```bash
# 1. 创建 docker-compose.yml
cat > docker-compose.yml << 'DOCKER'
version: '3'
services:
  binance-mirror:
    image: nginx:alpine
    ports:
      - "8080:80"
    volumes:
      - ./binance-data:/usr/share/nginx/html/data:ro
    restart: unless-stopped
DOCKER

# 2. 启动服务
docker-compose up -d

# 3. 测试访问
curl -I http://localhost:8080/data/
```

### 方法 3: Python HTTP Server (简单测试 / Quick Test)

```bash
# 进入数据目录
cd /path/to/binance-data

# 启动服务器
python -m http.server 8080

# 在另一个终端测试
curl -I http://localhost:8080/
```

---

## 📋 配置参考 / Configuration Reference

### 所有配置选项 / All Configuration Options

```json
{
    "exchange": {
        "name": "binance",
        
        // 自定义镜像 URL（可选）
        // Custom mirror URL (optional)
        "binance_data_mirror_url": "https://your-mirror.com",
        
        // 禁用 API 回退（可选，默认 false）
        // Disable API fallback (optional, default false)
        "disable_binance_api_fallback": false,
        
        // 其他标准配置...
        // Other standard configurations...
        "pair_whitelist": ["BTC/USDT:USDT"],
        "key": "",
        "secret": ""
    }
}
```

### 配置场景对照 / Configuration Scenarios

| 场景 / Scenario | binance_data_mirror_url | disable_binance_api_fallback |
|----------------|------------------------|------------------------------|
| 标准模式 / Standard | 不设置 / Not set | false |
| 使用镜像 / Use Mirror | 镜像URL / Mirror URL | false |
| 纯离线 / Pure Offline | 可选 / Optional | true |
| 镜像+离线 / Mirror+Offline | 镜像URL / Mirror URL | true |

---

## ⚡ 测试验证 / Testing & Verification

### 测试 1: 验证镜像连接 / Verify Mirror Connection

```bash
# 测试镜像服务器是否可访问
curl -I http://your-mirror/data/spot/daily/klines/BTCUSDT/1h/BTCUSDT-1h-2024-01-01.zip

# 预期结果：HTTP 200 或 404（如果文件不存在）
# Expected: HTTP 200 or 404 (if file doesn't exist)
```

### 测试 2: 验证数据下载 / Verify Data Download

```bash
# 配置使用镜像
export FREQTRADE_CONFIG='{"exchange":{"binance_data_mirror_url":"http://your-mirror"}}'

# 下载少量数据测试
freqtrade download-data \
  --exchange binance \
  --pairs BTC/USDT:USDT \
  --timeframe 1h \
  --days 7

# 检查日志中的数据源
# 应该显示从镜像下载
```

### 测试 3: 验证离线模式 / Verify Offline Mode

```bash
# 1. 断开网络（或配置防火墙阻止 Binance）

# 2. 配置纯离线模式
cat > offline_test.json << 'CONF'
{
    "exchange": {
        "name": "binance",
        "disable_binance_api_fallback": true
    }
}
CONF

# 3. 尝试下载（应该失败并报错，不会尝试访问 Binance API）
freqtrade download-data --config offline_test.json --pairs BTC/USDT:USDT

# 4. 回测已有数据（应该成功）
freqtrade backtesting --config offline_test.json --strategy TestStrategy
```

---

## 📊 性能对比 / Performance Comparison

### 下载速度对比 / Download Speed Comparison

| 数据源 / Data Source | 延迟 / Latency | 速度 / Speed | 可靠性 / Reliability |
|---------------------|--------------|-------------|---------------------|
| Binance API | 高 / High | 慢 / Slow | 受限流影响 / Rate Limited |
| Binance Vision | 中 / Medium | 快 / Fast | 较好 / Good |
| 本地镜像 / Local Mirror | 低 / Low | 很快 / Very Fast | 很好 / Excellent |
| 内网镜像 / Intranet Mirror | 很低 / Very Low | 极快 / Extremely Fast | 极好 / Excellent |

### 可用性对比 / Availability Comparison

| 情况 / Situation | Binance API | Binance Vision | 自定义镜像 / Custom Mirror |
|-----------------|-------------|----------------|---------------------------|
| 网络封锁 / Network Block | ❌ 不可用 | ❌ 不可用 | ✅ 可用 |
| 防火墙限制 / Firewall | ❌ 不可用 | ❌ 不可用 | ✅ 可用 |
| 完全离线 / Fully Offline | ❌ 不可用 | ❌ 不可用 | ✅ 可用（本地） |
| API 限流 / Rate Limited | ❌ 受限 | ✅ 不受限 | ✅ 不受限 |

---

## 🎓 最佳实践 / Best Practices

### 1. 镜像数据管理 / Mirror Data Management

- ✅ 定期同步最新数据（建议每天）
- ✅ 保留足够的历史数据（至少 90 天）
- ✅ 监控镜像服务器状态
- ✅ 备份重要数据

### 2. 配置管理 / Configuration Management

- ✅ 为不同环境准备不同配置文件
- ✅ 使用环境变量管理敏感信息
- ✅ 版本控制配置文件模板
- ✅ 文档化配置选项

### 3. 安全建议 / Security Recommendations

- ✅ 内网镜像使用访问控制
- ✅ 公网镜像使用 HTTPS
- ✅ 定期验证数据完整性
- ✅ 监控异常访问

---

## 🔧 故障排查 / Troubleshooting

### 常见问题 / Common Issues

#### 问题 1: 镜像连接超时

**症状**: 
```
Connection timeout when accessing mirror
```

**解决方案**:
1. 检查镜像服务器是否运行
2. 检查网络连接
3. 检查防火墙规则
4. 尝试使用 IP 地址而非域名

#### 问题 2: 数据格式错误

**症状**:
```
Error parsing data from mirror
```

**解决方案**:
1. 确认镜像目录结构正确
2. 验证 ZIP 文件完整性
3. 检查文件权限
4. 重新下载损坏的文件

#### 问题 3: 离线模式报错

**症状**:
```
Failed to download data with API fallback disabled
```

**解决方案**:
1. 确认本地有所需的数据
2. 检查 timerange 是否在数据范围内
3. 检查数据目录路径
4. 验证数据文件存在且完整

---

## 📚 相关文档 / Related Documentation

### 完整文档列表 / Complete Documentation

1. **OFFLINE_DATA_DOWNLOAD_GUIDE.md** - 离线数据下载详细指南
   - 三种方法详解
   - 镜像搭建教程
   - 配置示例
   - 故障排查

2. **BACKTESTING_OFFLINE_GUIDE.md** - 离线回测指南
   - 回测工作流程
   - 数据准备
   - 离线运行

3. **OFFLINE_BACKTEST_FAQ.md** - 常见问题解答
   - Q&A 格式
   - 快速查找
   - 实用建议

4. **QUICK_START.md** - 快速开始
   - 安装步骤
   - 基础使用
   - 命令参考

---

## ✅ 功能检查清单 / Feature Checklist

- [x] 自定义镜像 URL 支持
- [x] 禁用 API 回退选项
- [x] 向后兼容现有配置
- [x] 错误处理和日志
- [x] 完整文档
- [x] 配置示例
- [x] 测试验证
- [x] 使用场景说明
- [x] 镜像搭建教程
- [x] 故障排查指南

---

## 🚀 后续改进计划 / Future Improvements

### 计划中的功能 / Planned Features

1. **多镜像支持** / Multiple Mirrors
   - 配置多个镜像源
   - 自动切换
   - 负载均衡

2. **健康检查** / Health Check
   - 镜像可用性检测
   - 自动故障转移
   - 状态监控

3. **数据验证** / Data Validation
   - 自动验证数据完整性
   - 校验和检查
   - 损坏数据报告

4. **同步工具** / Sync Tools
   - 内置同步命令
   - 增量更新
   - 进度显示

---

**版本** / Version: 1.0  
**状态** / Status: ✅ 已完成 / Completed  
**最后更新** / Last Updated: 2026-02-05
