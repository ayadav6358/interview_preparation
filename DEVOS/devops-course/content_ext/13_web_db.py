EXT = dict(
guide=dict(
bigpicture=dict(
problem="""**Problem it solves:** An application alone is not a production system. It needs a fast front door (web server / reverse proxy), durable storage (database), a way to avoid hitting the database for every request (cache) and a way to handle slow or bursty work without blocking users (message queues). DevOps engineers deploy, tune, secure and troubleshoot all of these.""",
chain=["PROBLEM: one app process cannot serve traffic, store data safely and stay fast under load",
       "TRADITIONAL APPROACH: app talks directly to users and to a single database for everything",
       "PAIN: slow pages, database overload, lost data, tight coupling, downtime on spikes",
       "TECHNOLOGY: Nginx (proxy), PostgreSQL/MySQL (data), Redis (cache), RabbitMQ/SQS/Kafka (queues)",
       "SOLUTION: specialised components each doing one job well, connected by clear interfaces",
       "REAL-WORLD BENEFIT: scalability, resilience, faster responses, decoupled services"],
text="""Typical request: **Nginx** terminates TLS and routes; the **app** reads from **Redis** first (cache hit = fast), otherwise queries the **database** and stores the result in Redis; slow tasks (emails, reports) are put on a **queue** and processed by **workers**."""),
e2e=dict(diagram="""Client
  v
Nginx (TLS, gzip, rate limit, static files, reverse proxy)  :443
  v
App servers (stateless, 2+ instances)  :3000
  |-- read --> Redis (cache/session)  :6379  -- miss --> PostgreSQL primary :5432 (+ read replicas)
  |-- publish job --> Queue (RabbitMQ/SQS/Kafka)  --> Workers --> DB / email / third-party
  v
Response to client
Ops: backups (pg_dump/WAL), replication, monitoring (exporters), logs, failover""",
text="""Nginx is the entry point: it terminates **TLS**, serves static files, compresses and forwards dynamic requests to app servers (**reverse proxy** and load balancer). The app checks **Redis** for the data; a **cache miss** falls through to the **database**, and the result is stored in Redis with a **TTL** for next time. The database keeps the authoritative data with a **primary** (writes) and optional **replicas** (reads, failover). Work that does not need to finish before responding is published as a **message** to a queue; **workers** consume and process it asynchronously, enabling retries and smoothing spikes. Each component is monitored and backed up."""),
tools=dict(rows=[
["Nginx / HAProxy", "Reverse proxy, TLS, load balancing", "HTTP(S) requests", "Upstream requests/static files", "Edge"],
["PostgreSQL / MySQL", "Relational storage (ACID)", "SQL", "Rows/transactions", "Data tier"],
["pgBouncer / ProxySQL", "Connection pooling", "Many client connections", "Few DB connections", "Between app and DB"],
["Redis / Memcached", "In-memory cache, sessions, counters", "Key/value", "Fast reads", "Between app and DB"],
["RabbitMQ / SQS", "Task queue (work distribution)", "Messages", "Delivered jobs", "Async work"],
["Kafka", "Distributed event log/streaming", "Events", "Replayable ordered streams", "Event-driven systems"],
["pg_dump / pgBackRest / mysqldump / xtrabackup", "Backup", "Database", "Backup files/WAL", "DR"],
["postgres_exporter / redis_exporter / nginx-exporter", "Metrics", "Service stats", "Prometheus metrics", "Monitoring"]],
why="**Redis vs Memcached:** Redis supports data structures, persistence and replication; Memcached is simple multi-threaded caching. **RabbitMQ vs Kafka:** RabbitMQ is a smart broker for task queues and routing; Kafka is a durable distributed log for high-throughput event streaming and replay. **SQS vs RabbitMQ:** SQS is fully managed and simple; RabbitMQ gives richer routing and protocols but needs operation. **Postgres vs MySQL:** both solid; Postgres has advanced features (JSONB, extensions), MySQL is widely used and simple to operate."),
compare=[
("Nginx vs Apache vs HAProxy", ["Topic", "Nginx", "Apache", "HAProxy"], [["Model", "Event-driven", "Process/thread (also event MPM)", "Event-driven"], ["Best for", "Reverse proxy, static, TLS", ".htaccess, legacy modules", "L4/L7 load balancing"]]),
("SQL vs NoSQL", ["Topic", "SQL (PostgreSQL)", "NoSQL (DynamoDB/MongoDB)"], [["Schema", "Fixed, relational", "Flexible"], ["Transactions", "Strong ACID", "Varies"], ["Scale", "Vertical + replicas", "Horizontal by design"]]),
("Replication vs Backup", ["Topic", "Replication", "Backup"], [["Protects from", "Server failure", "Data corruption/deletion/human error"], ["Time", "Near real-time copy", "Point-in-time snapshot"], ["Note", "Replicates mistakes too", "Needed even with replicas"]]),
("Cache strategies", ["Strategy", "How", "Trade-off"], [["Cache-aside (lazy)", "App reads cache, on miss loads DB and fills cache", "Simple; possible stale data"], ["Write-through", "Write to cache and DB together", "Consistent; slower writes"], ["Write-back", "Write to cache, flush later", "Fast; risk of loss"]]),
("Queue vs Topic (pub/sub)", ["Topic", "Queue", "Topic/Log"], [["Delivery", "Each message to one consumer", "Each subscriber gets a copy"], ["Example", "Task processing", "Order events to billing and analytics"]]),
("Isolation levels", ["Level", "Prevents"], [["Read committed", "Dirty reads"], ["Repeatable read", "Non-repeatable reads"], ["Serializable", "Phantoms (strongest, slowest)"]])],
troubleshooting=[
("502 Bad Gateway from Nginx", "Upstream app down/slow, wrong upstream address/port, socket permissions", "`tail /var/log/nginx/error.log`, `curl` upstream directly, `ss -tulpn`", "Fix/restart app, correct `proxy_pass`, tune timeouts.", "Health checks, `nginx -t` in CI."),
("Database `too many connections`", "Connection leaks, no pooling, low max_connections", "`SELECT count(*) FROM pg_stat_activity;`, app pool config", "Use pgBouncer, fix leaks, adjust pool sizes.", "Pooling by default; alert at 80% of max."),
("Slow queries", "Missing index, full table scan, bad plan, lock contention", "`EXPLAIN (ANALYZE, BUFFERS)`, `pg_stat_statements`, slow query log", "Add index, rewrite query, vacuum/analyze, cache result.", "Query review and performance tests."),
("Replica lag / stale reads", "Heavy writes, network, long-running queries on replica", "`pg_stat_replication`, `SHOW REPLICA STATUS`", "Reduce load, tune replication, route critical reads to primary.", "Monitor lag with alert."),
("Redis memory full / evictions", "No TTL, big keys, wrong maxmemory-policy", "`INFO memory`, `redis-cli --bigkeys`, `INFO stats` evicted_keys", "Set TTLs, choose `allkeys-lru`, increase memory, fix big keys.", "Key naming/TTL standards; memory alerts."),
("Queue backlog grows", "Consumers slow/down, poison message, burst", "Queue depth metrics, consumer logs, DLQ", "Scale consumers, fix failing job, move bad message to DLQ.", "Autoscale on queue depth; DLQ + alerts.")],
practices={
"Development": ["Use connection pooling and timeouts; parameterised queries; idempotent consumers; migrations via Flyway/Liquibase."],
"Production": ["Nginx: `worker_processes auto`, keep-alive, gzip, rate limiting; DB: primary + replica, automated failover; Redis: persistence/replication chosen per use; queue: DLQ and retries."],
"Security": ["TLS everywhere; DB not public; least-privilege DB users; secrets in vault; Redis `requirepass`/ACLs and no public exposure; Nginx hides version, security headers."],
"Performance": ["Index wisely; cache hot reads; connection pooling; tune `shared_buffers`, `work_mem`; use read replicas; HTTP caching/CDN."],
"Reliability": ["Backups tested with restore drills; replication + failover; queue durability; graceful shutdown of workers."],
"Cost Optimization": ["Right-size DB instances; cache to reduce DB load; archive old data; managed services trade-off."],
"Monitoring & Logging": ["Exporters for each component; slow query log; Nginx access/error logs; queue depth and consumer lag."],
"Backup & Disaster Recovery": ["PostgreSQL: base backups + WAL archiving (PITR); MySQL: binlog + xtrabackup; cross-region copies; defined RPO/RTO."]},
mistakes={
"Beginner mistakes": ["Exposing DB/Redis ports publicly.", "Using default passwords."],
"Developer mistakes": ["N+1 queries.", "No timeouts.", "Caching without invalidation strategy."],
"DevOps mistakes": ["Replication treated as backup.", "No restore tests.", "Editing Nginx config without `nginx -t`."],
"Production mistakes": ["No connection pooling.", "Unbounded queues without DLQ.", "Running Redis without maxmemory policy."],
"Security mistakes": ["Wide-open `0.0.0.0/0` database security groups.", "Superuser DB account used by the app."]},
versions=[
"Nginx open source vs Nginx Plus features differ; Ingress-NGINX (Kubernetes) uses different annotations than plain Nginx config.",
"PostgreSQL major versions require pg_upgrade/dump-restore; `recovery.conf` was removed in v12 (use `standby.signal`); check docs for your version.",
"MySQL 8 changed default auth plugin (`caching_sha2_password`) which can break old clients.",
"Redis licence changed in 2024 (Valkey is a community fork): verify which distribution/version you deploy.",
"Kafka no longer requires ZooKeeper with KRaft mode in recent versions."],
hinglish="""**Nginx** front door hai: TLS, static files aur **reverse proxy**. **Database** permanent data rakhta hai; **replica** availability/read scaling deta hai par **backup ka replacement nahi**. **Redis** memory mein cache karta hai isliye fast hai; **TTL** zaroor lagao. **Queue** slow kaam ko background mein bhejti hai (email, report) taaki user ko wait na karna pade. **Connection pooling** aur **indexes** performance ke liye sabse important hain.""",
mnemonics=[("ACID", "Atomicity, Consistency, Isolation, Durability"), ("CAP", "Consistency, Availability, Partition tolerance: pick 2 when the network partitions"), ("Cache-aside", "Read cache > miss > read DB > fill cache"), ("Backup rule", "3-2-1: 3 copies, 2 media, 1 offsite"), ("Queue safety", "Retries + DLQ + idempotent consumers")],
client=dict(
s30="""Behind every application there are a few key building blocks: a web server that receives traffic, a database that stores data, a cache that makes it fast, and queues that handle background work. We deploy and operate these so the application stays fast, safe and available.""",
m2="""Our web layer uses Nginx to handle secure connections and distribute requests across application servers. Business data lives in a managed relational database with replicas for availability and automated backups so we can restore to any point in time. Frequently used data is cached in Redis, which reduces database load and response times. Long-running or bursty tasks, such as sending emails or generating reports, are placed on a message queue and processed in the background so users are never kept waiting. Each component is monitored, secured and sized for your traffic, and we regularly test restores and failover.""",
m5="""I will walk through the request path and the operations behind it. **Edge:** Nginx terminates TLS, serves static content, applies rate limits and proxies to stateless application instances. **Data:** PostgreSQL holds the source of truth, with a primary and replicas, connection pooling, indexing and query monitoring; backups use base snapshots plus write-ahead-log archiving for point-in-time recovery, and we rehearse restores. **Speed:** Redis caches hot reads and sessions using a cache-aside pattern with TTLs and an eviction policy. **Decoupling:** queues like SQS or RabbitMQ absorb spikes and enable retries with dead-letter queues, while Kafka is used where event streaming and replay are needed. **Operations:** metrics exporters, dashboards and alerts for latency, connections, replication lag and queue depth, plus security hardening and least-privilege access. This yields predictable performance, resilience to failures and clear recovery targets."""),
roadmap=[
("Beginner", ["How a web server works", "Basic SQL (SELECT/INSERT/JOIN)", "What is a cache and a queue", "Install Nginx/Postgres/Redis"]),
("Intermediate", ["Nginx reverse proxy/TLS/load balancing", "Indexes, EXPLAIN, transactions", "Redis data types and TTL", "RabbitMQ/SQS basics"]),
("Advanced", ["Replication, PITR, failover", "Connection pooling, tuning", "Cache patterns and invalidation", "Kafka partitions, consumer groups"]),
("Production", ["Backups and restore drills", "Monitoring with exporters", "Security hardening", "Capacity planning"]),
("Interview", ["Design cache + DB read path", "Explain replication vs backup", "Debug slow query", "Queue vs Kafka"])],
miniproject=dict(title="Nginx + Node API + PostgreSQL + Redis + worker queue (Compose)",
arch="""Browser --> Nginx :80 --> API :3000 --> Redis (cache) / PostgreSQL (data)
                                 |-- enqueue job --> Redis list/BullMQ or RabbitMQ --> Worker --> PostgreSQL
Volumes: pgdata ; healthchecks ; backup job (pg_dump) ; Prometheus exporters optional""",
steps=[
("Step 1: compose.yml", """services:
  nginx:
    image: nginx:1.27
    ports: ["80:80"]
    volumes: ["./nginx.conf:/etc/nginx/conf.d/default.conf:ro"]
    depends_on: [api]
  api:
    build: ./api
    environment: { DB_URL: "postgres://app:${DB_PASSWORD}@db:5432/app", REDIS_URL: "redis://cache:6379" }
    depends_on: { db: { condition: service_healthy } }
  worker:
    build: ./api
    command: ["node","worker.js"]
    environment: { DB_URL: "postgres://app:${DB_PASSWORD}@db:5432/app", REDIS_URL: "redis://cache:6379" }
    depends_on: { db: { condition: service_healthy } }
  db:
    image: postgres:16
    environment: { POSTGRES_USER: app, POSTGRES_PASSWORD: "${DB_PASSWORD}", POSTGRES_DB: app }
    volumes: [pgdata:/var/lib/postgresql/data]
    healthcheck: { test: ["CMD-SHELL","pg_isready -U app"], interval: 5s, retries: 10 }
  cache:
    image: redis:7-alpine
    command: ["redis-server","--maxmemory","128mb","--maxmemory-policy","allkeys-lru"]
volumes: { pgdata: {} }""", "The worker reuses the API image with a different command. Redis has a memory cap and LRU eviction so it behaves as a cache. Only Nginx publishes a port; DB and Redis stay internal."),
("Step 2: nginx.conf", """upstream api { server api:3000; keepalive 16; }
server {
  listen 80;
  gzip on;
  location /api/ { proxy_pass http://api; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; proxy_read_timeout 30s; }
  location / { root /usr/share/nginx/html; try_files $uri /index.html; }
}""", "`upstream` names the backend pool with keep-alive connections; `proxy_pass` forwards API calls; static files are served directly and single-page-app routes fall back to index.html. Validate with `nginx -t` before reload."),
("Step 3: Cache-aside in code (Node, illustrative)", """async function getUser(id) {
  const key = `user:${id}`;
  const cached = await redis.get(key);
  if (cached) return JSON.parse(cached);
  const { rows } = await pg.query('SELECT id, name FROM users WHERE id = $1', [id]);
  await redis.set(key, JSON.stringify(rows[0]), { EX: 60 });
  return rows[0];
}""", "Check cache first; on miss query with a **parameterised** query (prevents SQL injection) and store with a 60 second TTL. Invalidate or update the key when the user changes."),
("Step 4: Backup and restore drill", """docker compose exec -T db pg_dump -U app -Fc app > backup.dump
docker compose exec -T db psql -U app -c "CREATE DATABASE restore_test;"
docker compose exec -T db pg_restore -U app -d restore_test < backup.dump
docker compose exec db psql -U app -d restore_test -c "\\dt"
""", "A backup only counts once a restore is proven. This dumps in custom format, restores into a new database and lists tables. Production should use base backups + WAL archiving for point-in-time recovery.")]),
interview=[
("Beginner", "What is a web server?", "Software that serves HTTP requests: static files and proxying to applications.", "Basics.", "Nginx serving a React build."),
("Beginner", "What is a reverse proxy?", "A server in front of backends that forwards client requests, adding TLS, caching and load balancing.", "Architecture.", "Nginx in front of Node."),
("Beginner", "What is a database?", "Organised storage for persistent data with query capability.", "Basics.", "PostgreSQL."),
("Beginner", "SQL vs NoSQL?", "SQL is relational with a fixed schema and ACID transactions; NoSQL offers flexible models and horizontal scale.", "Selection.", "Orders in SQL, sessions in Redis."),
("Beginner", "What is caching?", "Storing frequently used data in fast storage to reduce latency and backend load.", "Performance.", "Redis."),
("Beginner", "What is a message queue?", "A buffer that decouples producers and consumers so work can be processed asynchronously.", "Decoupling.", "Email sending."),
("Beginner", "What is an index?", "A data structure that speeds up lookups on columns at the cost of extra writes/storage.", "DB performance.", "Index on email."),
("Beginner", "What is a primary key?", "A unique, non-null identifier for each row.", "Relational basics.", "id column."),
("Beginner", "What is a backup?", "A copy of data used to restore after loss or corruption.", "Reliability.", "Nightly pg_dump."),
("Beginner", "What is Redis?", "An in-memory data store used for cache, sessions, queues and counters.", "Common tool.", "Session storage."),
("Intermediate", "How does Nginx handle many connections?", "Event-driven, asynchronous worker processes using epoll; each worker handles thousands of connections without a thread per connection.", "Nginx internals.", "`worker_processes auto`."),
("Intermediate", "Nginx location matching order?", "Exact `=`, then longest prefix with `^~`, then regex in order, then longest prefix.", "Config correctness.", "`location /api/`."),
("Intermediate", "What is ACID?", "Atomicity, Consistency, Isolation, Durability guarantees of transactions.", "DB fundamentals.", "Money transfer."),
("Intermediate", "Explain indexes and when they hurt.", "B-tree indexes speed reads; each write must update indexes; too many indexes slow writes and use space; low-selectivity columns help little.", "Tuning.", "Index on boolean is rarely useful."),
("Intermediate", "How do you find a slow query?", "Slow query log/pg_stat_statements, then `EXPLAIN (ANALYZE)` to see plan; fix with index/rewrite.", "Troubleshooting.", "Seq scan on 10M rows."),
("Intermediate", "Replication types?", "Asynchronous (fast, possible lag/loss), synchronous (no loss, higher latency); physical (WAL) vs logical.", "HA.", "Postgres streaming replication."),
("Intermediate", "Why connection pooling?", "Database connections are expensive; pooling reuses a limited number, preventing exhaustion.", "Scaling.", "pgBouncer in transaction mode."),
("Intermediate", "Redis persistence options?", "RDB snapshots and AOF append-only log; combine for durability trade-offs; cache-only may disable both.", "Redis ops.", "AOF everysec."),
("Intermediate", "Redis eviction policies?", "noeviction, allkeys-lru, volatile-lru, allkeys-lfu, etc. when maxmemory reached.", "Memory management.", "allkeys-lru for cache."),
("Intermediate", "Cache invalidation strategies?", "TTL, explicit delete/update on write, versioned keys, write-through.", "Hard problem.", "Delete key after user update."),
("Intermediate", "RabbitMQ concepts?", "Producers publish to exchanges, routed by bindings to queues; consumers ack messages; DLQ for failures.", "Messaging.", "Direct/topic/fanout exchanges."),
("Intermediate", "SQS Standard vs FIFO?", "Standard: at-least-once, best-effort ordering, high throughput; FIFO: exactly-once processing and ordering with lower throughput.", "AWS messaging.", "Order processing in FIFO."),
("Intermediate", "Kafka basics?", "Topics split into partitions on brokers; producers append; consumer groups read with offsets; retention allows replay.", "Streaming.", "Clickstream events."),
("Intermediate", "How to secure Nginx?", "TLS 1.2+, hide version, security headers, rate limiting, restrict methods, keep updated, run as non-root worker, WAF/ModSecurity if needed.", "Hardening.", "`server_tokens off`."),
("Intermediate", "HTTP caching headers?", "Cache-Control, ETag, Expires; Nginx `proxy_cache` for upstream responses.", "Performance.", "Cache static for 1 year with hashed filenames."),
("Advanced", "Explain PostgreSQL MVCC and VACUUM.", "MVCC keeps row versions so readers do not block writers; VACUUM reclaims dead tuples and prevents bloat/transaction wraparound; autovacuum needs tuning.", "Postgres internals.", "Bloated table slowing queries."),
("Advanced", "Design point-in-time recovery for PostgreSQL.", "Periodic base backups + continuous WAL archiving to object storage; restore base then replay WAL to a target time; test regularly (pgBackRest/WAL-G).", "DR design.", "Recover to 10 min before a bad deploy."),
("Advanced", "How does automatic failover work?", "A manager (Patroni, RDS, orchestrator) detects primary failure via health checks/consensus, promotes a replica, and repoints clients via VIP/DNS/proxy; fencing prevents split-brain.", "HA.", "Patroni + etcd."),
("Advanced", "CAP theorem and practical meaning?", "During a network partition a system must choose consistency or availability; many systems tune per operation.", "Distributed systems.", "DynamoDB eventual vs strong reads."),
("Advanced", "Transaction isolation anomalies?", "Dirty read, non-repeatable read, phantom read, write skew; isolation levels trade correctness for performance.", "DB depth.", "Serializable for financial invariants."),
("Advanced", "Scaling databases?", "Vertical scale, read replicas, caching, partitioning/sharding, CQRS, choose appropriate storage per workload.", "Scale design.", "Shard by tenant ID."),
("Advanced", "Cache stampede and mitigations?", "Many requests rebuild an expired hot key simultaneously; use request coalescing/locks, jittered TTLs, stale-while-revalidate, pre-warming.", "Reliability.", "Homepage key expiry."),
("Advanced", "Kafka delivery semantics?", "At-most-once, at-least-once, exactly-once (idempotent producers + transactions); consumers commit offsets after processing for at-least-once.", "Messaging guarantees.", "Idempotent consumers."),
("Advanced", "Kafka partitions and ordering?", "Ordering is guaranteed only within a partition; key-based partitioning keeps related events ordered; consumer parallelism is limited by partition count.", "Design detail.", "Key by order ID."),
("Advanced", "How does Redis Cluster/Sentinel differ?", "Sentinel gives HA/failover for a primary+replicas; Cluster shards data across nodes with hash slots.", "Redis scaling.", "Sentinel for small setups."),
("Advanced", "Nginx performance tuning?", "worker_processes auto, worker_connections, keepalive to upstream, gzip/brotli, sendfile, open_file_cache, buffers, HTTP/2, caching, rate limits.", "Tuning.", "Tune on evidence with load tests."),
("Advanced", "Zero-downtime schema changes?", "Expand/contract migrations, online index creation (`CREATE INDEX CONCURRENTLY`), avoid long locks, backfill in batches.", "Ops.", "Add nullable column then backfill."),
("Advanced", "Outbox pattern?", "Write business change and an outbox event in one DB transaction; a relay publishes to the broker, ensuring consistency between DB and messages.", "Reliable messaging.", "Order created event."),
("Advanced", "Managed database vs self-hosted?", "Managed (RDS/Cloud SQL) reduces operations (patching, backups, failover) at higher cost/less control; self-host for special needs and expertise.", "Decision-making.", "Default to managed."),
("Scenario-Based", "Website is slow only during peak.", "Check Nginx/app saturation, DB connections/slow queries, cache hit ratio, queue backlog; add caching, indexes, pooling, scale out.", "Systematic diagnosis.", "Cache hit ratio dropped to 30%."),
("Scenario-Based", "Database disk is filling up.", "Find large tables/WAL/logs/temp files, vacuum/archive, expand storage, retention, alert early.", "Ops.", "Unarchived WAL growing."),
("Scenario-Based", "Accidental DELETE without WHERE in production.", "Stop writes if needed, restore from PITR to just before the mistake into a new instance, extract data and repair, add safeguards (permissions, transactions, reviews).", "Recovery.", "Point-in-time restore."),
("Scenario-Based", "Need to migrate to a bigger DB with minimal downtime.", "Set up replica/logical replication or DMS, sync, switch over quickly, validate, keep rollback.", "Migration.", "Cutover in 30 seconds."),
("Scenario-Based", "Emails must be sent reliably after checkout.", "Publish a message to a queue in the same transaction pattern (outbox), workers with retries, idempotency and DLQ.", "Async design.", "Order confirmation email."),
("Scenario-Based", "Redis outage takes down the site.", "App must degrade gracefully: timeouts, fall back to DB with rate limiting, circuit breaker, Redis HA (Sentinel/managed), avoid using Redis as sole store.", "Resilience.", "Sessions in signed cookies/DB fallback."),
("Scenario-Based", "Design rate limiting.", "Nginx `limit_req` at the edge plus Redis-based token bucket per API key in the app for fine-grained limits.", "Protection.", "100 req/min per key."),
("Scenario-Based", "Queue has millions of messages backlog.", "Scale consumers, check poison messages/DLQ, increase batch/prefetch, fix downstream slowness, temporarily shed low-priority work.", "Recovery.", "Autoscale on queue depth."),
("Scenario-Based", "Choose between RabbitMQ and Kafka.", "Task queues with routing and acknowledgements: RabbitMQ/SQS; high-volume event streams, replay and multiple independent consumers: Kafka.", "Tool selection.", "Payments events on Kafka."),
("Scenario-Based", "Zero-downtime Nginx config change.", "`nginx -t` then `nginx -s reload` (graceful), canary in a staging box, version config in Git.", "Change safety.", "New upstream added."),
("Scenario-Based", "Database credentials rotation.", "Use secret manager with rotation, app fetches secrets and reconnects, dual-user rotation strategy to avoid downtime.", "Security ops.", "RDS rotation Lambda."),
("Scenario-Based", "Read-heavy workload overloads primary.", "Add read replicas and route reads, add caching, optimise queries, materialised views.", "Scaling reads.", "Reporting on replica."),
("Scenario-Based", "How do you keep two services consistent without distributed transactions?", "Event-driven sagas/outbox, idempotent handlers, compensating actions, eventual consistency.", "Microservices data.", "Order/payment saga."),
("Troubleshooting-Based", "Nginx `upstream timed out (110)`.", "Backend too slow/unresponsive; check app/DB latency, increase `proxy_read_timeout` only after fixing root cause.", "Proxy debugging.", "Slow query in API."),
("Troubleshooting-Based", "Nginx `connect() failed (111: Connection refused)`.", "Upstream not listening or wrong host/port; verify with curl/ss.", "Proxy debugging.", "App crashed."),
("Troubleshooting-Based", "PostgreSQL `FATAL: remaining connection slots are reserved`.", "max_connections reached; use pooling, kill idle sessions, raise limits carefully.", "DB capacity.", "Leaked connections."),
("Troubleshooting-Based", "Deadlocks in database.", "Concurrent transactions lock resources in different order; keep transactions short, consistent lock order, retry on deadlock.", "Concurrency.", "Two updates crossing."),
("Troubleshooting-Based", "Replica is far behind.", "Long-running queries, IO, network, heavy write burst; check lag, tune, move heavy reads.", "Replication.", "Analytics query on replica."),
("Troubleshooting-Based", "Redis `OOM command not allowed`.", "maxmemory reached with noeviction; set eviction policy/TTL or raise memory.", "Redis ops.", "Queue in Redis exhausted memory."),
("Troubleshooting-Based", "Messages processed twice.", "At-least-once delivery, ack timeouts or retries; make consumers idempotent (dedupe key).", "Messaging semantics.", "Duplicate charge prevented by idempotency key."),
("Troubleshooting-Based", "Kafka consumer lag increasing.", "Consumers slower than producers; scale consumers (up to partitions), optimise processing, check rebalances/GC.", "Streaming ops.", "Lag alert."),
("Troubleshooting-Based", "TLS error on Nginx after renewal.", "Certificate/chain file wrong, key mismatch, not reloaded; check `nginx -t` and `openssl s_client`.", "TLS.", "Used cert.pem instead of fullchain."),
("Troubleshooting-Based", "Backup restores but app fails.", "Version/extension/role mismatch or missing WAL/config; verify restore procedure and app compatibility in drills.", "DR quality.", "Missing extension.")],
cheatsheet={
"Definitions": ["Reverse proxy; ACID; index; replication vs backup; cache-aside; TTL; queue vs topic; DLQ; idempotency; connection pooling."],
"Commands": ["`nginx -t` `nginx -s reload` `curl -I` `tail -f /var/log/nginx/error.log`", "`psql -U user -d db -c '\\dt'` `EXPLAIN ANALYZE` `pg_dump -Fc` `pg_restore` `SELECT * FROM pg_stat_activity`", "`redis-cli ping|info|monitor|--bigkeys|keys pattern (avoid in prod)|ttl key`", "`rabbitmqctl list_queues` `kafka-topics.sh --describe` `kafka-consumer-groups.sh --describe`"],
"Files": ["/etc/nginx/nginx.conf, conf.d/*.conf; postgresql.conf, pg_hba.conf; redis.conf; rabbitmq.conf"],
"Architecture": ["Client > Nginx > App > Redis/DB; App > Queue > Workers; replicas + backups."],
"Ports": ["HTTP 80, HTTPS 443, PostgreSQL 5432, MySQL 3306, Redis 6379, RabbitMQ 5672 (UI 15672), Kafka 9092, MongoDB 27017, pgBouncer 6432"],
"Differences": ["Nginx vs Apache vs HAProxy; SQL vs NoSQL; replication vs backup; RabbitMQ vs Kafka; Redis vs Memcached."],
"Troubleshooting commands": ["Nginx error log > upstream curl > `ss -tulpn` > DB `pg_stat_activity` > `EXPLAIN` > Redis `INFO` > queue depth/consumer logs"],
"Best practices": ["Private DB/cache, pooling, indexes, TTLs, DLQ, tested restores, monitoring exporters, TLS, least privilege, managed services when possible."]}
),
subs={
"nginx": dict(
define=dict(simple="Nginx is a fast web server that also sits in front of your app to route, secure and balance traffic.",
technical="Nginx is an event-driven, asynchronous HTTP/reverse-proxy server: a master process manages worker processes that multiplex connections; config is declarative (http > server > location).",
why="Efficient TLS termination, static serving and proxying.", without="App servers handle raw internet traffic directly.", use="Edge/reverse proxy for almost every web app.", avoid="Complex app logic in Nginx.", analogy="A receptionist who greets visitors, checks IDs and directs them to the right office."),
internals="""Master reads config and spawns workers (one per CPU). Each worker uses epoll to handle many connections in one loop. For each request Nginx matches a `server` (by `listen`/`server_name`), then a `location`, and either serves a file or proxies to an upstream with keep-alive connections. `nginx -s reload` starts new workers with new config and gracefully retires the old ones.""",
config=[("Production-style server block explained", """server {
    listen 443 ssl http2;
    server_name app.example.com;
    ssl_certificate     /etc/ssl/fullchain.pem;
    ssl_certificate_key /etc/ssl/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    server_tokens off;
    add_header Strict-Transport-Security "max-age=31536000" always;
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;

    location /api/ {
        limit_req zone=api burst=20 nodelay;
        proxy_pass http://api;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}""", [("listen 443 ssl http2", "HTTPS with HTTP/2."), ("ssl_protocols", "Disable old TLS versions."), ("server_tokens off", "Hide version."), ("add_header HSTS", "Force HTTPS in browsers."), ("limit_req_zone/limit_req", "Rate limit per client IP (10 req/s, burst 20). Note: `limit_req_zone` must be in the `http` context in real config."), ("proxy_set_header", "Pass original host/protocol to the app.")])],
commands=[("nginx -t", "Tests the configuration for syntax errors.", "`-T` dumps full config, `-c file`.", "syntax is ok / test is successful", "Reloading without testing.", "Error shows file and line number."),
("nginx -s reload", "Gracefully applies new config.", "`-s stop|quit|reopen`.", "No output.", "Using restart (drops connections).", "If reload fails, old config keeps running; read error log.")],
lab=dict(goal="Serve a site and proxy to an app.", prereq=["Docker"],
steps=[("mkdir site && echo '<h1>hi</h1>' > site/index.html && docker run -d --name web -p 8080:80 -v $PWD/site:/usr/share/nginx/html:ro nginx:1.27", "Serves static file."),
("curl -i localhost:8080", "200 OK with your HTML."),
("docker exec web nginx -t && docker exec web nginx -s reload", "Test and reload config gracefully.")]),
mnemonics=[("Nginx flow", "listen > server_name > location > proxy_pass/root")], hinglish="Nginx config badalne ke baad **pehle `nginx -t`, phir reload**. `restart` se connections tootte hain.",
practices={"Security": ["TLS 1.2+, HSTS, rate limits, hide version."], "Performance": ["gzip, keepalive upstream, caching."]}, mistakes={"DevOps mistakes": ["Reload without test."]},
versions=["`http2` is now set with `http2 on;` in newer Nginx versions (the `listen ... http2` parameter is deprecated): check your version."],
qa_extra=[("Troubleshooting-Based", "Nginx returns 413 on uploads.", "`client_max_body_size` too small (default 1m); raise it for the location/server.", "Common config issue.", "Uploading images.")]),

"sql-databases": dict(
define=dict(simple="A relational database stores data in tables and answers questions with SQL.",
technical="PostgreSQL/MySQL provide ACID transactions, indexes, query planners, replication and backup mechanisms (WAL/binlog); DevOps concerns are availability, performance, security and recoverability.",
why="Durable, consistent source of truth.", without="Data loss and inconsistency.", use="Structured business data.", avoid="Storing large blobs or high-frequency ephemeral data.", analogy="A well-organised filing cabinet with an index."),
internals="""Writes go to the **WAL** (write-ahead log) first for durability, then to memory pages and later to data files. The query planner uses statistics and indexes to choose an execution plan (`EXPLAIN`). Replicas stream WAL from the primary. **PITR** restores a base backup and replays WAL to a chosen time.""",
config=[("Useful PostgreSQL commands explained", """-- see active queries
SELECT pid, state, now()-query_start AS age, query FROM pg_stat_activity WHERE state <> 'idle' ORDER BY age DESC;
-- analyse a slow query
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM orders WHERE user_id = 42;
-- create index without blocking writes
CREATE INDEX CONCURRENTLY idx_orders_user ON orders(user_id);""", [("pg_stat_activity", "Shows running sessions and long queries."), ("EXPLAIN (ANALYZE, BUFFERS)", "Runs the query and shows the real plan/time; look for Seq Scan on big tables."), ("CREATE INDEX CONCURRENTLY", "Builds the index without locking writes (cannot run inside a transaction).")])],
lab=dict(goal="Run Postgres, load data, index and back up.", prereq=["Docker"],
steps=[("docker run -d --name pg -e POSTGRES_PASSWORD=secret -p 5432:5432 postgres:16", "Starts a database."),
("docker exec -it pg psql -U postgres -c 'CREATE TABLE t AS SELECT g AS id, md5(g::text) AS v FROM generate_series(1,500000) g;'", "500k rows."),
("docker exec -it pg psql -U postgres -c \"EXPLAIN ANALYZE SELECT * FROM t WHERE id = 4242;\"", "Seq Scan. Then CREATE INDEX ON t(id); and rerun: Index Scan, much faster."),
("docker exec pg pg_dump -U postgres -Fc postgres > backup.dump", "Logical backup.")]),
mnemonics=[("Backup rule", "3-2-1"), ("Query tuning", "EXPLAIN > index > rewrite > cache")], hinglish="Database mein **index** read fast karta hai. **Replica backup nahi hai**: alag se backup lo aur **restore test** karo.",
practices={"Reliability": ["PITR, tested restores, replication, failover."], "Security": ["Private network, TLS, least-privilege roles."]}, mistakes={"Production mistakes": ["No restore test.", "App uses superuser."]},
versions=["PostgreSQL major upgrades need pg_upgrade or dump/restore; `standby.signal` replaced `recovery.conf` from v12; MySQL 8 default auth plugin change."],
qa_extra=[("Advanced", "Why is `SELECT *` and missing WHERE dangerous in production?", "It reads and transfers unnecessary data and can lock/scan large tables; always select needed columns and limit access with least privilege and safe migration practices.", "Operational hygiene.", "Accidental full table scan during peak.")]),

"redis-cache": dict(
define=dict(simple="Redis keeps data in memory so reads are extremely fast; it is mostly used as a cache.",
technical="Redis is an in-memory data-structure store (strings, hashes, lists, sets, sorted sets, streams) with optional persistence (RDB/AOF), replication, Sentinel HA and Cluster sharding.",
why="Reduce database load and latency.", without="Every request hits the database.", use="Caching, sessions, rate limits, leaderboards, lightweight queues.", avoid="Sole source of truth for critical data.", analogy="A whiteboard next to your desk: fast to read, limited space, may be erased."),
internals="""Single-threaded command execution (I/O threads optional) over data in RAM gives microsecond latency. When memory reaches `maxmemory`, the eviction policy removes keys (or writes are refused with `noeviction`). Persistence: RDB snapshots fork the process; AOF appends every write and is fsynced per policy.""",
config=[("Redis cache configuration explained", """maxmemory 256mb
maxmemory-policy allkeys-lru
appendonly no
requirepass ${REDIS_PASSWORD}
bind 127.0.0.1
protected-mode yes""", [("maxmemory", "Memory cap so Redis cannot consume the whole host."), ("allkeys-lru", "Evict least recently used keys: ideal for a pure cache."), ("appendonly no", "No AOF for a cache (use yes for durability needs)."), ("requirepass", "Set a password: never leave Redis open."), ("bind/protected-mode", "Do not expose Redis to the internet.")])],
commands=[("redis-cli --bigkeys", "Samples keyspace to find the largest keys.", "`INFO memory`, `MEMORY USAGE key`, `TTL key`.", "Biggest key per type.", "Running `KEYS *` in production (blocks).", "Use `SCAN` for iteration.")],
lab=dict(goal="Practise cache-aside with TTL.", prereq=["Docker"],
steps=[("docker run -d --name r -p 6379:6379 redis:7-alpine", "Start Redis."), ("docker exec r redis-cli SET user:1 '{\"name\":\"Asha\"}' EX 30 && docker exec r redis-cli TTL user:1", "Value with a 30-second TTL counting down."), ("docker exec r redis-cli INFO stats | grep -E 'keyspace_hits|keyspace_misses'", "Hit/miss counters: compute hit ratio to judge cache effectiveness.")]),
mnemonics=[("Cache rules", "TTL, maxmemory, eviction policy, no public port")], hinglish="Redis cache mein **TTL** aur **maxmemory policy** zaroor lagao. Production mein **`KEYS *` mat chalao**, `SCAN` use karo.",
practices={"Security": ["Password/ACL, private network, TLS if needed."], "Reliability": ["Sentinel or managed HA; graceful degradation."]}, mistakes={"Production mistakes": ["No eviction policy.", "Public Redis."]},
versions=["Redis licence changed in 2024; Valkey is a compatible fork: confirm which you run and its docs. ACL support requires Redis 6+."],
qa_extra=[("Scenario-Based", "Cache hit ratio is low. What do you check?", "TTL too short, keys with unique parameters, evictions from small memory, cache warm-up, incorrect key design.", "Cache tuning.", "Keys include timestamps.")]),

"messaging-kafka": dict(
define=dict(simple="Message queues let services send work or events to each other without waiting for an immediate answer.",
technical="Brokers provide asynchronous, durable delivery: RabbitMQ/SQS distribute tasks to competing consumers with acknowledgements; Kafka stores an ordered, partitioned, replicated log that many consumer groups can read and replay.",
why="Decouple services, absorb spikes, enable retries.", without="Synchronous chains that fail together.", use="Emails, orders, event streams, ETL.", avoid="Using a queue where a simple function call suffices.", analogy="A post office: senders drop letters, receivers collect when ready."),
internals="""RabbitMQ: producer > exchange > (binding rules) > queue > consumer; message is removed after ack; failures go to a dead-letter queue. SQS: visibility timeout hides a message while processed; not deleted in time means redelivery. Kafka: producer appends to a partition (key decides which); messages persist for a retention period; consumers in a group split partitions and track offsets.""",
config=[("Kafka topic and consumer group commands explained", """kafka-topics.sh --bootstrap-server localhost:9092 --create --topic orders --partitions 3 --replication-factor 1
kafka-console-producer.sh --bootstrap-server localhost:9092 --topic orders
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic orders --group billing --from-beginning
kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group billing""", [("--partitions 3", "Parallelism and ordering unit."), ("--replication-factor", "Copies for fault tolerance (use 3 in production)."), ("--group billing", "Consumers in one group share the work."), ("--describe --group", "Shows LAG per partition (how far behind consumers are).")])],
lab=dict(goal="Send and receive messages with RabbitMQ.", prereq=["Docker"],
steps=[("docker run -d --name rabbit -p 5672:5672 -p 15672:15672 rabbitmq:3-management", "Broker with UI at http://localhost:15672 (default guest/guest: change in real use)."), ("Open the UI > Queues > Add queue 'jobs' > Publish a message", "Message appears in Ready count."), ("Get message with ack", "Queue length decreases: ack removes it.")]),
compare=[("Broker selection", ["Need", "Choose"], [["Simple managed task queue", "SQS"], ["Rich routing, protocols", "RabbitMQ"], ["High-volume events, replay, streaming", "Kafka"], ["Pub/sub fan-out on AWS", "SNS + SQS"]])],
mnemonics=[("Reliable consumers", "Ack, Retry, DLQ, Idempotent")], hinglish="Message **at-least-once** deliver hota hai, isliye **consumer idempotent** banao. Fail hone wale messages **DLQ** mein bhejo. Kafka mein **consumer lag** monitor karo.",
practices={"Reliability": ["DLQ, retries with backoff, idempotency, monitoring lag/depth."], "Security": ["TLS and auth on brokers; least-privilege topics/queues."]}, mistakes={"Developer mistakes": ["Assuming exactly-once delivery.", "Poison messages blocking a queue."]},
versions=["Kafka runs without ZooKeeper (KRaft) in recent versions; CLI tool names/flags vary (`.sh` scripts in Apache distribution). RabbitMQ classic vs quorum queues: quorum queues are recommended for HA."],
qa_extra=[("Scenario-Based", "How do you guarantee an order event is published if the DB commit succeeds?", "Use the outbox pattern: write the event to an outbox table in the same transaction and have a relay publish it, with idempotent consumers.", "Data consistency.", "Avoids dual-write failures.")])
})
