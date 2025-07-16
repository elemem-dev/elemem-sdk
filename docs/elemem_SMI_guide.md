Elemem 向量数据加速卡 SMI 使用手册

elem-smi使用手册

elem-smi -h 打印如下

	~ elem-smi -h                                                                                                                 
Hello elem-smi~

Usage: elem-smi [OPTIONS]

Options:
  -L, --list-elem                      列出所有扫描到的 card的所有信息
  -f, --filename <f>                   打印到日志而不是标准输出
  -i, --id <i>                         特定的忆阻器 card 索引
  -l, --loop <l>                       循环显示的时间周期, 单位 s
  -q, --query                          表示这是一个查询动作
  -c, --category <c>                   展示类别入参可以是 overview card ddr driver
  -d, --display <d>                    展示类别入参参考-L
  -r, --range <r>                      查看debug信息((card_start, card_end), (group_start, group_end), (chip_start, chip_end)), card范围[0, 7], group范围[0, 25], chip范围[0, 2]
  -u, --hdna                           查看card id与hdna和dna的对应关系
  -F, --find-me                        卡的LED蓝灯闪烁
  -C, --clear                          清除驱动数据统计
  -R, --reset                          reset card
      --play <play>                    play <0>:bin <1>:json
      --play_filler <play_filler>      play_filler <0xb0> <176> <0xb1> <177>...
      --play_file <play_file>          play_file <play_file_path>
      --play_mode <play_mode>          play_mode <0> normal <1> huge
      --play_loop <play_loop>          play_loop times
      --record <record>                record <0>:bin <1>:json
      --record_skip                    record_skip to skip record payload
      --stop_record                    stop_record
      --record_file <record_file>      record_file <record_file_path>
      --buff_stat <buff_stat>          buff_stat <0-10000>
      --buff_interval <buff_interval>  buff_interval <us>
  -h, --help                           Print help
  -V, --version                        Print version

其他参数

  -h, --help                           Print help
  -V, --version                        Print version

辅助参数

-f -i -l 为辅助参数，几乎所有的参数都支持

  -f, --filename <f>                   打印到日志而不是标准输出
  -i, --id <i>                         特定的忆阻器 card 索引
  -l, --loop <l>                       循环显示的时间周期, 单位 s

-i 不加表示针对所有card操作，加则表示指定card。

-l 不加表示只打印一次，加则表示每间隔x秒打印一次，建议使用-l 1

-f 不加则表示打印到终端，加则输出到指定文件路径，若同时加上了-l参数，则每次打印会覆盖之前的内容，使用如vscode能实时更新的文本编辑器打开可以看到数据实时刷新。

信息查看

完整信息

辅助参数:全部正常生效。

    ~ elem-smi -L
