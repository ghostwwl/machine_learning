
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
3. 多jvm各版本累积下来600-700个参数
4. 坑多: a. 有的参数具有互斥性，设置了A参数那么B参数将失效 b. 有的参数有顺序依赖，某个参数必须在另外一个参数之前设置，顺序变了导致无效问题
5. java 命令行从哪获取  


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
| -XX:InitialHeapSize | v | `指定初始堆的大小，默认单位为k。可以指定为m,g` |
| -XX:MaxHeapSize | v | `指定堆的最大的大小` |
| -XX:+UseSerialGC | bool | `串行收集器, 收集时会暂停所有工作线程，使用复制收集算法，在虚拟机运行在Client模式默认的新生代收集器` |
| -XX:+UseSerialOldGC | bool | `指定老年代为Serial收集器` |
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
| -XX:G1RSetUpdatingPauseTimePercent | int | `设置GC evacuation（疏散）阶段期间G1 GC更新RSets消耗时间的百分比（默认是目标停顿时间的10%）` |
| -XX:GCPauseIntervalMillis | int | `设置暂停间隔目标` |
| -XX:+UseConcMarkSweepGC | bool | `并发收集器, 对响应时间要求比较高的中、大规模应用, 老年代使用CMS收集器, 年轻代将会使用ParNew收集器` |
| -XX:+UseG1GC | bool | `开启G1` |
| -XX:+UseZGC | bool | `java11及以上的ZGC, 支持TB级别的堆，停顿时间(据说小于10ms)不会随着堆的增大而增长` |
| -XX:+CMSConcurrentMTEnabled | bool | `并发的CMS阶段以多线程执行 默认开启` |
| -XX:+UseParallelGC | bool | `使用多线程并行执行年轻代垃圾收集，也是使用复制算法，以吞吐量最大化（GC时间占总运行时间最小）为目标，是新生代收集器, Linux下1.6,1.7,1.8默认开启，老年代将会使用SerialOld垃圾收集器` |
| -XX:+UseParallelOldGC | bool | `除了激活年轻代并行垃圾收集，也激活了年老代并行垃圾收集, 年老代吞吐量优化收集器，使用多线程和标记-整理` |
| -XX:ParallelGCThreads | int | `设置并行垃圾回收的线程数` |
| -XX:MaxGCPauseMillis | int | `控制最大垃圾收集停顿时间。大于0的毫秒, 停顿时间是牺牲吞吐量和新生代空间换取的。新生代调小，吞吐量跟着小，垃圾收集时间就短，停顿就小` |
| -XX:GCTimeRatio | int | `设置吞吐量大小，0<x<100 的整数，允许的最大GC时间=1/（1+x）` |
| -XX:LargePageSizeInBytes | v | `内存页的大小不可设置过大， 会影响Perm的大小` |
| -XX:+UseLargePages | bool | `启用大内存分页, JDK 5 update 5后引入，但需要手动启用, JDK6默认启用` |
| -XX:-UseLargePages | bool | `关闭大内存分页` |
| -XX:+AggressiveHeap | bool | `选项会检测主机的资源（内存大小、处理器数量），然后调整相关的参 数，使得长时间运行的、内存申请密集的任务能够以最佳状态运行` |
| -XX:TargetSurvivorRatio | int | `设定幸存区的目标使用率` |
| -XX:NewSize | v | `新生代初始化内存的大小(注意：该值需要小于-Xms的值)` |
| -XX:MaxNewSize | v | `新生代可被分配的内存的最大上限(注意：该值需要小于-Xmx的值)` |
| -XX:SurvivorRatio | int | `新生代中Eden区域和Survivor区域（From幸存区或To幸存区）的比例，默认为8` |
| -XX:NewRatio | int | `新生代（eden+2*s）和老年代（不包含永久区）的比值` |
| -XX:PermSize | v | `非堆区初始内存分配大小, JDK8+移除了Perm` |
| -XX:MaxPermSize | v | `非堆区分配的内存的最大上限, JDK8+移除了Perm` |
| -XX:InitialTenuringThreshold | int | `老年代阀值初始值, 每个对象在坚持过一次Minor GC之后，年龄就增加1，当超过这个参数值时就进入老年代，最大支持15` |
| -XX:InitiatingHeapOccupancyPercent | int | `整堆使用达到这个比例后，触发并发 GC 周期，默认 45%` |
| -XX:PretenureSizeThreshold | v | `可以在新生代直接分配的对象最大值，0表示没有最大值, 当创建的对象超过指定大小时，直接把对象分配在老年代` |
| -XX:MaxTenuringThreshold | int | `老年代阀值最大值` |
| -XX:MaxHeapFreeRatio | int | `置堆空间最大空闲比例，默认值是 70` |
| -XX:+UseAdaptiveSizePolicy | bool | `开启GC自适应调节策略, 1.7以后默认会开启该参数，如果使用CMS回收算法，则会关闭该参数，该参数开启以后会使SurvivorRatio参数失效，如果显示指定了SurvivorRatio，需要关闭该参数` |
| -XX:-UseAdaptiveSizePolicy | bool | `关闭GC自适应调节策略` |
| -XX:+UseCMSCompactAtFullCollection | bool | `每次触发CMS Full GC的时候都对内存进行压缩，默认关闭` |
| -XX:CMSFullGCsBeforeCompaction | int | `设置多少次Full GC后,对年老代进行压缩, -XX:+UseCMSCompactAtFullCollection开启的情况下` |
| -XX:+CMSParallelRemarkEnabled | bool | `并行运行最终标记阶段` |
| -XX:-CMSParallelRemarkEnabled | bool | `不启用并行运行最终标记阶段` |
| -XX:+CMSScavengeBeforeRemark | bool | `在CMS GC前启动一次ygc` |
| -XX:+ScavengeBeforeFullGC | bool | `在Full GC前触发一次Minor GC 默认启用` |
| -XX:+UseCMSInitiatingOccupancyOnly | bool | `当old代占用确实达到了-XX:CMSInitiatingOccupancyFraction参数所设定的比例时才会触发cms gc, 默认关闭` |
| -XX:+CMSParallelInitialMarkEnabled | bool | `初始标记阶段开启多线程并发执行` |
| -XX:CMSMaxAbortablePrecleanTime | int | `指定CMS-concurrent-abortable-preclean阶段执行的时间，该阶段主要是执行一些预清理，减少应用暂停的时间` |
| -XX:CMSInitiatingOccupancyFraction | int | `设定CMS在对内存占用率达到百分之多少的时候开始GC(因为CMS会有浮动垃圾,所以一般都较早启动GC)` |
| -XX:CMSInitiatingPermOccupancyFraction | int | `设定永久代使用比率达到多少时，会回收永久代` |
| -XX:+CMSClassUnloadingEnabled | bool | `让CMS可以收集永久带，默认不会收集` |
| -XX:+CMSIncrementalMode | bool | `开启CMS收集器的增量模式, 增量模式会经常暂停CMS过程，以便对应用程序作出完全的让步` |
| -XX:ParallelCMSThreads | int | `设置CMS线程的数量` |
| -XX:ConcGCThreads | int | `设置G1线程的数量` |
| -XX:MaxDirectMemorySize | v | `最大直接内存（堆外）大小, Direct ByteBuffer分配的堆外内存到达指定大小后，即触发Full GC` |
| -XX:+ExplicitGCInvokesConcurrent | bool | `当调用System.gc()的时候，执行并行gc，只有在CMS或者G1下该参数才有效` |
| -XX:+ExplicitGCInvokesConcurrentAndUnloadsClasses | bool | `保证当有系统GC调用时，永久代也被包括进CMS垃圾回收的范围内。这标志，我们可以防止出现意料之外的”stop-the-world”的系统GC` |
| -XX:+HeapDumpBeforeFullGC | bool | `在Full GC前分别对内存做一个dump, 并将其保存在-XX:HeapDumpPath中` |
| -XX:+HeapDumpAfterFullGC | bool | `在Full GC前分别对内存做一个dump,并将其保存在-XX:HeapDumpPath中` |
| -XX:+HeapDumpOnOutOfMemoryError | bool | `OutOfMemoryError时拍摄一个“堆转储快照”，并将其保存在-XX:HeapDumpPath中` |
| -XX:OnOutOfMemoryError | v | `OOM时执行一个脚本` |
| -XX:HeapDumpPath | v | `导出OOM的路径` |
| -XX:MetaspaceSize | v | `JDK1.8以后用于替换PermSize, 设置元空间大小，Metaspace扩容时触发FullGC的初始化阈值，也是最小的阈值, 默认21807104（约20.8m）` |
| -XX:MaxMetaspaceSize | v | `JDK1.8以后用于替换MaxPermSize, 用于限制Metaspace增长的上限，防止因为某些情况导致Metaspace无限的使用本地内存，影响到其他程序, 默认是几乎无穷大，MaxMetaspaceSize设置太小，可能会导致频繁FullGC，甚至OOM` |
| -XX:+DisableExplicitGC | bool | `关闭System.gc()，禁用System.gc()触发FullGC，不建议开启，如果开启了这个参数可能会导致堆外内存无法及时回收造成内存溢出` |
| -XX:+DisableAttachMechanism | bool | `基于Attach API 的命令将无法执行，jmap/jinfo/jstack/jcmd等` |
| -XX:+PerfDisableSharedMem | bool | `关闭存储PerfData的内存共享，jvm在启动的时候都会分配一块内存来存PerfData，此参数决定这个PerfData对其他进程可见的问题，启用时其他进程将访问不了该内存，如jps，jstat等都无法工作。默认这个参数是关闭的，也就是默认支持共享的方式` |
| -XX:-UsePerfData | bool | `关闭了UsePerfData这个参数，那么jvm启动过程中perf memory不会被创建，jvm运行过程中自然不会再将这些性能数据保存起来，默认情况是是打开的` |
| -XX:+TraceClassLoading | bool | `监控类的加载` |
| -XX:+TraceClassUnloading | bool | `监控类的卸载` |
| -XX:+PrintClassHistogram | bool | `按下Ctrl+Break后，打印类的信息` |
| -XX:+PrintGC | bool | `开启GC日志打印` |
| -XX:+PrintGCDetails | bool | `打印GC回收的详细信息，会把Eden区，S区和Old区的收集前、收集后，总大小分别打印出来` |
| -XX:+PrintAdaptiveSizePolicy | bool | `在GC日志中输出大小调整的详细信息` |
| -XX:+PrintGCTimeStamps | bool | `打印GC停顿耗时` |
| -XX:+PrintGCDateStamps | bool | `只打印是何种类型的GC，和Heap的总大小` |
| -XX:+PrintGCApplicationStoppedTime | bool | `打印应用暂停时间，默认关闭` |
| -XX:+PrintGCApplicationConcurrentTime | bool | `打印每次垃圾回收前，应用未中断的执行时间` |
| -XX:+PrintReferenceGC | bool | `打印各种引用的处理时间` |
| -XX:+PrintHeapAtGC | bool | `每次GC前后，打印GC堆的概况, 默认关闭` |
| -XX:+PrintTenuringDistribution | bool | `用于显示每次Minor GC时Survivor区中各个年龄段的对象的大小, 打印存活实例年龄信息，默认关闭` |
| -XX:+UnlockExperimentalJVMOptions | bool | `解锁jvm参数防止“Unrecognized VM option”终止` |
| -XX:+UseBiasedLocking | bool | `开启偏向锁` |
| -XX:BiasedLockingStartupDelay | int | `关闭激活延时, 偏向锁在Java 6和Java 7里是默认启用的, 但是它在应用程序启动几秒钟之后才激活，一般jVM默认会在程序启动后4秒钟之后才激活偏向锁  -XX:BiasedLockingStartupDelay=0 程序启动0毫秒后激活` |
| -XX:-UseBiasedLocking | bool | `关闭偏向锁` |
| -XX:+UseSpinning | bool | `开启自旋锁, Java1.6默认开启` |
| -XX:PreBlockSpin | int | `自旋次数, 默认值10次, 必须先开启`-XX:+UseSpinning`, JDK1.7后，去掉此参数，由jvm控制` |
| -XX:SoftRefLRUPolicyMSPerMB | int | `每兆堆空闲空间的 soft reference 保持存活的毫秒数` |
| -XX:+DoEscapeAnalysis | bool | `开启逃逸分析(大型应用可能出现开启逃逸分析性能有所下降，1.6.23默认开启)` |
| -XX:DoEscapeAnalysis | bool | `关闭逃逸分析` |
| -XX:+PrintEscapeAnalysis | bool | `开启逃逸分析性能的输出` |
| -XX:+EliminateAllocations | bool | `开启标量替换` |
| -XX:+PrintEliminateAllocations | bool | `输出标量替换的情况` |
| -XX:+OmitStackTraceInFastThrow | bool | `开启JVM优化抛出堆栈异常` |
| -XX:-OmitStackTraceInFastThrow | bool | `关闭JVM优化抛出堆栈异常` |
| -XX:+NeverTenure | bool | `对象永远不会晋升到老年代.当我们确定不需要老年代时，可以这样设置` |
| -XX:+AlwaysTenure | bool | `表示没有幸存区,所有对象在第一次GC时，会晋升到老年代` |
| -XX:+AlwaysPreTouch | bool | `在服务启动的时候真实的分配物理内存给JVM, -Xmx和-Xms只是设置了大小单并为真实分配` |
| -XX:-AlwaysPreTouch | bool | `在服务启动的时候真实的分配物理内存给JVM, -Xmx和-Xms只是设置了大小单并为真实分配` |
| -XX:CompressedClassSpaceSize | v | `只有当-XX:+UseCompressedClassPointers开启了才有效` |
| -XX:+TieredCompilation | bool | `启用分层编译，结合了C1(Client)的启动性能优势和C2(Server)模式的峰值性能优势, java 1.8默认开启分层编译，该参数无效` |
| -XX:-TieredCompilation | bool | `关闭分层编译，结合了C1(Client)的启动性能优势和C2(Server)模式的峰值性能优势` |
| -XX:AutoBoxCacheMax | int | `自动装箱和拆箱范围设置(节省了常用数值的内存开销和创建对象的开销，提高了效率)` |
| -XX:＋UseCodeCacheFlushing | int | `当JVM code cache填满时会丢掉一些编译了的代码从而避免进入interpreted-only 模式` |
| -XX:CICompilerCount | int | `最大并行编译数` |
| -XX:-CICompilerCountPerCPU | bool | `关闭编译线程数依赖于处理器核数自动配置` |
| -XX:+CICompilerCountPerCPU | bool | `编译线程数依赖于处理器核数自动配置` |
| -XX:+FlightRecorder | bool | `默认情况下，JFR 在 JVM 中是禁用的, 启用JFR, 打开飞行记录器` |
| -XX:+CMSPermGenSweepingEnabled | bool | `是否会清理持久代。默认是不清理的，可以设置这个参数来调试持久代内存溢出问题` |
| -XX:GCLogFileSize | v | `GC文件滚动大小，需配置UseGCLogFileRotation，设置为0表示仅通过jcmd命令触发` |
| -XX:+UseGCLogFileRotation | bool | `滚动GC日志文件，须配置Xloggc` |
| -XX:NumberOfGCLogFiles | int | `滚动GC日志文件数，默认0，不滚动` |
| -XX:MinHeapFreeRatio | int | `GC后，如果发现空闲堆内存占到整个预估上限值的40%，则增大上限值` |
| -XX:PrintFLSStatistics | int | `打印每次GC前后内存碎片的统计信息` |
| -XX:NativeMemoryTracking | v | `开启NMT(Native memory tracking options)本机内存追踪，其中该值默认为off，可以设置为summary或者detail来开启；开启的话，大概会增加5%-10%的性能消耗` |
| -XX:+PrintNMTStatistics | bool | `在jvm shutdown的时候输出整体的native memory统计，默认关闭, 必须配合参数-XX:+UnlockDiagnosticVMOptions使用，并且只能加在其后才能生效` |
| -XX:+ParallelRefProcEnabled | bool | `采用多线程的方式发现需要处理的finalize方法的对象，非多线程执行对象的finalize方法` |
| -XX:ParGCCardsPerStrideChunk | int | `GC工作线程的任务粒度，可以帮助不使用补丁而获得最佳性能，这个补丁用来优化新生代垃圾回收的卡表扫描时间` |
| -XX:+PrintCodeCache | bool | `在JVM停止的时候打印codeCache使用情况` |
| -XX:+PrintGCCause | bool | `打印gc cause` |
| -XX:+PrintParallelOldGCPhaseTimes | bool | `` |
| -XX:+PrintVMOptions | bool | `程序运行时，打印虚拟机接受到的命令行显式参数` |
| -XX:+PrintCommandLineFlags | bool | `打印传递给虚拟机的显式和隐式参数, 会显示一些没有设置参数的默认值参数` |
| -XX:+PrintFlagsFinal | bool | `打印所有的系统参数的值, 貌似有700-800个呢` |
| -XX:+PrintPromotionFailure | bool | `` |
| -XX:+PrintSafepointStatistics | bool | `` |
| -XX:+TraceSafepointCleanupTime | bool | `` |
| -XX:-TraceSafepointCleanupTime | bool | `` |
| -XX:+UnlockCommercialFeatures | bool | `开启商业选项，许多商业特性都需要这个选项的支持` |
| -XX:PrintSafepointStatisticsCount | int | `` |
| -XX:+PrintCodeCacheOnCompilation | bool | `用于在方法每次被编译时输出code cache的使用情况, 默认关闭` |
| -XX:ReservedCodeCacheSize | v | `保留代码高速缓存大小，通常默认是240M` |
| -XX:InitialCodeCacheSize | v | `设置初始CodeCache大小，一般默认是48M` |
| -XX:+UnlockDiagnosticVMOptions | bool | `解锁诊断参数, 默认关闭` |
| -XX:+UnlockExperimentalVMOptions | bool | `解锁实验函数` |
| -XX:+UseCompressedOops | bool | `普通对象指针压缩, 压缩指针，起到节约内存占用` |
| -XX:+UseCompressedClassPointers | bool | `类指针压缩` |
| -XX:+UseFastAccessorMethods | bool | `原始类型的快速优化` |
| -XX:+UseStringDeduplication | bool | `消除了较长时间内存在的重复字符串。它们不会消除短期字符串对象中的重复字符串, 仅在您使用G1 GC算法时有效` |
| -XX:-UseGCOverheadLimit | bool | `JDK1.6.0_37和JDK_1.7.0_60默认开启, JVM的一种推断，如果垃圾回收耗费了98%的时间，但是回收的内存还不到2%，那么JVM会认为即将发生OOM，让程序提前结束, 此参数关闭该特性` |
| -XX:+ClassUnloading | bool | `对持久代卸载的类进行回收` |



