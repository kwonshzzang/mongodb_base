## Overview

이 문서는 local 환경에서 MongoDB를 Replica Set으로 구축하는 방법을 작성한다. 

## 참고

- https://www.mongodb.com/docs/manual/tutorial/deploy-replica-set/
- https://www.mongodb.com/docs/manual/tutorial/deploy-replica-set-for-testing/

## 환경

해당 실습은 MacOS에서 진행되었으며 MongoDB 5.0.12 버전을 사용한다. 

Window나 Linux 계열의 다른 플랫폼에서 사용하더라도 binary의 옵션은 동일하여, 똑같은 실습 진행이 가능하다. 


## 실습

### Binary 설치

https://www.mongodb.com/try/download/community

### 환경준비

```bash
mkdir -p mongodb/data{1,2,3}
mkdir -p mongodb/config
mkdir -p mongodb/logs

rm -rf mongodb/data{1,2,3}
```

### 실행방법1. Binary 옵션 이용


```bash
cd ~/Downloads
cd mongodb-macos-aarch64-7.0.5
cd bin

# 각각 다른 터미널에서 실행한다.
mongod --replSet rs1 --port 27017 --bind_ip "0.0.0.0" --dbpath /Users/kwonsoonhyun/Dev/mongodb/data1 --oplogSize 128
mongod --replSet rs1 --port 27018 --bind_ip "0.0.0.0" --dbpath /Users/kwonsoonhyun/Dev/mongodb/data2 --oplogSize 128
mongod --replSet rs1 --port 27019 --bind_ip "0.0.0.0" --dbpath /Users/kwonsoonhyun/Dev/mongodb/data3 --oplogSize 128
```

### 실행방법2. Config 파일 이용

```bash
vim mongodb/config/mongod1.conf
vim mongodb/config/mongod2.conf
vim mongodb/config/mongod3.conf
```

#### mongod1.conf

```yaml
net:
    port: 27017
    bindIp: 0.0.0.0

storage:
    dbPath: "/Users/kwonsoonhyun/Dev/mongodb/data1"
    directoryPerDB: true

replication:
    oplogSizeMB: 128
    replSetName: "rs1"

systemLog:
    path: "/Users/kwonsoonhyun/Dev/mongodb/logs/mongod1.log"
    destination: "file"
```

#### mongod2.conf

```yaml
net:
    port: 27018
    bindIp: 0.0.0.0

storage:
    dbPath: "/Users/kwonsoonhyun/Dev/mongodb/data2"
    directoryPerDB: true

replication:
    oplogSizeMB: 128
    replSetName: "rs1"

systemLog:
    path: "/Users/kwonsoonhyun/Dev/mongodb/logs/mongod2.log"
    destination: "file"
```

#### mongod3.conf

```yaml
net:
    port: 27019
    bindIp: 0.0.0.0

storage:
    dbPath: "/Users/kwonsoonhyun/Dev/mongodb/data3"
    directoryPerDB: true

replication:
    oplogSizeMB: 128
    replSetName: "rs1"

systemLog:
    path: "/Users/kwonsoonhyun/Dev/mongodb/logs/mongod3.log"
    destination: "file"
```

#### config 파일 실행

```bash
cd ~/Downloads
cd mongodb-macos-aarch64-7.0.5
cd bin

mongod -f /Users/kwonsoonhyun/Dev/mongodb/config/mongod1.conf
mongod -f /Users/kwonsoonhyun/Dev/mongodb/config/mongod2.conf
mongod -f /Users/kwonsoonhyun/Dev/mongodb/config/mongod3.conf
```

### Replica Set Initiate

#### 멤버 접속

```bash
cd ~/Downloads
cd mongodb-macos-aarch64-7.0.5
cd bin

mongosh "mongodb://localhost:27017"
```

#### Replica Set Initiate and Check

