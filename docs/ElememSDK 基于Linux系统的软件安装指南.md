# ElememSDK 基于Linux系统的软件安装指南

## 概述

本指南将详细介绍如何在Linux系统上安装和配置ElememSDK。安装过程简单直接，主要包括下载、解压、停止旧服务和启动新服务等步骤。

## 系统要求

- **操作系统**: Linux发行版（Ubuntu 24.04）
- **权限**: 需要sudo管理员权限

## 安装步骤
### 步骤1：

安装软件运行时依赖
```bash
#!/bin/bash

set -ue

apt update
apt install -y build-essential
apt install -y libgoogle-perftools-dev
apt install -y libhdf5-dev
apt install -y libhiredis-dev
apt install -y libopenblas-dev
apt install -y wget
apt install -y cmake
apt install -y redis-server redis-tools

WORK_DIR=$(mktemp -d "./elem_XXXXXX")
FAISS_DIR="$WORK_DIR/faiss"
mkdir -p "$FAISS_DIR"
cd "$FAISS_DIR"
FAISS_PACKAGE="faiss.tar.gz"
wget https://github.com/facebookresearch/faiss/archive/refs/tags/v1.9.0.tar.gz -O ${FAISS_PACKAGE}
tar --strip-components=1 -xzf ${FAISS_PACKAGE}
cmake -B build . -DFAISS_ENABLE_GPU=OFF -DFAISS_ENABLE_PYTHON=OFF -DBUILD_TESTING=OFF -DBUILD_SHARED_LIBS=ON
make -C build -j faiss
make -C build install
echo 'export LD_LIBRARY_PATH=/usr/local/lib:${LD_LIBRARY_PATH:-}' >> /etc/profile
source /etc/profile

echo "deploy.sh completed successfully."
```


### 步骤2：下载安装包

首先从官方渠道获取ElememSDK的安装包。

```bash
# 使用wget下载（请替换为实际的下载链接）
wget https://releases.example.com/elemem-sdk/elemem-sdk-latest.tar.gz
```

**注意**: 请确保从官方授权的下载地址获取安装包，以保证软件的完整性和安全性。

### 步骤3：解压缩安装包

将下载的压缩包解压到指定目录：

```bash
# 解压到当前目录
tar -xzf elemem-sdk-latest.tar.gz
```

解压后，您应该看到类似以下的目录结构：

```
elemem-sdk/
├── bin/
├── lib/
├── config/
├── start.sh
├── stop.sh
├── README.md
└── LICENSE
```

### 步骤4：进入安装目录

```bash
cd elemem-sdk
```

### 步骤5：停止现有服务

在安装新版本之前，需要先停止可能正在运行的旧版本服务：

```bash
sudo ./stop.sh
```

**说明**: 
- 此命令会安全地停止ElememSDK相关的所有服务进程
- 如果是首次安装，此步骤可能显示"服务未运行"的提示，这是正常现象
- 停止过程可能需要几秒钟时间，请耐心等待

### 步骤6：启动服务

停止完成后，执行启动脚本：

```bash
sudo ./start.sh
```

**说明**:
- 此命令会启动ElememSDK的所有必要服务
- 启动过程中会进行配置检查和服务初始化
- 成功启动后，系统会显示相关的状态信息

## 验证安装

### 检查服务状态

```bash
# 检查进程是否正在运行
ps aux | grep index_coordinator
ps aux | grep reram_engine

# 检查端口占用情况（如果适用）
netstat -tlnp | grep index_coordinator
netstat -tlnp | grep reram_engine
```

### 查看日志

```bash
# 查看运行时日志
less index_coordinator/log/index_coordinator.log
less index_coordinator/log/index_coordinator.log.wf
less vpu_engine/log/hilbert_1s.log
less vpu_engine/log/hilbert_1s.log.wf
```

## 常见问题解决

### 权限问题

如果遇到权限相关错误，请确保：

1. 使用sudo执行停止和启动脚本
2. 检查脚本文件的执行权限：
   ```bash
   chmod +x start.sh stop.sh
   ```

### 端口冲突

如果启动时提示端口被占用：

1. 检查占用端口的进程：
   ```bash
   lsof -i :端口号
   ```

2. 停止冲突的服务或修改配置文件中的端口设置

### 依赖缺失

如果提示缺少依赖库：

```bash
sudo apt-get update
sudo apt-get install 依赖包名
```

## 注意事项

- 在生产环境中安装前，建议先在测试环境中验证
- 安装过程中请保持网络连接稳定
- 建议在执行安装前备份重要数据
- 如遇到问题，请查看日志文件或联系技术支持

## 技术支持

如果在安装过程中遇到问题，请：

1. 查看安装日志文件
2. 检查系统环境是否满足要求
3. 参考官方文档或联系技术支持团队

---

*本指南适用于ElememSDK最新版本，如有更新请以官方文档为准。*