- 在容器里获取容器的内存限制
> -XX:MaxRAM=$(cat /sys/fs/cgroup/memory/memory.limit_in_bytes)

- https://heapdump.cn/article/180768


### 关于 Xmx 说明

- 因为资源是有限:
    - 到达限制 直接影响是 gc
    - 容器有限内存 `cat /sys/fs/cgroup/memory/memory.limit_in_bytes` 


- `-Xmx` 就是 `MaxHeapSize`
- `-XX:MaxHeapSize`
- `-XX:MaxRAMFraction` (在191版本后，-XX:{Min|Max}RAMFraction 被弃用)
    - 如果机器配置的物理内存非常少, JVM还要确保预留足够的内存给操作系统, `-XX:MinRAMFraction`，默认值为2 即50%
    - 取值范围: 1 - 4  默认值是 4 
```text

    +----------------+-------------------+
    | MaxRAMFraction | % of RAM for heap |
    |----------------+-------------------|
    |              1 |  int(100/1) = 100%|
    |              2 |  int(100/2) = 50% |
    |              3 |  int(100/3) = 33% |
    |              4 |  int(100/4) = 25% |
    +----------------+-------------------+

```  
- `-XX:MaxRAMPercentage` (其值介于 ) 
    - 一般配合 `-XX:+UseContainerSupport`(该特性在Java 8u191+引入, java10默认开启) 使用
    - 取值范围: 0.0 到 100.0 之间，默认值为 25.0

