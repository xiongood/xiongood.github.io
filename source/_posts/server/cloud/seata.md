---
title: seata的简单使用
img: https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/seata.jpg
categories:
 - 后端
tags:
 - 微服务
 - seata
 - java
---

## 搭建for wind11

### 下载源码和编译好的包

源码用来获取各种脚本

编译好的包用来启动服务

```http
https://github.com/seata/seata/releases/tag/v1.3.0
```

![image-20230614140448345](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230614140449.png)

### 配置数据库

#### 新建数据库并且运行sql脚本

创建seata库

![image-20230614140642862](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230614140643.png)

```sql
-- -------------------------------- The script used when storeMode is 'db' --------------------------------
-- the table to store GlobalSession data
CREATE TABLE IF NOT EXISTS `global_table`
(
    `xid`                       VARCHAR(128) NOT NULL,
    `transaction_id`            BIGINT,
    `status`                    TINYINT      NOT NULL,
    `application_id`            VARCHAR(32),
    `transaction_service_group` VARCHAR(32),
    `transaction_name`          VARCHAR(128),
    `timeout`                   INT,
    `begin_time`                BIGINT,
    `application_data`          VARCHAR(2000),
    `gmt_create`                DATETIME,
    `gmt_modified`              DATETIME,
    PRIMARY KEY (`xid`),
    KEY `idx_gmt_modified_status` (`gmt_modified`, `status`),
    KEY `idx_transaction_id` (`transaction_id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8;

