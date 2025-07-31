# ElememSDK Demo使用说明书-Python

## 1. 概述
本使用说明书详细介绍了如何使用Python语言编写的ElememSDK示例程序。该程序示范如何连接ElememSDK服务端，并执行索引的创建、训练、添加数据、查询数据、更新数据以及删除操作。

## 2. 环境准备

### 2.1 开发环境要求
- Python 3.7及以上版本
- ElememSDK Python客户端
- Docker（推荐使用Docker运行）

### 2.2 目录结构

拉取最新的elemem-sdk代码
```
git clone https://github.com/elemem-dev/elemem-sdk
```

进入到example/python目录，文件结构如下：

```
├── client_demo.py
├── requirements.txt
└── run.sh
```

### 2.3 依赖安装
如果使用run.sh 运行，则不需要运行如下的安装命令，因为run.sh中已包含。
使用以下命令安装所需的Python依赖：
```shell
python3 -m venv .venv
source .venv/bin/activate # 建议进入虚拟环境运行
pip install -r requirements.txt
```

## 3. 程序运行

### 3.1 命令行参数说明
| 参数           | 描述                    | 默认值               |
|---------------|-------------------------|----------------------|
| `--server`    | ElememSDK服务器地址     | localhost:7000       |
| `--hdf5`      | HDF5数据文件路径         | 必填                 |
| `--index`     | 索引名称                | sift                 |

### 3.2 运行示例

```shell
python client_demo.py --server 192.168.1.100:7000 --hdf5 data/SIFT_1M.hdf5 --index sift
```
或使用提供的脚本：
```shell
./run.sh
```

## 4. 功能说明
程序运行时，会执行以下一系列操作：

### 4.1 连接服务器
启动时自动连接指定ElememSDK服务端，连接成功会记录日志：
```
启动 Hilbert 客户端演示
服务器: <server>
HDF5 文件: <hdf5路径>
索引名称: <索引名>
```

### 4.2 索引操作
程序执行以下索引操作：
- 删除旧索引（如果存在）
- 创建新索引
- 查询所有索引

### 4.3 数据操作
执行索引的数据管理操作：
- 训练索引
- 添加向量
- 查询向量
- 执行搜索测试（计算召回率）
- 更新向量
- 随机查询搜索
- 删除向量
- 删除索引

每个步骤成功执行后会输出详细日志信息。

## 5. 常见问题与排查

- **连接失败**：确认服务器IP及端口正确。
- **索引或数据操作失败**：检查日志以确定具体错误原因。

## 6. 技术支持
如遇到任何问题或需要更多帮助，请联系ElememSDK技术支持团队。

---

本说明书旨在帮助您快速入门ElememSDK的Python示例程序。希望对您的开发工作有所助益！

