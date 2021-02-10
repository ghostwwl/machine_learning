
# JVM参数相关(jvm参数解析)




**参数类型 type 在代码里的定义：**


- bool 表示开关参数，只验证参数的存在性
- v 表示解析出来字符串参数，并且这个参数不可能在命令行中多次出现
- int 表示整形参数，并且这个参数不可能在命令行中多次出现
- list 表示参数可以多次出现，结果会汇总到列表中
- dict 表示参数可以可以多次出现，结果加入到 system property 中


**<font color="red">问题：</font>**  
1. 如果单值参数同一参数多次出现，如： `-Xms12G -Xms8G` 以哪个值为准  
2. -D 重复配置的问题 > `-Dfile.encode="UTF-8"` 和 `-Dfile.encode="GBK"`  
3. java 命令行从哪获取  


	> 比喻下面的结巴 setsid 或者 nohup 后面那一串 怎面拿到
	> 现在想到的是，能不能直接从机器java的进程拿 `/proc/pid/cmdline` 值
现在用的是, 如果同时出现后面的覆盖签名的

```bash
#定义启动 jvm 的参数信息。
JVM_OPTS="-server -XX:+PrintGCDetails -XX:+PrintGCDateStamps \ 
          -Xloggc:$GC_LOG \
          -XX:+HeapDumpOnOutOfMemoryError \
          -XX:ErrorFile=$ERROR_LOG \
          -XX:HeapDumpPath=/export/Logs/$APP_NAME/dump.hprof \
          -Xms6G -Xmx6G -Xmn2G -Xss256k \
          -XX:MaxDirectMemorySize=2G \
          -XX:+ExplicitGCInvokesConcurrent \
          -XX:SurvivorRatio=7 -XX:+UseParNewGC -XX:+UseConcMarkSweepGC \
          -XX:CMSMaxAbortablePrecleanTime=1500 -XX:+CMSParallelRemarkEnabled \
          -XX:+CMSScavengeBeforeRemark -XX:+UseCMSInitiatingOccupancyOnly \
          -XX:CMSInitiatingOccupancyFraction=68 -XX:GCTimeRatio=49" 


CLASSPATH="$BASEDIR/conf/:$BASEDIR/lib/*"

[[ -z $(get_pid) ]] || {
    echo "ERROR:  $APP_NAME already running" >&2
    exit 1
}

echo "Starting $APP_NAME ...."
[[ -x $JAVA ]] || {
    echo "ERROR: no executable java found at $JAVA" >&2
    exit 1
}
cd $BASEDIR
setsid "$JAVA" $JVM_OPTS  -classpath "$CLASSPATH"  -Dbasedir="$BASEDIR"  -Dapp.name="$APP_NAME"  -Dfile.encoding="UTF-8"  $MAIN_CLASS "$@" > /dev/null 2>&1 &

```




