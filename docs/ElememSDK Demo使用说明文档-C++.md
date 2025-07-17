# ElememSDK Demo使用说明书-C++

## 1. 概述

本使用说明书介绍了如何使用C++语言编写的ElememSDK示例程序。该程序演示了如何连接ElememSDK服务端并执行索引创建、训练、数据添加、查询、更新和删除等操作。

## 2. 环境准备

### 2.1 开发环境要求

- 操作系统：Ubuntu 24.04
- C++编译器：支持C++17标准的编译器（推荐GCC或Clang）
- ElememSDK相关依赖库
- Bazel构建工具
- Docker环境

### 2.2 程序目录结构

拉取最新的elemem-sdk代码
```
git clone https://github.com/elemem-dev/elemem-sdk
```

进入到example/c++目录，文件结构如下：

```
├── BUILD.bazel
├── hilbert_client_demo.cpp
├── include
│   └── hilbert_client.h
├── lib
│   └── libhilbert_client.so
└── WORKSPACE.bazel
```

### 2.3 构建程序

使用Bazel进行程序编译：

```shell
bazel build //:hilbert_client_demo
```

## 3. Docker镜像运行

程序已封装在Docker镜像`elemem-sdk-demo-c++`中，执行以下命令运行：

```shell
docker run --rm -it elemem-sdk-demo-c++ --ip <IP> --port <PORT>
```

## 4. 程序运行

### 4.1 命令行参数说明

程序支持以下命令行参数：

| 参数             | 描述               | 默认值       |
| -------------- | ---------------- | --------- |
| `-h`, `--help` | 显示帮助信息           | -         |
| `-i`, `--ip`   | ElememSDK服务器IP地址 | 127.0.0.1 |
| `-p`, `--port` | ElememSDK服务器端口号  | 7000      |

### 4.2 运行示例

```shell
./bazel-bin/hilbert_client_demo --ip 192.168.1.100 --port 7000
```

## 5. 功能说明

程序连接到ElememSDK服务器后，会执行以下操作：

### 5.1 连接服务器

程序启动时自动连接ElememSDK服务端，连接成功则输出：

```
Connected to server at <IP>:<Port>
```

### 5.2 索引操作

程序会依次对两种索引类型（IVF和BF）执行以下操作：

- 创建索引（`create_index`）
- 查询所有索引（`query_all_index`）
- 删除索引（`delete_index`）

### 5.3 数据操作

程序对创建的索引执行数据相关操作，包括：

- 训练索引（`train`）
- 添加数据（`add`）
- 搜索数据（`search`）
- 删除数据（`remove`）
- 更新数据（`update`）
- 查询数据（`query`）

每个操作执行成功后会输出相应的成功提示信息。

## 6. 常见问题与排查

- **连接失败**：请检查服务端地址和端口是否正确。
- **索引创建失败**：检查索引名是否已存在，或服务端状态是否正常。
- **数据操作失败**：请确认数据维度（dim）和数量是否符合服务端限制。

## 7. 技术支持

如遇到任何问题或需要进一步帮助，请联系ElememSDK技术支持团队。

---

本使用说明书为您提供了快速使用ElememSDK示例程序的必要指导，希望对您的开发工作有所帮助。