+-------------------------+----------------------------------+-----------------------+-------------------------+-------------------------+
|        overview         |                                  |                       |                         |                         |
+-------------------------+----------------------------------+-----------------------+-------------------------+-------------------------+
|       card_index        |            group_num             |       chip_num        |        bank_size        |          alive          |
+-------------------------+----------------------------------+-----------------------+-------------------------+-------------------------+
|            0            |                26                |          78           |           16            |            1            |
+-------------------------+----------------------------------+-----------------------+-------------------------+-------------------------+
|      soft_version       |          driver_version          |      smi_version      |    firmware_version     |      fpga_version       |
+-------------------------+----------------------------------+-----------------------+-------------------------+-------------------------+
|   2.0.1.202507031525    |        2.0.1.202507031525        |  2.0.6.202507141135   |        25070801         |        25071411         |
+-------------------------+----------------------------------+-----------------------+-------------------------+-------------------------+
|          card           |             card_idx             |           0           |                         |                         |
+-------------------------+----------------------------------+-----------------------+-------------------------+-------------------------+
|          name           |               dna                |       power.cap       |        power.use        |                         |
+-------------------------+----------------------------------+-----------------------+-------------------------+-------------------------+
|        ELEM-CH21        | 000000004002000001718B6305602505 |           0           |            0            |                         |
+-------------------------+----------------------------------+-----------------------+-------------------------+-------------------------+
|          temp           |              cycle               |         index         |    utilization.rram     |                         |
+-------------------------+----------------------------------+-----------------------+-------------------------+-------------------------+
|           42℃           |                0                 |           0           |            0            |                         |
+-------------------------+----------------------------------+-----------------------+-------------------------+-------------------------+
|           ddr           |             card_idx             |           0           |                         |                         |
+-------------------------+----------------------------------+-----------------------+-------------------------+-------------------------+
|      memory.total       |        memory.used(Mbyte)        |   memory.h2c_buffer   |    memory.c2h_buffer    |                         |
+-------------------------+----------------------------------+-----------------------+-------------------------+-------------------------+
|           8GB           |                10                |          0%           |           0%            |                         |
+-------------------------+----------------------------------+-----------------------+-------------------------+-------------------------+
|         driver          |             card_idx             |           0           |                         |                         |
+-------------------------+----------------------------------+-----------------------+-------------------------+-------------------------+
|     driver_version      |        2.0.1.202507031525        |       pci_speed       | Speed 8.0GT/s, Width x4 |                         |
+-------------------------+----------------------------------+-----------------------+-------------------------+-------------------------+
| driver.h2c.speed (MB/s) |          driver.h2c.qps          | driver.h2c.hugepacket |    driver.h2c.packet    | driver.h2c.packing.rate |
+-------------------------+----------------------------------+-----------------------+-------------------------+-------------------------+
|            0            |                0                 |           0           |            0            |            0            |
+-------------------------+----------------------------------+-----------------------+-------------------------+-------------------------+
| driver.c2h.speed (MB/s) |          driver.c2h.qps          | driver.c2h.hugepacket |    driver.c2h.packet    | driver.c2h.packing.rate |
+-------------------------+----------------------------------+-----------------------+-------------------------+-------------------------+
|            0            |                0                 |           0           |            0            |            0            |
+-------------------------+----------------------------------+-----------------------+-------------------------+-------------------------+

部分信息

辅助参数:全部正常生效。

    ~ elem-smi -q -c overview
+--------------------+--------------------+--------------------+------------------+--------------+
|      overview      |                    |                    |                  |              |
+--------------------+--------------------+--------------------+------------------+--------------+
|     card_index     |     group_num      |      chip_num      |    bank_size     |    alive     |
+--------------------+--------------------+--------------------+------------------+--------------+
|         0          |         26         |         78         |        16        |      1       |
+--------------------+--------------------+--------------------+------------------+--------------+
|    soft_version    |   driver_version   |    smi_version     | firmware_version | fpga_version |
+--------------------+--------------------+--------------------+------------------+--------------+
| 2.0.1.202507031525 | 2.0.1.202507031525 | 2.0.6.202507141135 |     25070801     |   25071411   |
+--------------------+--------------------+--------------------+------------------+--------------+

    ~ elem-smi -q -c card
+-----------+----------------------------------+-----------+------------------+
|   card    |             card_idx             |     0     |                  |
+-----------+----------------------------------+-----------+------------------+
|   name    |               dna                | power.cap |    power.use     |
+-----------+----------------------------------+-----------+------------------+
| ELEM-CH21 | 000000004002000001718B6305602505 |     0     |        0         |
+-----------+----------------------------------+-----------+------------------+
|   temp    |              cycle               |   index   | utilization.rram |
+-----------+----------------------------------+-----------+------------------+
|    42℃    |                0                 |     0     |        0         |
+-----------+----------------------------------+-----------+------------------+

    ~ elem-smi -q -c ddr -i 0
+--------------+--------------------+-------------------+-------------------+
|     ddr      |      card_idx      |         0         |                   |
+--------------+--------------------+-------------------+-------------------+
| memory.total | memory.used(Mbyte) | memory.h2c_buffer | memory.c2h_buffer |
+--------------+--------------------+-------------------+-------------------+
|     8GB      |         12         |        0%         |        0%         |
+--------------+--------------------+-------------------+-------------------+

    ~ elem-smi -q -c driver
