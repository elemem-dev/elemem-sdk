

```
#include <getopt.h>

#include <cstdlib>
#include <random>
#include <string>

#include "hilbert_client.h"

void print_usage(const char* prog_name) {
    std::cout << "Usage: " << prog_name << " [OPTIONS]\n\n"
              << "Options:\n"
              << "  -h, --help        Show this help message and exit\n"
              << "  -i --ip <IP>      Server IP address (default: 127.0.0.1)\n"
              << "  -p --port <PORT>  Server port number (default: 7000)\n";
}

int main(int argc, char* argv[]) {
    std::string ip = "127.0.0.1";
    int port = 7000;

    const char* short_opts = "hi:p:";
    const struct option long_opts[] = {{"help", no_argument, nullptr, 'h'},
                                       {"ip", required_argument, nullptr, 'i'},
                                       {"port", required_argument, nullptr, 'p'},
                                       {nullptr, 0, nullptr, 0}};

    int opt = 0;
    while ((opt = getopt_long(argc, argv, short_opts, long_opts, nullptr)) != -1) {
        switch (opt) {
            case 'h':
                print_usage(argv[0]);
                return 0;
            case 'i':
                ip = optarg;
                break;
            case 'p':
                try {
                    port = std::stoi(optarg);
                    if (port <= 0 || port > 65535) {
                        throw std::out_of_range("port out of range");
                    }
                } catch (...) {
                    std::cerr << "Invalid port: " << optarg << "\n\n";
                    print_usage(argv[0]);
                    return 1;
                }
                break;
            default:
                std::cerr << "\n";
                print_usage(argv[0]);
                return 1;
        }
    }

    std::string endpoint = ip + ":" + std::to_string(port);
    hilbert::HilbertClient client;
    if (client.init(endpoint) != 0) {
        std::cerr << "Fail to initialize client at " << endpoint << '\n';
        return -1;
    }

    std::cout << "Connected to server at " << endpoint << "\n";

    std::vector<hilbert::IndexType> index_types{hilbert::IndexType::IVF, hilbert::IndexType::BF};
    for (auto index_type : index_types) {
        std::string name = "ttttt";
        const uint32_t dim = 128;
        uint32_t replica_num = 1;
        uint32_t card_num = 1;

        std::mt19937 gen(42);
        std::normal_distribution<> dist(0.0, 1.0);

        const size_t nb = 200;
        std::vector<float> xbs(dim * nb);
        for (size_t i = 0; i < nb * dim; ++i) {
            xbs[i] = dist(gen);
        }
        const uint32_t nlist = 3;
        uint32_t nprobe = 3;
        std::vector<hilbert::vec_id_t> ids;

        client.delete_index(name);
        if (client.create_index(name, dim, replica_num, index_type, card_num) != 0) {
            std::cerr << "Fail to create index" << '\n';
            return -1;
        }
        std::cout << "Index created successfully" << '\n';
        if (client.create_index(name + "xxx", dim, replica_num, index_type, card_num) != 0) {
            std::cerr << "Fail to create index" << '\n';
            return -1;
        }
        std::cout << "Index created successfully" << '\n';

        std::vector<hilbert::Index> indices;
        if (client.query_all_index(indices) != 0) {
            std::cerr << "Fail to query all index" << '\n';
            return -1;
        }
        for (const auto& idx : indices) {
            std::cout << "Index name: " << idx.name << ", dim: " << idx.dim << ", nlist: " << idx.nlist
                      << ", nb: " << idx.nb << '\n';
        }

        if (client.delete_index(name + "xxx") != 0) {
            std::cerr << "Fail to delete index" << '\n';
            return -1;
        }
        std::cout << "Index deleted successfully" << '\n';

        if (client.train(name, nb, dim, xbs.data(), nlist) != 0) {
            std::cerr << "Fail to train index" << '\n';
            return -1;
        }
        std::cout << "Index trained successfully" << '\n';

        if (client.add(name, nb, dim, xbs.data(), ids) != 0) {
            std::cerr << "Fails to add index" << '\n';
            return -1;
        }
        std::cout << "Index added successfully" << '\n';

        if (client.add(name, nb, dim, xbs.data(), ids) != 0) {
            std::cerr << "Fails to add index" << '\n';
            return -1;
        }
        std::cout << "Index added successfully" << '\n';

        uint32_t nq = 1;
        std::vector<float> query(dim, 0.5);
        uint32_t k = 1;
        ids.clear();
        std::vector<float> distances;
        for (int i = 0; i < std::min(xbs.size(), size_t(10)); ++i) {
            std::vector<float> query(xbs.data() + i * dim, xbs.data() + (i + 1) * dim);
            ids.clear();
            distances.clear();
            if (client.search(name, nq, dim, query.data(), nprobe, k, distances, ids) != 0) {
                std::cerr << "Fail to search data" << '\n';
                return -1;
            }
            std::cout << "Data searched successfully" << '\n';
        }

        uint64_t id = 1;
        if (client.remove(name, id) != 0) {
            std::cerr << "Fail to remove data" << '\n';
            return -1;
        }
        std::cout << "Data removed successfully" << '\n';

        id = 2;
        std::vector<float> new_vec(dim, 0.5);
        if (client.update(name, id, dim, new_vec.data()) != 0) {
            std::cerr << "Fail to update data" << '\n';
            return -1;
        }
        std::cout << "Data updated successfully" << '\n';

        std::vector<float> vec;
        if (client.query(name, id, vec) != 0) {
            std::cerr << "Fail to query data" << '\n';
            return -1;
        }
        if (vec == new_vec) {
            std::cout << "Data queried successfully" << '\n';
        } else {
            std::cerr << "Queried data does not match updated data" << '\n';
            return -1;
        }

        std::cout << "All operations completed successfully" << '\n';
    }
    return 0;
}
```