-- the table to store BranchSession data
CREATE TABLE IF NOT EXISTS `branch_table`
(
    `branch_id`         BIGINT       NOT NULL,
    `xid`               VARCHAR(128) NOT NULL,
    `transaction_id`    BIGINT,
    `resource_group_id` VARCHAR(32),
    `resource_id`       VARCHAR(256),
    `branch_type`       VARCHAR(8),
    `status`            TINYINT,
    `client_id`         VARCHAR(64),
    `application_data`  VARCHAR(2000),
    `gmt_create`        DATETIME(6),
    `gmt_modified`      DATETIME(6),
    PRIMARY KEY (`branch_id`),
    KEY `idx_xid` (`xid`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8;

-- the table to store lock data
CREATE TABLE IF NOT EXISTS `lock_table`
(
    `row_key`        VARCHAR(128) NOT NULL,
    `xid`            VARCHAR(96),
    `transaction_id` BIGINT,
    `branch_id`      BIGINT       NOT NULL,
    `resource_id`    VARCHAR(256),
    `table_name`     VARCHAR(32),
    `pk`             VARCHAR(36),
    `gmt_create`     DATETIME,
    `gmt_modified`   DATETIME,
    PRIMARY KEY (`row_key`),
    KEY `idx_branch_id` (`branch_id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8;

```

另外创建一个日志表(每个业务表都需要)

```sql
-- 注意此处0.3.0+ 增加唯一索引 ux_undo_log
CREATE TABLE `undo_log` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `branch_id` bigint(20) NOT NULL,
  `xid` varchar(100) NOT NULL,
  `context` varchar(128) NOT NULL,
  `rollback_info` longblob NOT NULL,
  `log_status` int(11) NOT NULL,
  `log_created` datetime NOT NULL,
  `log_modified` datetime NOT NULL,
  `ext` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ux_undo_log` (`xid`,`branch_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

```

#### 编辑包中file.conf

主要是将数据库换为db

![image-20230614142153911](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230614142154.png)

![image-20230614142122792](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230614142123.png)

完整版如下：

```shell
## transaction log store, only used in seata-server
store {
  ## store mode: file、db、redis
  mode = "db"

  ## file store property
  file {
    ## store location dir
    dir = "sessionStore"
    # branch session size , if exceeded first try compress lockkey, still exceeded throws exceptions
    maxBranchSessionSize = 16384
    # globe session size , if exceeded throws exceptions
    maxGlobalSessionSize = 512
    # file buffer size , if exceeded allocate new buffer
    fileWriteBufferCacheSize = 16384
    # when recover batch read size
    sessionReloadReadSize = 100
    # async, sync
    flushDiskMode = async
  }

  ## database store property
  db {
    ## the implement of javax.sql.DataSource, such as DruidDataSource(druid)/BasicDataSource(dbcp)/HikariDataSource(hikari) etc.
    datasource = "druid"
    ## mysql/oracle/postgresql/h2/oceanbase etc.
    dbType = "mysql"
    driverClassName = "com.mysql.jdbc.Driver"
    url = "jdbc:mysql://xxx.xxx.xxx.xxx:3306/seata"
    user = "root"
    password = "123456"
    minConn = 5
    maxConn = 30
    globalTable = "global_table"
    branchTable = "branch_table"
    lockTable = "lock_table"
    queryLimit = 100
    maxWait = 5000
  }

  ## redis store property
  redis {
    host = "127.0.0.1"
    port = "6379"
    password = ""
    database = "0"
    minConn = 1
    maxConn = 10
    queryLimit = 100
  }

}

```

### 配置注册中心

#### 新增命名空间

需要新增命名空间id

19e11a82-91ea-4d16-8dfc-fa989e748c83

![image-20230614143747718](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230614143748.png)

#### 修改配置registry.conf

此处直接修改了 配置中心和注册中心的 配置

![image-20230614143934142](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230614143935.png)

![image-20230614153628255](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230614153629.png)

```shell
registry {
  # file 、nacos 、eureka、redis、zk、consul、etcd3、sofa
  type = "nacos"

  nacos {
    application = "seata-server"
    serverAddr = "xxx.xxx.xxx.xxx:8848"
    group = "SEATA_GROUP"
    namespace = "19e11a82-91ea-4d16-8dfc-fa989e748c83"
    cluster = "default"
    username = "nacos"
    password = "nacos"
  }
  eureka {
    serviceUrl = "http://localhost:8761/eureka"
    application = "default"
    weight = "1"
  }
  redis {
    serverAddr = "localhost:6379"
    db = 0
    password = ""
    cluster = "default"
    timeout = 0
  }
  zk {
    cluster = "default"
    serverAddr = "127.0.0.1:2181"
    sessionTimeout = 6000
    connectTimeout = 2000
    username = ""
    password = ""
  }
  consul {
    cluster = "default"
    serverAddr = "127.0.0.1:8500"
  }
  etcd3 {
    cluster = "default"
    serverAddr = "http://localhost:2379"
  }
  sofa {
    serverAddr = "127.0.0.1:9603"
    application = "default"
    region = "DEFAULT_ZONE"
    datacenter = "DefaultDataCenter"
    cluster = "default"
    group = "SEATA_GROUP"
    addressWaitTime = "3000"
  }
  file {
    name = "file.conf"
  }
}

config {
  # file、nacos 、apollo、zk、consul、etcd3
  type = "nacos"

  nacos {
    serverAddr = "xxx.xxx.xxx.xxx:8848"
    namespace = "19e11a82-91ea-4d16-8dfc-fa989e748c83"
    group = "SEATA_GROUP"
    username = "nacos"
    password = "nacos"
  }
  consul {
    serverAddr = "127.0.0.1:8500"
  }
  apollo {
    appId = "seata-server"
    apolloMeta = "http://192.168.1.204:8801"
    namespace = "application"
  }
  zk {
    serverAddr = "127.0.0.1:2181"
    sessionTimeout = 6000
    connectTimeout = 2000
    username = ""
    password = ""
  }
  etcd3 {
    serverAddr = "http://localhost:2379"
  }
  file {
    name = "file.conf"
  }
}

```

### 配置配置中心

#### 推送配置信息（操作源码）

##### 修改配置(执行时将注释去掉)

![image-20230614144759044](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230614144800.png)

完整的配置如下：（执行时去掉注释）

```c
transport.type=TCP
transport.server=NIO
transport.heartbeat=true
transport.enableClientBatchSendRequest=false
transport.threadFactory.bossThreadPrefix=NettyBoss
transport.threadFactory.workerThreadPrefix=NettyServerNIOWorker
transport.threadFactory.serverExecutorThreadPrefix=NettyServerBizHandler
transport.threadFactory.shareBossWorker=false
transport.threadFactory.clientSelectorThreadPrefix=NettyClientSelector
transport.threadFactory.clientSelectorThreadSize=1
transport.threadFactory.clientWorkerThreadPrefix=NettyClientWorkerThread
transport.threadFactory.bossThreadSize=1
transport.threadFactory.workerThreadSize=default
transport.shutdown.wait=3
# \seata-1.3.0\config\seata-config-core\src\main\resources
# 这里的名字与file.conf中vgroup_mapping.my_test_tx_group = "default"相同
service.vgroupMapping.my_test_tx_group=default
# 这里的名字与file.conf中default.grouplist = "127.0.0.1:8091"相同
service.default.grouplist=127.0.0.1:8091
service.enableDegrade=false
service.disableGlobalTransaction=false
client.rm.asyncCommitBufferLimit=10000
client.rm.lock.retryInterval=10
client.rm.lock.retryTimes=30
client.rm.lock.retryPolicyBranchRollbackOnConflict=true
client.rm.reportRetryCount=5
client.rm.tableMetaCheckEnable=false
client.rm.sqlParserType=druid
client.rm.reportSuccessEnable=false
client.rm.sagaBranchRegisterEnable=false
client.tm.commitRetryCount=5
client.tm.rollbackRetryCount=5
client.tm.degradeCheck=false
client.tm.degradeCheckAllowTimes=10
client.tm.degradeCheckPeriod=2000
# 此处指定为db
store.mode=db
store.file.dir=file_store/data
store.file.maxBranchSessionSize=16384
store.file.maxGlobalSessionSize=512
store.file.fileWriteBufferCacheSize=16384
store.file.flushDiskMode=async
store.file.sessionReloadReadSize=100
store.db.datasource=druid
store.db.dbType=mysql
# 如果数据库版本为8.0以上，则修改为com.mysql.cj.jdbc.Driver
store.db.driverClassName=com.mysql.jdbc.Driver
store.db.url=jdbc:mysql://xxx.xxx.xxx.xxx:3306/seata?useUnicode=true
store.db.user=root
store.db.password=123456

store.db.minConn=5
store.db.maxConn=30
store.db.globalTable=global_table
store.db.branchTable=branch_table
store.db.queryLimit=100
store.db.lockTable=lock_table
store.db.maxWait=5000
store.redis.host=127.0.0.1
store.redis.port=6379
store.redis.maxConn=10
store.redis.minConn=1
store.redis.database=0
store.redis.password=null
store.redis.queryLimit=100
server.recovery.committingRetryPeriod=1000
server.recovery.asynCommittingRetryPeriod=1000
server.recovery.rollbackingRetryPeriod=1000
server.recovery.timeoutRetryPeriod=1000
server.maxCommitRetryTimeout=-1
server.maxRollbackRetryTimeout=-1
server.rollbackRetryTimeoutUnlockEnable=false
client.undo.dataValidation=true
client.undo.logSerialization=jackson
client.undo.onlyCareUpdateColumns=true
server.undo.logSaveDays=7
server.undo.logDeletePeriod=86400000
client.undo.logTable=undo_log
client.log.exceptionRate=100
transport.serialization=seata
transport.compressor=none
metrics.enabled=false
metrics.registryType=compact
metrics.exporterList=prometheus
metrics.exporterPrometheusPort=9898
```

##### 推送配置到nacos

![image-20230614150133986](C:/Users/java0/AppData/Roaming/Typora/typora-user-images/image-20230614150133986.png)

```sh
sh nacos-config.sh -h 140.143.225.240 -p 8848 -g SEATA_GROUP -t 19e11a82-91ea-4d16-8dfc-fa989e748c83 -u nacos -w nacos
```

修改完后如下：

![image-20230614153346404](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230614153347.png)

#### 修改配置

在修改注册中心的时候，已经配置

### 启动seata

```sh
seata-server.bat
```

![image-20230614150927036](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230614150928.png)

启动后

![image-20230614151522749](https://pub-b24cf0a8c1f14e9386435977aa464959.r2.dev/img/20230614151523.png)

## 客户端整合seata

所有需要事务控制的都需要该配置

### pom

```xml
<dependency>
    <groupId>com.alibaba.cloud</groupId>
    <artifactId>spring-cloud-starter-alibaba-seata</artifactId>
</dependency>
```

### application.yml

```yaml

# seata配置信息
seata:
  # 是否启用，true为启用
  enabled: true
  # 分布式事务服务id，默认同当前application.name相同
  application-id: yuanlai-seata-client
  # 这里的名字与file.conf中vgroup_mapping.my_test_tx_group = "default"相同
  tx-service-group: my_test_tx_group
  enable-auto-data-source-proxy: true
  # 此处配置该模块要连接的seata服务端等详细信息
  service:
    # 此处配置事务组信息，这里的名字与file.conf中的相同，也就是vgroup_mapping.my_test_tx_group = "default"
    vgroup-mapping:
      my_test_tx_group: default
      # seata服务端地址，可以单个也可以多个。此处为单个。
    grouplist:
      default: 127.0.0.1:8091

      # 指定seata的配置中心信息
  config:
    # 指定seata配置中心类型，为nacos
    type: nacos
    # nacos配置中心的详细信息
    nacos:
      # 所在的命名空间
      namespace: 19e11a82-91ea-4d16-8dfc-fa989e748c83
      # naocs配置中心地址
      server-addr: xxx.xxx.xxx.xxx:8848
      # 所在的组
      group: SEATA_GROUP
      # nacos控制台登录账户
      username: "nacos"
      # nacos控制台登录密码
      password: "nacos"

      # 指定seata的注册中心信息
  registry:
    # 指定seata注册中心类型，为nacos
    type: nacos
    # nacos注册中心的详细信息
    nacos:
      # 指定本seata客户端在nacos注册中心的服务名
      application: seata-server
      # nacos注册中心地址
      server-addr: xxx.xxx.xxx.xxx:8848
      # 所在的组
      group: SEATA_GROUP
      # 所在的命名空间
      namespace: 19e11a82-91ea-4d16-8dfc-fa989e748c83
      # nacos控制台登录账户
      username: "nacos"
      # nacos控制台登录密码
      password: "nacos"
```

### 测试

在需要进行事务控制的地方 加上注解@GlobalTransactional

```java
import com.yuanlai.test.entity.YuanTest;
import com.yuanlai.api.common.utils.base.BaseController;
import com.yuanlai.api.common.utils.result.ResultMsg;
import com.yuanlai.api.common.utils.result.ResultMsgUtil;
import com.yuanlai.test.service.OpenFeignService;
import com.yuanlai.test.service.YuanTestService;
import io.seata.spring.annotation.GlobalTransactional;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.bind.annotation.*;

/**
 * @author ：ZhangYiXiong
 * @date ：Created in 2022/2/9 星期三 17:09
 * @description：
 * @modified By：
 * @version:
 */
@RestController
@RequestMapping("/test/")
@Api(tags = "测试接口")
@CrossOrigin
@Slf4j
public class TestController extends BaseController {

    @Autowired
    YuanTestService yuanTestService;

    @Autowired
    OpenFeignService openFeignService;

    @GetMapping ("save")
    @ApiOperation(value = "测试seata", notes = "测试seata")
    @GlobalTransactional
    public ResultMsg save() {
        YuanTest yuanTest = new YuanTest("lisi",20);
        yuanTestService.getBaseMapper().insert(yuanTest);
        openFeignService.save();
        //System.out.println(1/0);
        return ResultMsgUtil.ok();
    }
}
```