+-------------------------+--------------------+-----------------------+-------------------------+-------------------------+
|         driver          |      card_idx      |           0           |                         |                         |
+-------------------------+--------------------+-----------------------+-------------------------+-------------------------+
|     driver_version      | 2.0.1.202507031525 |       pci_speed       | Speed 8.0GT/s, Width x4 |                         |
+-------------------------+--------------------+-----------------------+-------------------------+-------------------------+
| driver.h2c.speed (MB/s) |   driver.h2c.qps   | driver.h2c.hugepacket |    driver.h2c.packet    | driver.h2c.packing.rate |
+-------------------------+--------------------+-----------------------+-------------------------+-------------------------+
|            0            |         0          |           0           |            0            |            0            |
+-------------------------+--------------------+-----------------------+-------------------------+-------------------------+
| driver.c2h.speed (MB/s) |   driver.c2h.qps   | driver.c2h.hugepacket |    driver.c2h.packet    | driver.c2h.packing.rate |
+-------------------------+--------------------+-----------------------+-------------------------+-------------------------+
|            0            |         0          |           0           |            0            |            0            |
+-------------------------+--------------------+-----------------------+-------------------------+-------------------------+

单个查看

辅助参数:全部正常生效。

单个查看强制要求使用-i参数，支持的参数可以参考-L

    ~ elem-smi -q -d card_index -i 0
0
    ~ elem-smi -q -d group_num -i 0
26
    ~ elem-smi -q -d chip_num -i 0
78
    ~ elem-smi -q -d bank_size -i 0
16
    ~ elem-smi -q -d alive -i 0
1
    ~ elem-smi -q -d soft_version -i 0
2.0.1.202507031525
    ~ elem-smi -q -d driver_version -i 0
2.0.1.202507031525
    ~ elem-smi -q -d smi_version -i 0
2.0.5.202507111025
    ~ elem-smi -q -d firmware_version -i 0
25070801
    ~ elem-smi -q -d fpga_version -i 0
25070401
    ~ elem-smi -q -d name -i 0
ELEM-CH21
    ~ elem-smi -q -d dna -i 0
0000000040020000017142632D408285
    ~ elem-smi -q -d power.cap -i 0         #当前硬件不支持
0
    ~ elem-smi -q -d power.use -i 0         #当前硬件在没有外接电源时读出来的是错误值
0
    ~ elem-smi -q -d temp -i 0
45℃
    ~ elem-smi -q -d cycle -i 0            #数字版本不支持
0
    ~ elem-smi -q -d index -i 0
0
    ~ elem-smi -q -d utilization.rram -i 0 #数字版本不支持
0
    ~ elem-smi -q -d memory.total -i 0
8GB
    ~ elem-smi -q -d memory.used -i 0
12Mbyte
    ~ elem-smi -q -d memory.h2c_buffer -i 0
0%
    ~ elem-smi -q -d memory.c2h_buffer -i 0
0%
    ~ elem-smi -q -d pci_speed -i 0
Speed 8.0GT/s, Width x4
    ~ elem-smi -q -d driver.h2c.speed -i 0
0
    ~ elem-smi -q -d driver.h2c.qps -i 0
0
    ~ elem-smi -q -d driver.h2c.hugepacket -i 0
0
    ~ elem-smi -q -d driver.h2c.packet -i 0
0
    ~ elem-smi -q -d driver.h2c.packing.rate -i 0
0
    ~ elem-smi -q -d driver.c2h.speed -i 0
0
    ~ elem-smi -q -d driver.c2h.qps -i 0
0
    ~ elem-smi -q -d driver.c2h.hugepacket -i 0
0
    ~ elem-smi -q -d driver.c2h.packet -i 0
0
    ~ elem-smi -q -d driver.c2h.packing.rate -i 0
0

除此之外-d还拥有几个-L中没有显示的调试信息

    ~ elem-smi -q -d timestamp -i 0
1990.344468s
    ~ elem-smi -q -d memory.group_buffer -i 0