- `-XX:ErgoHeapSizeLimit`

- `-XX:MaxRAM`  (用来限制整个 java 应用能用内存总数)
    - 默认值: 128GB 



```c
void Arguments::set_heap_size() {
  julong phys_mem;

  // If the user specified one of these options, they
  // want specific memory sizing so do not limit memory
  // based on compressed oops addressability.
  // Also, memory limits will be calculated based on
  // available os physical memory, not our MaxRAM limit,
  // unless MaxRAM is also specified.
  bool override_coop_limit = (!FLAG_IS_DEFAULT(MaxRAMPercentage) ||
                           !FLAG_IS_DEFAULT(MaxRAMFraction) ||
                           !FLAG_IS_DEFAULT(MinRAMPercentage) ||
                           !FLAG_IS_DEFAULT(MinRAMFraction) ||
                           !FLAG_IS_DEFAULT(InitialRAMPercentage) ||
                           !FLAG_IS_DEFAULT(InitialRAMFraction) ||
                           !FLAG_IS_DEFAULT(MaxRAM));
  if (override_coop_limit) {
    if (FLAG_IS_DEFAULT(MaxRAM)) {
      phys_mem = os::physical_memory();
      FLAG_SET_ERGO(MaxRAM, (uint64_t)phys_mem);
    } else {
      phys_mem = (julong)MaxRAM;
    }
  } else {
    phys_mem = FLAG_IS_DEFAULT(MaxRAM) ? MIN2(os::physical_memory(), (julong)MaxRAM)
                                       : (julong)MaxRAM;
  }


  // Convert deprecated flags
  if (FLAG_IS_DEFAULT(MaxRAMPercentage) &&
      !FLAG_IS_DEFAULT(MaxRAMFraction))
    MaxRAMPercentage = 100.0 / MaxRAMFraction;

  if (FLAG_IS_DEFAULT(MinRAMPercentage) &&
      !FLAG_IS_DEFAULT(MinRAMFraction))
    MinRAMPercentage = 100.0 / MinRAMFraction;

  if (FLAG_IS_DEFAULT(InitialRAMPercentage) &&
      !FLAG_IS_DEFAULT(InitialRAMFraction))
    InitialRAMPercentage = 100.0 / InitialRAMFraction;

  // If the maximum heap size has not been set with -Xmx,
  // then set it as fraction of the size of physical memory,
  // respecting the maximum and minimum sizes of the heap.
  if (FLAG_IS_DEFAULT(MaxHeapSize)) {
    julong reasonable_max = (julong)((phys_mem * MaxRAMPercentage) / 100);
    const julong reasonable_min = (julong)((phys_mem * MinRAMPercentage) / 100);
    if (reasonable_min < MaxHeapSize) {
      // Small physical memory, so use a minimum fraction of it for the heap
      reasonable_max = reasonable_min;
    } else {
      // Not-small physical memory, so require a heap at least
      // as large as MaxHeapSize
      reasonable_max = MAX2(reasonable_max, (julong)MaxHeapSize);
    }

    if (!FLAG_IS_DEFAULT(ErgoHeapSizeLimit) && ErgoHeapSizeLimit != 0) {
      // Limit the heap size to ErgoHeapSizeLimit
      reasonable_max = MIN2(reasonable_max, (julong)ErgoHeapSizeLimit);
    }

    reasonable_max = limit_heap_by_allocatable_memory(reasonable_max);

    if (!FLAG_IS_DEFAULT(InitialHeapSize)) {
      // An initial heap size was specified on the command line,
      // so be sure that the maximum size is consistent.  Done
      // after call to limit_heap_by_allocatable_memory because that
      // method might reduce the allocation size.
      reasonable_max = MAX2(reasonable_max, (julong)InitialHeapSize);
    } else if (!FLAG_IS_DEFAULT(MinHeapSize)) {
      reasonable_max = MAX2(reasonable_max, (julong)MinHeapSize);
    }

#ifdef _LP64
    if (UseCompressedOops || UseCompressedClassPointers) {
      // HeapBaseMinAddress can be greater than default but not less than.
      if (!FLAG_IS_DEFAULT(HeapBaseMinAddress)) {
        if (HeapBaseMinAddress < DefaultHeapBaseMinAddress) {
          // matches compressed oops printing flags
          log_debug(gc, heap, coops)("HeapBaseMinAddress must be at least " SIZE_FORMAT
                                     " (" SIZE_FORMAT "G) which is greater than value given " SIZE_FORMAT,
                                     DefaultHeapBaseMinAddress,
                                     DefaultHeapBaseMinAddress/G,
                                     HeapBaseMinAddress);
          FLAG_SET_ERGO(HeapBaseMinAddress, DefaultHeapBaseMinAddress);
        }
      }
    }
    if (UseCompressedOops) {
      // Limit the heap size to the maximum possible when using compressed oops
      julong max_coop_heap = (julong)max_heap_for_compressed_oops();

      if (HeapBaseMinAddress + MaxHeapSize < max_coop_heap) {
        // Heap should be above HeapBaseMinAddress to get zero based compressed oops
        // but it should be not less than default MaxHeapSize.
        max_coop_heap -= HeapBaseMinAddress;
      }

      // If user specified flags prioritizing os physical
      // memory limits, then disable compressed oops if
      // limits exceed max_coop_heap and UseCompressedOops
      // was not specified.
      if (reasonable_max > max_coop_heap) {
        if (FLAG_IS_ERGO(UseCompressedOops) && override_coop_limit) {
          log_info(cds)("UseCompressedOops and UseCompressedClassPointers have been disabled due to"
            " max heap " SIZE_FORMAT " > compressed oop heap " SIZE_FORMAT ". "
            "Please check the setting of MaxRAMPercentage %5.2f."
            ,(size_t)reasonable_max, (size_t)max_coop_heap, MaxRAMPercentage);
          FLAG_SET_ERGO(UseCompressedOops, false);
          if (COMPRESSED_CLASS_POINTERS_DEPENDS_ON_COMPRESSED_OOPS) {
            FLAG_SET_ERGO(UseCompressedClassPointers, false);
          }
        } else {
          reasonable_max = MIN2(reasonable_max, max_coop_heap);
        }
      }
    }
#endif // _LP64

    log_trace(gc, heap)("  Maximum heap size " SIZE_FORMAT, (size_t) reasonable_max);
    FLAG_SET_ERGO(MaxHeapSize, (size_t)reasonable_max);
  }

  // If the minimum or initial heap_size have not been set or requested to be set
  // ergonomically, set them accordingly.
  if (InitialHeapSize == 0 || MinHeapSize == 0) {
    julong reasonable_minimum = (julong)(OldSize + NewSize);

    reasonable_minimum = MIN2(reasonable_minimum, (julong)MaxHeapSize);

    reasonable_minimum = limit_heap_by_allocatable_memory(reasonable_minimum);

    if (InitialHeapSize == 0) {
      julong reasonable_initial = (julong)((phys_mem * InitialRAMPercentage) / 100);
      reasonable_initial = limit_heap_by_allocatable_memory(reasonable_initial);

      reasonable_initial = MAX3(reasonable_initial, reasonable_minimum, (julong)MinHeapSize);
      reasonable_initial = MIN2(reasonable_initial, (julong)MaxHeapSize);

      FLAG_SET_ERGO(InitialHeapSize, (size_t)reasonable_initial);
      log_trace(gc, heap)("  Initial heap size " SIZE_FORMAT, InitialHeapSize);
    }
    // If the minimum heap size has not been set (via -Xms or -XX:MinHeapSize),
    // synchronize with InitialHeapSize to avoid errors with the default value.
    if (MinHeapSize == 0) {
      FLAG_SET_ERGO(MinHeapSize, MIN2((size_t)reasonable_minimum, InitialHeapSize));
      log_trace(gc, heap)("  Minimum heap size " SIZE_FORMAT, MinHeapSize);
    }
  }
}



```





