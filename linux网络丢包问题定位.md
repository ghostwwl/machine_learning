### linux丢包问题查找及定位

#### 1. 操作系统处理不过来，发生丢包
- 传统　NAPI　接口实现的网卡驱动
    - `cat /proc/net/dev | awk '{print $1, $4, $5}'`
    - 每个网络接口一行统计数据，第 4 列（errs）是接收出错的数据包数量，第 5 列（drop）是接收不过来丢弃的数量。


- 非 NAPI 接口实现的网卡驱动，每个 CPU 有一个队列，当在队列中缓存的数据包数量超过 net.core.netdev_max_backlog 时，网卡驱动程序会丢掉数据包
    - `cat /proc/net/softnet_stat`
    - 每个 CPU 有一行统计数据，第二列是对应 CPU 丢弃的数据包数量。


#### 2. 应用处理不过来发生丢包(这种情况是我们需要处理的，基本是要在负载之后扩容)
- linux 内核中记录了两个计数器
    - ListenOverflows：当 socket 的 listen queue 已满，当新增一个连接请求时，应用程序来不及处理
    - ListenDrops：包含上面的情况，除此之外，当内存不够无法为新的连接分配 socket 相关的数据结构时，会加 1，有异常情况下会增加 1
    - 分别对应`/proc/net/netstat` 中的第 21 列（ListenOverflows）和第 22 列（ListenDrops）

- 查看方法 `cat /proc/net/netstat | awk '/TcpExt/ { print $21,$22 }'`
    - 如果使用 netstat 命令，有丢包时会看到 “times the listen queue of a socket overflowed” 以及 “SYNs to LISTEN sockets ignored” 对应行前面的数字, 如果值为 0 则不会输出对应的行
