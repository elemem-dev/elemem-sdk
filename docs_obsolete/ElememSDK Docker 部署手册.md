
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
sudo docker compose up -d server # -d是为了让容器在后台运行，不使用此参数会直接在当前运行，并直接打印日志到当前窗口。docker-compose.yml 中配置了本地端口8000映射到容器内端口8000
可以通过sudo docker logs elemem_server查看容器启动的日志，容器内的服务是通过supervisor控制的。
关于compose使用的一些说明：
在旧版中，可能需要使用sudo docker-compose up -d server。在旧版docker时，docker-compose是一个独立的命令，属于Compose v1(2023年标记为deprecated), 新版docker(≥20.10.13), compse v2(2020年推出的)可以作为一个插件安装，安装后compse是docker的一个子命令，建议使用最新版。

# 运行 C++ Demo
sudo docker compose run --rm client # --rm 代表退出后就删除本次创建的容器，请根据自己需要修改运行参数

# 127.0.0.1 可更换为docker宿主机的ip
# --hdf5 后可配置为本地数据文件的路径
# compose文件中可以看到挂载了/mnt/到容器内的/mnt/
# entrypoint.sh 详细写了如何运行各个demo，可以按需修改
cd /root/hilbert
bash entrypoint.sh --server 127.0.0.1:7000  --hdf5 /mnt/Algorithm/datapath/QA_/SIFT/SIFT_1M.hdf5

# 查看运行状态
sudo docker compose ps -a

# 其他未尽docker相关命令，请参考docker文档，在此不一一赘述
```


---
