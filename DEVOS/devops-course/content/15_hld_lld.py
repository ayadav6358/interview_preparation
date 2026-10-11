TOPIC = dict(slug="hld-lld", title="HLD & LLD (Design + Diagrams + Real Examples)", intro="HLD = bird's-eye view (components, flow, decisions). LLD = implementation detail (configs, code, commands). Interview mein 'design a CI/CD platform' jaise sawal aate hain, isliye dono practice karo.", subs=[

dict(slug="how-to-design", title="How to Approach HLD & LLD", level="Basic",
intro="Design sawal ka framework: Requirements -> Constraints -> High-level diagram -> Components -> Data/Traffic flow -> Scale & HA -> Security -> Observability -> Cost -> Trade-offs. HLD mein 'kya aur kyun', LLD mein 'kaise'.",
diagram="""
1 Clarify: functional + non-functional (SLA 99.9%, RPO/RTO, users, budget)
2 HLD   : boxes and arrows, tech choices with WHY
3 LLD   : subnets/CIDR, SG rules, Dockerfile, YAML, pipeline, alerts, runbooks
4 Review: failure modes (what if AZ dies? DB fails? bad deploy?), cost, security
""",
install="# diagram tools: draw.io (diagrams.net), Excalidraw, Mermaid, 'diagrams' python lib",
examples=[("Design answer template","""Requirements -> Architecture diagram -> Component choices -> Scaling -> HA/DR -> Security -> Monitoring -> CI/CD -> Cost -> Trade-offs & risks"""),
("Mermaid example (paste in mermaid.live)","""flowchart LR
  U[User] --> CF[CloudFront] --> ALB --> APP[EKS pods] --> DB[(RDS)]
  APP --> R[(Redis)]""")],
problems=[("Candidate jumps into tools without requirements","-","Always ask: traffic, uptime target, compliance, team size, budget.")],
qa=[("HLD vs LLD?","HLD: architecture, components, interactions. LLD: detailed module/config/schema level design."),
("How do you choose between ECS and EKS?","Team K8s skills, portability, ecosystem needs vs simplicity/ops overhead."),
("What non-functional requirements do you ask?","Availability, latency, throughput, RPO/RTO, security/compliance, cost, scalability."),
("How to show trade-offs?","State options, criteria, chosen option and why, risks and mitigations."),
("How do you handle single point of failure?","Redundancy across AZs, health checks, failover, avoiding shared fate.")]),

dict(slug="hld-3tier-aws", title="HLD 1: Highly Available 3-Tier Web App on AWS", level="Intermediate",
intro="Sabse common design: users -> CDN -> ALB -> app tier (ASG/EKS) -> DB (Multi-AZ) with cache and object storage.",
diagram="""
                     Users
                       |
              Route53 (DNS, health checks)
                       |
          CloudFront (CDN) + WAF   ----> S3 (static assets)
                       |
   ┌────────────── VPC 10.0.0.0/16 ────────────────────────────┐
   │  AZ-a                          AZ-b                       │
   │ [Public]  ALB  NAT-a           [Public]  ALB  NAT-b       │
   │ [Private] App EC2/EKS  ───┐    [Private] App EC2/EKS ──┐  │
   │                           ├──> ElastiCache Redis       │  │
   │ [DB]  RDS Primary <==sync==> RDS Standby (Multi-AZ)    │  │
   └───────────────────────────────────────────────────────────┘
   Cross-cutting: IAM roles, SG per tier, CloudWatch, CloudTrail, KMS, Secrets Manager, S3 backups
""",
install="# implement with Terraform (see Terraform topic: VPC + EKS + RDS)",
examples=[("Design decisions & why","""CDN+WAF: latency, DDoS/OWASP protection
ALB in public subnets, app in private: no direct internet access to compute
Multi-AZ everywhere: survive AZ failure (RTO minutes)
Redis: reduce DB load, session store
RDS Multi-AZ + PITR backups: RPO ~5 min
ASG target tracking 50% CPU: elastic scale
VPC endpoints: private S3/ECR access, lower NAT cost"""),
("Capacity & cost sketch","""Traffic 500 rps peak -> 4x t3.large (2/AZ), db.m6g.large Multi-AZ, cache.t3.medium
Estimate via AWS Pricing Calculator; add Savings Plan after 1 month baseline""")],
problems=[("AZ outage takes site down","All instances in one AZ / single NAT","Spread ASG across 2-3 AZ, NAT per AZ, Multi-AZ DB, test failover."),
("Traffic spike overloads DB","No cache, no read replica","Cache-aside with Redis, read replicas, RDS Proxy, rate limiting at WAF/ALB.")],
qa=[("How do you make this design survive a region failure?","Cross-region replication (S3 CRR, Aurora Global), Route53 failover, IaC to rebuild, warm standby region."),
("Where do sessions live?","Stateless app: JWT or Redis; avoid sticky sessions."),
("How do deployments happen without downtime?","Rolling/blue-green via ASG instance refresh or CodeDeploy/ArgoCD."),
("How to secure the DB?","Private subnet, SG only from app SG, encryption at rest (KMS) and in transit, IAM auth/secrets rotation."),
("How to scale the DB writes?","Vertical scale, sharding, or move to Aurora/DynamoDB depending on access patterns.")]),

dict(slug="hld-cicd-gitops-platform", title="HLD 2: End-to-End CI/CD + GitOps Platform", level="Advanced",
intro="Developer push se production tak. Build once, scan, sign, deploy via GitOps, observe and rollback.",
diagram="""
Dev -> GitHub (PR, checks, CODEOWNERS)
        |
   GitHub Actions (OIDC)  ── test -> SAST -> build image -> Trivy -> cosign -> push ECR
        |
   update image tag in GitOps repo (PR/auto-commit)
        |
   ArgoCD (per cluster) ── sync ──> EKS dev -> staging -> prod (canary via Argo Rollouts)
        |
   Prometheus/Grafana/Loki ── SLO alerts ── PagerDuty ; auto-rollback on failed analysis
Infra: Terraform (VPC, EKS, IAM, ECR) via separate pipeline + policy checks (Checkov/OPA)
Secrets: Vault/Secrets Manager + External Secrets
""",
install="# Implementation: LLD pages 'CI pipeline', 'Terraform', 'Kubernetes manifests'",
examples=[("Key decisions","""GitOps pull model: cluster creds never leave cluster
Separate app repo and config repo: clean audit trail, different permissions
Immutable tags (git sha) + image digest pinning
Progressive delivery with automated metric analysis
Promotion via PR between env folders"""),
("Failure modes","""Bad image -> caught by scan gate | Bad config -> canary aborts, ArgoCD rollback
ArgoCD down -> running workloads unaffected, deployments pause | GitHub down -> hotfix via break-glass procedure""")],
problems=[("Prod and Git state diverge","Manual kubectl edits","selfHeal on, restrict kubectl write RBAC, all changes via PR."),
("Pipeline is single point of failure","Only one runner/instance","HA runners, autoscaled ephemeral runners, documented break-glass path.")],
qa=[("Why separate config repo?","Different lifecycle/permissions, clean deploy history, avoids CI loops."),
("How to promote dev->prod?","PR changing tag/values in prod overlay with approval, or automated promotion after checks."),
("How do you ensure only trusted images run?","cosign signatures + admission policy (Kyverno/Sigstore policy-controller)."),
("How to rollback?","Revert Git commit or Argo Rollouts abort; ArgoCD syncs previous state."),
("How to secure the pipeline?","OIDC, least-privilege, pinned actions, isolated runners, scan everything, protected branches.")]),

dict(slug="hld-observability-platform", title="HLD 3: Observability & Alerting Platform", level="Advanced",
intro="Central monitoring for many services/clusters: metrics, logs, traces, alerts with SLOs.",
diagram="""
Apps (OTel SDK) ──> OTel Collector ──┬─> Prometheus/Mimir (metrics) ─┐
Pods logs ──> Promtail/Fluent Bit ───┼─> Loki (logs)                 ├─> Grafana (dashboards, explore)
Traces ──────────────────────────────┴─> Tempo (traces)             ─┘
Prometheus rules ──> Alertmanager ──> PagerDuty (page) / Slack (warn) / Jira (ticket)
Long-term: object storage (S3) backend, retention tiers ; Blackbox exporter for external probes
""",
install="# helm: kube-prometheus-stack, loki, tempo, otel-collector (see Monitoring topic)",
examples=[("Sizing & retention example","""Prometheus 15d local + remote_write to Mimir 13 months
Loki 14d hot, S3 90d ; Traces 7d with tail-sampling (errors+slow 100%, rest 5%)"""),
("SLO dashboard contents","""SLI availability + latency p95, error budget remaining, burn rate, deploy markers, top failing endpoints""")],
problems=[("Monitoring itself goes down during outage","Same cluster/failure domain","Run monitoring in separate cluster/account, external synthetic checks, dead-man's-switch alert.")],
qa=[("How to monitor 50 clusters?","Federation/remote_write to central Mimir/Thanos, per-cluster agents (Grafana Agent/OTel)."),
("How to reduce alert noise?","SLO burn-rate alerts, grouping, inhibition, ownership routing, regular alert review."),
("What is dead-man's-switch?","Always-firing alert that pages when it stops, proving alerting pipeline works."),
("Cardinality control?","Label hygiene, relabel drop, limits."),
("Cost control of logs?","Sampling, retention tiers, drop debug in prod.")]),

dict(slug="lld-vpc-cidr-sg", title="LLD 1: VPC Subnets, CIDR & Security Group Rules", level="Intermediate",
intro="HLD ka network ab exact numbers ke saath.",
diagram="""
VPC 10.0.0.0/16
 public-a  10.0.1.0/24  (ALB, NAT-a)      public-b  10.0.2.0/24 (ALB, NAT-b)
 private-a 10.0.11.0/24 (app/EKS nodes)   private-b 10.0.12.0/24
 db-a      10.0.21.0/24 (RDS)             db-b      10.0.22.0/24

RT public : 0.0.0.0/0 -> IGW
RT private: 0.0.0.0/0 -> NAT (same AZ)
RT db     : local only
""",
install="# Terraform module vpc (Terraform topic)",
examples=[("Security group matrix","""sg-alb : in 443 from 0.0.0.0/0 ; out all
sg-app : in 3000 from sg-alb ; out 5432 to sg-db, 6379 to sg-redis, 443 to 0.0.0.0/0 (via NAT)
sg-db  : in 5432 from sg-app ; no outbound needed
sg-bastion/SSM: prefer SSM Session Manager, no inbound 22"""),
("Terraform SG snippet","""resource "aws_security_group_rule" "db_from_app" {
  type = "ingress"  from_port = 5432  to_port = 5432  protocol = "tcp"
  security_group_id        = aws_security_group.db.id
  source_security_group_id = aws_security_group.app.id
}""")],
problems=[("App can't reach RDS","SG on DB missing rule from app SG","Check SG reference, route, DB endpoint DNS, `nc -zv db 5432` from app.")],
qa=[("Why reference SG instead of CIDR?","Follows instances as they scale; tighter."),
("Why NAT per AZ?","Avoid cross-AZ dependency and data charges; AZ failure isolation."),
("How many IPs does AWS reserve per subnet?","5."),
("How do private instances get patches?","NAT or VPC endpoints/mirror repo."),
("NACL use case?","Coarse subnet-level deny (e.g. block an IP range).")]),

dict(slug="lld-cicd-pipeline", title="LLD 2: CI Pipeline, Dockerfile & Deploy Config", level="Intermediate",
intro="Exact GitHub Actions workflow, Dockerfile aur GitOps tag update ka implementation.",
diagram="""
push main -> checkout -> test -> trivy fs -> OIDC assume role -> buildx -> trivy image -> push ECR(sha)
          -> yq set image.tag in gitops repo -> git push (bot) -> ArgoCD syncs
""",
install="# secrets: none for AWS (OIDC). GITOPS_TOKEN fine-grained PAT or GitHub App for config repo",
examples=[("Workflow","""name: ci
on: { push: { branches: [main] }, pull_request: }
permissions: { id-token: write, contents: read }
env: { REGION: ap-south-1, REPO: myapp }
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci && npm test
      - uses: aquasecurity/trivy-action@master
        with: { scan-type: fs, severity: 'HIGH,CRITICAL', exit-code: '1' }
      - uses: aws-actions/configure-aws-credentials@v4
        with: { role-to-assume: "arn:aws:iam::123456789012:role/gha-ecr", aws-region: "${{ env.REGION }}" }
      - id: ecr
        uses: aws-actions/amazon-ecr-login@v2
      - name: Build, scan, push
        run: |
          IMG=${{ steps.ecr.outputs.registry }}/$REPO:${{ github.sha }}
          docker build -t $IMG .
          trivy image --exit-code 1 --severity CRITICAL $IMG
          [ "${{ github.ref }}" = "refs/heads/main" ] && docker push $IMG || true
  deploy-config:
    if: github.ref == 'refs/heads/main'
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { repository: acme/gitops, token: "${{ secrets.GITOPS_TOKEN }}" }
      - run: |
          yq -i '.image.tag = "${{ github.sha }}"' charts/myapp/values-dev.yaml
          git config user.name bot && git config user.email bot@acme.io
          git commit -am "myapp: ${{ github.sha }}" && git push"""),
("IAM trust policy for OIDC","""{
 "Effect":"Allow","Principal":{"Federated":"arn:aws:iam::123456789012:oidc-provider/token.actions.githubusercontent.com"},
 "Action":"sts:AssumeRoleWithWebIdentity",
 "Condition":{"StringLike":{"token.actions.githubusercontent.com:sub":"repo:acme/myapp:ref:refs/heads/main"}}
}""")],
problems=[("Pipeline can assume role from any repo/branch","Trust policy too broad","Restrict `sub` claim to repo and branch/environment.")],
qa=[("Why tag with git sha?","Immutable, traceable to code."),
("Why OIDC?","No long-lived secrets, short-lived credentials, scoped by repo/branch."),
("How to speed up builds?","Layer caching (buildx gha cache), dependency caching, parallel jobs."),
("How to prevent deploying unscanned image?","Gate build on scan; admission controller verifying signatures."),
("Where is approval enforced?","GitHub Environment protection for prod or PR approval on config repo.")]),

dict(slug="lld-k8s-app-manifests", title="LLD 3: Kubernetes App Manifests (Production Grade)", level="Advanced",
intro="Deployment + Service + Ingress + HPA + PDB + NetworkPolicy + ServiceAccount: production checklist wala YAML.",
diagram="""
Ingress(host) -> Service -> Deployment(3 pods, probes, limits, non-root, spread across zones)
HPA 3..15 (CPU 70%) | PDB minAvailable 2 | NetworkPolicy: only ingress-nginx -> app ; app -> db
""",
install="kubectl apply -f app.yaml -n prod   # or via Helm chart / ArgoCD",
examples=[("Production Deployment","""apiVersion: apps/v1
kind: Deployment
metadata: { name: myapp, namespace: prod }
spec:
  replicas: 3
  strategy: { type: RollingUpdate, rollingUpdate: { maxSurge: 1, maxUnavailable: 0 } }
  selector: { matchLabels: { app: myapp } }
  template:
    metadata: { labels: { app: myapp } }
    spec:
      serviceAccountName: myapp
      securityContext: { runAsNonRoot: true, seccompProfile: { type: RuntimeDefault } }
      topologySpreadConstraints:
      - { maxSkew: 1, topologyKey: topology.kubernetes.io/zone, whenUnsatisfiable: ScheduleAnyway, labelSelector: { matchLabels: { app: myapp } } }
      terminationGracePeriodSeconds: 30
      containers:
      - name: myapp
        image: 123456789012.dkr.ecr.ap-south-1.amazonaws.com/myapp:abc123
        ports: [{ containerPort: 3000 }]
        envFrom: [{ secretRef: { name: myapp-secrets } }]
        resources: { requests: { cpu: 200m, memory: 256Mi }, limits: { memory: 512Mi } }
        readinessProbe: { httpGet: { path: /ready, port: 3000 }, periodSeconds: 5 }
        livenessProbe:  { httpGet: { path: /health, port: 3000 }, initialDelaySeconds: 15 }
        lifecycle: { preStop: { exec: { command: ["sleep","10"] } } }
        securityContext: { allowPrivilegeEscalation: false, readOnlyRootFilesystem: true, capabilities: { drop: [ALL] } }"""),
("NetworkPolicy allowing only ingress controller","""apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: { name: myapp-allow-ingress, namespace: prod }
spec:
  podSelector: { matchLabels: { app: myapp } }
  policyTypes: [Ingress]
  ingress:
  - from: [{ namespaceSelector: { matchLabels: { kubernetes.io/metadata.name: ingress-nginx } } }]
    ports: [{ port: 3000 }]""")],
problems=[("502 errors during rollout","Traffic sent to terminating pods","preStop sleep + readiness + grace period so LB deregisters first.")],
qa=[("Why memory limit but no CPU limit?","CPU limits cause throttling; memory is incompressible so limit prevents node OOM."),
("Why readOnlyRootFilesystem?","Stops attackers writing binaries; mount emptyDir for temp."),
("What does maxUnavailable: 0 ensure?","Old pods removed only after new are ready."),
("Why topology spread?","Survive AZ failure."),
("Why ServiceAccount per app?","Least-privilege RBAC and IRSA mapping.")]),

dict(slug="lld-monitoring-alerts-runbook", title="LLD 4: Alert Rules, Dashboards & Runbook", level="Advanced",
intro="Exact alert rules, dashboard panels aur runbook jo on-call engineer follow karega.",
diagram="""
Alert HighErrorRate -> runbook: 1 check deploy 2 check dependency 3 rollback 4 escalate
Dashboard rows: Traffic | Errors | Latency p50/p95/p99 | Saturation (CPU, mem, pods) | Dependencies (DB, cache)
""",
install="# apply as PrometheusRule CRD (kube-prometheus-stack)",
examples=[("PrometheusRule","""apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata: { name: myapp, namespace: monitoring, labels: { release: mon } }
spec:
  groups:
  - name: myapp.slo
    rules:
    - alert: MyAppHighErrorRate
      expr: sum(rate(http_requests_total{app="myapp",code=~"5.."}[5m])) / sum(rate(http_requests_total{app="myapp"}[5m])) > 0.02
      for: 5m
      labels: { severity: page, team: backend }
      annotations: { summary: "myapp 5xx > 2%", runbook_url: "https://wiki/runbooks/myapp-5xx" }
    - alert: MyAppLatencyHigh
      expr: histogram_quantile(0.95, sum by(le)(rate(http_request_duration_seconds_bucket{app="myapp"}[5m]))) > 0.5
      for: 10m
      labels: { severity: ticket }
    - alert: PodCrashLooping
      expr: increase(kube_pod_container_status_restarts_total{namespace="prod"}[15m]) > 3
      for: 5m
      labels: { severity: page }"""),
("Runbook: HighErrorRate","""1. Grafana dashboard 'myapp overview': when did it start? Deploy annotation near start?
2. YES -> rollback: argocd app rollback myapp-prod (or git revert) -> verify errors drop
3. NO  -> check dependencies (RDS CPU/connections, Redis), recent infra changes, traffic spike
4. kubectl -n prod logs deploy/myapp --since=15m | grep -i error
5. Scale up if saturation, enable maintenance/feature-flag off if needed
6. Escalate to backend on-call after 15 min without progress; post updates every 15 min
7. Postmortem within 48h""")],
problems=[("Alert fires but nobody knows what to do","No runbook","Every page-level alert must link a tested runbook.")],
qa=[("What makes a good alert?","Actionable, symptom-based, has runbook, correct severity/owner."),
("How to test alerts?","Fire in staging via fault injection, `promtool test rules`."),
("What to include in a runbook?","Impact, diagnosis steps, mitigation, escalation, related dashboards/commands."),
("What is alert routing by team label?","Alertmanager routes to owner's channel/pager."),
("How to review alert quality?","Track pages per week, ack time, % non-actionable; prune regularly.")]),

dict(slug="real-problem-walkthroughs", title="Real Problem Walkthroughs (Scenario Practice)", level="Advanced",
intro="Interview aur job mein aane wale real scenarios: symptom -> investigation steps -> fix -> prevention.",
diagram="""
Method: Symptom -> Scope (who/what/since when) -> Recent change? -> Golden signals -> Hypothesis -> Test -> Mitigate -> Fix -> Prevent
""",
install="# practice in a kind cluster / free-tier AWS by deliberately breaking things",
examples=[("Scenario 1: Site slow after deploy","""Scope: p95 latency 3s, errors normal, started 10:05 = deploy time
Check: Grafana latency by endpoint -> /search slow; traces show DB query 2.5s
Cause: new query missing index (EXPLAIN ANALYZE shows seq scan)
Mitigate: rollback | Fix: CREATE INDEX CONCURRENTLY | Prevent: query perf test in CI, slow query alert"""),
("Scenario 2: Pods CrashLoopBackOff after config change","""logs --previous: 'DB_HOST undefined'
Cause: ConfigMap key renamed but Deployment still references old key
Fix: correct env mapping, roll out | Prevent: helm template + kubeconform in CI, staging deploy gate"""),
("Scenario 3: Disk full on server at 3 AM","""df -h -> /var 100% ; du -xh /var | sort -h -> /var/log/app 40G
Cause: no log rotation + debug logging enabled
Fix: truncate/compress logs, add logrotate, set log level info | Prevent: disk alert at 80%, predict_linear alert"""),
("Scenario 4: Terraform apply wants to destroy the database","""Plan shows '-/+ aws_db_instance' due to changed identifier
Action: STOP. Use prevent_destroy, revert change or moved block; check snapshot exists
Prevent: PR plan review, policy check blocking destroy of prod DB"""),
("Scenario 5: AWS bill jumped 3x","""Cost Explorer group by service/usage type -> NAT Gateway data processing spike
Cause: pods pulling images/S3 via NAT | Fix: VPC endpoints, ECR pull-through cache
Prevent: budgets + anomaly detection, tags""")],
problems=[("Panic in incident","No process","Use the method above and incident roles; mitigate first.")],
qa=[("Website is down, what do you check first?","DNS -> LB health -> app pods/instances -> dependencies (DB/cache) -> recent deploys -> logs/metrics."),
("Pod is Pending, why?","Insufficient resources, taints, PVC unbound, node selector mismatch; see describe events."),
("How do you reduce deployment risk?","Small changes, feature flags, canary, automated tests/analysis, easy rollback."),
("How to find cost anomalies?","Cost Explorer/Anomaly Detection, tags, usage type breakdown."),
("How do you handle a leaked secret?","Rotate immediately, audit usage, remove from history, add scanning, root-cause the process gap.")]),
])