调试 -XX:+PrintFlagsFinal 
运行中的进程: jinfo -p 2981|grep jvm_args
jinfo -flags 2981

java -XX:+PrintCommandLineFlags -version



## Java主流垃圾回收器


- Seria
    > 串行垃圾回收器, 单线程的串行收集器，会出现Stop The World，即该收集器运行时会暂停其他所有线程
    > -XX:+UseSerialGC 新生代和老年代都用串行收集器 Serial + Serial Old
- Parallel Scavenge 
    > 出现 STW(Stop The World 会暂停其他所有线程), 采用复制算法的多线程新生代垃圾回收器，Parallel收集器更关注系统的吞吐量。
    > 吞吐量就是CPU用于运行用户代码的时间与CPU总消耗时间的比值，即吞吐量=运行用户代码时间 / (运行用户代码时间 + 垃圾收集时间)
    > -XX:+UseParallelGC  新生代使用 ParallelScavenge，老年代使用 Serial Old
- Parallel Old 
    > Parallel Old收集器是Parallel Scavenge收集器的老年代版本，采用多线程和”标记－整理”算法，也是比较关注吞吐量。在注重吞吐量及CPU资源敏感的场合，都可以优先考虑Parallel Scavenge加Parallel Old收集器。
    > -XX:+UseParallelOldGC 使用ParallelOld收集器
    > -XX:ParallelGCThreads 并行回收线程数量