group  0 group_recv_buffer      0%, group_send_buffer      0%
group  1 group_recv_buffer      0%, group_send_buffer      0%
group  2 group_recv_buffer      0%, group_send_buffer      0%
group  3 group_recv_buffer      0%, group_send_buffer      0%
group  4 group_recv_buffer      0%, group_send_buffer      0%
group  5 group_recv_buffer      0%, group_send_buffer      0%
group  6 group_recv_buffer      0%, group_send_buffer      0%
group  7 group_recv_buffer      0%, group_send_buffer      0%
group  8 group_recv_buffer      0%, group_send_buffer      0%
group  9 group_recv_buffer      0%, group_send_buffer      0%
group 10 group_recv_buffer      0%, group_send_buffer      0%
group 11 group_recv_buffer      0%, group_send_buffer      0%
group 12 group_recv_buffer      0%, group_send_buffer      0%
group 13 group_recv_buffer      0%, group_send_buffer      0%
group 14 group_recv_buffer      0%, group_send_buffer      0%
group 15 group_recv_buffer      0%, group_send_buffer      0%
group 16 group_recv_buffer      0%, group_send_buffer      0%
group 17 group_recv_buffer      0%, group_send_buffer      0%
group 18 group_recv_buffer      0%, group_send_buffer      0%
group 19 group_recv_buffer      0%, group_send_buffer      0%
group 20 group_recv_buffer      0%, group_send_buffer      0%
group 21 group_recv_buffer      0%, group_send_buffer      0%
group 22 group_recv_buffer      0%, group_send_buffer      0%
group 23 group_recv_buffer      0%, group_send_buffer      0%
group 24 group_recv_buffer      0%, group_send_buffer      0%
group 25 group_recv_buffer      0%, group_send_buffer      0%
    ~ elem-smi -q -d memory.uage -i 0
group  0 reading_efficiency 0.00%   exclusive_ratio 0.00% bandwidth_utilization 0.00%
group  1 reading_efficiency 0.00%   exclusive_ratio 0.00% bandwidth_utilization 0.00%
group  2 reading_efficiency 0.00%   exclusive_ratio 0.00% bandwidth_utilization 0.00%
group  3 reading_efficiency 0.00%   exclusive_ratio 0.00% bandwidth_utilization 0.00%
group  4 reading_efficiency 0.00%   exclusive_ratio 0.00% bandwidth_utilization 0.00%
group  5 reading_efficiency 0.00%   exclusive_ratio 0.00% bandwidth_utilization 0.00%
group  6 reading_efficiency 0.00%   exclusive_ratio 0.00% bandwidth_utilization 0.00%
group  7 reading_efficiency 0.00%   exclusive_ratio 0.00% bandwidth_utilization 0.00%
group  8 reading_efficiency 0.00%   exclusive_ratio 0.00% bandwidth_utilization 0.00%
group  9 reading_efficiency 0.00%   exclusive_ratio 0.00% bandwidth_utilization 0.00%
group 10 reading_efficiency 0.00%   exclusive_ratio 0.00% bandwidth_utilization 0.00%
group 11 reading_efficiency 0.00%   exclusive_ratio 0.00% bandwidth_utilization 0.00%
group 12 reading_efficiency 0.00%   exclusive_ratio 0.00% bandwidth_utilization 0.00%
group 13 reading_efficiency 0.00%   exclusive_ratio 0.00% bandwidth_utilization 0.00%
group 14 reading_efficiency 0.00%   exclusive_ratio 0.00% bandwidth_utilization 0.00%
group 15 reading_efficiency 0.00%   exclusive_ratio 0.00% bandwidth_utilization 0.00%
group 16 reading_efficiency 0.00%   exclusive_ratio 0.00% bandwidth_utilization 0.00%
group 17 reading_efficiency 0.00%   exclusive_ratio 0.00% bandwidth_utilization 0.00%
group 18 reading_efficiency 0.00%   exclusive_ratio 0.00% bandwidth_utilization 0.00%
group 19 reading_efficiency 0.00%   exclusive_ratio 0.00% bandwidth_utilization 0.00%
group 20 reading_efficiency 0.00%   exclusive_ratio 0.00% bandwidth_utilization 0.00%
group 21 reading_efficiency 0.00%   exclusive_ratio 0.00% bandwidth_utilization 0.00%
group 22 reading_efficiency 0.00%   exclusive_ratio 0.00% bandwidth_utilization 0.00%
group 23 reading_efficiency 0.00%   exclusive_ratio 0.00% bandwidth_utilization 0.00%
group 24 reading_efficiency 0.00%   exclusive_ratio 0.00% bandwidth_utilization 0.00%

各层收发包数查看

辅助参数:因为三元组中已经指定了card信息，因此-i参数无效，其他有效。

    ~ elem-smi -q -r "((0,0),(0,25),(0,2))"

第一个参数是card序号，范围是0-7，第二个group序号，范围是0-25，第三个序号是chip序号，范围是0-2。



DNA查看