```javascript
rs.initiate({
    _id: "rs1",
    members:[
        {_id: 0, host: "localhost:27017"},
        {_id: 1, host: "localhost:27018"},
        {_id: 2, host: "localhost:27019"}
    ]
});

rs.status();
---------------------------------------------------------------------------------------------------------

{
  set: 'rs1',
  date: ISODate('2024-01-23T04:45:19.803Z'),
  myState: 1,
  term: Long('1'),
  syncSourceHost: '',
  syncSourceId: -1,
  heartbeatIntervalMillis: Long('2000'),
  majorityVoteCount: 2,
  writeMajorityCount: 2,
  votingMembersCount: 3,
  writableVotingMembersCount: 3,
  optimes: {
    lastCommittedOpTime: { ts: Timestamp({ t: 1705985113, i: 5 }), t: Long('1') },
    lastCommittedWallTime: ISODate('2024-01-23T04:45:13.319Z'),
    readConcernMajorityOpTime: { ts: Timestamp({ t: 1705985113, i: 5 }), t: Long('1') },
    appliedOpTime: { ts: Timestamp({ t: 1705985113, i: 5 }), t: Long('1') },
    durableOpTime: { ts: Timestamp({ t: 1705985113, i: 5 }), t: Long('1') },
    lastAppliedWallTime: ISODate('2024-01-23T04:45:13.319Z'),
    lastDurableWallTime: ISODate('2024-01-23T04:45:13.319Z')
  },
  lastStableRecoveryTimestamp: Timestamp({ t: 1705985102, i: 1 }),
  electionCandidateMetrics: {
    lastElectionReason: 'electionTimeout',
    lastElectionDate: ISODate('2024-01-23T04:45:12.254Z'),
    electionTerm: Long('1'),
    lastCommittedOpTimeAtElection: { ts: Timestamp({ t: 1705985102, i: 1 }), t: Long('-1') },
    lastSeenOpTimeAtElection: { ts: Timestamp({ t: 1705985102, i: 1 }), t: Long('-1') },
    numVotesNeeded: 2,
    priorityAtElection: 1,
    electionTimeoutMillis: Long('10000'),
    numCatchUpOps: Long('0'),
    newTermStartDate: ISODate('2024-01-23T04:45:12.343Z'),
    wMajorityWriteAvailabilityDate: ISODate('2024-01-23T04:45:12.928Z')
  },
  members: [
    {
      _id: 0,
      name: 'localhost:27017',
      health: 1,
      state: 1,
      stateStr: 'PRIMARY',
      uptime: 663,
      optime: { ts: Timestamp({ t: 1705985113, i: 5 }), t: Long('1') },
      optimeDate: ISODate('2024-01-23T04:45:13.000Z'),
      lastAppliedWallTime: ISODate('2024-01-23T04:45:13.319Z'),
      lastDurableWallTime: ISODate('2024-01-23T04:45:13.319Z'),
      syncSourceHost: '',
      syncSourceId: -1,
      infoMessage: 'Could not find member to sync from',
      electionTime: Timestamp({ t: 1705985112, i: 1 }),
      electionDate: ISODate('2024-01-23T04:45:12.000Z'),
      configVersion: 1,
      configTerm: 1,
      self: true,
      lastHeartbeatMessage: ''
    },
    {
      _id: 1,
      name: 'localhost:27018',
      health: 1,
      state: 2,
      stateStr: 'SECONDARY',
      uptime: 17,
      optime: { ts: Timestamp({ t: 1705985113, i: 5 }), t: Long('1') },
      optimeDurable: { ts: Timestamp({ t: 1705985113, i: 5 }), t: Long('1') },
      optimeDate: ISODate('2024-01-23T04:45:13.000Z'),
      optimeDurableDate: ISODate('2024-01-23T04:45:13.000Z'),
      lastAppliedWallTime: ISODate('2024-01-23T04:45:13.319Z'),
      lastDurableWallTime: ISODate('2024-01-23T04:45:13.319Z'),
      lastHeartbeat: ISODate('2024-01-23T04:45:18.295Z'),
      lastHeartbeatRecv: ISODate('2024-01-23T04:45:19.296Z'),
      pingMs: Long('0'),
      lastHeartbeatMessage: '',
      syncSourceHost: 'localhost:27017',
      syncSourceId: 0,
      infoMessage: '',
      configVersion: 1,
      configTerm: 1
    },
    {
      _id: 2,
      name: 'localhost:27019',
      health: 1,
      state: 2,
      stateStr: 'SECONDARY',
      uptime: 17,
      optime: { ts: Timestamp({ t: 1705985113, i: 5 }), t: Long('1') },
      optimeDurable: { ts: Timestamp({ t: 1705985113, i: 5 }), t: Long('1') },
      optimeDate: ISODate('2024-01-23T04:45:13.000Z'),
      optimeDurableDate: ISODate('2024-01-23T04:45:13.000Z'),
      lastAppliedWallTime: ISODate('2024-01-23T04:45:13.319Z'),
      lastDurableWallTime: ISODate('2024-01-23T04:45:13.319Z'),
      lastHeartbeat: ISODate('2024-01-23T04:45:18.295Z'),
      lastHeartbeatRecv: ISODate('2024-01-23T04:45:19.296Z'),
      pingMs: Long('0'),
      lastHeartbeatMessage: '',
      syncSourceHost: 'localhost:27017',
      syncSourceId: 0,
      infoMessage: '',
      configVersion: 1,
      configTerm: 1
    }
  ],
  ok: 1,
  '$clusterTime': {
    clusterTime: Timestamp({ t: 1705985113, i: 5 }),
    signature: {
      hash: Binary.createFromBase64('AAAAAAAAAAAAAAAAAAAAAAAAAAA=', 0),
      keyId: Long('0')
    }
  },
  operationTime: Timestamp({ t: 1705985113, i: 5 })
}
```