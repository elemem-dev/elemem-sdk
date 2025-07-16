# Hilbert V2 软件接口文档

## 通用返回值的数据结构

以下接口默认都会有通用的返回结构体，每个接口里不再赘述。

| 参数名 | 类型 | 说明 |
|--------|------|------|
| status.code | int32 | 状态码<br/>0：成功<br/>2100：SDK common error<br/>2101：Index name already exists<br/>2102：Index name does not exist<br/>2103：Index creation failed<br/>2104：Index deletion failed<br/>2105：Index number exceeds maximum limit<br/>2106：Index training failed<br/>2107：Index search failed<br/>2108：Index add failed<br/>2109：Index remove failed<br/>2110：Index query failed<br/>2111：Index update failed<br/>2112：Failed to read file<br/>2113：Invalid index name |
| status.message | string | 对状态码的描述。例如code为0时，message为成功 |

> 标记黄色内容是内部参数，用户和测试无需关注

## 管理index

### create_index

**功能：** 创建索引，索引数量最大不超过128个，超过128个后会返回error

**输入参数：**

| 参数名 | 类型 | 是否必选 | 默认值 | 说明 |
|--------|------|----------|--------|------|
| name | string | 是 | - | 索引名称，只能包含字母数字和下划线，长度大于等于1小于等于50字节 |
| dim | uint32_t | 是 | - | 维度[1,8192] |
| dim_ddr | uint32_t | 否 | dim | ddr上存放的维度 |
| ddr_data_type | enum | 否 | fp16 | ddr数据精度（一期只支持fp16） |
| base_data_type | enum | 否 | float | base数据精度（一期只支持float） |
| replica_num | uint32_t | 否 | - | 副本数量[1,10] |
| index_type | enum | 否 | 0 | 0:bf，1：ivf |
| card_num | uint32_t | - | - | 用户要使用的卡数量 |

**输出参数：**

| 参数名 | 类型 | 是否必选 | 默认值 | 说明 |
|--------|------|----------|--------|------|
| status.code | int32 | 是 | - | 状态码<br/>0：成功<br/>非0：失败 |

### delete_index

**功能：** 删除索引

**输入参数：**

| 参数名 | 类型 | 是否必选 | 默认值 | 说明 |
|--------|------|----------|--------|------|
| name | string | 是 | - | 索引名称 |
| reset_flag | int32 | 是 | - | 第0位表示是否处理fpga的ddr<br/>第1位表示是否处理chip |

**输出参数：**

| 参数名 | 类型 | 是否必选 | 默认值 | 说明 |
|--------|------|----------|--------|------|
| status.code | int32 | 是 | - | 状态码<br/>0：成功<br/>非0：失败 |

### query_all_index

**功能：** 查询所有的Index

**输出参数：**

| 参数名 | 类型 | 是否必选 | 默认值 | 说明 |
|--------|------|----------|--------|------|
| index_list | Array<Index> | - | - | Index数组 |
| index.name | string | - | - | 名称 |
| index.nlist | uint32_t | - | - | nlist |
| index.dim | uint32_t | - | - | 维度 |
| index.nb | uint32_t | - | - | 底库大小 |
| index.index_type | enum | - | - | 索引类型，bf、ivf |
| status.code | int32 | 是 | - | 状态码<br/>0：成功<br/>非0：失败 |

## 底库管理

### train

**功能：** 抽样后的底库训练，分簇

**输入参数：**

| 参数名 | 类型 | 是否必选 | 默认值 | 说明 |
|--------|------|----------|--------|------|
| name | string | 是 | - | 索引名称 |
| nb | uint32_t | 是 | - | train的数据大小 |
| dim | uint32_t | 是 | - | 维度，范围同create_index |
| base | float* | 是 | - | 底库数据 |
| nlist | uint32_t | 是 | - | 簇数量 |
| nq | int32 | 否 | - | - |
| query | float* | 否 | - | - |
| bar | float* | 否 | - | - |
| bar_num | uint32_t | 否 | - | - |

**输出参数：**

| 参数名 | 类型 | 是否必选 | 默认值 | 说明 |
|--------|------|----------|--------|------|
| status.code | int32 | 是 | - | 状态码<br/>0：成功<br/>非0：失败 |

### add

**功能：** 添加底库

**输入参数：**

| 参数名 | 类型 | 是否必选 | 默认值 | 说明 |
|--------|------|----------|--------|------|
| name | string | 是 | - | 索引名称 |
| nb | uint32_t | 是 | - | train的数据大小 |
| dim | uint32_t | 是 | - | 维度 |
| base | float* | 是 | - | 底库数据 |
| nlist | uint32_t | 是 | - | 簇数量 |
| mode_flag | int32 | 否 | 0 | 1：写到忆阻器；2：写到纯数字；1\|2：混合模式 |

