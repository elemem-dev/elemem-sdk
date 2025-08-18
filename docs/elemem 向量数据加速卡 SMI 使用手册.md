# Elemem 向量数据加速卡 SMI 使用手册

## 概述

elem-smi 是 Elemem 向量数据加速卡的系统管理接口工具，用于监控、管理和调试加速卡的各项功能。

## 命令语法

```bash
elem-smi [OPTIONS]
```

## 参数说明

### 基本参数

| 参数 | 长参数 | 描述 |
|------|--------|------|
| `-h` | `--help` | 显示帮助信息 |
| `-V` | `--version` | 显示版本信息 |

### 信息查询参数

| 参数 | 长参数 | 描述 |
|------|--------|------|
| `-L` | `--list-elem` | 列出所有扫描到的卡的完整信息 |
| `-q` | `--query` | 表示这是一个查询动作 |
| `-c <category>` | `--category <c>` | 指定展示类别：`overview`、`card`、`driver` |
| `-d <display>` | `--display <d>` | 单项查询，具体参数参考 `-L` 输出 |
| `-r <range>` | `--range <r>` | 查看调试信息，格式：`((card_start,card_end),(group_start,group_end),(chip_start,chip_end))` |
| `-u` | `--hdna` | 查看卡ID与HDNA和DNA的对应关系 |

**范围说明：**
- card范围：[0, 7]
- group范围：[0, 25] 
- chip范围：[0, 2]

### 操作控制参数

| 参数 | 长参数 | 描述 |
|------|--------|------|
| `-F` | `--find-me` | 使卡的LED蓝灯闪烁10秒 |
| `-C` | `--clear` | 清除驱动数据统计 |
| `-R` | `--reset` | 重置指定卡 |

### 缓存统计参数

| 参数 | 描述 |
|------|------|
| `--buff_stat <count>` | 缓存统计采样次数（0-10000） |
| `--buff_interval <us>` | 采样间隔（微秒） |

### 辅助参数

| 参数 | 长参数 | 描述 | 适用范围 |
|------|--------|------|----------|
| `-f <filename>` | `--filename <f>` | 输出到指定文件而非标准输出 | 几乎所有参数 |
| `-i <id>` | `--id <i>` | 指定卡索引（不加表示所有卡） | 几乎所有参数 |
| `-l <seconds>` | `--loop <l>` | 循环显示间隔（秒），建议使用 `-l 1` | 几乎所有参数 |

**注意事项：**
- `-i` 参数：不加表示对所有卡操作，加上则指定特定卡
- `-l` 参数：不加表示只打印一次，加上表示循环打印
- `-f` 参数：配合 `-l` 使用时，每次打印会覆盖文件内容，可用支持实时更新的编辑器查看

## 使用示例

### 基本信息查询

#### 查看所有卡的完整信息
```bash
elem-smi -L
```

#### 查看概览信息
```bash
elem-smi -q -c overview
```

#### 查看指定卡的卡信息
```bash
elem-smi -q -c card -i 0
```

#### 查看驱动信息
```bash
elem-smi -q -c driver
```

### 单项查询

以下命令需要使用 `-i` 参数指定卡号：

#### 基本信息查询
```bash
# 查看卡索引
elem-smi -q -d card_index -i 0

# 查看组数量
elem-smi -q -d group_num -i 0

# 查看芯片数量  
elem-smi -q -d chip_num -i 0

# 查看存储体大小
elem-smi -q -d bank_size -i 0

# 查看卡状态
elem-smi -q -d alive -i 0
```

#### 版本信息查询
```bash
# 软件版本
elem-smi -q -d soft_version -i 0

# 驱动版本
elem-smi -q -d driver_version -i 0

# SMI版本
elem-smi -q -d smi_version -i 0

# 固件版本
elem-smi -q -d firmware_version -i 0

# FPGA版本
elem-smi -q -d fpga_version -i 0
```

#### 硬件信息查询
```bash
# 卡名称
elem-smi -q -d name -i 0

# DNA信息
elem-smi -q -d dna -i 0

# 功耗信息（当前硬件可能不支持）
elem-smi -q -d power.cap -i 0
elem-smi -q -d power.use -i 0

# 温度
elem-smi -q -d temp -i 0

# PCI速度
elem-smi -q -d pci_speed -i 0
```

#### 驱动性能查询
```bash
# H2C方向
elem-smi -q -d driver.h2c.speed -i 0      # 速度 (MB/s)
elem-smi -q -d driver.h2c.qps -i 0        # QPS
elem-smi -q -d driver.h2c.hugepacket -i 0 # 大包数量
elem-smi -q -d driver.h2c.packet -i 0     # 包数量
elem-smi -q -d driver.h2c.packing.rate -i 0 # 打包率

# C2H方向
elem-smi -q -d driver.c2h.speed -i 0      # 速度 (MB/s)
elem-smi -q -d driver.c2h.qps -i 0        # QPS
elem-smi -q -d driver.c2h.hugepacket -i 0 # 大包数量
elem-smi -q -d driver.c2h.packet -i 0     # 包数量
elem-smi -q -d driver.c2h.packing.rate -i 0 # 打包率
```

### 调试信息查询

#### 时间戳
```bash
elem-smi -q -d timestamp -i 0
```

#### 组缓冲区状态
```bash
elem-smi -q -d memory.group_buffer -i 0
```

#### 查看DNA映射关系
```bash
elem-smi -q -u
```

#### 卡操作
```bash
# 让卡蓝灯闪烁10秒
elem-smi -F -i 0

# 重置卡
elem-smi -R -i 0

# 清除驱动统计
elem-smi -C -i 0
```

### 循环监控

#### 实时监控所有卡信息
```bash
elem-smi -L -l 1
```

#### 实时监控特定卡的温度
```bash
elem-smi -q -d temp -i 0 -l 1
```

#### 监控信息输出到文件
```bash
elem-smi -L -l 1 -f /tmp/monitor.log
```

## 输出格式说明

### 表格输出
命令的输出采用表格格式，包含以下信息分类：

1. **overview** - 概览信息：卡索引、组数、芯片数、版本等
2. **card** - 卡信息：名称、DNA、功耗、温度等  
3. **driver** - 驱动信息：版本、PCI速度、传输统计

## 故障排除

### 常见问题

1. **权限不足**
   - 确保以root权限或具有设备访问权限的用户运行

2. **找不到设备**
   - 检查驱动是否正确安装
   - 确认设备连接正常

## 版本信息

本手册适用于 elem-smi 2.0.x 版本系列。

如需获取最新版本信息，请使用：
```bash
elem-smi --version
```