| 参数 | 类型 | 说明 |
| :--- | :--- | :--- |
| -client | bool | `client模式启动` |
| -server | bool | `Service模式启动` |
| -classpath | list | `加入classpath` |
| -cp | list | `加入classpath` |
| -D | dict | `加入到system property中` |
| -d32 | bool | `启动的操作系统位数` |
| -d64 | bool | `启动的操作系统位数` |
| -enableassertions | bool | `启动断言` |
| -ea | bool | `启动断言` |
| -disableassertions | bool | `禁止断言` |
| -da | bool | `禁止断言` |
| -enablesystemassertions | bool | `启动系统断言` |
| -esa | bool | `启动系统断言` |
| -disablesystemassertions | bool | `禁止系统断言` |
| -dsa | bool | `禁止系统断言` |
| -jar | bool | `启动jar` |
| -verbose | bool | `打印载入的class信息` |
| -verbose:class | bool | `打印载入的class信息` |
| -verbose:gc | bool | `打印GC的收集时的信息` |
| -verbose:jni | bool | `打印jni调用native的方法行为` |
| -version | bool | `打印java的版本信息后退出` |
| -showversion | bool | `打印java的版本信息，但不退出` |
| -Xint | bool | `设置jvm以解释模式执行，所有字节码解释执行` |
| -Xverify | v | `缺省情况下，验证器处于开启状态，必须针对所有生产服务器启用验证器` |
| -Xbatch | bool | `关闭后台代码编译` |
| -Xdebug | bool | `启动debug` |
| -Xbootclasspath: | list | `指定用冒号分割的文件目录、jar或者zip文件，加入到boot class, 用来代替java2 SDK中的boot class 文件` |
| -Xbootclasspath/a: | list | `和Xbootclasspath 参数用途一样，只是该选项是追加path到bootstrap class path中，而非替换` |
| -Xbootclasspath/p: | list | `和Xbootclasspath/a 参数用途一样，只是追加的目录将优先于默认的bootstrap class path` |
| -Xcheck:jni | bool | `在执行native方法前进行检查。JVM会校验传递给jni方法的参数在执行jni请求前。在native中一个非法的数据将会导致JVM终止。如果开启该参数，将会降低性能` |
| -Xfuture | bool | `对class文件进行严格检查。目的为了向后兼容。推荐开发人员使用该参数` |
| -Xnoclassgc | bool | `关闭class 的gc功能` |
| -Xincgc | bool | `开启增量gc的功能，默认是关闭的。有助于减少gc的停顿时间，但可能会导致大概10%的性能损耗` |
| -Xloggc: | v | `和verbose:gc参数类似，只是将gc信息打印在文件而不是控制台。和verbose:gc不同的是输出的信息中带有时间` |
| -Xms | v | `指定初始堆的大小，默认单位为k。可以指定为m,g` |
| -Xmx | v | `指定堆的最大的大小` |
| -Xmn | v | `设置年轻代大小为` |
| -Xss | v | `设置每个线程的堆栈大小。JDK5.0以后每个线程堆栈大小为1M，以前每个线程堆栈大小为256K` |
| -Xprof | bool | `跟踪正在运行的程序，并输出跟踪信息到控制台。该参数主要用在开发环境，而不是生产环境` |
| -Xrunhprof | bool | `开启cpu、heap或者监视器的性能分析。具体介绍，可以参考  java -Xrunhprof:help` |
| -XX:ErrorFile | v | `保存错误日志或者数据到文件中` |
| -XX:+UseSerialGC | bool | `串行收集器, 收集时会暂停所有工作线程，使用复制收集算法，在虚拟机运行在Client模式默认的新生代收集器` |
| -XX:+UseParNewGC | bool | `是Serial的多线程版本，虚拟机运行在Server模式的默认新生代收集器` |
| -XX:-UseParNewGC | bool | `关闭年轻代的并行GC` |
| -XX:G1HeapRegionSize | v | `设置the size of a G1 region的大小` |
| -XX:G1NewSizePercent | int | `设置年轻代最小值所占总堆的百分比。默认值是堆的 5%` |
| -XX:G1MaxNewSizePercent | int | `设置年轻代最大值所占总堆的百分比。默认值是堆的 60%` |
| -XX:G1MixedGCLiveThresholdPercent | int | `old generation region中的存活对象的占比` |
| -XX:G1HeapWastePercent | int | `设置浪费堆百分比, 可回收百分比小于堆废物百分比，Java HotSpot VM 不会启动混合垃圾周期。默认值是 10%` |
| -XX:G1MixedGCCountTarget | int | `一次global concurrent marking之后，最多执行Mixed GC的次数` |
| -XX:G1OldCSetRegionThresholdPercent | int | `一次Mixed GC中能被选入CSet的最多old generation region数量。默认值是堆的 10%` |
| -XX:G1ReservePercent | int | `设置作为空闲空间的预留内存百分比，以降低目标空间溢出的风险。默认值是 10% 增加或减少时，请确保对总的堆调整相同的量` |
| -XX:+UseConcMarkSweepGC | bool | `并发收集器, 对响应时间要求比较高的中、大规模应用` |
| -XX:+UseG1GC | bool | `开启G1` |
| -XX:+UseZGC | bool | `java11及以上的ZGC, 支持TB级别的堆，停顿时间不会随着堆的增大而增长` |
| -XX:+CMSConcurrentMTEnabled | bool | `并发的CMS阶段以多线程执行 默认开启` |
| -XX:+UseParallelGC | bool | ` 使用多线程并行执行年轻代垃圾收集，也是使用复制算法，以吞吐量最大化（GC时间占总运行时间最小）为目标，是新生代收集器` |
| -XX:+UseParallelOldGC | bool | `除了激活年轻代并行垃圾收集，也激活了年老代并行垃圾收集, 年老代吞吐量优化收集器，使用多线程和标记-整理` |
| -XX:ParallelGCThreads | int | `设置并行垃圾回收的线程数` |
| -XX:MaxGCPauseMillis | int | `控制最大垃圾收集停顿时间。大于0的毫秒, 停顿时间是牺牲吞吐量和新生代空间换取的。新生代调小，吞吐量跟着小，垃圾收集时间就短，停顿就小` |
| -XX:GCTimeRatio | int | `设置吞吐量大小，0<x<100 的整数，允许的最大GC时间=1/（1+x）` |
| -XX:LargePageSizeInBytes | v | `内存页的大小不可设置过大， 会影响Perm的大小` |
| -XX:+UseLargePages | bool | `启用大内存分页, JDK 5 update 5后引入，但需要手动启用, JDK6默认启用` |
| -XX:-UseLargePages | bool | `关闭大内存分页` |
| -XX:TargetSurvivorRatio | int | `设定幸存区的目标使用率` |
| -XX:NewSize | v | `新生代初始化内存的大小(注意：该值需要小于-Xms的值)` |
| -XX:MaxNewSize | v | `新生代可被分配的内存的最大上限(注意：该值需要小于-Xmx的值)` |
| -XX:SurvivorRatio | int | `新生代中Eden区域和Survivor区域（From幸存区或To幸存区）的比例，默认为8` |
| -XX:NewRatio | int | `新生代（eden+2*s）和老年代（不包含永久区）的比值` |
| -XX:PermSize | v | `非堆区初始内存分配大小, JDK8+移除了Perm` |
| -XX:MaxPermSize | v | `非堆区分配的内存的最大上限, JDK8+移除了Perm` |
| -XX:InitialTenuringThreshold | int | `老年代阀值初始值` |
| -XX:InitiatingHeapOccupancyPercent | int | `整堆使用达到这个比例后，触发并发 GC 周期，默认 45%` |
| -XX:MaxTenuringThreshold | int | `老年代阀值最大值` |
| -XX:+UseAdaptiveSizePolicy | bool | `开启GC自适应调节策略` |
| -XX:-UseAdaptiveSizePolicy | bool | `关闭GC自适应调节策略` |
| -XX:+HeapDumpOnOutOfMemoryError | bool | `OutOfMemoryError时拍摄一个“堆转储快照”，并将其保存在-XX:HeapDumpPath中` |
| -XX:+UseCMSCompactAtFullCollection | bool | `每次触发CMS Full GC的时候都整理一次碎片` |
| -XX:CMSFullGCsBeforeCompaction | int | `设置多少次Full GC后,对年老代进行压缩, -XX:+UseCMSCompactAtFullCollection开启的情况下` |
| -XX:+CMSParallelRemarkEnabled | bool | `并行运行最终标记阶段` |
| -XX:+CMSScavengeBeforeRemark | bool | `在CMS GC前启动一次ygc` |
| -XX:+UseCMSInitiatingOccupancyOnly | bool | `当old代占用确实达到了-XX:CMSInitiatingOccupancyFraction参数所设定的比例时才会触发cms gc` |
| -XX:+CMSParallelInitialMarkEnabled | bool | `初始标记阶段开启多线程并发执行` |
| -XX:CMSMaxAbortablePrecleanTime | int | `指定CMS-concurrent-abortable-preclean阶段执行的时间，该阶段主要是执行一些预清理，减少应用暂停的时间` |
| -XX:CMSInitiatingOccupancyFraction | int | `设定CMS在对内存占用率达到百分之多少的时候开始GC(因为CMS会有浮动垃圾,所以一般都较早启动GC)` |
| -XX:+CMSClassUnloadingEnabled | bool | `让CMS可以收集永久带，默认不会收集` |
| -XX:+CMSIncrementalMode | bool | `开启CMS收集器的增量模式, 增量模式会经常暂停CMS过程，以便对应用程序作出完全的让步` |
| -XX:ParallelCMSThreads | int | `设置CMS线程的数量` |
| -XX:ConcGCThreads | int | `设置G1线程的数量` |
| -XX:MaxDirectMemorySize | v | `Direct ByteBuffer分配的堆外内存到达指定大小后，即触发Full GC` |
| -XX:+ExplicitGCInvokesConcurrent | bool | `当调用System.gc()的时候，执行并行gc，只有在CMS或者G1下该参数才有效` |
| -XX:+ExplicitGCInvokesConcurrentAndUnloadsClasses | bool | `保证当有系统GC调用时，永久代也被包括进CMS垃圾回收的范围内。这标志，我们可以防止出现意料之外的”stop-the-world”的系统GC` |
| -XX:OnOutOfMemoryError | v | `OOM时执行一个脚本` |
| -XX:HeapDumpPath | v | `导出OOM的路径` |
| -XX:MetaspaceSize | v | `设置元空间大小，Metaspace扩容时触发FullGC的初始化阈值，也是最小的阈值, 默认21807104（约20.8m）` |
| -XX:MaxMetaspaceSize | v | `用于限制Metaspace增长的上限，防止因为某些情况导致Metaspace无限的使用本地内存，影响到其他程序, 默认是几乎无穷大，MaxMetaspaceSize设置太小，可能会导致频繁FullGC，甚至OOM` |
| -XX:+DisableExplicitGC | bool | `关闭System.gc()` |
| -XX:+TraceClassLoading | bool | `监控类的加载` |
| -XX:+PrintClassHistogram | bool | `按下Ctrl+Break后，打印类的信息` |
| -XX:+PrintGC | bool | `` |
| -XX:+PrintGCDetails | bool | `` |
| -XX:+PrintGCTimeStamps | bool | `` |
| -XX:+PrintGCDateStamps | bool | `` |
| -XX:+PrintGCApplicationStoppedTime | bool | `` |
| -XX:+PrintGCApplicationConcurrentTime | bool | `` |
| -XX:+PrintReferenceGC | bool | `打印各种引用的处理时间` |
| -XX:+PrintHeapAtGC | bool | `每次GC前后，打印GC堆的概况` |
| -XX:+PrintTenuringDistribution | bool | `用于显示每次Minor GC时Survivor区中各个年龄段的对象的大小` |
| -XX:+UnlockExperimentalJVMOptions | bool | `解锁jvm参数防止“Unrecognized VM option”终止` |
| -XX:+UseBiasedLocking | bool | `开启偏向锁` |
| -XX:BiasedLockingStartupDelay | int | `关闭激活延时` |
| -XX:-UseBiasedLocking | bool | `关闭偏向锁` |
| -XX:+UseSpinning | bool | `开启自旋锁` |
| -XX:PreBlockSpin | int | `自旋次数` |
| -XX:SoftRefLRUPolicyMSPerMB | int | `每兆堆空闲空间的 soft reference 保持存活的毫秒数` |
| -XX:+DoEscapeAnalysis | bool | `开启逃逸分析` |
| -XX:DoEscapeAnalysis | bool | `关闭逃逸分析` |
| -XX:-OmitStackTraceInFastThrow | bool | `关闭JVM优化抛出堆栈异常` |
| -XX:+NeverTenure | bool | `对象永远不会晋升到老年代.当我们确定不需要老年代时，可以这样设置` |
| -XX:+AlwaysTenure | bool | `表示没有幸存区,所有对象在第一次GC时，会晋升到老年代` |