**输出参数：**

| 参数名 | 类型 | 是否必选 | 默认值 | 说明 |
|--------|------|----------|--------|------|
| ids | std::vector<uint32_t> | 是 | - | 系统自动生成的底库id，每个base的元素都有一个id |
| status.code | int32 | 是 | - | 状态码<br/>0：成功<br/>非0：失败 |

### 数据文件说明

#### 测试功能和文件需求

| 测试功能\需要文件 | chip quant data | 聚类 | mapping |
|------------------|-----------------|------|---------|
| chip quant | √ | × | × |
| 聚类 | × | √ | × |
| (优先)mapping | × | √ | √ |

#### 文件格式说明

**base_data: 文件1**
- train: base type: vector size=nb*dim
- test: query type: vector size=nq*dim

**chip quant data**
- quant_base_data: chip数据, 单文件

**聚类 (文件2)**
- centroids: 簇中心向量
  - centroids: 簇中心 type: vector size=nlist*dim value=簇向量
- cluster_ids: idx->簇id映射
  - centroids_idx: 映射 type: vector size=nb, value=簇id

**mapping (文件3)**
- clusters_res: 簇资源描述
  - key=簇id int; value=resource list
  - 每个簇副本 vector<resource>

单个block resource结构：
- card_id: 范围0-7
- group_id: 0-25
- chip_id
- bank_id
- ddr_start, len
- col_start, len

**说明：** digital模式，resource没有chip,bank,col这些数据，len是ddr长度，len=vec_num*vec_size，单位byte，vec_size = dim*2bytes+32，vec_num = len/vec_size

- vec_num ≤ 16*1024个
- 最大ddr地址(ddr_start+len) ≤ 256*1024*1024

**bar_list: 文件4**
- key=bar_list value=list (size=bar_num)
- bar_num: 32-128个float，必须是32的倍数
- bar_ids: card_id对应一个未分配的bar_id，每个card一个，可能不同；如果使用空卡mapping，bar_id都默认0即可

### add_from_mapping

**功能：** 从映射文件中添加底库

**输入参数：**

| 参数名 | 类型 | 是否必选 | 默认值 | 说明 |
|--------|------|----------|--------|------|
| name | string | 是 | "_index" | 索引名称 |
| mapping_path | string | 是 | - | mapping文件路径 |

**输出参数：**

| 参数名 | 类型 | 是否必选 | 默认值 | 说明 |
|--------|------|----------|--------|------|
| status.code | int32 | 是 | - | 状态码<br/>0：成功<br/>非0：失败 |

### add_with_clusters_replicas

**功能：** 用户自己train分簇，并给定每个簇副本数量，每个副本在vpu上的地址，以及量化后的数据

**输入参数：**

| 参数名 | 类型 | 是否必选 | 默认值 | 说明 |
|--------|------|----------|--------|------|
| name | string | 是 | "_index" | 索引名称 |
| clusters | cluster | 是 | - | cluster数据 |
| cluster.replicas | cluster_replica | 是 | - | cluster副本 |
| cluster.replica.fp32data | float* | 是 | - | cluster副本原始向量 |
| cluster.replica.fp16data | float* | 是 | - | cluster副本fp16数据 |
| cluster.replica.int8data | int32* | 是 | - | cluster副本忆阻器上量化后数据 |
| cluster.replica.positions | position | 是 | - | 每个向量在vpu上的地址 |

**输出参数：**

| 参数名 | 类型 | 是否必选 | 默认值 | 说明 |
|--------|------|----------|--------|------|
| status.code | int32 | 是 | - | 状态码<br/>0：成功<br/>非0：失败 |

### add_with_clusters_data（二期）

**功能：** 用户自己train分簇，并给定每个簇副本数量，以及量化后的数据，软件自动为每个簇和副本分配硬件资源

**输入参数：**

| 参数名 | 类型 | 是否必选 | 默认值 | 说明 |
|--------|------|----------|--------|------|
| name | string | 是 | "_index" | 索引名称 |
| clusters | cluster | 是 | - | cluster数据 |
| cluster.replica_num | cluster_replica | 是 | - | cluster副本 |
| cluster.replica_fp32data | float* | 是 | - | cluster副本原始向量 |
| cluster.replica_fp16data | float* | 是 | - | cluster副本fp16数据 |
| cluster.replica_int8data | int32* | 是 | - | cluster副本忆阻器上量化后数据 |

**输出参数：**

| 参数名 | 类型 | 是否必选 | 默认值 | 说明 |
|--------|------|----------|--------|------|
| status.code | int32 | 是 | - | 状态码<br/>0：成功<br/>非0：失败 |

