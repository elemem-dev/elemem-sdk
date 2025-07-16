#!/bin/bash

pip install -r requirements.txt

python3 client_demo.py --server "127.0.0.1:7000" --hdf5 "/mnt/Algorithm/datapath/QA_/SIFT/SIFT_1M.hdf5"