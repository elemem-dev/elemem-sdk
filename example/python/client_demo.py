import logging
import numpy as np
import h5py
import argparse
#from elemem_sdk import HilbertClient, get_data_from_hdf5
from elemem_sdk import hilbert_client
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger('HilbertDemo')
logger.setLevel(logging.DEBUG)

def run_demo(server, hdf5_path, index_name="sift"):
    client = hilbert_client.HilbertClient(server, debug=True)
    try:
        # 1. 清理旧索引
        try:
            logger.info(f"尝试删除旧索引: {index_name}")
            client.delete_index(index_name)
        except Exception as e:
            logger.warning(f"删除索引失败: {str(e)} (可能索引不存在)")

        # 2. 创建新索引
        logger.info("\n" + "="*50 + "\nStarting CREATE INDEX\n" + "="*50)
        client.create_index(index_name, 128, 1, 1, 1)

        # 3. 查询所有索引
        logger.info("\n" + "="*50 + "\nStarting QUERY ALL INDEXES\n" + "="*50)
        indices = client.query_all_index()

        # 4. 准备数据
        data, nb, dim = hilbert_client.get_data_from_hdf5(hdf5_path)

        # 5. 训练索引
        logger.info("\n" + "="*50 + "\nStarting TRAIN\n" + "="*50)
        client.train(
                name=index_name,
                data=data,
                nlist=128
        )

        # 6. 准备数据
        data, nb, dim = hilbert_client.get_data_from_hdf5(hdf5_path)
        # 7. 添加向量
        logger.info("\n" + "="*50 + "\nStarting ADD\n" + "="*50)
        ids = client.add(
                name=index_name,
                data=data
        )

        # 8. 查询向量
        logger.info("\n" + "="*50 + "\nStarting QUERY VECTOR\n" + "="*50)
        if ids:
            vector_id = ids[0]
            query_response = client.query_vector(index_name, vector_id)
            logger.info(f"查询到向量元数据: ID={vector_id}, 维度={len(query_response.data)}")

        # 9. 搜索测试
        logger.info("\n" + "="*50 + "\n执行搜索测试\n" + "="*50)
        nq = 100
        with h5py.File(hdf5_path, 'r') as f:
            base = f['train'][:nq]
        distances, labels = client.search(index_name, base, k=1, nprob=5)
        top1 = labels[:, 0]
        truth = np.arange(nq, dtype=top1.dtype)
        recall1 = np.mean(top1 == truth)
        logger.info(f"Recall@1 over {nq} queries: {recall1 * 100:.2f}%")

        # 10. 更新向量
        logger.info("\n" + "="*50 + "\nStarting UPDATE VECTOR\n" + "="*50)
        if ids:
            new_data = np.random.rand(dim).astype(np.float32).tolist()
            client.update_vector(index_name, vector_id, new_data)

        # 11. 搜索随机查询
        logger.info("\n" + "="*50 + "\nStarting SEARCH\n" + "="*50)
        nq = 10
        test_queries = np.random.rand(nq, dim).astype(np.float32)
        distances, labels = client.search(index_name, test_queries, k=3)
        logger.info("\nSearch Results:")
        for i in range(nq):
            logger.info(f"查询 {i+1}: 距离={distances[i]}, 标签={labels[i]}")

        # 12. 删除向量
        logger.info("\n" + "="*50 + "\nStarting DELETE VECTOR\n" + "="*50)
        if ids:
            client.delete_vector(index_name, vector_id)

        # 13. 删除索引
        logger.info("\n" + "="*50 + "\nStarting DELETE INDEX\n" + "="*50)
        client.delete_index(index_name)

        logger.info("\n" + "="*50 + "\nALL OPERATIONS COMPLETED SUCCESSFULLY\n" + "="*50)

    except Exception as e:
        logger.exception("Operation failed")
        logger.error("\n" + "="*50, "\nOPERATION FAILED\n" + "="*50)
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Hilbert Client Demo')
    parser.add_argument('--server', default='localhost:7000', help='Server address')
    parser.add_argument('--hdf5', required=True, default='.data/SIFT_1M.hdf5', help='HDF5 data path')
    parser.add_argument('--index', default='sift', help='name of index')
    args = parser.parse_args()

    logger.info(f"启动 Hilbert 客户端演示")
    logger.info(f"服务器: {args.server}")
    logger.info(f"HDF5 文件: {args.hdf5}")
    logger.info(f"索引名称: {args.index}")

    run_demo(args.server, args.hdf5, args.index)
