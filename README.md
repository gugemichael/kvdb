# Design of KVDB

##  Introduce

**KVDB** is key value store has `persistent` database engine and supply `cluster` feature. KVDB consist of one BucketServer and many KVDB instance node . BucketServer manage keys hashed location and KVDB instance node  alive or meta information just like a cluster router. and role  as master of the cluster. KVDB instance node s store datas' in its storage engine like Redis or Memcached in memory write(set) and query(get) and write with ahead log (WAL log), KVDB has high performance with multi-threads(benefit from **Go routines**). you can using KVDB cluster just as one single big memory instance node . 

- **Key value data struct based** 
- **Data persistence with WAL log** 
- **Cluster with BucketServer and KVDB instance node  ** 

## Architecture

![这里写图片描述](http://img.blog.csdn.net/20160531184212947)


##  Key value command

- key max length is 250 (defined by MAX_KEY_LENGTH) 
	- value max length is 8MB (defined by MAX_ITEM_LENGTH) 

#### kvdb node commands for client
	| command   | usage    | description |
	| :-------- | :--------| :-- |
	| set  | set key value |  save one key   |
	| setex | set key 30 value | save one key with expire time |
	| setnx | set key value | save one key only if it doesn’t exist |
	| mset | set key1 value1 key2 value2 |  save multi keys  |
	| cas  | cas key old_value new_value |  compare and set one key   |
	| get  | get key | read one key |
	| mget | mget key1 key2 | read multi keys |
	| exists | exists key1 key2 | check if the key exist |
	| persist | persist key | disable expire on specified key |
	| expire | expire key 30 | set expire time in seconds |
	| pexpire | pexpire key 30000 | set expire time in milliseconds |
	| ttl | ttl key | get expire time in seconds from key |
	| pttl | pttl key | get expire time in milliseconds from key |
	| randomkey | randomkey | randomly return one key |
	| append  | append mykey abcdefg | append value of exist key |
	| prepend | prepend mykey abcdefg | prepend value of exist key |
	| incr | incr mykey | incr numerical key |
	| incrby | incrby mykey 1 | incr numerical key by number |
	| decr | decr mykey | decr numerical key |
	| decrby | decrby mykey 1 | decr numerical key by number |
	| getset | getset key value | get and set key new value |
	| del | del key | delete exist key |


#### kvdb node commands for internal
	| command   | usage    | description |
	| :-------- | :--------| :------- |
	| save | save | flush all dirty keys to disk that all in memory |
	| bgrewrite | bgrewrite | rewrite WAL log (redolog) in background |
	| flushall | flushall | delete all items |
	| stats | stats | prints server statistics |
	| version | version | prints server version |
	| ping | ping | return pong |
	| error | error | return last error of current session |

## BucketServer

	- **data value location**
	every key is hashing to its owner KVDB instance node . A single key only and only if belongs to single KVDB node exactly.
	- **virtual bucket**
	RangServer divide all hash into virtual bucket slots called `vbucket`.

	> slot = hash(key) % vbucket.size()
	> kvdb_node  = vbucket[slot].KVDB 
	> value = kvdb_node .get(key)

	- **vbuckets rebalance with node failure or new node joined**
	![Alt text](http://img.blog.csdn.net/20160422163252118)

	- **more detail of vbuckets algorithm please read https://github.com/gugemichael/kvdb/blob/master/tools/vbuckets.py**


## Memory

	- **memory pool use slab chunk**
	- **only for values store without keys**


## Storage engine


#### WAL log

	- **disk operation write() with append only**
	- **periodic make rewriting of WAL log. could reduce recovery overhead**
	- **flush policy configable :**
		- flush request keys before respond to client (every request)
		- flush accumulated keys every second
			- flush accumulated period dirty keys that time has passed MAX_DIRTY_TIME
				- flush accumulated period dirty keys over MAX_DIRTY_KEYS
					- flush synchronic every key on memory usage ratio has over MAX_DIRTY_RATIO

#### recovery

					- **only doing recover when server restart**
					- **there has a switch of servicing for client in recover processing or not**
					- **replay commands in WAL ** 


## Logging

#### Slow log

