TOPIC = dict(slug="11-monitoring-observability", title="Monitoring, Logging & Observability", intro="Jo dikhta nahi usse fix nahi kar sakte. Metrics + Logs + Traces = observability. Alerts sahi hone chahiye, noisy nahi.", subs=[

dict(slug="observability-concepts", title="Observability Concepts & Golden Signals", level="Basic",
intro="Monitoring 'kya toota' batati hai, observability 'kyun toota'. Three pillars: metrics (numbers), logs (events), traces (request path).",
diagram="""
Metrics: CPU 80%, req/s, p99 latency   -> Prometheus
Logs   : 'ERROR db timeout user=42'    -> Loki / ELK
Traces : gateway -> api -> db (120ms)  -> Jaeger / Tempo
Golden signals: Latency | Traffic | Errors | Saturation
RED (services): Rate, Errors, Duration ; USE (resources): Utilization, Saturation, Errors
""",
install="# concept topic; next pages install tools",
examples=[("Design alert philosophy","""Alert on SYMPTOMS (user pain: error rate, latency), not causes (CPU 80%).
Every page must be actionable + have a runbook.
Severity: page (wake up) vs ticket (next day) vs info.""")],
problems=[("Alert fatigue: team ignores pages","Too many noisy cause-based alerts","Alert on SLO burn rate, delete non-actionable alerts, group/route in Alertmanager.")],
qa=[("Monitoring vs observability?","Monitoring watches known failure modes; observability lets you ask new questions from telemetry."),
("Four golden signals?","Latency, traffic, errors, saturation."),
("What is an SLI/SLO/SLA?","SLI measured indicator; SLO target; SLA contractual promise with penalty."),
("Why p99 not average latency?","Averages hide tail latency affecting real users."),
("Black-box vs white-box monitoring?","Black-box tests from outside (probes); white-box uses internal metrics.")]),

dict(slug="prometheus", title="Prometheus & PromQL", level="Intermediate",
intro="Pull-based metrics system. Targets ko scrape karta hai, time-series DB mein store. PromQL query language. Kubernetes ka de-facto standard.",
diagram="""
[node_exporter][app /metrics][kube-state-metrics] <--scrape-- Prometheus --rules--> Alertmanager -> Slack/PagerDuty
                                                      |
                                                   Grafana (dashboards)
""",
install="""# Docker quick start
docker run -d -p 9090:9090 -v $PWD/prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus
docker run -d -p 9100:9100 prom/node-exporter
# Kubernetes (recommended)
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install mon prometheus-community/kube-prometheus-stack -n monitoring --create-namespace""",
examples=[("prometheus.yml","""global: { scrape_interval: 15s }
scrape_configs:
- job_name: node
  static_configs: [{ targets: ['localhost:9100'] }]
- job_name: myapp
  metrics_path: /metrics
  static_configs: [{ targets: ['app:3000'] }]"""),
("Useful PromQL","""# CPU usage %
100 - avg by(instance)(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100
# request rate and error ratio
sum(rate(http_requests_total[5m]))
sum(rate(http_requests_total{code=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))
# p95 latency
histogram_quantile(0.95, sum by(le)(rate(http_request_duration_seconds_bucket[5m])))
# memory available %
node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes * 100"""),
("Instrument a Python app","""from prometheus_client import Counter, Histogram, start_http_server
REQ = Counter("http_requests_total", "reqs", ["code"])
LAT = Histogram("http_request_duration_seconds", "latency")
start_http_server(8000)
@LAT.time()
def handle(): REQ.labels("200").inc()""")],
problems=[("Prometheus memory explodes","High cardinality labels (user_id, url with ids)","Drop/aggregate labels, relabeling, limits; check `topk(10, count by(__name__)({__name__=~'.+'}))`."),
("Need long-term storage / HA","Single Prometheus local TSDB","Remote write to Thanos/Mimir/VictoriaMetrics.")],
qa=[("Pull vs push model?","Prometheus pulls (scrapes) targets; push via Pushgateway only for short-lived jobs."),
("Counter vs gauge vs histogram?","Counter only increases (use rate()); gauge goes up/down; histogram buckets for quantiles."),
("rate vs irate?","rate = average per-second over window; irate = instantaneous last two points."),
("What is cardinality?","Number of unique label combinations; high cardinality kills performance."),
("How does service discovery work in K8s?","ServiceMonitor/PodMonitor CRDs via Prometheus Operator.")]),

dict(slug="grafana-alertmanager", title="Grafana Dashboards & Alertmanager", level="Intermediate",
intro="Grafana visualization, Alertmanager routing/grouping/silencing of alerts. Actionable alerts with runbooks.",
diagram="""
Prometheus rule fires -> Alertmanager: group -> dedupe -> route (severity/team)
   ├─ critical -> PagerDuty
   └─ warning  -> Slack #alerts
Inhibition: node down suppresses pod alerts on that node
""",
install="""docker run -d -p 3000:3000 grafana/grafana    # admin/admin
# add Prometheus datasource http://prometheus:9090; import dashboard IDs 1860 (node), 15760 (k8s)""",
examples=[("Alert rules","""groups:
- name: app
  rules:
  - alert: HighErrorRate
    expr: sum(rate(http_requests_total{code=~"5.."}[5m])) / sum(rate(http_requests_total[5m])) > 0.02
    for: 5m
    labels: { severity: page }
    annotations: { summary: "5xx > 2%", runbook: "https://wiki/runbooks/5xx" }
  - alert: DiskFilling
    expr: predict_linear(node_filesystem_avail_bytes[6h], 24*3600) < 0
    for: 30m
    labels: { severity: ticket }"""),
("alertmanager.yml","""route:
  receiver: slack
  group_by: [alertname, cluster]
  routes:
  - matchers: [severity="page"]
    receiver: pagerduty
receivers:
- name: slack
  slack_configs: [{ api_url_file: /etc/am/slack_url, channel: '#alerts', send_resolved: true }]
- name: pagerduty
  pagerduty_configs: [{ routing_key_file: /etc/am/pd_key }]""")],
problems=[("Alerts flap (fire/resolve repeatedly)","No `for:` duration / noisy metric","Add `for: 5m`, use averaging windows."),
("Dashboards nobody uses","Too many panels, no purpose","One overview dashboard per service: RED/USE, link runbooks and deployments annotations.")],
qa=[("What is `for` in alert rule?","Condition must hold this long before firing."),
("Grouping vs inhibition vs silence?","Group batches alerts; inhibition suppresses dependent alerts; silence mutes temporarily."),
("Grafana provisioning?","Datasources/dashboards as code (YAML/JSON) for reproducibility."),
("How to alert on missing data?","`absent()` or `up == 0`."),
("Predictive alert?","`predict_linear` to catch disk exhaustion early.")]),

dict(slug="logging-elk-loki", title="Centralized Logging (ELK & Loki)", level="Intermediate",
intro="Logs har server par mat dekho, ek jagah collect karo. Structured JSON logs best hain. Loki lightweight (labels index), ELK full-text search.",
diagram="""
Pods/VMs -> agent (Promtail / Fluent Bit / Filebeat) -> Loki | Logstash -> Elasticsearch -> Grafana | Kibana
Structured log: {"ts":"..","level":"error","trace_id":"abc","msg":"db timeout"}
""",
install="""helm repo add grafana https://grafana.github.io/helm-charts
helm install loki grafana/loki-stack -n monitoring --set promtail.enabled=true,grafana.enabled=false""",
examples=[("LogQL queries","""{namespace="prod", app="api"} |= "error"
sum by(app)(rate({namespace="prod"} |= "error" [5m]))
{app="api"} | json | level="error" | line_format "{{.msg}}" """),
("Fluent Bit config snippet","""[INPUT]  Name tail
         Path /var/log/containers/*.log
[FILTER] Name kubernetes
[OUTPUT] Name es
         Host elasticsearch
         Index app-logs""")],
problems=[("Can't correlate logs across services","No request/trace ID","Propagate `trace_id` header, include in every log line."),
("Log storage costs exploding","Debug logs, long retention","Retention policies, drop noisy logs, sample, hot/warm/cold tiers.")],
qa=[("ELK vs Loki?","ELK indexes full text (powerful, heavy); Loki indexes labels only (cheap, simple)."),
("Why structured logging?","Machine-parseable, filterable fields."),
("Sidecar vs DaemonSet log agent?","DaemonSet one per node (efficient); sidecar per pod for special cases."),
("What to never log?","Passwords, tokens, PII."),
("Log rotation?","Prevent disk filling; logrotate or container runtime limits.")]),

dict(slug="tracing-slo", title="Tracing (OpenTelemetry) & SLOs", level="Advanced",
intro="Microservices mein ek request kai services se jaati hai; tracing se bottleneck milta hai. SLO aur error budget se reliability vs feature velocity balance hoti hai.",
diagram="""
Request -> gateway (span) -> orders (span) -> payments (span) -> DB (span)   = one trace_id
OTel SDK -> Collector -> Tempo/Jaeger ; link trace_id in logs & metrics (exemplars)

SLO 99.9% / 30d => error budget 43.2 min. Burn-rate alert: 14.4x over 1h => page
""",
install="""helm repo add open-telemetry https://open-telemetry.github.io/opentelemetry-helm-charts
helm install otel open-telemetry/opentelemetry-collector -n monitoring --set mode=deployment
helm install tempo grafana/tempo -n monitoring""",
examples=[("Python auto-instrumentation","""pip install opentelemetry-distro opentelemetry-exporter-otlp
opentelemetry-bootstrap -a install
OTEL_SERVICE_NAME=orders OTEL_EXPORTER_OTLP_ENDPOINT=http://otel:4317 opentelemetry-instrument python app.py"""),
("Availability SLI and burn-rate alert","""# SLI: good requests / total
sum(rate(http_requests_total{code!~"5.."}[5m])) / sum(rate(http_requests_total[5m]))
# multi-window burn rate for 99.9% SLO
(sum(rate(http_requests_total{code=~"5.."}[1h])) / sum(rate(http_requests_total[1h]))) > (14.4 * 0.001)""")],
problems=[("Latency high but which service?","No tracing","Add OTel; check flame/waterfall for slowest span; N+1 queries are common."),
("Feature team wants speed, SRE wants stability","No shared metric","Error budget policy: budget left -> ship; exhausted -> freeze features, fix reliability.")],
qa=[("What is a span vs trace?","Span is one operation; trace is the tree of spans for a request."),
("What is OpenTelemetry?","Vendor-neutral standard/SDKs/collector for telemetry."),
("Error budget?","Allowed unreliability = 1 - SLO."),
("Sampling strategies?","Head-based (probabilistic) vs tail-based (keep errors/slow)."),
("SLA vs SLO?","SLA is external contract; SLO is internal stricter target.")]),
])
