EXT = dict(
guide=dict(
bigpicture=dict(
problem="""**Problem it solves:** Production systems fail in surprising ways. Without visibility you learn about problems from angry customers, and you cannot find the cause quickly. **Monitoring** tells you *that* something is wrong; **observability** (metrics + logs + traces) helps you understand *why*, even for problems you did not predict.""",
chain=["PROBLEM: you cannot fix what you cannot see",
       "TRADITIONAL APPROACH: SSH into servers, tail logs, wait for user complaints",
       "PAIN: slow detection, slow diagnosis, alert noise, blind spots across microservices",
       "TECHNOLOGY: Prometheus, Grafana, Alertmanager, Loki/ELK, OpenTelemetry/Jaeger",
       "SOLUTION: collect metrics, logs and traces centrally; alert on symptoms; dashboards and SLOs",
       "REAL-WORLD BENEFIT: faster detection and recovery (lower MTTD/MTTR), data-driven capacity and reliability decisions"],
text="""**Three pillars:** **Metrics** (numbers over time: CPU, request rate), **Logs** (events with details), **Traces** (path of one request across services). **Golden signals** to watch for any service: **Latency, Traffic, Errors, Saturation**."""),
e2e=dict(diagram="""Application / Node / Kubernetes
   | exposes /metrics (exporters, client libs)      | writes logs     | sends traces (OpenTelemetry)
   v                                                v                 v
Prometheus (scrape every 15s, store TSDB)      Promtail/Fluent Bit   OTel Collector
   |  rules (recording + alerting)                  v                 v
   v                                               Loki / Elasticsearch  Tempo / Jaeger
Alertmanager (group, dedupe, route)                  |                 |
   v                                                 +--------+--------+
Slack / PagerDuty / Email                                     v
                                                      Grafana (dashboards, Explore, alerts)
   v
On-call engineer: alert > dashboard > logs > trace > fix > postmortem""",
text="""Applications and hosts expose **metrics** on an HTTP endpoint; **Prometheus** pulls (scrapes) them on an interval and stores them as time series. **Alerting rules** in Prometheus fire when a PromQL expression holds for a duration; **Alertmanager** groups, de-duplicates, silences and routes alerts to Slack/PagerDuty. Logs are collected by agents (Promtail/Fluent Bit) into **Loki** or **Elasticsearch**; traces flow via **OpenTelemetry** to Tempo/Jaeger. **Grafana** queries all of them so an engineer can go from an alert to the dashboard, then to logs and finally to the trace of a slow request. Findings feed **postmortems** and SLO reviews."""),
tools=dict(rows=[
["Prometheus", "Metrics collection and alert rules", "/metrics endpoints", "Time series, alerts", "Core monitoring"],
["Exporters (node, cAdvisor, blackbox, kube-state-metrics)", "Expose metrics from systems", "OS/containers/probes", "/metrics", "Everywhere"],
["Alertmanager", "Route and dedupe alerts", "Prometheus alerts", "Notifications", "On-call"],
["Grafana", "Dashboards and visualization", "Data sources", "Dashboards, alerts", "Teams and NOC"],
["Loki / ELK (Elasticsearch, Logstash, Kibana)", "Log storage and search", "Log streams", "Searchable logs", "Troubleshooting"],
["OpenTelemetry / Jaeger / Tempo", "Distributed tracing", "Instrumented requests", "Trace timelines", "Microservices"],
["CloudWatch", "AWS-native metrics/logs/alarms", "AWS service data", "Alarms, dashboards", "AWS environments"],
["PagerDuty / Opsgenie", "On-call scheduling", "Alerts", "Pages and escalations", "Incident response"]],
why="**Prometheus vs CloudWatch:** Prometheus is open-source, powerful PromQL, great for Kubernetes; CloudWatch is managed and integrated with AWS services. Many teams use both. **Loki vs ELK:** Loki indexes only labels (cheaper, simple, Grafana-native); Elasticsearch indexes full text (powerful search, heavier to run). **Pull vs push:** Prometheus pulls; short-lived jobs use the Pushgateway."),
compare=[
("Monitoring vs Observability", ["Topic", "Monitoring", "Observability"], [["Question", "Is it broken? (known failures)", "Why is it broken? (unknown unknowns)"], ["Data", "Predefined metrics/alerts", "Rich metrics + logs + traces, explorable"]]),
("Metrics vs Logs vs Traces", ["Topic", "Metrics", "Logs", "Traces"], [["Shape", "Numbers over time", "Text events", "Request path with spans"], ["Cost", "Low", "High volume", "Medium (sampling)"], ["Best for", "Alerting, trends", "Details/errors", "Latency across services"]]),
("Counter vs Gauge vs Histogram", ["Type", "Meaning", "Example"], [["Counter", "Only increases (resets on restart)", "http_requests_total"], ["Gauge", "Goes up and down", "memory_usage_bytes"], ["Histogram", "Distribution in buckets", "request_duration_seconds"]]),
("SLI vs SLO vs SLA", ["Term", "Meaning", "Example"], [["SLI", "Measured indicator", "% requests < 300ms and non-5xx"], ["SLO", "Internal target", "99.9% over 30 days"], ["SLA", "Contract with penalties", "99.5% or credits"]]),
("Symptom-based vs cause-based alerts", ["Topic", "Symptom-based", "Cause-based"], [["Example", "Error rate > 2%", "CPU > 80%"], ["Recommendation", "Page on these", "Dashboards / tickets"]])],
troubleshooting=[
("Prometheus target is DOWN", "Wrong port/path, network/firewall, app not exposing /metrics, TLS/auth", "Prometheus UI > Status > Targets error text, `curl host:port/metrics`", "Fix scrape config/port/network policy.", "Service discovery + test after deploy."),
("Alert storm / too many notifications", "Cause-based alerts, no grouping, flapping", "Alertmanager UI, alert history", "Group by service, add `for:` duration, inhibit rules, alert on symptoms/SLOs.", "Alert review each sprint; every alert needs a runbook."),
("Grafana panel shows 'No data'", "Wrong data source/query, label mismatch, time range, metric renamed", "Explore query directly, check metric exists in Prometheus", "Fix query/labels/time range.", "Provision dashboards as code and test."),
("Prometheus using too much memory/disk", "High cardinality labels (user_id, URL with IDs), long retention", "`topk(10, count by (__name__)({__name__=~\".+\"}))`, TSDB status page", "Drop/relabel high-cardinality labels; shorten retention; remote storage (Thanos/Mimir).", "Label hygiene; cardinality limits."),
("Logs missing in Loki/ELK", "Agent not running/permissions, wrong path/labels, pipeline errors, rate limits", "Agent logs, `kubectl logs promtail`, LogQL by label", "Fix agent config/permissions/labels.", "Alert on log pipeline health."),
("Alerts never fire", "Rule syntax/`for` too long, Prometheus not loading rules, Alertmanager routing", "Prometheus Status > Rules, `promtool check rules`, Alertmanager config", "Correct rule/routes; test with a synthetic alert.", "Alert on missing data (`absent()`), watchdog alert.")],
practices={
"Development": ["Instrument apps with client libraries (RED metrics); structured JSON logs with request IDs; propagate trace context."],
"Production": ["Golden signals per service; SLO-based alerts; dashboards as code; runbook link in every alert; redundancy for Prometheus/Alertmanager."],
"Security": ["Protect Grafana/Prometheus with auth and network policy; never log secrets/PII; RBAC in Grafana; TLS for scrape endpoints where needed."],
"Performance": ["Recording rules for expensive queries; control label cardinality; scrape interval tuned; retention plan."],
"Reliability": ["HA Alertmanager cluster; watchdog/dead-man's-switch alert; external uptime checks (blackbox)."],
"Cost Optimization": ["Log sampling/retention tiers; drop noisy logs; metrics downsampling; Loki over full-text for cost."],
"Monitoring & Logging": ["Central logs, correlation IDs across metrics/logs/traces, audit logs retained per policy."],
"Backup & Disaster Recovery": ["Dashboards and alert rules in Git; remote-write to long-term storage; test restore of Grafana provisioning."]},
mistakes={
"Beginner mistakes": ["Alerting on CPU only.", "Only looking at averages instead of percentiles."],
"Developer mistakes": ["High-cardinality labels (user IDs).", "Unstructured logs."],
"DevOps mistakes": ["No runbooks for alerts.", "Dashboards with no owner or purpose."],
"Production mistakes": ["Single Prometheus with no backup.", "No alert for monitoring being down."],
"Security mistakes": ["Secrets in logs.", "Grafana exposed publicly with default admin password."]},
versions=[
"Prometheus, Alertmanager and Grafana change UI and config across releases: check the release notes; Grafana 9+ has unified alerting replacing legacy alerting.",
"Loki config schema versions change (`schema_config`); Promtail is being succeeded by Grafana Alloy: verify the recommended agent for your version.",
"OpenTelemetry is the standard for traces/metrics/logs instrumentation; OpenTracing/OpenCensus are legacy.",
"On Kubernetes, kube-prometheus-stack (Helm chart) bundles Prometheus Operator, Grafana, exporters and rules: chart values differ per version."],
hinglish="""**Metrics** = numbers (CPU, requests), **Logs** = events ki detail, **Traces** = ek request ka poora safar. Har service ke liye **4 golden signals** dekho: **Latency, Traffic, Errors, Saturation**. **Prometheus** metrics ko khud scrape karta hai, **Alertmanager** alerts ko group karke Slack/PagerDuty bhejta hai, aur **Grafana** dashboard dikhata hai. Alert **symptom** par lagao (error rate zyada) sirf CPU par nahi, aur har alert ke saath **runbook** do. **SLO** batata hai kitni reliability chahiye.""",
mnemonics=[("Golden signals", "L-T-E-S: Latency, Traffic, Errors, Saturation"), ("RED (services)", "Rate, Errors, Duration"), ("USE (resources)", "Utilization, Saturation, Errors"), ("Three pillars", "Metrics, Logs, Traces (M-L-T)"), ("Alert rule", "Page on symptoms, dashboard for causes")],
client=dict(
s30="""Monitoring and observability give us live visibility into how our applications are performing. We collect metrics, logs and traces, alert the team when users are affected, and use the data to fix problems quickly and plan capacity.""",
m2="""We instrument every service and server so we can see request rate, errors, response time and resource usage in real time. Prometheus collects the numbers, Grafana displays them on dashboards, and Alertmanager notifies the on-call engineer through Slack or a paging tool when users are impacted. Logs and traces are searchable in one place, so we can move from an alert to the exact failing request in minutes. We define service level objectives, for example 99.9 percent availability, and report against them. This reduces downtime, speeds up recovery and gives you evidence for reliability commitments.""",
m5="""I will explain in four parts. **Collect:** metrics via Prometheus exporters and application libraries, logs via agents into Loki or Elasticsearch, traces via OpenTelemetry. **Understand:** Grafana dashboards organised around the golden signals (latency, traffic, errors, saturation) and per-service RED views, with correlation between metrics, logs and traces using request IDs. **Act:** alerting rules based on symptoms and SLO burn rates, routed through Alertmanager with grouping, silences and escalation, each linked to a runbook. **Improve:** SLOs and error budgets guide priorities; postmortems turn incidents into fixes; retention and label policies keep cost under control. The outcome is lower mean time to detect and recover, fewer noisy alerts and data-driven capacity planning."""),
roadmap=[
("Beginner", ["Metrics vs logs vs traces", "Golden signals", "Node exporter + Prometheus", "Basic Grafana dashboard"]),
("Intermediate", ["PromQL (rate, sum by, histogram_quantile)", "Alert rules and Alertmanager", "Kubernetes monitoring (kube-state-metrics)", "Loki/ELK basics"]),
("Advanced", ["SLIs/SLOs and burn-rate alerts", "OpenTelemetry tracing", "Recording rules, federation, Thanos/Mimir", "Cardinality management"]),
("Production", ["HA setup", "Dashboards/alerts as code", "On-call and runbooks", "Cost and retention"]),
("Interview", ["Explain golden signals", "Write a PromQL error-rate query", "Design alerting for an API", "Debug high latency using the three pillars"])],
miniproject=dict(title="Monitor a web service with Prometheus, Grafana and Alertmanager (Docker Compose)",
arch="""app (/metrics :8000) + node-exporter (:9100)
        v scrape 15s
Prometheus (:9090) -- rules --> Alertmanager (:9093) --> Slack webhook
        v
Grafana (:3000) dashboards (Prometheus + Loki datasources)""",
steps=[
("Step 1: compose.yml", """services:
  prometheus:
    image: prom/prometheus:latest
    volumes: ["./prometheus.yml:/etc/prometheus/prometheus.yml:ro", "./rules.yml:/etc/prometheus/rules.yml:ro"]
    ports: ["9090:9090"]
  alertmanager:
    image: prom/alertmanager:latest
    ports: ["9093:9093"]
  node-exporter:
    image: prom/node-exporter:latest
    ports: ["9100:9100"]
  grafana:
    image: grafana/grafana:latest
    ports: ["3000:3000"]""", "Four components on one network. In real projects pin versions instead of `latest` and add volumes for persistence."),
("Step 2: prometheus.yml and alert rule", """# prometheus.yml
global: { scrape_interval: 15s }
rule_files: [rules.yml]
alerting: { alertmanagers: [{ static_configs: [{ targets: ["alertmanager:9093"] }] }] }
scrape_configs:
  - job_name: node
    static_configs: [{ targets: ["node-exporter:9100"] }]

# rules.yml
groups:
- name: basic
  rules:
  - alert: InstanceDown
    expr: up == 0
    for: 2m
    labels: { severity: page }
    annotations: { summary: "{{ $labels.instance }} is down", runbook: "https://wiki/runbooks/instance-down" }
  - alert: HighErrorRate
    expr: sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m])) > 0.02
    for: 10m
    labels: { severity: page }""", "`up == 0` fires when a target cannot be scraped; `for: 2m` avoids flapping. The error-rate rule alerts on a **symptom** (more than 2 percent 5xx for 10 minutes) and needs an app exposing `http_requests_total`. Annotations carry the runbook link."),
("Step 3: Start and verify", """docker compose up -d
curl -s localhost:9100/metrics | head
# open http://localhost:9090/targets  (all UP)
# open http://localhost:3000  (admin/admin: change it) > add Prometheus datasource http://prometheus:9090
# PromQL: 100 - (avg by(instance)(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)""", "Check targets, connect Grafana and run a CPU utilisation query. `rate()` converts a counter into a per-second rate."),
("Step 4: Test the alert", """docker compose stop node-exporter
# after ~2 minutes: Prometheus > Alerts shows InstanceDown FIRING; Alertmanager UI shows it
docker compose start node-exporter""", "Proves the alert path end to end. Configure a Slack receiver in `alertmanager.yml` to receive notifications.")]),
interview=[
("Beginner", "What is monitoring?", "Collecting and analysing system data to detect problems and track health and performance.", "Basics.", "CPU and error dashboards."),
("Beginner", "Monitoring vs observability?", "Monitoring shows known failure indicators; observability lets you investigate unknown problems with rich telemetry.", "Concept.", "Trace explains a new slowdown."),
("Beginner", "What are the three pillars?", "Metrics, logs and traces.", "Foundation.", "Prometheus, Loki, Jaeger."),
("Beginner", "What are the four golden signals?", "Latency, traffic, errors, saturation.", "SRE basics.", "API dashboard."),
("Beginner", "What is Prometheus?", "Open-source metrics system that scrapes endpoints, stores time series and evaluates alert rules.", "Core tool.", "Kubernetes monitoring."),
("Beginner", "What is Grafana?", "Visualization/dashboard platform that queries many data sources.", "Core tool.", "Dashboards for teams."),
("Beginner", "What is an exporter?", "A process that exposes metrics of another system in Prometheus format.", "Prometheus ecosystem.", "node_exporter."),
("Beginner", "What is an alert?", "A notification triggered when a condition is met, needing human or automated action.", "Basics.", "Disk > 90%."),
("Beginner", "What is a log?", "A time-stamped record of an event.", "Basics.", "Nginx access log."),
("Beginner", "What is uptime monitoring?", "External checks that verify a service is reachable and responding.", "Availability.", "Blackbox exporter/Pingdom."),
("Intermediate", "Pull vs push monitoring?", "Prometheus pulls from targets; push systems receive from agents. Pushgateway supports short-lived batch jobs.", "Architecture.", "Cron jobs push results."),
("Intermediate", "Explain metric types.", "Counter (monotonic), gauge (up/down), histogram/summary (distributions).", "Prometheus depth.", "request_duration_seconds histogram."),
("Intermediate", "What does rate() do?", "Computes per-second average increase of a counter over a window, handling resets.", "PromQL.", "`rate(http_requests_total[5m])`."),
("Intermediate", "Write a query for 5xx error percentage.", "`sum(rate(http_requests_total{status=~\"5..\"}[5m])) / sum(rate(http_requests_total[5m])) * 100`.", "PromQL practice.", "Alert if > 2."),
("Intermediate", "How do you calculate p95 latency?", "`histogram_quantile(0.95, sum by (le)(rate(http_request_duration_seconds_bucket[5m])))`.", "Percentiles.", "Averages hide slow users."),
("Intermediate", "What does Alertmanager do?", "Deduplicates, groups, silences, inhibits and routes alerts to receivers.", "Alert pipeline.", "Route severity=page to PagerDuty."),
("Intermediate", "What is the `for` clause in an alert rule?", "Condition must hold for that duration before firing, reducing flapping.", "Alert quality.", "`for: 5m`."),
("Intermediate", "How to monitor Kubernetes?", "kube-state-metrics (object state), node-exporter, cAdvisor/kubelet, metrics-server, Prometheus Operator, Grafana dashboards.", "K8s ops.", "kube-prometheus-stack."),
("Intermediate", "Loki vs Elasticsearch?", "Loki indexes labels only (cheap, simple); Elasticsearch indexes full text (rich search, heavier).", "Tool choice.", "Kubernetes logs in Loki."),
("Intermediate", "What is structured logging?", "Logs in JSON with consistent fields (level, request_id) for easy querying.", "Log quality.", "LogQL `| json`."),
("Intermediate", "What is a dashboard best practice?", "Organise by service and signals, show SLO status, use percentiles, add links to runbooks, avoid clutter.", "Design.", "Top row: error rate, latency, traffic."),
("Intermediate", "What is log retention and why?", "How long logs are kept, balancing cost and compliance/debug needs.", "Cost.", "7 days hot, 90 days cold."),
("Intermediate", "What is an SLO?", "A reliability target for an SLI over a period, with an error budget.", "SRE.", "99.9% success in 30 days."),
("Intermediate", "What is a synthetic monitor?", "Scripted external checks simulating user journeys.", "User perspective.", "Login flow probe."),
("Intermediate", "Explain recording rules.", "Precompute expensive expressions and store as new series to speed dashboards/alerts.", "Performance.", "job:http_requests:rate5m."),
("Advanced", "What is high cardinality and why is it dangerous?", "Too many unique label combinations create huge numbers of series, consuming memory/disk and slowing queries.", "Prometheus scaling.", "user_id label."),
("Advanced", "Explain burn-rate alerting for SLOs.", "Alert on how fast the error budget is consumed using multi-window (e.g. 1h and 5m) thresholds, catching fast and slow burns while reducing noise.", "Modern alerting.", "14.4x burn over 1h pages."),
("Advanced", "How does distributed tracing work?", "A trace ID propagates via headers across services; each unit of work is a span with timing; collector assembles spans into a timeline.", "Microservices.", "Find the slow DB call."),
("Advanced", "Scaling Prometheus?", "Functional sharding, federation, Thanos/Mimir/Cortex for global view and long-term storage, remote write.", "Large scale.", "Multi-cluster."),
("Advanced", "HA for Prometheus and Alertmanager?", "Run two identical Prometheus replicas scraping the same targets; Alertmanager in a gossip cluster dedupes alerts.", "Reliability.", "Watchdog alert."),
("Advanced", "What is OpenTelemetry?", "Vendor-neutral standard, SDKs and collector for traces, metrics and logs.", "Modern instrumentation.", "Auto-instrument Java service."),
("Advanced", "Sampling strategies for traces?", "Head-based (probabilistic at start) vs tail-based (decide after seeing the trace, keep errors/slow).", "Cost and value.", "Keep 100% of errors."),
("Advanced", "Correlating metrics, logs and traces?", "Shared labels/IDs (service, pod, trace_id); Grafana links exemplars from metrics to traces and logs.", "Observability depth.", "Click from spike to trace."),
("Advanced", "Design alerting for a payment API.", "SLO burn-rate pages on availability/latency, saturation warnings, dependency checks, runbooks, on-call routing, separate ticket-level alerts.", "System design.", "Multi-window burn alerts."),
("Advanced", "How to reduce alert fatigue?", "Alert on symptoms, add for-durations, group and inhibit, delete unactionable alerts, review weekly, tier severity.", "On-call health.", "Only page when action is needed."),
("Advanced", "Blackbox vs whitebox monitoring?", "Blackbox tests from outside like users; whitebox uses internal metrics; use both.", "Coverage.", "Blackbox exporter + app metrics."),
("Advanced", "What are exemplars?", "Sample trace IDs attached to metric data points linking metrics to traces.", "Correlation.", "Latency histogram bucket to trace."),
("Scenario-Based", "Users report slowness but CPU is normal.", "Check latency percentiles, traffic, errors, dependencies (DB/cache), saturation (connections, queue), then traces to find the slow span.", "Diagnosis.", "DB connection pool exhaustion."),
("Scenario-Based", "Team ignores alerts due to noise.", "Audit alerts, remove non-actionable, symptom-based SLO alerts, tune thresholds/for, add runbooks, track alert-to-incident ratio.", "Culture and tuning.", "Reduced pages by 70%."),
("Scenario-Based", "Design monitoring for a Kubernetes platform.", "kube-prometheus-stack, node/kubelet/cAdvisor, app RED metrics, Loki, Tempo/OTel, Alertmanager routing per team, SLO dashboards, cost management.", "Platform design.", "Multi-tenant labels."),
("Scenario-Based", "Prometheus disk fills up.", "Check series growth/cardinality, retention size, WAL; drop labels, reduce retention, use remote storage.", "Capacity.", "Unbounded URL label."),
("Scenario-Based", "You need to detect a silent failure (no traffic).", "Alert on `absent()` or traffic drop vs baseline, synthetic checks.", "Coverage gap.", "Checkout no orders for 10 minutes."),
("Scenario-Based", "Set an SLO for a new API.", "Choose SLIs (availability, latency), measure baseline, set realistic target, error budget policy, dashboards and burn alerts.", "SRE practice.", "99.9% with p95 < 300ms."),
("Scenario-Based", "Logs cost too much.", "Sample/filter noisy logs, shorter retention for debug, structured labels, tiered storage, metrics instead of logs for counting.", "FinOps.", "Drop health-check logs."),
("Scenario-Based", "Alert fired at 3am; how does on-call proceed?", "Acknowledge, check runbook, dashboards (golden signals), recent deploys, mitigate (rollback/scale), communicate, then postmortem.", "Incident flow.", "Rollback the bad release."),
("Scenario-Based", "Multi-cluster global view.", "Thanos/Mimir with remote write, Grafana multi-datasource, consistent labels (cluster, env).", "Scale.", "Three regions."),
("Scenario-Based", "Monitor a batch job.", "Push success timestamp/duration via Pushgateway or use Kubernetes job metrics; alert if not run within the expected time.", "Batch monitoring.", "Nightly backup missed."),
("Scenario-Based", "Application Insights alternative on-prem.", "OpenTelemetry auto-instrumentation + Tempo/Jaeger + Prometheus + Loki + Grafana.", "Tool choice.", "Self-hosted stack."),
("Troubleshooting-Based", "Target shows 'context deadline exceeded'.", "Scrape timeout: slow endpoint/network; increase timeout, fix app, check firewall.", "Prometheus scrape.", "Heavy /metrics."),
("Troubleshooting-Based", "PromQL returns empty.", "Wrong metric/label names, no data in range, staleness; check with the metric browser and `label_values`.", "Query debugging.", "Label `job` mismatch."),
("Troubleshooting-Based", "Grafana alert not sending.", "Contact point/notification policy misconfigured, mute timing, data source error; use test notification.", "Grafana alerting.", "Wrong Slack webhook."),
("Troubleshooting-Based", "Alertmanager not routing.", "Route matchers wrong; `amtool config routes test` to check labels.", "Routing.", "severity label case mismatch."),
("Troubleshooting-Based", "Sudden metric gaps.", "Scrape failures, Prometheus restart/overload, network, relabeling drop; check `up` and Prometheus logs.", "Data quality.", "Target churn."),
("Troubleshooting-Based", "Loki query is slow.", "Too broad selector/time range; narrow labels first, add filters, increase resources or use recording rules/metrics.", "Log performance.", "Query {job=~\".+\"}."),
("Troubleshooting-Based", "Dashboard values look wrong (too high).", "Using `increase` vs `rate` incorrectly, wrong aggregation, counter resets, units (bytes vs bits).", "PromQL correctness.", "Sum across replicas duplicates."),
("Troubleshooting-Based", "Missing pod metrics in Kubernetes.", "ServiceMonitor/PodMonitor labels not matching, Prometheus RBAC/namespace selection, port name.", "Operator usage.", "Label selector mismatch."),
("Troubleshooting-Based", "Trace shows gaps.", "Missing instrumentation or context propagation across a service/queue; ensure headers are forwarded.", "Tracing.", "Async worker not propagating."),
("Troubleshooting-Based", "Elasticsearch cluster yellow/red.", "Unassigned shards (disk watermark, node down); check `_cluster/health`, allocation explain, free disk.", "ELK ops.", "Disk full on data node.")],
cheatsheet={
"Definitions": ["Metrics/logs/traces; golden signals (L-T-E-S); RED; USE; SLI/SLO/SLA; cardinality; exporter; scrape; recording rule."],
"Commands": ["`curl host:9100/metrics` `promtool check config|rules file` `amtool alert|silence` `amtool config routes test`", "PromQL: `rate(x[5m])` `sum by (label)(...)` `histogram_quantile(0.95, sum by (le)(rate(x_bucket[5m])))` `up == 0` `absent(x)`", "LogQL: `{app=\"api\"} |= \"error\" | json | level=\"error\"`", "`kubectl top pods` `kubectl logs -f pod` `docker stats`"],
"Files": ["prometheus.yml rules.yml alertmanager.yml grafana provisioning (datasources/dashboards) loki-config.yml promtail.yml otel-collector.yaml"],
"Architecture": ["Targets > Prometheus > rules > Alertmanager > receivers; logs > Loki; traces > Tempo; all in Grafana."],
"Ports": ["Prometheus 9090, Alertmanager 9093, node_exporter 9100, Grafana 3000, Loki 3100, Tempo 3200/4317 (OTLP gRPC), Jaeger UI 16686, Elasticsearch 9200, Kibana 5601"],
"Differences": ["Monitoring vs observability; counter vs gauge vs histogram; SLI/SLO/SLA; Loki vs ELK; pull vs push; symptom vs cause alerts."],
"Troubleshooting commands": ["Targets page > `curl /metrics` > query in Explore > check labels > logs `kubectl logs` > traces > recent deploys"],
"Best practices": ["Golden signals, SLO burn alerts, runbooks, low cardinality, dashboards as code, HA Alertmanager, structured logs, retention policy."]}
),
subs={
"observability-concepts": dict(
define=dict(simple="Observability means you can understand what is happening inside a system by looking at the data it produces.",
technical="Observability is the ability to infer internal state from outputs: metrics, logs, traces (and events/profiles), enabling investigation of unknown failure modes. The golden signals summarise service health.",
why="Distributed systems fail in new ways.", without="Guessing during incidents.", use="All production systems.", avoid="Collecting everything without purpose (cost).", analogy="A car dashboard plus black-box recorder."),
internals="""Each request generates telemetry: counters and timers (metrics), events (logs) and spans (traces) that share identifiers. Backends store them, Grafana correlates them: a metric spike leads to related logs by labels/time and to a trace by exemplar/trace_id.""",
realworld=dict(diagram="""checkout API: Latency p95 up (metric) -> errors in payment-service logs -> trace shows 2s DB span""", text="An e-commerce checkout slows. The RED dashboard shows p95 latency rising, logs from the payment service show timeouts, and one trace reveals a database call taking two seconds because of a missing index. You go from symptom to cause in minutes."),
lab=dict(goal="Explore golden signals with a demo app.", prereq=["Docker"],
steps=[("docker run -d -p 8080:8080 --name demo quay.io/brancz/prometheus-example-app:v0.3.0", "Example app exposing /metrics."),
("curl -s localhost:8080/metrics | head -20", "You will see counters and histograms in Prometheus text format."),
("for i in $(seq 1 50); do curl -s localhost:8080/ >/dev/null; done; curl -s localhost:8080/metrics | grep http_requests_total", "Counter value increased.")]),
mnemonics=[("Signals", "L-T-E-S"), ("Pillars", "M-L-T")], hinglish="Sirf CPU dekhna kaafi nahi. **Latency, Traffic, Errors, Saturation** har service ke liye dekho.",
practices={"Production": ["RED per service, USE per resource."]}, mistakes={"Beginner mistakes": ["Alerting on averages."]},
qa_extra=[("Intermediate", "Why percentiles instead of averages?", "Averages hide slow tail requests; p95/p99 show what unlucky users experience.", "Metric literacy.", "Average 200ms but p99 5s.")]),

"prometheus": dict(
define=dict(simple="Prometheus collects numbers about your systems and lets you query and alert on them.",
technical="Prometheus scrapes HTTP endpoints (text exposition format) on an interval, stores samples in a local time-series database and evaluates PromQL alert/recording rules; service discovery finds targets dynamically.",
why="Reliable metric collection with a powerful query language.", without="No trend or alert data.", use="Infrastructure and application metrics.", avoid="Long-term storage without remote write; log storage.", analogy="A reporter who visits every service every 15 seconds and writes down its numbers."),
internals="""Scrape loop: discover targets (static or Kubernetes SD) > relabel > HTTP GET /metrics > parse > append to the TSDB head (memory + WAL) > compact to blocks on disk. Rule evaluation runs each interval; firing alerts are sent to Alertmanager.""",
config=[("prometheus.yml explained", """global:
  scrape_interval: 15s
scrape_configs:
  - job_name: kubernetes-pods
    kubernetes_sd_configs: [{ role: pod }]
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: "true"
""", [("scrape_interval", "How often to scrape; trade-off resolution vs load."), ("kubernetes_sd_configs", "Discover pods automatically."), ("relabel_configs keep", "Only scrape pods annotated `prometheus.io/scrape: true`.")])],
commands=[("promtool check config prometheus.yml", "Validates config and referenced rule files.", "`check rules`, `query instant`.", "SUCCESS", "Editing config without validation.", "On error read the line reference.")],
lab=dict(goal="Run Prometheus and query.", prereq=["Docker"],
steps=[("Create prometheus.yml scraping localhost:9090 then docker run -d -p 9090:9090 -v $PWD/prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus", "Prometheus scrapes itself."),
("Open http://localhost:9090 and run: rate(prometheus_http_requests_total[5m])", "Graph of request rate."),
("Status > Targets", "Shows UP and last scrape duration.")]),
mnemonics=[("PromQL", "Selector > range > function > aggregate: sum by (job)(rate(x[5m]))")], hinglish="**rate()** counter ko per-second speed mein badalta hai. Labels mein user_id jaise unique values mat daalo (**high cardinality**).",
practices={"Performance": ["Recording rules; keep labels low cardinality."]}, mistakes={"Developer mistakes": ["High-cardinality labels."]},
qa_extra=[("Advanced", "Why does Prometheus pull instead of push?", "Central control over targets and rates, easy detection of down targets (`up`), simpler client libraries; Pushgateway for batch jobs.", "Design reasoning.", "Discovering pods via Kubernetes SD.")]),

"grafana-alertmanager": dict(
define=dict(simple="Grafana draws dashboards; Alertmanager decides who gets notified and how.",
technical="Grafana queries data sources and renders panels; Alertmanager receives alerts from Prometheus, groups by labels, inhibits/silences, and routes to receivers with repeat intervals.",
why="Humans need clear views and actionable notifications.", without="Raw numbers and alert floods.", use="All production monitoring.", avoid="Dashboards without a purpose.", analogy="Grafana = instrument panel; Alertmanager = dispatcher of the right alarm to the right person."),
internals="""Prometheus sends alert instances (labels + annotations) to Alertmanager. Alertmanager waits `group_wait`, groups alerts with the same `group_by` labels into one notification, sends to the matched receiver, and repeats after `repeat_interval` if still firing. Inhibit rules suppress dependent alerts (e.g. disk warning when node is down).""",
config=[("alertmanager.yml explained", """route:
  receiver: slack-default
  group_by: [alertname, service]
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
  routes:
    - matchers: [ severity = "page" ]
      receiver: pagerduty
receivers:
  - name: slack-default
    slack_configs: [{ channel: "#alerts", api_url_file: /etc/alertmanager/slack_url }]
  - name: pagerduty
    pagerduty_configs: [{ routing_key_file: /etc/alertmanager/pd_key }]""", [("group_by", "Alerts with the same labels become one notification."), ("group_wait", "Wait to collect related alerts before first send."), ("repeat_interval", "Re-notify if still firing."), ("routes matchers", "Send severity=page to PagerDuty."), ("api_url_file", "Keep secrets in files, not in the config.")])],
lab=dict(goal="Send a test alert to Slack.", prereq=["Slack incoming webhook", "Prometheus + Alertmanager running"],
steps=[("Configure the receiver and reload Alertmanager", "Use a file for the webhook."), ("amtool alert add test severity=warning --annotation=summary='test' --alertmanager.url=http://localhost:9093", "Creates a test alert."), ("Check Slack", "Notification arrives; verify grouping.")]),
mnemonics=[("Alert path", "Rule > Prometheus > Alertmanager > Route > Receiver")], hinglish="Alertmanager **group aur dedupe** karta hai, isliye 100 alerts ki jagah ek notification aata hai. Har alert par **runbook link** lagao.",
practices={"Reliability": ["Cluster Alertmanager; watchdog alert."], "Security": ["Auth on Grafana; secrets in files."]}, mistakes={"DevOps mistakes": ["Alerts without owner/runbook."]},
qa_extra=[("Intermediate", "What are inhibition and silences?", "Inhibition suppresses alerts when a related alert fires; silences mute alerts matching labels for a time (for maintenance).", "Alert hygiene.", "Silence during planned upgrade.")]),

"logging-elk-loki": dict(
define=dict(simple="Central logging collects logs from all servers and containers into one searchable place.",
technical="Agents (Promtail/Fluent Bit/Filebeat) tail logs, add labels/metadata, and ship them to Loki (label-indexed) or Elasticsearch (full-text indexed) where Grafana/Kibana query them.",
why="Logs are scattered across ephemeral containers.", without="SSH into pods that no longer exist.", use="All production systems.", avoid="Logging secrets/PII or debug spam.", analogy="A central library for all applications' diaries."),
internals="""Pod stdout > container runtime writes /var/log/containers/*.log > agent tails, enriches with Kubernetes labels > pushes to Loki (compresses chunks, indexes labels) > Grafana Explore runs LogQL: first select streams by labels, then filter lines.""",
config=[("LogQL examples explained", """{namespace="prod", app="api"} |= "error"
{app="api"} | json | level="error" | line_format "{{.msg}}"
sum by (app)(rate({namespace="prod"} |= "error" [5m]))""", [("{labels}", "Stream selector using indexed labels (fast)."), ("|= \"error\"", "Line contains filter."), ("| json", "Parse JSON fields."), ("rate(...)", "Turn logs into a metric for alerts.")])],
lab=dict(goal="Run Loki + Grafana and query logs.", prereq=["Docker Compose"],
steps=[("Use the official Loki docker-compose example (grafana/loki repo `production/docker-compose.yaml`)", "Starts Loki, Promtail and Grafana (check the current file in the repo)."), ("Open Grafana > Explore > Loki > {job=\"varlogs\"}", "See system logs."), ("Add |= \"error\"", "Filter lines.")]),
compare=[("Loki vs ELK", ["Topic", "Loki", "ELK"], [["Index", "Labels only", "Full text"], ["Cost", "Lower", "Higher"], ["Query", "LogQL", "KQL/Lucene"], ["Best for", "Kubernetes + Grafana users", "Complex search/analytics"]])],
mnemonics=[("Log rules", "Structured, Central, No secrets, Retained")], hinglish="Logs **JSON format** mein likho aur **request_id** rakho taaki metrics aur traces se jod sako. Passwords/PII kabhi log mat karo.",
practices={"Security": ["Mask PII/secrets; restrict log access."], "Cost Optimization": ["Retention tiers; drop noisy logs."]}, mistakes={"Security mistakes": ["Logging tokens and passwords."]},
qa_extra=[("Scenario-Based", "How to trace one user's failed request across services?", "Use a correlation/request ID in every log and pass it in headers, then search by that ID; better use trace_id with OpenTelemetry.", "Debugging distributed systems.", "Support ticket lookup.")]),

"tracing-slo": dict(
define=dict(simple="Tracing follows one request through many services; SLOs define how reliable the service should be.",
technical="OpenTelemetry instruments code to create spans with trace/span IDs propagated via W3C `traceparent` headers; SLOs use SLIs to compute error budgets and burn rates.",
why="Find bottlenecks in microservices and prioritise reliability work.", without="Blind spots and endless reliability debates.", use="Distributed systems.", avoid="100% SLO targets (unrealistic).", analogy="A courier tracking number; SLO = delivery promise."),
internals="""An incoming request gets a trace ID; each service creates spans (start, duration, attributes), passes `traceparent` to downstream calls, and exports spans to the OTel Collector > Tempo/Jaeger. The backend stitches them into a timeline. For SLOs: error budget = 1 - target (99.9% => 0.1%); burn rate = actual error rate / allowed error rate.""",
config=[("SLO / burn-rate example explained", """# SLI: availability
sum(rate(http_requests_total{status!~"5.."}[5m])) / sum(rate(http_requests_total[5m]))

# Burn rate alert idea (SLO 99.9% => budget 0.001)
( sum(rate(http_requests_total{status=~"5.."}[1h])) / sum(rate(http_requests_total[1h])) ) > (14.4 * 0.001)""", [("SLI query", "Fraction of good requests."), ("0.001", "Error budget for 99.9%."), ("14.4", "Fast-burn factor: budget would be gone in about 2 days if sustained (see SRE workbook)."), ("1h window", "Pair with a short window (5m) to reduce false positives.")])],
lab=dict(goal="Send traces to Jaeger.", prereq=["Docker"],
steps=[("docker run -d --name jaeger -p 16686:16686 -p 4317:4317 jaegertracing/all-in-one:latest", "Jaeger UI and OTLP receiver (check flags for your version)."), ("Run an app with OpenTelemetry auto-instrumentation exporting OTLP to localhost:4317", "Spans start arriving."), ("Open http://localhost:16686 and find the service", "View trace timelines and slowest spans.")]),
mnemonics=[("Error budget", "1 - SLO"), ("Trace", "Trace > Spans > Attributes")], hinglish="**SLO 100% nahi hota.** 99.9% ka matlab 0.1% error budget; budget khatam ho to naye features rok kar reliability par kaam karo.",
practices={"Production": ["Tail sampling for errors; propagate context everywhere."]}, mistakes={"DevOps mistakes": ["Tracing only some services."]},
qa_extra=[("Advanced", "What happens when the error budget is exhausted?", "Freeze risky releases and prioritise reliability work per the error-budget policy until the service recovers.", "SRE governance.", "Feature freeze for a sprint.")])
})