### remove

**功能：** 删除向量

**输入参数：**

| 参数名 | 类型 | 是否必选 | 默认值 | 说明 |
|--------|------|----------|--------|------|
| name | string | 是 | - | 索引名称 |
| id | uint32_t | 是 | - | 向量的id |

**输出参数：**

| 参数名 | 类型 | 是否必选 | 默认值 | 说明 |
|--------|------|----------|--------|------|
| status.code | int32 | 是 | - | 状态码<br/>0：成功<br/>非0：失败 |

### query

**功能：** 查询向量

**输入参数：**

| 参数名 | 类型 | 是否必选 | 默认值 | 说明 |
|--------|------|----------|--------|------|
| name | string | 是 | "_index" | 索引名称 |
| id | uint32_t | 否 | - | 向量的id |
| out_flag | uint32_t | 否 | 0 | 第0位表示是否输出hbm上的数据<br/>第1位表示是否输出芯片上的数据 |

**输出参数：**

| 参数名 | 类型 | 是否必选 | 默认值 | 说明 |
|--------|------|----------|--------|------|
| data | std::vector<float> | 是 | - | 查询的原始向量 |
| digital_data | float* | 否 | - | fpga ddr上的数据 |
| reram_data | int8* | 否 | - | 忆阻器上的数据 |
| status.code | int32 | 是 | - | 状态码<br/>0：成功<br/>非0：失败 |

### update

**功能：** 更新向量，忆阻器上的数据和ddr上的数据

**输入参数：**

| 参数名 | 类型 | 是否必选 | 默认值 | 说明 |
|--------|------|----------|--------|------|
| name | string | 是 | "_index" | 索引名称 |
| id | uint32_t | 否 | - | 向量的id |
| dim | uint32_t | 是 | - | 维度[16,8192] |
| data | float* | 是 | - | 向量数据 |

**输出参数：**

| 参数名 | 类型 | 是否必选 | 默认值 | 说明 |
|--------|------|----------|--------|------|
| status.code | int32 | 是 | - | 状态码<br/>0：成功<br/>非0：失败 |

## 搜索接口

### search

**功能：** 向量相似度搜索

**输入参数：**

| 参数名 | 类型 | 是否必选 | 默认值 | 说明 |
|--------|------|----------|--------|------|
| name | string | 是 | "_index" | 索引名称 |
| nq | uint32_t | 是 | - | query向量个数 |
| dim | uint32_t | 是 | - | 维度[16,8192] |
| query | float* | 是 | - | 查询向量的指针 |
| nprob | uint32_t | 是 | - | 选中簇的个数 |
| k | uint32_t | 是 | - | 最多召回的底库数量 |

**输出参数：**

| 参数名 | 类型 | 是否必选 | 默认值 | 说明 |
|--------|------|----------|--------|------|
| distance | std::vector<float> | 是 | - | 保存距离的指针 float32 |
| label | std::vector<uint32_t> | 是 | - | 保存结果向量id |
| search_mode | int32 | 是 | - | 0:未加速（fpga模式）；1：加速模式（reram模式） |
| status.code | int32 | 是 | - | 状态码<br/>0：成功<br/>非0：失败 |

### search_with_quant_data

**功能：** 向量相似度搜索，用户自己量化query数据，可以自定义th，例如希望芯片全筛，th=-128

**输入参数：**

| 参数名 | 类型 | 是否必选 | 默认值 | 说明 |
|--------|------|----------|--------|------|
| name | string | 是 | "_index" | 索引名称 |
| nq | int32 | 是 | - | query向量个数 |
| query | float* | 是 | - | 查询向量的指针 |
| ddr_query | float* | 否 | - | - |
| quant_query | int8* | 否 | - | 量化query |
| th | int32 | 否 | 0 | thd指令需要的th_num，0是不指定 |
| sample_rate | float | 否 | - | 粗筛比例 |
| k | int32 | 是 | - | 最多召回的底库数量 |
| nprob | int32 | 是 | - | 选中簇的个数 |

**输出参数：**

| 参数名 | 类型 | 是否必选 | 默认值 | 说明 |
|--------|------|----------|--------|------|
| distance | float* | 是 | - | 保存距离的指针 float32 |
| label | uint32_t* | 是 | - | 保存标签data_index int |
| status.code | int32 | 是 | - | 状态码<br/>0：成功<br/>非0：失败 |

## 参数说明

### 通用参数
- **nq**: query向量个数
- **query**: query向量指针
- **k**: 最多召回数量
- **distance**: 保存距离的指针 float32
- **label**: 保存标签data_index int
- **base**: 向量指针