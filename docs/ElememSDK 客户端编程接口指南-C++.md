## 4. C++ 接口说明

### 4.1 初始化
```c++
hilbert::HilbertClient client;
const std::string server_address = "127.0.0.1:7000";
const int32_t timeout_ms = -1;
const int log_level = 3; //日志等级，0:trace,1:debug,2:info,3:warn,4:err,5:critical,6:off
client.init(server_address, timeout_ms, log_level);
```
### 4.2 创建索引
```c++
std::string name = "test_index"; //只能包含字母数字下划线，长度[1,50]
uint32_t dim = 128; // [1,8192]
uint32_t replica_num = 1; //[0,2]
hilbert::IndexType index_type = hilbert::IndexType::IVF;
uint32_t card_num = 1; //使用卡数，范围[1,8]
client.create_index(name, dim, replica_num, index_type, card_num);
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
### 4.5 训练索引
```c++
const std::string name = "test_index";
const vec_size_t nb = 10000;
const uint32_t dim = 128;
std::vector<float> xbs(nb * dim);
std::mt19937 gen(42);
std::normal_distribution<> dist(0.0, 1.0);
for (size_t i = 0; i < nb * dim; ++i) {
    xbs[i] = dist(gen);
}
const uint32_t nlist = 12;  //簇个数，必须小于nb
client.train(name, nb, dim, xbs.data(), nlist);
```
### 4.6 添加向量
```c++
std::vector<vec_id_t> ids;
client.add(name, nb, dim, xbs.data(), ids);
```
### 4.7 搜索向量
```c++
uint32_t nq = 1;
std::vector<float> query(dim * nq);
for (size_t i = 0; i < dim * nq; ++i) {
    query[i] = dist(gen);
}
uint32_t nprob = 10;
uint32_t k = 5;
std::vector<float> distances;
std::vector<vec_id_t> ids;
client.search(name, nq, dim, query.data(), nprob, k, distances, ids);
```
### 4.8 删除向量
```c++
vec_id_t id = 1;
client.remove(name, id);
```
### 4.9 更新向量
```c++
std::vector<float> new_vec(dim);
for (size_t i = 0; i < dim; ++i) {
    new_vec[i] = dist(gen);
}
client.update(name, id, dim, new_vec.data());
```
### 4.10 查询向量
```c++
std::vector<float> vec;
client.query(name, id, vec);
```