- Parrallel Scavenge + Parrallel Old
    > 吞吐量优先，后台任务型服务适合；除了激活年轻代并行垃圾收集，也激活了年老代并行垃圾收集, 年老代吞吐量优化收集器，使用多线程和标记-整理
    > -XX:+UseParallelOldGC 新生代 ParallelScavenge + 老年代 ParallelOld 组合；
    > -XX:ParallelGCThreads 并行回收线程数量
- ParNew 
    > 类似于 Parallel Scavenge 收集器，可以理解为Parallel Scavenge收集器的加强版，主要就是为了用来配合和CMS一起使用 
    > ParNew收集器是一个工作在新生代的垃圾收集器，它只是简单的将串行收集器多线程化，它的回收策略和算法和串行回收器一样。新生代并行，老年代串行；新生代复制算法、老年代标记-压缩。
    > -XX:+UseParNewGC 新生代并行老年代串行
    > -XX:ParallelGCThreads 并行回收线程数量
- CMS 回收器
    > 经典的低停顿搜集器，绝大多数商用、延时敏感的服务在使用； CMS(Concurrent Mark Sweep)并发标记请除，它使用的是标记请除法，工作在老年代，主要关注系统的停顿时间
    > -XX:+UseParNewGC -XX:+UseConcMarkSweepGC 新生代使用 ParNew，老年代使用 CMS；
    > -XX:ParallelCMSThreads  CMS线程数量
