TOPIC = dict(slug="13-webservers-databases", title="Web Servers, Databases & Messaging", intro="Production apps ke saath yeh components hamesha hote hain: Nginx, DB, cache, queue. DevOps engineer ko inhe deploy, tune aur troubleshoot karna aana chahiye.", subs=[

dict(slug="nginx", title="Nginx: Web Server & Reverse Proxy", level="Basic",
intro="Nginx static files serve karta hai, reverse proxy/load balancer aur SSL terminator ka kaam karta hai. Event-driven, bahut fast.",
diagram="""
Client -> Nginx :443 (TLS, gzip, rate limit, cache)
            ├── /        -> static /var/www/html
            ├── /api     -> upstream node app :3000
            └── /ws      -> websocket upstream
""",
install="""sudo apt install nginx -y
sudo systemctl enable --now nginx
nginx -t && sudo systemctl reload nginx     # ALWAYS test before reload""",
examples=[("Reverse proxy + SSL + gzip + rate limit","""limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
server {
    listen 443 ssl http2;
    server_name app.example.com;
    ssl_certificate     /etc/letsencrypt/live/app.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/app.example.com/privkey.pem;
    gzip on; gzip_types text/css application/json application/javascript;

    location / { root /var/www/html; try_files $uri /index.html; }   # SPA
    location /api/ {
        limit_req zone=api burst=20 nodelay;
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    location /ws/ {
        proxy_pass http://127.0.0.1:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
server { listen 80; server_name app.example.com; return 301 https://$host$request_uri; }"""),
("Debug","""sudo tail -f /var/log/nginx/error.log
curl -I localhost; nginx -T | less     # dump effective config""")],
problems=[("502 Bad Gateway","Upstream down/wrong port/socket permission","Check app status, `proxy_pass`, error.log."),
("413 Request Entity Too Large","Default body limit 1MB","`client_max_body_size 20m;`"),
("WebSocket disconnects","Missing Upgrade headers / proxy_read_timeout","Add upgrade headers, raise timeout.")],
qa=[("Nginx vs Apache?","Nginx event-driven, lower memory, great as proxy; Apache process/thread, .htaccess flexibility."),
("Forward vs reverse proxy?","Reverse proxy sits in front of servers."),
("What is `try_files`?","Try files in order then fallback (used for SPAs)."),
("How does nginx handle load?","Master + worker processes with epoll event loop."),
("Nginx load-balancing methods?","round robin, least_conn, ip_hash, weighted.")]),

dict(slug="sql-databases", title="Relational Databases (PostgreSQL/MySQL) Operations", level="Intermediate",
intro="DevOps ko DB admin nahi banna, par backup, restore, replication, connection pooling, slow query basics aani chahiye.",
diagram="""
App -> pgbouncer (pool) -> Primary (RW) --streaming replication--> Replica (RO)
Backups: nightly pg_dump / continuous WAL archive -> S3 (PITR)
""",
install="""docker run -d --name pg -e POSTGRES_PASSWORD=secret -p 5432:5432 -v pgdata:/var/lib/postgresql/data postgres:16
docker exec -it pg psql -U postgres""",
examples=[("Backup & restore","""pg_dump -h host -U app -Fc appdb > appdb.dump
pg_restore -h host -U app -d appdb_new --clean appdb.dump
# MySQL: mysqldump --single-transaction db > db.sql"""),
("Find slow queries and missing index","""SELECT query, calls, mean_exec_time FROM pg_stat_statements ORDER BY mean_exec_time DESC LIMIT 5;
EXPLAIN ANALYZE SELECT * FROM orders WHERE user_id = 42;
CREATE INDEX CONCURRENTLY idx_orders_user ON orders(user_id);"""),
("Connections","""SELECT count(*), state FROM pg_stat_activity GROUP BY state;
SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE state='idle in transaction' AND now()-state_change > interval '10 min';""")],
problems=[("'too many connections'","Each app pod opens many connections","Use pgbouncer/RDS Proxy, tune pool size."),
("Disk full on DB","WAL/logs/bloat growth","Monitor, archive WAL, VACUUM, increase storage (alert at 80%)."),
("Restore never tested and failed when needed","Untested backups","Schedule automated restore drills.")],
qa=[("ACID?","Atomicity, Consistency, Isolation, Durability."),
("Index trade-off?","Faster reads, slower writes and extra storage."),
("Replication types?","Sync vs async; physical streaming vs logical."),
("RPO/RTO?","Recovery point (data loss tolerance) and recovery time objective."),
("What is PITR?","Restore to any moment using base backup + WAL archives.")]),

dict(slug="redis-cache", title="Redis & Caching", level="Intermediate",
intro="In-memory key-value store: cache, sessions, rate limits, queues. Latency kam aur DB load kam.",
diagram="""
App -> Redis (hit? return) ; miss -> DB -> store in Redis with TTL (cache-aside)
HA: Primary + replicas + Sentinel (failover) | Cluster (sharding)
""",
install="docker run -d --name redis -p 6379:6379 redis:7\ndocker exec -it redis redis-cli",
examples=[("Basics","""SET user:1 '{"name":"a"}' EX 300
GET user:1; TTL user:1
INCR rate:ip:1.2.3.4; EXPIRE rate:ip:1.2.3.4 60
LPUSH queue job1; BRPOP queue 0
INFO memory; MONITOR   # careful in prod"""),
("Eviction config","""maxmemory 2gb
maxmemory-policy allkeys-lru
appendonly yes""")],
problems=[("Cache stampede when key expires","Many requests hit DB together","Jitter TTLs, locking/request coalescing, stale-while-revalidate."),
("Redis OOM","No maxmemory/eviction","Set maxmemory + policy, monitor `used_memory`.")],
qa=[("Redis persistence options?","RDB snapshots and AOF log; can combine."),
("Cache-aside vs write-through?","Cache-aside app loads on miss; write-through writes to cache and DB together."),
("Sentinel vs Cluster?","Sentinel = HA failover; Cluster = sharding + HA."),
("Why is Redis fast?","In-memory, single-threaded event loop, efficient data structures."),
("Common use cases?","Cache, session store, rate limiting, leaderboards, pub/sub, queues.")]),

dict(slug="messaging-kafka", title="Message Queues: RabbitMQ, SQS & Kafka", level="Advanced",
intro="Services ko decouple karne ke liye async messaging. Queue = task distribution; Kafka = distributed log/event streaming.",
diagram="""
Producer -> Kafka topic (partitions 0..n) -> Consumer group (each partition to one consumer)
Retention by time/size; consumers track offsets. Replication factor 3 for durability.
Queue (SQS/RabbitMQ): message consumed once then removed.
""",
install="""# Kafka (KRaft) via docker
docker run -d --name kafka -p 9092:9092 apache/kafka:latest
docker exec -it kafka /opt/kafka/bin/kafka-topics.sh --create --topic orders --bootstrap-server localhost:9092 --partitions 3""",
examples=[("Produce/consume","""docker exec -it kafka /opt/kafka/bin/kafka-console-producer.sh --topic orders --bootstrap-server localhost:9092
docker exec -it kafka /opt/kafka/bin/kafka-console-consumer.sh --topic orders --from-beginning --bootstrap-server localhost:9092
kafka-consumer-groups.sh --describe --group billing --bootstrap-server localhost:9092   # LAG"""),
("Dead letter queue idea","""main queue --(fail x3)--> DLQ -> alert + manual/automatic replay""")],
problems=[("Consumer lag keeps growing","Slow consumers / too few partitions","Scale consumers up to partition count, optimize processing, increase partitions."),
("Duplicate processing","At-least-once delivery","Make consumers idempotent (dedupe key).")],
qa=[("Kafka vs RabbitMQ?","Kafka: log, high throughput, replay, streaming. RabbitMQ: smart broker, routing, per-message ack."),
("What is a consumer group?","Consumers sharing partitions of a topic for parallelism."),
("At-most/at-least/exactly-once?","Delivery guarantees; exactly-once needs idempotence/transactions."),
("What is a DLQ?","Queue for messages that repeatedly fail."),
("Why partitions?","Parallelism and ordering per key.")]),
])
