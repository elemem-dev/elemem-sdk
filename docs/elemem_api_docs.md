# Hilbert V2 软件接口文档

## 通用返回值的数据结构

以下接口默认都会有通用的返回结构体，每个接口里不再赘述。

| 参数名 | 类型 | 说明 |
|--------|------|------|
| status.code | int32 | 状态码<br/>0：成功<br/>2100：SDK common error<br/>2101：Index name already exists<br/>2102：Index name does not exist<br/>2103：Index creation failed<br/>2104：Index deletion failed<br/>2105：Index number exceeds maximum limit<br/>2106：Index training failed<br/>2107：Index search failed<br/>2108：Index add failed<br/>2109：Index remove failed<br/>2110：Index query failed<br/>2111：Index update failed<br/>2112：Failed to read file<br/>2113：Invalid index name |
| status.message | string | 对状态码的描述。例如code为0时，message为成功 |

## 管理index

### create_index

**功能：** 创建索引，索引数量最大不超过128个，超过128个后会返回error

**输入参数：**

| 参数名 | 类型 | 是否必选 | 默认值 | 说明 |
|--------|------|----------|--------|------|
| name | string | 是 | - | 索引名称，只能包含字母数字和下划线，长度大于等于1小于等于50字节 |
| dim | uint32_t | 是 | - | 维度[1,8192] |
| dim_ddr | uint32_t | 否 | dim | ddr上存放的维度 |
| ddr_data_type | enum | 否 | fp16 | ddr数据精度 |
| base_data_type | enum | 否 | float | base数据精度 |
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

**输出参数：**

| 参数名 | 类型 | 是否必选 | 默认值 | 说明 |
|--------|------|----------|--------|------|
| ids | std::vector<uint32_t> | 是 | - | 系统自动生成的底库id，每个base的元素都有一个id |
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

**输出参数：**

| 参数名 | 类型 | 是否必选 | 默认值 | 说明 |
|--------|------|----------|--------|------|
| data | std::vector<float> | 是 | - | 查询的原始向量 |
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
| status.code | int32 | 是 | - | 状态码<br/>0：成功<br/>非0：失败 |