- G1
    > JDK 9默认搜集器，堆内存比较大（6G-8G以上）的时候表现出比较高吞吐量和短暂的停顿时间；
    > -XX:+UseG1GC
    > -XX:ParallelGCThreads 并行回收线程数量
    > -XX:ConcGCThreads G1并发标记线程数量
- ZGC 
    > JDK11中推出的一款低延迟垃圾回收器，目前处在实验阶段；
    > 在JDK11中，ZGC被以实验性的特性引入，在JDK15中正式投入使用。在JDK16发布后，GC暂停时间已经缩小到1ms以内，并且时间复杂度为o(1)了，这也意味着GC停顿时间是一个固定值，不会受到堆内存大小的影响了
    > 在ZGC中，为了更灵活高效的管理内存，使用了内存多重映射，把同一块儿物理内存映射为Marked0、Marked1、Remapped三个虚拟内存。当应用程序创建对象时，会在堆上申请一个虚拟地址，这时 ZGC 会为这个对象在 Marked0、Marked1 和 Remapped 这三个视图空间分别申请一个虚拟地址，这三个虚拟地址映射到同一个物理地址。Marked0、Marked1 和 Remapped 这三个虚拟内存作为 ZGC 的三个视图空间，在同一个时间点内只能有一个有效。ZGC 就是通过这三个视图空间的切换，来完成并发的垃圾回收。
    > -XX:+UseZGC
- Epsilon GC
    > 与ZGC一起在JDK11中被引入的Epsilon GC是A NoOp Garbage Collector（没有操作的垃圾收集器）。JDK上对这个特性的描述是：开发一个处理内存分配但不实现任何实际内存回收机制的GC， 一旦可用堆内存用完，JVM就会退出。也就是说，这是一个没有什么卵用的GC。它的作用主要在于进行性能测试，它可以有效的过滤掉GC对于性能的影响，因为它什么也不做。另外它也可以用于进行内存压力测试，看看多久程序会崩溃，用于检测自己的代码质量
    > -XX:+UseEpsilonGC
- Shenandoah GC
    > JDK12开始引入了Shenandoah GC，它的主要目标是使99.9%的停顿小于10ms，这种算法与其它GC算法的主要区别是引入了一个Concurrent Evacuation的过程，在这一过程中，JVM将对象集合从集合集复制到其它区别
    > -XX:+UseShenandoahGC 开启






### GC收集器

- 新生代
    - Serial
    - Parallel Scavenge
    - ParNew
- 老年代
    - Serial Old
    - Parallel Old
    - CMS
- G1
    - https://www.oracle.com/technical-resources/articles/java/g1gc.html




（1）串行回收器：Serial、Serial Old
（2）并行回收器：ParNew、Parallel Scavenge、Parallel Old
（3）并发回收器：CMS、G1



| ———— | 新生GC代策略 | 年老代GC策略 | 说明 | 
|:---:| :--- | :--- | :--- | 
| 组合1 | Serial | Serial Old | Serial和Serial Old都是单线程进行GC，特点就是GC时暂停所有应用线程。 | 
| 组合2 | Serial | CMS+Serial Old | CMS（Concurrent Mark Sweep）是并发GC，实现GC线程和应用线程并发工作，不需要暂停所有应用线程。另外，当CMS进行GC失败时，会自动使用Serial Old策略进行GC。 | 
| 组合3 | ParNew | cms | 使用-XX:+UseParNewGC选项来开启。ParNew是Serial的并行版本，可以指定GC线程数，默认GC线程数为CPU的数量。可以使用-XX:ParallelGCThreads选项指定GC的线程数。
如果指定了选项-XX:+UseConcMarkSweepGC选项，则新生代默认使用ParNew GC策略。| 
| 组合4 | ParNew | Serial Old | 使用-XX:+UseParNewGC选项来开启。新生代使用ParNew GC策略，年老代默认使用Serial Old GC策略。 | 
| 组合5 | Parallel Scavenge | Serial Old | `Parallel Scavenge策略主要是关注一个可控的吞吐量：应用程序运行时间 / (应用程序运行时间 + GC时间)，可见这会使得CPU的利用率尽可能的高，适用于后台持久运行的应用程序，而不适用于交互较多的应用程序。` | 
| 组合6 | Parallel Scavenge | Parallel Old | Parallel Old是Serial Old的并行版本 | 
| 组合7 | G1GC | G1GC |-XX:+UnlockExperimentalVMOptions -XX:+UseG1GC #开启<br />
`-XX:MaxGCPauseMillis =50` #暂停时间目标<br />
`-XX:GCPauseIntervalMillis =200` #暂停间隔目标<br />
`-XX:+G1YoungGenSize=512m` #年轻代大小<br />
`-XX:SurvivorRatio=6` #幸存区比例 |





```shell
# https://toutiao.io/k/3nkgnj9

-Xms4096M -Xmx4096M -Xmn1536M 
-XX:MetaspaceSize=256M 
-XX:MaxMetaspaceSize=256M 
-XX:+UseParNewGC 
-XX:+UseConcMarkSweepGC 
-XX:+CMSScavengeBeforeRemark 
-XX:CMSInitiatingOccupancyFraction=75 
-XX:+UseCMSInitiatingOccupancyOnly

```



## 常用调优参数

**常见的 JVM 调优参数有哪些？**
> -Xms256m：初始化堆大小为 256m；
> -Xmx2g：最大内存为 2g；
> -Xmn50m：新生代的大小50m；
> -XX:+PrintGCDetails 打印 gc 详细信息；
> -XX:+HeapDumpOnOutOfMemoryError  在发生OutOfMemoryError错误时，来 dump 出堆快照；
> -XX:NewRatio=4    设置年轻的和老年代的内存比例为 1:4；
> -XX:SurvivorRatio=8 设置新生代 Eden 和 Survivor 比例为 8:2；
> -XX:+UseSerialGC   新生代和老年代都用串行收集器 Serial + Serial Old
> -XX:+UseParNewGC 指定使用 ParNew + Serial Old 垃圾回收器组合；
> -XX:+UseParallelGC  新生代使用 ParallelScavenge，老年代使用 Serial Old
> -XX:+UseParallelOldGC：新生代 ParallelScavenge + 老年代 ParallelOld 组合；
> -XX:+UseConcMarkSweepGC：新生代使用 ParNew，老年代使用 CMS；
> -XX:NewSize：新生代最小值；
> -XX:MaxNewSize：新生代最大值
> -XX:MetaspaceSize 元空间初始化大小
> -XX:MaxMetaspaceSize 元空间最大值




