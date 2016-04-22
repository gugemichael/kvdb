# KVDB
key value based database with Golang language


##  Introduce

**KVDB** is key value store has `persistent` database engine and supply `cluster` feature. KVDB consist of one BucketServer and many KVDB instance node . BucketServer manage keys hashed location and KVDB instance node  alive or meta information just like a cluster router. and role  as master of the cluster. KVDB instance node s store datas' in its storage engine like Redis or Memcached in memory write(set) and query(get) and write with ahead log (WAL log), KVDB has high performance with multi-threads(benefit from **Go routines**). you can using KVDB cluster just as one single big memory instance node . 

- **Key value data struct based** 
- **Data persistence with WAL log** 
- **Cluster with BucketServer and KVDB instance node** 

## Architecture

![arch](http://img.blog.csdn.net/20160422121013289)


##  Key value command

- key max length is 250 (defined by MAX_KEY_LENGTH) 
- value max length is 64MB (defined by MAX_ITEM_LENGTH) 

| command   | usage    | description |
| :-------- | :--------| :-- |
| set  | set mykey 0 0 3 |  save one key   |
| mset | mset mykey1 0 0 3 mykey2 0 0 5  |  save multi keys  |
| cas  | cas mykey 0 0 3 |  compare adn set one key   |
| get  | get mykey | read one key |
| mget | mget mykey1 mykey2 | read multi keys |
| add  | add mykey 0 0 3 | save one key if not exist|
| replace | replace mykey 0 0 3 | replace value of exist key|
| append  | append mykey 0 0 1 | append value of exist key |
| prepend | prepend mykey 0 0 1 | prepend value of exist key |
| incr | incr mykey 1 | incr numerical key |
| decr | decr mykey 1 | decr numerical key |
| delete | delete mykey | delete exist key |
| flush_all | flush_all | delete all items |
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

## Memory

- **memory pool use slab chunk**
- **only for values store without keys**



## Storage

#### WAL log

- **disk operation write() with append only**
- **periodic make check point of WAL log. could reduce recovery overhead**
- **flush policy configable :**
	- flush request keys before respond to client (every request)
	- flush accumulated keys every second
	- flush accumulated period dirty keys that time has passed MAX_DIRTY_TIME
	- flush accumulated period dirty keys over MAX_DIRTY_KEYS
	- flush synchronic every key on memory usage ratio has over MAX_DIRTY_RATIO

#### recovery

- **only doing recover when server restart**
- **there has a switch of servicing for client in recover processing or not**
- **replay commands in WAL log after checkpoint** 