辅助参数:全部正常生效。

    ~ elem-smi -q -u
+------------+------------+----------------------------------+
| card_index |    hdna    |               dna                |
+------------+------------+----------------------------------+
|     0      | 1665656026 | 000000004002000001718B6305602505 |
+------------+------------+----------------------------------+

卡灯闪烁

辅助参数:无输出，因此-f参数无效，且指令是单次的，因此-l参数也无效。必须要指定卡号，因此-i参数必须添加。

输入该指令后卡蓝灯会闪烁10s。

    ~ elem-smi -F -i 0

复位卡

辅助参数:无输出，因此-f参数无效，且指令是单次的，因此-l参数也无效。必须要指定卡号，因此-i参数必须添加。

    ~ elem-smi -R -i 0

清除驱动计数统计

辅助参数:无输出，因此-f参数无效，且指令是单次的，因此-l参数也无效。必须要指定卡号，因此-i参数必须添加。

    ~ elem-smi -C -i 0

录制功能

辅助参数:所有辅助参数无效。

录制相关参数如下:

      --record <record>                record <0>:bin <1>:json
      --record_skip                    record_skip to skip record payload
      --stop_record                    stop_record
      --record_file <record_file>      record_file <record_file_path>

详细解释:

--record 0 表示录制文件类型为bin，目前只支持bin不支持json。是必选参数。

--record_file file 选择回放文件的路径，必须要写为绝对路径。是必选参数。

--record_skip 加上此参数可以不将payload记录到文件中，只记录头部和时间戳，仅特殊场景下使用，是非必选参数，不适用时表示记录payload。

完整功能示例:

    ~ elem-smi --record 0 --record_file /tmp/default.bin --record_skip

停止回放为一个单独的参数，在需要停止或者更换录制文件路径时要先调用一下。

    ~ elem-smi --stop_record

回放功能

辅助参数:所有辅助参数无效。

回放相关参数如下:

      --play <play>                    play <0>:bin <1>:json
      --play_filler <play_filler>      play_filler <0xb0> <176> <0xb1> <177>...
      --play_file <play_file>          play_file <play_file_path>
      --play_mode <play_mode>          play_mode <0> normal <1> huge
      --play_loop <play_loop>          play_loop times

详细解释:

--play 0 表示回放文件类型为bin，目前只支持bin不支持json。是必选参数。

--play_file file 选择回放文件的路径，可以使用相对路径。是必选参数。

--play_filler 0xb0 表示只回放文件中opcode为0xb0类型的包，也可以写作10进制176。是非必选参数，不使用时表示全部回放。

--play_mode 0 表示回放是否使用组包模式。是非必选参数，不适用时表示使用不租包模式。

--play_loop 2 表示回放次数。是非必选参数，不使用时表示默认为1次。

完整功能示例:

    ~ elem-smi --play 0 --play_file /tmp/default.bin --play_filler 0xb0 --play_mode 1 --play_loop 2
卡号 速率(MB/s)         QPS        平均收包字节      平均发包字节       最大包长       最小包长        
0      29.36            9199       3347.11          8233.96          3540         32          

回放一旦开启会自动调用elem-smi --stop_record停止录制，并且在回放完成后打印数据统计。

录制的文件中包含卡号信息，如录制的8卡文件，不建议在只有1卡的机器上回放。

缓存统计

辅助参数:因为实际刷新时间和采样参数有关，因此-l参数无效，其他有效。

    ~ elem-smi --buff_stat 10000 --buff_interval 10
总采样时间过短（buff_stat * buff_interval < 1s），请增加采样次数或采样间隔！
    ~ elem-smi --buff_stat 10000 --buff_interval 100
+------------+-------+----------+----------+----------+------+----------+
| card_index |   0   | 实际用时  | 1.614 秒  |          |      |          |
+------------+-------+----------+----------+----------+------+----------+
|            |   0   |  0%-25%  | 25%-75%  | 75%-100% | 100% | 总采样数  |
+------------+-------+----------+----------+----------+------+----------+
|    h2c     | 10000 |    0     |    0     |    0     |  0   |  10000   |
+------------+-------+----------+----------+----------+------+----------+
|    c2h     | 10000 |    0     |    0     |    0     |  0   |  10000   |
+------------+-------+----------+----------+----------+------+----------+