## Java变量生命周期


### 0、 JVM 中常用的调优、故障处理等工具。

- jps ：虚拟机进程工具，全称是 JVM Process Status Tool，它的功能和 Linux 中的 ps 类似，可以列出正在运行的虚拟机进程，并显示虚拟机执行主类 Main Class 所在的本地虚拟机唯一 ID，虽然功能比较单一，但是这个命令绝对是使用最高频的一个命令。
- jstat：虚拟机统计信息工具，用于监视虚拟机各种运行状态的信息的命令行工具，它可以显示本地或者远程虚拟机进程中的类加载、内存、垃圾收集、即时编译等运行时数据。
- jinfo：Java 配置信息工具，全称是 Configuration Info for Java，它的作用是可以实时调整虚拟机各项参数。
- jmap：Java 内存映像工具，全称是 Memory Map For Java，它用于生成转储快照，用来排查内存占用情况
- jhat：虚拟机堆转储快照分析工具，全称是 JVM Heap Analysis Tool，这个指令通常和 jmap 一起搭配使用，jhat 内置了一个 HTTP/Web 服务器，生成转储快照后可以在浏览器中查看。不过，一般还是 jmap 命令使用的频率比较高。
- jstack：Java 堆栈跟踪工具，全称是 Stack Trace for Java ，顾名思义，这个命令用来追踪堆栈的使用情况，用于虚拟机当前时刻的线程快照，线程快照就是当前虚拟机内每一条正在执行的方法堆栈的集合。



### 1、java类的成员变量：静态变量、实例变量


#### 静态变量：static 修饰 的类变量

> 1）类的静态变量在内存中只有1个，虚拟机在加载的过程中分配内存。  
> 2）静态变量位于方法区，被类的所有实例共享。  
> 3）静态变量可以直接通过类名进行访问，生命周期取决于类自身的生命周期。  
> 4）静态变量是类相关的变量，它的生命周期是从这个类声明到这类被垃圾回收机制彻底回收才会被销毁。  



#### 实例变量：

> 1）类的实例，每创建一个实例，java虚拟机为实例变量分配一次内存。  
> 2）实例变量位于堆区，生命周期取决于实例的生命周期。  
> 3）实例变量只能由创建出它的对象来调用。  
> 4）实例变量是从这个对象被创建开始，直到这个对象没有任何引用变量去引用它，被回收，实例变量消失。  
> 5）对象被引用，实例变量就存在。  


静态变量生命周期是类的开始和销毁；

实例变量生命周期是对象的开始和销毁。



### 2、局部变量

作用域：定义范围内有效。

作为语句和方法快而存在，存在于方法的参数列表和方法定义中。

初始化：局部变量在使用前必须被程序员主动的初始化；成员变量则会被系统提供一个默认的初始值

类的成员变量能够定义后直接使用，而局部变量在定义后先要赋初值，然后才能使用。






### 2、OOM快速定位

#### 为什么会发生OOM ？

1. 业务正常运行起来就需要比较多的内存，而给JVM设置的内存过小
    - 具体表现就是程序跑不起来，或者跑一会就挂了
2. GC回收内存的速度赶不上程序运行消耗内存的速度
    - 出现这种情况一般就是往list、map中填充大量数据，内存紧张时JVM拆东墙补西墙补不过来了
    - 查询记得分页啊！不需要的字段，尤其是数据量大的字段，就不要返回了
3. 存在内存泄漏情况，久而久之也会造成OOM。哪些情况会造成内存泄漏呢？
    - 比如打开文件不释放
    - 创建网络连接不关闭
    - 不再使用的对象未断开引用关系
    - 使用静态变量持有大对象引用……


#### JVM挂了有哪些可能性 ？
- Windows： 系统角度说，JVM进程如果不是你手动关闭的，那就是OOM导致的
- Linux：不一定，因为Linux系统有一种保护机制：OOM Killer
    - 这个机制是Unix内核独有的，它的出现是为了保证系统在可用内存较少的情况下依旧能够运行，会选择杀掉一些分值较高的进程来回收内存。
        - 这个分值是Unix内核根据一些参数动态计算出来的
- 除了OOM Killer，剩下的就是OOM导致JVM进程挂了



#### 生产环境如何快速定位问题 ？

- 算上直接内存，共有五个区域会发生OOM：直接内存、元空间、本地方法栈、虚拟机栈、元空间
- 本地方法栈与虚拟机栈的OOM咱们可以不用管，为什么呢？因为这两个区域的OOM你在开发阶段或在测试阶段就能发现 -->所以这两个区域的OOM是不会生成dump文件的。
- 查找过程来了:
    - 首先排除是不是被Linux杀死了, `sudo egrep -i -r 'Out Of' /var/log` 查看
        - 如果是，关闭一些服务，或者把一些服务移走，腾出点内存
    - 排除后可以确定是OOM导致的，那具体是哪个OOM导致的呢？看有没有生成dump文件
        - 如果生成了，要么是堆OOM，要么是元空间OOM
        - 如果没生成，直接可以确定是直接内存导致的OOM
    - 是堆OOM还是元空间OOM。这时候需要把dump文件从服务器上下载下来，用visualvm分析（其他工具如MAT、JProfiler都可以）
        - 发现发生OOM的位置是创建对象，调用构造方法之类的代码，那一定是堆OOM
            - <init>就是构造方法的字节码格式
        - 发现发生OOM的位置是类加载器那些方法，那一定是元空间OOM



#### 一些成熟的建议

