# 向量数据库性能测试教程

## 概述

本教程介绍如何使用提供的C++代码对向量数据库进行QPS和召回率性能测试。测试基于SIFT数据集，支持IVF索引的多线程性能评估。

## 环境准备

参考向量数据加速卡安装指南中的软件部署，docker部署方案，启动docker客户端。
```bash
cd docker
sudo docker compose run --rm client

# 进入性能测试目录
cd /root/hilbert/c++

# 执行qps recall测试
./bazel-bin/test_qps_recall config.ini

```

## 配置文件说明

### config.ini 参数详解

```ini
[hdf5]
file = /mnt/soft/data_set/SIFT_1M.hdf5  # SIFT数据集路径

[search]
nq = 10000              # 查询向量数量
topk = 10               # 返回最相似的K个结果
thread_num = 32         # 并发线程数
index_name = sift_1M_s10  # 索引名称前缀
nlist = 512             # IVF聚类中心数量
nprob = 16              # 搜索时探测的聚类数量
batch_size = 200        # 批处理大小
thread_repeat = 10      # 每线程重复次数
need_ivf_recall = false # 是否计算IVF召回率对比
```

### 关键性能参数

| 参数 | 作用 | 性能影响 |
|------|------|----------|
| `thread_num` | 并发线程数 | 影响QPS，过高可能导致资源竞争 |
| `batch_size` | 批处理大小 | 影响吞吐量和延迟平衡 |
| `nlist` | 聚类中心数 | 影响索引质量和搜索速度 |
| `nprob` | 探测聚类数 | 召回率与速度的权衡 |

## 快速开始

### 1. 基础性能测试
```bash
# 使用默认配置运行
./bazel-bin/test_qps_recall config.ini
```

### 2. 修改配置进行对比测试


>**注意，以下是E5服务器上的典型配置，其他配置的服务器需要针对性的调优**


**高QPS配置（牺牲部分召回率）：**
```ini
nlist = 4096
nprob = 48
thread_num = 128
batch_size = 500
```

**高召回率配置（降低QPS）：**
```ini
nlist = 4096
nprob = 64
thread_num = 128
batch_size = 100
```

## 性能调优指南

### 线程数优化
```bash
# 测试不同线程数的影响
for threads in 8 16 32 64; do
    sed -i "s/thread_num = .*/thread_num = $threads/" config.ini
    echo "Testing with $threads threads:"
    ./test_qps_recall config.ini | grep QPS
done
```

### 批处理大小优化
```bash
# 测试不同批处理大小
for batch in 50 100 200 500 1000; do
    sed -i "s/batch_size = .*/batch_size = $batch/" config.ini
    echo "Testing batch_size=$batch:"
    ./test_qps_recall config.ini | grep QPS
done
```

### nprob参数扫描
```ini
# 在配置文件中设置多个nprob值进行对比
nprob = 1,2,8,16,24,32,48,64
```

## 输出结果解析

### 典型输出格式
```
[NlistPerf-MT] nlist=512 batch_size=200 nprob=16 threads=32 QPS=15420.5 Recall=0.892 IVF Recall=0.945 Latency(ms)=1.24
```

### 指标含义
- **QPS**: 每秒查询数量，衡量系统吞吐能力
- **Recall**: 召回率，与ground truth的匹配度
- **IVF Recall**: 与Faiss IVF实现的召回率对比
- **Latency**: 平均延迟（毫秒）

## 性能基准对比

### 推荐测试场景

| 场景 | nlist | nprob | 期望QPS | 期望Recall |
|------|-------|-------|---------|------------|
| 高性能搜索 | 4096 | 48 | >40000 | >=0.95 |
| 高精度搜索 | 4096 | 128 | >7000 | >=0.99 |

### 性能瓶颈分析

**CPU瓶颈识别：**
```bash
# 运行测试时监控CPU使用率
top -p $(pgrep test_qps_recall)
```

**内存使用监控：**
```bash
# 监控内存占用
ps aux | grep test_qps_recall
```

## 常见问题排查

### 1. QPS过低
- 检查线程数是否合理（建议为CPU核心数的1-2倍）
- 调整batch_size增加批处理效率
- 降低nprob值减少计算量

### 2. 召回率不理想
- 增加nprob值
- 调整nlist数量
- 检查数据质量和分布

### 3. 延迟过高
- 减少batch_size
- 降低nprob
- 检查网络连接（如果是分布式部署）

