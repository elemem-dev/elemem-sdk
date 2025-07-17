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
