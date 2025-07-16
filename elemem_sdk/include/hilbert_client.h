#pragma once

#include <iostream>
#include <random>
#include <memory>
#include <sstream>


namespace hilbert {

enum class IndexType {
    BF = 0,
    IVF = 1,
};

struct Index {
    std::string name;
    uint32_t nlist;
    uint32_t dim;
    uint32_t nb;
    IndexType index_type;
    uint32_t replica_num;
};

using vec_id_t = uint32_t;
using vec_size_t = uint32_t;

class HilbertClient {
public:
    HilbertClient();
    virtual ~HilbertClient();
    int init(const std::string& server_address, const int32_t timeout_ms = -1);
    int create_index(const std::string& name, const uint32_t dim, const uint32_t replica_num,
                     const IndexType index_type, const uint32_t card_num);
    int delete_index(const std::string& name);
    int query_all_index(std::vector<Index>& indices);
    int train(const std::string& name, const vec_size_t nb, const uint32_t dim, const float* xbs, const uint32_t nlist, const int timeout_ms = -1);
    int add(const std::string& name, const vec_size_t nb, const uint32_t dim, const float* xbs, std::vector<vec_id_t>& ids, const int timeout_ms = -1);
    int remove(const std::string& name, const vec_id_t id);
    int query(const std::string& name, const vec_id_t id, std::vector<float>& data);
    int update(const std::string& name, const vec_id_t id, const uint32_t dim, const float* data);
    int search(const std::string& name, const vec_size_t nq, const uint32_t dim, const float* query,
               const uint32_t nprob, const uint32_t k, std::vector<float>& distances, std::vector<vec_id_t>& ids);

private:
    class Impl;
    std::unique_ptr<Impl> _impl;
};

}  // namespace hilbert