### 多索引对比测试
```ini
# 配置文件支持多个nlist值
nlist = 512,1024,2048,4096
```
## 加速卡性能监测指标指南

在进行性能测试时，可以通过 `elem-smi` 工具实时监测加速卡运行时的各项关键指标，为性能优化提供重要参考依据。

### 1. 通道缓冲区占用率监测

#### H2C Buffer（主机到卡缓冲区）
- **0%**: 硬件接收 search 包的缓冲区为空
  - 说明发包速率低于硬件处理能力
  - 硬件未满载运行
- **100%**: 硬件接收包缓冲区已满
  - 说明发包速率超过硬件处理能力
  - 硬件满载，软件发包逻辑处于阻塞状态
- **0-100%**: 发包速率与硬件处理能力处于平衡状态
  - 硬件满载运行，软件未发生阻塞

#### C2H Buffer（卡到主机缓冲区）
- **0%**: 硬件向软件发送回包的缓冲区为空
  - 说明软件层及时读取了所有回包
- **100%**: 软件读取回包能力不足
  - 导致硬件缓冲区写满，阻塞硬件执行
- **0-25%**: 理想的运行状态

#### 监测命令
```bash
# 每1秒更新一次监测状态
elem-smi -q -c ddr -l 1
```
```
+--------------+--------------------+-------------------+-------------------+
|     ddr      |      card_idx      |         0         |                   |
+--------------+--------------------+-------------------+-------------------+
| memory.total | memory.used(Mbyte) | memory.h2c_buffer | memory.c2h_buffer |
+--------------+--------------------+-------------------+-------------------+
|     8GB      |         2          |        0%         |        0%         |
+--------------+--------------------+-------------------+-------------------+
|     ddr      |      card_idx      |         1         |                   |
+--------------+--------------------+-------------------+-------------------+
| memory.total | memory.used(Mbyte) | memory.h2c_buffer | memory.c2h_buffer |
+--------------+--------------------+-------------------+-------------------+
|     8GB      |         0          |        0%         |        0%         |
+--------------+--------------------+-------------------+-------------------+
|     ddr      |      card_idx      |         2         |                   |
+--------------+--------------------+-------------------+-------------------+
| memory.total | memory.used(Mbyte) | memory.h2c_buffer | memory.c2h_buffer |
+--------------+--------------------+-------------------+-------------------+
|     8GB      |         0          |        0%         |        0%         |
+--------------+--------------------+-------------------+-------------------+
|     ddr      |      card_idx      |         3         |                   |
+--------------+--------------------+-------------------+-------------------+
| memory.total | memory.used(Mbyte) | memory.h2c_buffer | memory.c2h_buffer |
+--------------+--------------------+-------------------+-------------------+
|     8GB      |         0          |        0%         |        0%         |
+--------------+--------------------+-------------------+-------------------+
|     ddr      |      card_idx      |         4         |                   |
+--------------+--------------------+-------------------+-------------------+
| memory.total | memory.used(Mbyte) | memory.h2c_buffer | memory.c2h_buffer |
+--------------+--------------------+-------------------+-------------------+
|     8GB      |         0          |        0%         |        0%         |
+--------------+--------------------+-------------------+-------------------+
```
### 2. HBM 内存利用率监测

监测指定加速卡的 HBM（高带宽内存）利用率，包括 26 个 group 的详细信息。

#### 关键指标
- **bandwidth_utilization**: 对应 group 的 HBM 读取利用率
  - 数值越高越好
  - 正常情况下约为 60% 左右

