
# 向量数据加速卡 使用手册

## 1. 产品简介

本产品为高性能向量加速卡，结合专用硬件、驱动与 SDK，面向向量检索、推荐系统、AI 特征比对等场景，提供低延迟、高吞吐的计算能力。

---

## 2. 环境准备

### 2.1 硬件要求

- 主机：支持 PCIe gen4 x16 插槽，推荐 4U/2U 工业机
- 电源：推荐 ≥850W
- 卡数量支持：最多支持 8 母卡

### 2.2 软件要求

| 软件组件       | 最低版本 | 安装方式                  |
|----------------|----------|---------------------------|
| Ubuntu         | 22.04    | 官方镜像安装              |
| Python         | ≥3.8     | `sudo apt install python3` |
| g++/gcc        | ≥13      | `sudo apt install gcc-13` |
| bazel          | ≥6.3.0    | 脚本安装                  |
| docker         | ≥28.1.1    | 官方镜像安装                  |

---

## 3. 安装与部署

### 3.1 驱动安装

```bash
wget https://github.com/elemem-dev/elemem-sdk/release/v2.0/hilbert_driver_v2.0.0.deb
sudo dpkg -i hilbert_driver_v2.0.0.deb
modprobe hilbert
```

验证是否识别：
```bash
elemem-smi -a # 打印卡的详细信息，说明安装成功
```

### 3.2 安装docker相关

- 安装 [Docker](https://docs.docker.com/get-docker/)
- 安装 [Docker Compose](https://docs.docker.com/compose/install/)


### 3.3 安装加速卡 SDK 运行 Demo

```
# 下载 SDK 工程代码
git clone https://github.com/elemem-dev/elemem-sdk.git

# 进入工程目录
cd elemem-sdk

# 工程目录结构如下
- demo
- docker-compose.yml

# 启动加速卡引擎
docker compose up -d server # docker-compose.yml 中配置了本地端口8008映射到容器内端口8000

curl http://localhost:8008/health # 返回ok说明安装成功

# 运行 C++ Demo
docker compose run --rm client -i 127.0.0.1 -p 8008 # 127.0.0.1 更换为docker宿主机的ip

# 查看运行状态
docker compose ps

# 运行 SDK Demo
$ docker exec -it elemem_sdk_demo /bin/bash && cd elemem_sdk_demo
$ python3 sdk_demo.py
$ ./sdk_demo
```
---


## 4. C++ 接口说明

### 4.1 初始化
```c++
hilbert::HilbertClient client;
client.init("127.0.0.1:8000");
```
### 4.2 创建索引
```c++
std::string name = "test_index";
uint32_t dim = 128;
uint32_t replica_num = 1;
hilbert::SearchType search_type = hilbert::SearchType::IVF;
client.create_index(name, dim, replica_num, search_type);
```
### 4.3 删除索引
```c++
client.delete_index(name);
```
### 4.4 查询索引
```c++
std::vector<hilbert::Index> indices;
client.query_all_index(indices);
```
### 4.5 添加向量
```c++
std::vector<float> xbs(dim * 10, 0.5);
client.add(name, 10, dim, xbs);
```
### 4.6 搜索向量
```c++
uint32_t nq = 1;
std::vector<float> query(dim, 0.5);
uint32_t nprob = 10;
uint32_t k = 5;
client.search(name, nq, dim, query.data(), nprob, k);
```
### 4.7 删除向量
```c++
uint64_t id = 1;
client.Delete(name, id);
```
### 4.8 更新向量
```c++
std::vector<float> new_vec(dim, 0.5);
client.update(name, id, dim, new_vec.data());
```
### 4.9 查询向量
```c++
std::vector<float> vec;
client.query(name, id, vec);
```

## 5. Python 接口说明

### 5.1 初始化

```python
import hilbert
hilbert.hilbert_init()
```

### 5.2 添加向量

```python
index = hilbert.BFIndex(dim=128)
index.full_add(nb=1000, base=hilbert.swig_ptr(vectors), sync=True)
```

### 5.3 搜索向量

```python
index.full_search(nq=10, query=hilbert.swig_ptr(q), k=100,
                  distance=hilbert.swig_ptr(d), labels=hilbert.swig_ptr(l))
```

### 5.4 保存/加载索引

```python
index.save(b"my_index")
index.load(b"my_index")
```

---

## 6. 调试与性能分析

日志路径：
```bash
/var/log/elemem/vpu_engine.log
/var/log/elemem/vpu_engine.log.wf
```

性能查看：
```bash
elemem-smi watch -n 1
```

---

## 7. 常见问题 FAQ

| 问题                           | 解决方法                     |
|--------------------------------|------------------------------|
| 无法识别加速卡                | 检查 PCIe 插槽与驱动安装     |
| 添加向量失败                  | 检查资源是否耗尽 / 参数错误 |
| 搜索结果为空或精度低          | 检查索引构建流程是否完整     |

---

## 8. 附录

- [性能对比数据](docs/perf_report.md)