1. 调优参数务必加上`-XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=xxxx.dump.log`，发生OOM让JVM自动dump出内存
2. 堆内存不要设置的特别大，因为你设置的特别大，发生OOM时生成的dump文件就特别大，不好分析。建议不超过8G。
3. 想主动dump出JVM的内存，有挺多方式
    - 不管哪种方式，主动dump内存会引发STW，请择时操作
    - 通过arthas提供的命令heapdump主动dump出JVM的内存，这个操作会引发FGC，背后是STW，操作时请选择好时机



### 3、cpu占用过高

- 获取进程id：
    - 用 ps 或 top 或 pgrep 等任何你熟悉的工具
    - 也可以用 jps

- 查看进程的  用 top -Hp 命令查看线程的情况
    - 找到占用 cpu 高的线程

- 把占用 cpu 高的线程转为 16 禁止
    - > `[ghostwwl@ghostwwl project]$ printf "%x" 7885`

- 用 jstack 工具查看线程栈情况
    - >  jstack 7797 | grep 1ecd -A 10
    - 应该可以看到正在运行的方法


### 4、死锁

- 获取进程id
- jstack查看
    - jstack 自动会把产生死锁的信息，及是什么线程产生的， 输出到最后，所以我们只需要看最后的内容就行了
    - > Found 1 deadlock.
- 根据线程可以找到线程运行的函数，然后定位锁相关代码


### 5、内存泄漏

- 获取进程id
- 用jstat分析gc活动情况
    - > jstat -gcutil -t -h8 7797 1000
    - 上面是命令: 输出gc的情况，输出时间，每8行输出一个行头信息，统计的进程号是 7797，每1000毫秒输出一次信息
- 拿出内存快照分析: jmap -dump:live,format=b,file=heap.bin 7797

```bash 
(base) [ghostwwl@ghostwwl project]$ jstat -gcutil -t -h8 7797 1000
Timestamp         S0     S1     E      O      M     CCS    YGC     YGCT    FGC    FGCT    CGC    CGCT     GCT   
       415901.4   0.00 100.00  59.48  78.29  96.72  90.52    887   22.899     6    5.608    97    6.845   35.352
       415902.5   0.00 100.00  59.48  78.29  96.72  90.52    887   22.899     6    5.608    97    6.845   35.352
       415903.5   0.00 100.00  59.48  78.29  96.72  90.52    887   22.899     6    5.608    97    6.845   35.352
       415904.5   0.00 100.00  59.48  78.29  96.72  90.52    887   22.899     6    5.608    97    6.845   35.352
       415905.5   0.00 100.00  59.48  78.29  96.72  90.52    887   22.899     6    5.608    97    6.845   35.352
       415906.5   0.00 100.00  59.48  78.29  96.72  90.52    887   22.899     6    5.608    97    6.845   35.352
       415907.5   0.00 100.00  59.49  78.29  96.72  90.52    887   22.899     6    5.608    97    6.845   35.352
       415908.5   0.00 100.00  59.49  78.29  96.72  90.52    887   22.899     6    5.608    97    6.845   35.352
Timestamp         S0     S1     E      O      M     CCS    YGC     YGCT    FGC    FGCT    CGC    CGCT     GCT   
       415909.5   0.00 100.00  59.59  78.29  96.72  90.52    887   22.899     6    5.608    97    6.845   35.352
       415910.5   0.00 100.00  59.59  78.29  96.72  90.52    887   22.899     6    5.608    97    6.845   35.352
       415911.5   0.00 100.00  59.59  78.29  96.72  90.52    887   22.899     6    5.608    97    6.845   35.352
       415912.5   0.00 100.00  59.59  78.29  96.72  90.52    887   22.899     6    5.608    97    6.845   35.352
```




### 常用jvm 调试

```bash 
JVM_EXPORT_DIR="./jvm_export"
PIDS=`ps  --no-heading -C java -f --width 1000 |awk '{print $2'}`

if [ ! -d $JVM_EXPORT_DIR ]; then
	mkdir -p $JVM_EXPORT_DIR
fi

for PID in $PIDS ; do
	jstack $PID > $JVM_EXPORT_DIR/jstack-$PID.dump 2>&1
	echo -e ".\c"
	jinfo $PID > $JVM_EXPORT_DIR/jinfo-$PID.dump 2>&1
	echo -e ".\c"
	jstat -gcutil $PID > $JVM_EXPORT_DIR/jstat-gcutil-$PID.dump 2>&1
	echo -e ".\c"
	jstat -gccapacity $PID > $JVM_EXPORT_DIR/jstat-gccapacity-$PID.dump 2>&1
	echo -e ".\c"
	jmap $PID > $JVM_EXPORT_DIR/jmap-$PID.dump 2>&1
	echo -e ".\c"
	jmap -heap $PID > $JVM_EXPORT_DIR/jmap-heap-$PID.dump 2>&1
	echo -e ".\c"
	jmap -histo $PID > $JVM_EXPORT_DIR/jmap-histo-$PID.dump 2>&1
	echo -e ".\c"
	if [ -r /usr/bin/lsof ]; then
	/usr/bin/lsof -p $PID > $JVM_EXPORT_DIR/lsof-$PID.dump
	echo -e ".\c"
	fi
done
if [ -r /bin/netstat ]; then
/bin/netstat -an > $JVM_EXPORT_DIR/netstat.dump 2>&1
echo -e ".\c"
fi
if [ -r /usr/bin/iostat ]; then
/usr/bin/iostat > $JVM_EXPORT_DIR/iostat.dump 2>&1
echo -e ".\c"
fi
if [ -r /usr/bin/mpstat ]; then
/usr/bin/mpstat > $JVM_EXPORT_DIR/mpstat.dump 2>&1
echo -e ".\c"
fi
if [ -r /usr/bin/vmstat ]; then
/usr/bin/vmstat > $JVM_EXPORT_DIR/vmstat.dump 2>&1
echo -e ".\c"
fi
if [ -r /usr/bin/free ]; then
/usr/bin/free -t > $JVM_EXPORT_DIR/free.dump 2>&1
echo -e ".\c"
fi
if [ -r /usr/bin/sar ]; then
/usr/bin/sar > $JVM_EXPORT_DIR/sar.dump 2>&1
echo -e ".\c"
fi
if [ -r /usr/bin/uptime ]; then
/usr/bin/uptime > $JVM_EXPORT_DIR/uptime.dump 2>&1
echo -e ".\c"
fi
echo "OK!"

```
















