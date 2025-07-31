
### 安装docker相关

- 安装 [Docker](https://docs.docker.com/get-docker/)
- 安装 [Docker Compose](https://docs.docker.com/compose/install/)


### 安装加速卡 SDK 运行 Demo

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
sudo docker compose run --rm client     --server 127.0.0.1:7000     --hdf5 /mnt/Algorithm/datapath/QA_/SIFT/SIFT_1M.hdf5
# 127.0.0.1 可更换为docker宿主机的ip
# --hdf5 后可配置为本地数据文件的路径

# 查看运行状态
docker compose ps

# 运行 SDK Demo
$ docker exec -it elemem_sdk_demo /bin/bash && cd elemem_sdk_demo
$ python3 sdk_demo.py
$ ./sdk_demo
```
---