#### 监测命令
```bash
# 监测指定卡（如卡4）的内存使用情况
elem-smi -q -d memory.uage -l 1 -i 4
```
```
group  0 reading_efficiency 0.00%   exclusive_ratio 0.00% bandwidth_utilization 0.00%
group  1 reading_efficiency 0.00%   exclusive_ratio 0.00% bandwidth_utilization 0.00%
group  2 reading_efficiency 0.00%   exclusive_ratio 0.00% bandwidth_utilization 0.00%
group  3 reading_efficiency 0.00%   exclusive_ratio 0.00% bandwidth_utilization 0.00%
group  4 reading_efficiency 0.00%   exclusive_ratio 0.00% bandwidth_utilization 0.00%
group  5 reading_efficiency 0.00%   exclusive_ratio 0.00% bandwidth_utilization 0.00%
group  6 reading_efficiency 0.00%   exclusive_ratio 0.00% bandwidth_utilization 0.00%
group  7 reading_efficiency 0.00%   exclusive_ratio 0.00% bandwidth_utilization 0.00%
group  8 reading_efficiency 0.00%   exclusive_ratio 0.00% bandwidth_utilization 0.00%
group  9 reading_efficiency 0.00%   exclusive_ratio 0.00% bandwidth_utilization 0.00%
group 10 reading_efficiency 0.00%   exclusive_ratio 0.00% bandwidth_utilization 0.00%
group 11 reading_efficiency 0.00%   exclusive_ratio 0.00% bandwidth_utilization 0.00%
group 12 reading_efficiency 0.00%   exclusive_ratio 0.00% bandwidth_utilization 0.00%
group 13 reading_efficiency 0.00%   exclusive_ratio 0.00% bandwidth_utilization 0.00%
group 14 reading_efficiency 0.00%   exclusive_ratio 0.00% bandwidth_utilization 0.00%
group 15 reading_efficiency 0.00%   exclusive_ratio 0.00% bandwidth_utilization 0.00%
group 16 reading_efficiency 0.00%   exclusive_ratio 0.00% bandwidth_utilization 0.00%
group 17 reading_efficiency 0.00%   exclusive_ratio 0.00% bandwidth_utilization 0.00%
group 18 reading_efficiency 0.00%   exclusive_ratio 0.00% bandwidth_utilization 0.00%
group 19 reading_efficiency 0.00%   exclusive_ratio 0.00% bandwidth_utilization 0.00%
group 20 reading_efficiency 0.00%   exclusive_ratio 0.00% bandwidth_utilization 0.00%
group 21 reading_efficiency 0.00%   exclusive_ratio 0.00% bandwidth_utilization 0.00%
group 22 reading_efficiency 0.00%   exclusive_ratio 0.00% bandwidth_utilization 0.00%
group 23 reading_efficiency 0.00%   exclusive_ratio 0.00% bandwidth_utilization 0.00%
group 24 reading_efficiency 0.00%   exclusive_ratio 0.00% bandwidth_utilization 0.00%
group 25 reading_efficiency 0.00%   exclusive_ratio 0.00% bandwidth_utilization 0.00%
```

### 3. Search QPS 监测

`elem-smi` 在驱动层统计所有包的收发计数信息，提供底层硬件 QPS 数据作为性能参考。

#### 关键指标
- **driver.h2c.qps**: 软件向硬件发包的 QPS
- **driver.c2h.qps**: 软件读取硬件回包的 QPS

#### 监测命令
```bash
# 监测指定卡（如卡0）
elem-smi -q -c driver -i 0 -l 1

# 监测所有卡
elem-smi -q -c driver -l 1
```
<pre style="font-size: 12px; line-height: 1.2;">
+-------------------------+--------------------+-----------------------+-------------------------+-------------------------+
|         driver          |      card_idx      |           0           |                         |                         |
+-------------------------+--------------------+-----------------------+-------------------------+-------------------------+
|     driver_version      | 2.0.2.202507171648 |       pci_speed       | Speed 8.0GT/s, Width x4 |                         |
+-------------------------+--------------------+-----------------------+-------------------------+-------------------------+
| driver.h2c.speed (MB/s) |   driver.h2c.qps   | driver.h2c.hugepacket |    driver.h2c.packet    | driver.h2c.packing.rate |
+-------------------------+--------------------+-----------------------+-------------------------+-------------------------+
|            0            |         0          |        4295921        |        45785767         |        10.657963        |
+-------------------------+--------------------+-----------------------+-------------------------+-------------------------+
| driver.c2h.speed (MB/s) |   driver.c2h.qps   | driver.c2h.hugepacket |    driver.c2h.packet    | driver.c2h.packing.rate |
+-------------------------+--------------------+-----------------------+-------------------------+-------------------------+
|            0            |         0          |       12123190        |        45785767         |        3.7767096        |
+-------------------------+--------------------+-----------------------+-------------------------+-------------------------+
|         driver          |      card_idx      |           1           |                         |                         |
+-------------------------+--------------------+-----------------------+-------------------------+-------------------------+
|     driver_version      | 2.0.2.202507171648 |       pci_speed       | Speed 8.0GT/s, Width x4 |                         |
+-------------------------+--------------------+-----------------------+-------------------------+-------------------------+
| driver.h2c.speed (MB/s) |   driver.h2c.qps   | driver.h2c.hugepacket |    driver.h2c.packet    | driver.h2c.packing.rate |
+-------------------------+--------------------+-----------------------+-------------------------+-------------------------+
|            0            |         0          |           0           |            0            |            0            |
+-------------------------+--------------------+-----------------------+-------------------------+-------------------------+
| driver.c2h.speed (MB/s) |   driver.c2h.qps   | driver.c2h.hugepacket |    driver.c2h.packet    | driver.c2h.packing.rate |
+-------------------------+--------------------+-----------------------+-------------------------+-------------------------+
|            0            |         0          |           0           |            0            |            0            |
+-------------------------+--------------------+-----------------------+-------------------------+-------------------------+
|         driver          |      card_idx      |           2           |                         |                         |
+-------------------------+--------------------+-----------------------+-------------------------+-------------------------+
|     driver_version      | 2.0.2.202507171648 |       pci_speed       | Speed 8.0GT/s, Width x4 |                         |
+-------------------------+--------------------+-----------------------+-------------------------+-------------------------+
| driver.h2c.speed (MB/s) |   driver.h2c.qps   | driver.h2c.hugepacket |    driver.h2c.packet    | driver.h2c.packing.rate |
+-------------------------+--------------------+-----------------------+-------------------------+-------------------------+
|            0            |         0          |           0           |            0            |            0            |
+-------------------------+--------------------+-----------------------+-------------------------+-------------------------+
| driver.c2h.speed (MB/s) |   driver.c2h.qps   | driver.c2h.hugepacket |    driver.c2h.packet    | driver.c2h.packing.rate |
+-------------------------+--------------------+-----------------------+-------------------------+-------------------------+
|            0            |         0          |           0           |            0            |            0            |
+-------------------------+--------------------+-----------------------+-------------------------+-------------------------+
|         driver          |      card_idx      |           3           |                         |                         |
+-------------------------+--------------------+-----------------------+-------------------------+-------------------------+
|     driver_version      | 2.0.2.202507171648 |       pci_speed       | Speed 8.0GT/s, Width x4 |                         |
+-------------------------+--------------------+-----------------------+-------------------------+-------------------------+
| driver.h2c.speed (MB/s) |   driver.h2c.qps   | driver.h2c.hugepacket |    driver.h2c.packet    | driver.h2c.packing.rate |
+-------------------------+--------------------+-----------------------+-------------------------+-------------------------+
|            0            |         0          |         3570          |          8873           |        2.485434         |
+-------------------------+--------------------+-----------------------+-------------------------+-------------------------+
| driver.c2h.speed (MB/s) |   driver.c2h.qps   | driver.c2h.hugepacket |    driver.c2h.packet    | driver.c2h.packing.rate |
+-------------------------+--------------------+-----------------------+-------------------------+-------------------------+
|            0            |         0          |         5263          |          8873           |        1.6859206        |
+-------------------------+--------------------+-----------------------+-------------------------+-------------------------+
|         driver          |      card_idx      |           4           |                         |                         |
+-------------------------+--------------------+-----------------------+-------------------------+-------------------------+
|     driver_version      | 2.0.2.202507171648 |       pci_speed       | Speed 8.0GT/s, Width x4 |                         |
+-------------------------+--------------------+-----------------------+-------------------------+-------------------------+
| driver.h2c.speed (MB/s) |   driver.h2c.qps   | driver.h2c.hugepacket |    driver.h2c.packet    | driver.h2c.packing.rate |
+-------------------------+--------------------+-----------------------+-------------------------+-------------------------+
|            0            |         0          |           0           |            0            |            0            |
+-------------------------+--------------------+-----------------------+-------------------------+-------------------------+
| driver.c2h.speed (MB/s) |   driver.c2h.qps   | driver.c2h.hugepacket |    driver.c2h.packet    | driver.c2h.packing.rate |
+-------------------------+--------------------+-----------------------+-------------------------+-------------------------+
|            0            |         0          |           0           |            0            |            0            |
+-------------------------+--------------------+-----------------------+-------------------------+-------------------------+
</pre>

### 性能优化建议

1. **缓冲区优化**: 保持 H2C Buffer 在 75-100% 范围内, 保持 C2H Buffer 在 0-25% 范围内
2. **内存利用率**: 目标 HBM 利用率达到 60% 左右
3. **实时监控**: 使用 `-l 1` 参数进行秒级监控，及时发现性能瓶颈

## 最佳实践

1. **渐进式调优**：从默认参数开始，逐步调整单个参数
2. **多轮测试**：每个配置运行多次取平均值
3. **资源监控**：关注CPU、内存、网络使用情况
4. **记录基准**：建立性能基线用于回归测试

