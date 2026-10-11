EXT = dict(
guide=dict(
bigpicture=dict(
problem="""**Problem it solves:** In senior interviews and real projects you are asked to *design* a system, not just use a tool: "Design a highly available web app on AWS", "Design a CI/CD platform". A good answer needs a repeatable method. **HLD (High-Level Design)** shows the big picture: components, flow and technology choices with reasons. **LLD (Low-Level Design)** shows the implementation detail: CIDRs, security group rules, YAML, pipeline, alerts, runbooks.""",
chain=["PROBLEM: 'design X' questions and real architecture decisions are open-ended",
       "TRADITIONAL APPROACH: jump straight to tools or draw random boxes",
       "PAIN: missing requirements, no failure thinking, unjustified choices, cannot implement the design",
       "TECHNOLOGY: a design framework (requirements > HLD > LLD > review) with diagrams and trade-offs",
       "SOLUTION: clarify needs, draw components, justify choices, then specify exact configuration",
       "REAL-WORLD BENEFIT: clear, defensible designs that teams can build and operate"],
text="""HLD answers **what and why** (components, data flow, scaling, HA, security, cost). LLD answers **how** (exact subnets, rules, manifests, commands). Always finish with **failure modes** and **trade-offs**: seniors are judged on these."""),
e2e=dict(diagram="""1. Clarify requirements
   functional (what it does) + non-functional (users, RPS, SLA 99.9%, RPO/RTO, compliance, budget)
   v
2. Constraints and assumptions (team skills, cloud, deadlines)
   v
3. HLD: boxes and arrows, technology choices with WHY
   v
4. Data/traffic flow + deployment flow (request path, CI/CD path)
   v
5. Scale + HA + DR (autoscaling, Multi-AZ, backup, failover)
   v
6. Security + observability + cost
   v
7. LLD: CIDR/SG/YAML/pipeline/alerts/runbooks
   v
8. Failure analysis (AZ down? DB down? bad deploy? traffic spike?)
   v
9. Trade-offs, risks, alternatives, next steps""",
text="""Start by **asking questions**: expected users and traffic, uptime target, data sensitivity, budget and team skills. Turn answers into numbers (for example 99.9 percent means about 43 minutes downtime per month). Draw the **HLD** and explain each choice ("ALB because HTTP path routing and health checks"). Describe the **request flow** and the **deployment flow**. Then explicitly cover **scaling, high availability, disaster recovery, security, observability and cost**. Drop to **LLD** for the critical parts on request: subnet plan, security group chaining, Kubernetes manifests, pipeline. Finish by walking through **failure scenarios** and stating **trade-offs** honestly."""),
tools=dict(rows=[
["draw.io / Excalidraw / Mermaid", "Diagrams", "Design ideas", "Architecture diagrams", "HLD and documentation"],
["Terraform / CloudFormation", "Implement infrastructure design", "LLD spec", "Real infrastructure", "After design approval"],
["Kubernetes YAML / Helm", "Implement workload design", "LLD manifests", "Running app", "Application layer"],
["CI/CD (GitHub Actions/Jenkins/ArgoCD)", "Implement delivery design", "Pipeline definition", "Automated releases", "Delivery"],
["Prometheus/Grafana/Alertmanager", "Implement observability design", "Alert rules, dashboards", "Visibility + pages", "Operations"],
["Well-Architected Framework / ADRs", "Review and record decisions", "Design + questions", "Improved design, decision log", "Governance"]],
why="**Diagram-as-code (Mermaid) vs GUI tools:** Mermaid lives in Git and is reviewable; draw.io is faster for rich visuals. **ADR (Architecture Decision Record)** documents *why* a choice was made so future teams understand trade-offs."),
compare=[
("HLD vs LLD", ["Topic", "HLD", "LLD"], [["Focus", "Components, flow, decisions", "Exact configuration and code"], ["Audience", "Architects, stakeholders, interviewers", "Engineers implementing/operating"], ["Example", "ALB > ASG > RDS Multi-AZ", "10.0.10.0/24, SG rules, YAML"], ["Changes", "Rare", "Frequent"]]),
("Vertical vs Horizontal scaling", ["Topic", "Vertical", "Horizontal"], [["How", "Bigger machine", "More machines"], ["Limit", "Hardware ceiling, downtime", "Needs stateless design"], ["HA", "Single point of failure", "Redundancy built in"]]),
("Active-Passive vs Active-Active", ["Topic", "Active-Passive", "Active-Active"], [["Traffic", "Standby idle until failover", "All sites serve traffic"], ["Cost", "Lower", "Higher"], ["Failover", "Takes time", "Near instant, complex data sync"]]),
("Monolith vs Microservices", ["Topic", "Monolith", "Microservices"], [["Deploy", "One unit", "Independent units"], ["Complexity", "Simple ops", "Distributed system complexity"], ["Good for", "Small teams/early stage", "Large orgs, independent scaling"]]),
("Sync vs Async communication", ["Topic", "Sync (HTTP/gRPC)", "Async (queue/events)"], [["Coupling", "Tight", "Loose"], ["Latency", "Immediate response", "Eventual"], ["Failure", "Cascades", "Buffered/retried"]]),
("RPO vs RTO", ["Term", "Meaning"], [["RPO", "Max tolerable data loss (time)"], ["RTO", "Max tolerable downtime"]])],
troubleshooting=[
("Design has a single point of failure", "One instance/AZ/NAT/database without redundancy", "Walk the diagram asking 'what if this fails?' for every box", "Add redundancy (multi-AZ, replicas, multiple NATs/LBs), automatic failover.", "Failure-mode review as part of every design."),
("Design cannot scale for peak", "Stateful servers, DB bottleneck, no caching/queue", "Estimate RPS and data size; find the narrowest component", "Stateless app + autoscaling, cache, read replicas, async processing, CDN.", "Load test against the design assumptions."),
("Security groups too open", "0.0.0.0/0 rules, shared SG for all tiers", "Review SG/NACL/IAM in LLD", "Chain SGs (ALB > app > DB), private subnets, least-privilege IAM roles.", "IaC scanning and design review checklist."),
("Cost overruns after launch", "Over-provisioned instances, NAT data, cross-AZ traffic, idle environments", "Cost model per component; Cost Explorer by tag", "Rightsize, VPC endpoints, schedules, commitments, caching.", "Cost estimate in the design doc; budgets."),
("Design works on paper but ops cannot run it", "Too complex, no observability/runbooks, unfamiliar tech", "Ask 'who will run this at 3am and how?'", "Simplify, add dashboards/alerts/runbooks, train, prefer managed services.", "Include operations in design review."),
("Diagram unclear in interview", "Too many boxes, no flow, no labels", "Ask if a stranger could follow the request path", "Number the steps, label ports/protocols, separate HLD and LLD views.", "Practise a consistent diagram style.")],
practices={
"Development": ["Write short design docs and ADRs; keep diagrams in Git (Mermaid)."],
"Production": ["Multi-AZ; stateless services; managed services where sensible; IaC for every LLD element; runbooks."],
"Security": ["Least privilege, private subnets for data, encryption in transit/at rest, WAF, secrets in a manager, audit logs."],
"Performance": ["Cache, CDN, async processing, right database choice, load testing."],
"Reliability": ["Define SLOs and RPO/RTO; health checks, autoscaling, graceful degradation, DR tested."],
"Cost Optimization": ["Cost per component in the design; commitments/spot/serverless where fit; lifecycle policies."],
"Monitoring & Logging": ["Golden signals per tier, central logs, tracing, alerts tied to SLOs with runbooks."],
"Backup & Disaster Recovery": ["Backup + PITR for data stores, cross-region copies, DR strategy chosen by RPO/RTO, regular drills."]},
mistakes={
"Beginner mistakes": ["Starting with tools instead of requirements.", "Drawing boxes with no request flow."],
"Developer mistakes": ["Ignoring operations and failure handling.", "Tight coupling through synchronous chains."],
"DevOps mistakes": ["Over-engineering (Kubernetes for a static site).", "No cost or security consideration."],
"Production mistakes": ["Single AZ/NAT/DB.", "No tested restore or failover."],
"Security mistakes": ["Public databases, wide-open SGs, shared IAM users."]},
versions=[
"Cloud services, limits and prices change: verify service quotas (for example subnets per VPC, ALB limits) and pricing on the provider's documentation before finalising an LLD.",
"AWS reserves 5 IP addresses per subnet; other clouds reserve a different number.",
"Kubernetes API versions (`apps/v1`, `networking.k8s.io/v1`, `autoscaling/v2`) differ across cluster versions: validate manifests against your cluster (`kubectl apply --dry-run=server`).",
"Managed offering names differ by cloud (EKS/AKS/GKE, RDS/Cloud SQL/Azure DB)."],
hinglish="""**HLD = bade boxes aur flow (kya aur kyun)**, **LLD = exact configuration (kaise)**. Design sawal aaye to pehle **requirements poochho** (users, uptime, budget, data), phir HLD banao, phir **scaling, HA, security, monitoring, cost** cover karo aur last mein **failure scenarios** aur **trade-offs** batao. Kisi bhi box ke liye poochho: "**ye fail ho gaya to kya hoga?**" Har technology choice ke saath **kyun** batana zaroori hai.""",
mnemonics=[("Design answer order", "R-C-H-C-D-S-S-O-C-T: Requirements, Constraints, HLD, Components, Data flow, Scale/HA, Security, Observability, Cost, Trade-offs"), ("Failure questions", "What if AZ, DB, deploy, dependency, or traffic spike fails?"), ("Nines", "99.9% = ~43 min/month; 99.99% = ~4.3 min/month"), ("HLD vs LLD", "What/Why vs How")],
client=dict(
s30="""A good design starts from your business needs: how many users, how much downtime you can tolerate, what data must be protected, and your budget. We then propose an architecture, explain every choice, and specify exactly how to build and operate it.""",
m2="""We begin by agreeing requirements: expected traffic, availability targets, recovery objectives and compliance needs. From these we create a high-level design showing the main components, how requests flow, how the system scales and how it survives failures. We then produce low-level specifications, such as network ranges, firewall rules, deployment files and alert definitions, so the engineering team can implement it consistently through infrastructure as code. We review the design against failure scenarios, security and cost, and document the trade-offs so decisions are transparent and can be revisited as the business grows.""",
m5="""I will describe our approach in five steps. **Requirements:** we quantify availability, performance, data protection and budget, for instance a 99.9 percent SLO with an RPO of five minutes. **High-level design:** we choose components, for example CDN, load balancer, stateless application tier, managed database with standby, cache and queues, and show request and deployment flows with the reasoning for each choice. **Resilience and scale:** multi-zone deployment, autoscaling, backups and a disaster recovery strategy matched to your recovery objectives. **Low-level design:** address plan, security group chaining, Kubernetes manifests with probes, limits and network policies, the CI/CD and GitOps pipeline, and the alert rules and runbooks the on-call team will use. **Review:** we walk through failure scenarios, security and cost, list risks and alternatives, and record decisions in short architecture decision records. This gives you a design that is understandable, buildable and operable."""),
roadmap=[
("Beginner", ["Requirements gathering (functional vs non-functional)", "Basic cloud building blocks (VPC, LB, compute, DB)", "Reading and drawing architecture diagrams"]),
("Intermediate", ["Design 3-tier HA app", "CI/CD pipeline design", "Observability design", "CIDR/SG design"]),
("Advanced", ["Multi-region DR, active-active", "Microservices, async messaging, caching strategies", "Security architecture (zero trust)", "Capacity planning and cost modelling"]),
("Production", ["Architecture Decision Records", "Well-Architected reviews", "Game days and failure testing", "Documentation and runbooks"]),
("Interview", ["Practise 5 standard designs aloud", "Failure and trade-off discussion", "Estimate capacity/availability numbers", "Walk through LLD details on demand"])],
miniproject=dict(title="Design and specify: HA 3-tier web app on AWS with CI/CD and monitoring",
arch="""Users --> Route 53 --> CloudFront+WAF --> ALB (public subnets, 2 AZ)
        --> EKS/ASG app tier (private subnets) --> RDS Multi-AZ (isolated) + Redis + S3
CI/CD: GitHub > Actions (build, scan, sign) > ECR > ArgoCD > EKS
Observability: Prometheus/Grafana/Loki, alerts > Alertmanager > PagerDuty ; CloudTrail/GuardDuty""",
steps=[
("Step 1: Requirements (quantified)", """Users: 50k daily, peak 500 RPS
Availability SLO: 99.9% (~43 min/month)
RPO 5 min, RTO 30 min
Data: PII (encrypt, audit)
Budget: moderate; team of 6 knows Kubernetes
Assumptions: single region (ap-south-1) with backup copies to a second region""", "Turning vague goals into numbers drives every later decision. State assumptions explicitly so the interviewer/stakeholder can correct them."),
("Step 2: HLD flow and choices", """1 User > Route 53 (DNS, health-checked)
2 CloudFront + WAF (cache static, block attacks, TLS)
3 ALB in 2 public subnets (L7 routing, health checks)
4 App on EKS (stateless pods, HPA) in private subnets
5 RDS PostgreSQL Multi-AZ (primary + standby) in isolated subnets
6 Redis for cache/sessions; S3 for uploads
7 SQS + workers for async jobs
Why: managed services reduce ops; stateless tier scales horizontally; Multi-AZ meets 99.9%""", "Each box has a reason. The request flow is numbered so it can be explained in order. State what you did NOT choose and why (for example DynamoDB: relational data and transactions fit PostgreSQL)."),
("Step 3: LLD: network and security", """VPC 10.0.0.0/16
public  a/b: 10.0.0.0/24, 10.0.1.0/24     (ALB, NAT)
app     a/b: 10.0.10.0/24, 10.0.11.0/24   (EKS nodes)
db      a/b: 10.0.20.0/24, 10.0.21.0/24   (RDS)
alb-sg : in 443 from 0.0.0.0/0
app-sg : in 8080 from alb-sg
db-sg  : in 5432 from app-sg
NAT gateway per AZ; S3/ECR VPC endpoints; flow logs on""", "Exact address plan and SG chaining. One NAT per AZ avoids cross-AZ dependency; endpoints reduce NAT cost and keep traffic private. (AWS reserves 5 addresses per subnet.)"),
("Step 4: Failure analysis and trade-offs", """AZ-a down       -> ALB stops sending to AZ-a targets; HPA/ASG keep capacity in AZ-b; RDS fails over (~1-2 min)
DB primary fail -> Multi-AZ automatic failover; app retries with backoff
Bad deploy      -> readiness fails, rolling update halts; argocd rollback / git revert
Traffic spike   -> CloudFront cache, HPA + node autoscaling, queue absorbs writes
Region outage   -> restore from cross-region backups (RTO 30 min needs runbook + IaC), upgrade to warm standby if RTO tightens
Trade-offs: EKS gives portability but more ops than ECS; Multi-AZ RDS doubles DB cost; single region accepted for cost""", "Seniors are judged on this section. Every failure has a detection, an automatic or manual response and a measurable time. Trade-offs are stated honestly with the option to upgrade later.")]),
interview=[
("Beginner", "What is HLD?", "High-Level Design: the overall architecture showing major components, their relationships, data flow and technology choices.", "Basics.", "Boxes and arrows of a 3-tier app."),
("Beginner", "What is LLD?", "Low-Level Design: detailed implementation specs such as network ranges, configuration files, schemas and code structure.", "Basics.", "Subnet CIDRs and SG rules."),
("Beginner", "What are functional vs non-functional requirements?", "Functional describe what the system does; non-functional describe qualities: performance, availability, security, cost.", "Requirement gathering.", "Login vs 99.9% uptime."),
("Beginner", "What is a single point of failure?", "A component whose failure stops the whole system.", "Reliability.", "One database instance."),
("Beginner", "What is high availability?", "Designing so the system stays operational despite component failures, typically through redundancy and failover.", "Core goal.", "Multi-AZ."),
("Beginner", "Why use a load balancer?", "Distributes traffic, performs health checks and hides individual server failures.", "Basic building block.", "ALB in front of app servers."),
("Beginner", "What is a CDN?", "A network of edge servers caching content close to users.", "Performance.", "CloudFront."),
("Beginner", "What is caching in design?", "Storing frequently accessed data in fast storage to cut latency and load.", "Performance.", "Redis in front of DB."),
("Beginner", "What is scalability?", "Ability to handle growth by adding resources (vertical or horizontal).", "Core goal.", "Autoscaling group."),
("Beginner", "What is a diagram used for in design?", "To communicate components and flows clearly among stakeholders.", "Communication.", "draw.io/Mermaid."),
("Intermediate", "Give a framework for answering a design question.", "Clarify requirements, state constraints/assumptions, HLD, components with reasons, data flow, scale/HA/DR, security, observability, cost, failure modes, trade-offs.", "Interview technique.", "See e2e diagram."),
("Intermediate", "Design a highly available 3-tier web app on AWS.", "Route 53, CloudFront/WAF, ALB across 2 AZs, ASG/EKS in private subnets, RDS Multi-AZ, Redis, S3, NAT per AZ, SG chaining, monitoring, backups.", "Most common design.", "See mini project."),
("Intermediate", "How do you calculate availability from SLO?", "Downtime = (1 - SLO) x period: 99.9% is about 43 minutes per 30 days; 99.99% about 4.3 minutes.", "Numbers matter.", "Explain nines to business."),
("Intermediate", "Vertical vs horizontal scaling?", "Vertical adds power to one machine (limits, downtime); horizontal adds machines (needs stateless design, gives redundancy).", "Scaling choice.", "Stateless web tier."),
("Intermediate", "How do you make an app stateless?", "Externalise state: sessions in Redis/DB/JWT, files in S3, config via environment.", "Design for scale.", "Move uploads to S3."),
("Intermediate", "How to design security groups for 3 tiers?", "ALB SG allows 443 from internet; app SG allows app port only from ALB SG; DB SG allows DB port only from app SG.", "Least privilege.", "SG referencing SG."),
("Intermediate", "Sync vs async communication?", "Sync gives immediate answers but couples services; async decouples and buffers via queues/events.", "Architecture.", "Email sending via SQS."),
("Intermediate", "Design a CI/CD platform.", "Git > CI (build/test/scan/sign) > registry > GitOps repo > ArgoCD > Kubernetes with progressive delivery, secrets management, observability and rollback.", "DevOps design.", "See HLD 2."),
("Intermediate", "What is RPO/RTO and how does it drive DR design?", "RPO limits data loss, RTO limits downtime; tighter targets require warmer, costlier DR (backup/restore < pilot light < warm standby < active-active).", "DR.", "RPO 5 min needs continuous replication."),
("Intermediate", "Design an observability platform.", "Metrics (Prometheus/Thanos), logs (Loki), traces (Tempo/OTel), Grafana, Alertmanager routing, SLO dashboards, retention and access control, multi-cluster labels.", "Ops design.", "See HLD 3."),
("Intermediate", "How do you estimate capacity?", "Convert users to peak RPS, measure per-instance throughput via load test, add headroom (30-50%) and redundancy (N+1/N+2), consider data growth.", "Sizing.", "500 RPS / 100 RPS per pod = 5 pods + headroom."),
("Intermediate", "What is an Architecture Decision Record?", "A short document capturing a decision, context, options and consequences.", "Governance.", "Why we chose EKS."),
("Intermediate", "Where should databases live in a VPC?", "Isolated private subnets with no internet route, accessible only from the app tier.", "Security.", "RDS subnet group."),
("Intermediate", "Explain multi-AZ vs multi-region.", "Multi-AZ protects against data-centre failure within a region (low latency, automatic); multi-region protects against regional failures and adds complexity/cost.", "Resilience level.", "Most apps start with multi-AZ."),
("Advanced", "Design multi-region active-active.", "Global DNS/anycast routing, stateless services in each region, data replication strategy (multi-master or partitioned ownership), conflict resolution, global session/cache handling, consistent deployments, cost and testing.", "Hard design.", "DynamoDB global tables."),
("Advanced", "How do you handle data consistency across services?", "Avoid distributed transactions; use sagas, outbox pattern, idempotency and eventual consistency where acceptable.", "Microservices data.", "Order/payment saga."),
("Advanced", "Explain graceful degradation and load shedding.", "When overloaded or dependencies fail, serve reduced functionality or reject low-priority requests to protect core flows.", "Resilience.", "Disable recommendations."),
("Advanced", "Design rate limiting for a public API.", "Edge (WAF/CDN) coarse limits plus token-bucket per API key in Redis; return 429 with Retry-After; monitoring and burst allowance.", "Protection.", "100 req/min per key."),
("Advanced", "How do you design zero-downtime deployments including DB changes?", "Progressive delivery, backward-compatible expand/contract migrations, feature flags, readiness probes and automated rollback.", "Release engineering.", "Add column then backfill then switch."),
("Advanced", "Security architecture for a regulated workload.", "Multi-account isolation, private networking, KMS encryption, IAM least privilege, audit logging, WAF, vulnerability management, segregation of duties, evidence collection.", "Compliance.", "PCI DSS segmentation."),
("Advanced", "How to choose between ECS, EKS and Lambda?", "Lambda for event-driven; ECS for simple containers with less ops; EKS for Kubernetes ecosystem, portability and complex platforms; consider team skills and cost.", "Trade-off reasoning.", "Team with K8s experience picks EKS."),
("Advanced", "Design for cost efficiency.", "Right-size, autoscale, commitments for baseline, Spot for stateless, caching/CDN, lifecycle policies, VPC endpoints, tagging and budgets, architecture simplification.", "FinOps.", "NAT cost reduced by endpoints."),
("Advanced", "How do you validate a design?", "Failure-mode review, load tests, game days, security review, Well-Architected review, cost estimate, prototype critical paths.", "Verification.", "Chaos test AZ loss."),
("Advanced", "What are the main bottlenecks in a typical web architecture?", "Database (connections, queries), single-threaded/stateful components, network egress (NAT), synchronous dependencies, cache stampedes.", "Performance analysis.", "Pooling and read replicas."),
("Advanced", "Explain how to design multi-tenant SaaS.", "Tenant isolation model (silo/pool/bridge), tenant-aware auth and data partitioning, noisy-neighbour controls, per-tenant metrics and cost allocation.", "SaaS architecture.", "Row-level security per tenant."),
("Advanced", "Design a GitOps-based platform for 50 microservices.", "Config repos per environment, ApplicationSets, shared pipeline templates, policy as code, secrets via external secrets, progressive delivery, per-team namespaces/RBAC and cost tags.", "Platform design.", "Golden path templates."),
("Advanced", "How would you design logging at scale?", "Structured logs, agents to Kafka/Loki, retention tiers, sampling, PII redaction, access control, cost budgets, correlation IDs.", "Observability at scale.", "Hot 7 days, cold 90 days."),
("Scenario-Based", "Design a URL shortener's infrastructure.", "Read-heavy: CDN/cache (Redis), stateless API behind ALB, key-value store (DynamoDB) for mappings, ID generation service, analytics via async queue, rate limiting, multi-AZ.", "Classic design.", "99.99% redirect availability."),
("Scenario-Based", "Design the platform for a video streaming service.", "Object storage + CDN for content, transcoding pipeline with queues/workers (spot instances), metadata DB, adaptive bitrate, DRM/auth, analytics.", "Media workloads.", "S3 + MediaConvert + CloudFront."),
("Scenario-Based", "E-commerce flash sale traffic spike.", "CDN caching, queue-based order intake, pre-scaling, DB read replicas/cache, inventory service consistency, rate limiting and virtual waiting room, load test.", "Peak design.", "Order queue absorbs spike."),
("Scenario-Based", "Migrate an on-prem monolith to AWS.", "Assess, lift-and-shift/replatform first, network connectivity (VPN/Direct Connect), DB migration (DMS), strangler pattern for gradual decomposition, cutover plan and rollback.", "Migration.", "Strangler fig."),
("Scenario-Based", "Design CI/CD for regulated banking apps.", "Approvals and segregation of duties, signed commits/artifacts, immutable images, environment promotion, audit trail, private runners, vulnerability gates, change records.", "Compliance delivery.", "Continuous delivery with gates."),
("Scenario-Based", "Set up observability for 30 microservices.", "Standard instrumentation library, OTel collector, central Prometheus/Loki/Tempo, RED dashboards template, SLOs per service, alert routing by team label.", "Standardisation.", "Backstage integration."),
("Scenario-Based", "Design DR for a database with RPO 1 min, RTO 15 min.", "Cross-region replica (async) or Aurora Global Database, automated promotion runbook/Route 53 failover, tested regularly; accept small data-loss window measurement.", "DR trade-offs.", "Aurora global RPO ~1s."),
("Scenario-Based", "Secure a public API used by mobile apps.", "WAF, API gateway with auth (OAuth2/OIDC), rate limiting, TLS, input validation, secrets management, logging/monitoring, DDoS protection.", "API security.", "Cognito/JWT + WAF."),
("Scenario-Based", "How would you design internal developer self-service?", "Portal with templates, automated repo/pipeline/infra provisioning, guardrails via policy, docs, cost visibility, feedback loop.", "Platform engineering.", "Backstage scaffolder."),
("Scenario-Based", "Reduce the latency for users in Asia and Europe.", "CDN, regional deployments, latency-based DNS, read replicas near users, caching, optimise payloads, HTTP/3.", "Global performance.", "Route 53 latency routing."),
("Scenario-Based", "Design job scheduling for nightly reports.", "EventBridge/CronJob triggers containerised job, queue for parallelism, idempotency, retries/DLQ, monitoring for missed runs, output to S3.", "Batch design.", "Report Lambda/ECS task."),
("Scenario-Based", "Design a secrets flow for Kubernetes apps.", "External Secrets/Vault with IRSA/K8s auth, short TTL, rotation, no secrets in Git, audit, least privilege per namespace.", "Security.", "ESO from Secrets Manager."),
("Scenario-Based", "Design network for 3 environments (dev/stage/prod).", "Separate AWS accounts and VPCs with non-overlapping CIDRs, shared services via Transit Gateway, SCPs, environment-specific SGs and IAM.", "Multi-env.", "10.1/16, 10.2/16, 10.3/16."),
("Scenario-Based", "A design review says your architecture is too complex. Response?", "Justify each component with requirement mapping; remove what is not needed; prefer managed services; document phased approach.", "Judgement.", "Start with ECS, evolve later."),
("Troubleshooting-Based", "Users report intermittent 502s after a scale-out.", "New instances failing health checks or registered before ready; check readiness/warm-up, ALB target health, deregistration delay, app startup time.", "Design edge case.", "Slow start on ALB."),
("Troubleshooting-Based", "Database CPU high after launching a feature.", "New queries without indexes/N+1, missing cache, connection storms; use slow query log, add indexes/caching, pooling.", "Capacity design.", "Missing index on new column."),
("Troubleshooting-Based", "Costs spiked after multi-AZ rollout.", "Cross-AZ data transfer and extra NAT/replicas; review traffic patterns, use AZ-aware routing/endpoints.", "Cost design.", "Chatty services across AZs."),
("Troubleshooting-Based", "Failover test took 20 minutes instead of 5.", "Manual steps, DNS TTL, cold standby, unverified runbook; automate promotion, lower TTL, warm capacity, rehearse.", "DR validation.", "Route 53 TTL 3600."),
("Troubleshooting-Based", "Private subnet instances cannot pull images from ECR.", "No NAT route or VPC endpoints for ECR/S3, SG blocks, missing IAM permission; add endpoints or NAT.", "LLD detail.", "ecr.api, ecr.dkr and S3 endpoints."),
("Troubleshooting-Based", "Kubernetes pods cannot reach RDS.", "SG for RDS does not allow node/pod SG, subnet/route, DNS, credentials; fix SG referencing and network policies.", "Network design.", "SG for pods."),
("Troubleshooting-Based", "Pipeline deploys but ArgoCD does not sync.", "Repo/credentials, path/branch mismatch, app project restrictions, webhook/refresh interval; check app events and diff.", "GitOps design.", "Wrong targetRevision."),
("Troubleshooting-Based", "Alerts fire but on-call cannot act.", "No runbook/dashboard link, unclear ownership, non-actionable thresholds; redesign alerts with symptom focus and runbooks.", "Operational design.", "Add runbook annotation."),
("Troubleshooting-Based", "Autoscaling oscillates (flapping).", "Thresholds too tight, short cooldown/stabilisation window, metric lag; tune target, cooldowns, use step scaling.", "Scaling design.", "HPA stabilisation window."),
("Troubleshooting-Based", "Disaster recovery plan exists but nobody knows it.", "No drills/ownership; schedule game days, keep runbooks in Git, assign owners, measure actual RTO/RPO.", "Process.", "Quarterly DR test.")],
cheatsheet={
"Definitions": ["HLD (what/why) vs LLD (how); functional vs non-functional; SPOF; HA; RPO/RTO; SLO; stateless; horizontal scaling; ADR."],
"Commands": ["Design tools: draw.io, Excalidraw, Mermaid (`flowchart LR`), `diagrams` Python lib", "Validation: `terraform plan`, `kubectl apply --dry-run=server`, `kubectl auth can-i`, load test `k6 run`", "Availability math: downtime = (1 - SLO) x period"],
"Files": ["design.md / ADRs (docs/adr/0001-*.md), architecture.mmd, Terraform modules, Helm chart values, pipeline YAML, alert rules, runbooks"],
"Architecture": ["Users > DNS > CDN/WAF > LB > stateless app (multi-AZ) > cache/DB/queue; CI/CD > registry > GitOps > cluster; observability across all."],
"Ports": ["HTTPS 443, app 8080/3000, PostgreSQL 5432, Redis 6379, Prometheus 9090, Grafana 3000, Alertmanager 9093"],
"Differences": ["HLD vs LLD; vertical vs horizontal; active-passive vs active-active; sync vs async; monolith vs microservices; multi-AZ vs multi-region."],
"Troubleshooting commands": ["Failure-mode walk-through per box; capacity math; `kubectl describe`; SG/route review; cost by tag"],
"Best practices": ["Quantify requirements, multi-AZ, stateless tiers, least-privilege SGs/IAM, IaC, observability with SLOs and runbooks, cost model, documented trade-offs, tested DR."]}
),
subs={
"how-to-design": dict(
define=dict(simple="A step-by-step method for answering 'design this system' questions and for planning real projects.",
technical="Structured design process: elicit functional/non-functional requirements, define constraints, produce HLD (components, interactions, data flows), refine into LLD, evaluate failure modes and trade-offs, and record decisions.",
why="Open-ended design needs a repeatable structure.", without="Random, incomplete designs.", use="Interviews and architecture work.", avoid="Jumping to tools first.", analogy="An architect gathers client needs before drawing a blueprint."),
internals="""Requirements become numbers (RPS, SLO, RPO/RTO). Numbers drive choices (multi-AZ, cache, queue). HLD identifies components and flows; LLD specifies configuration. The failure-mode review tests each component: detection, impact, mitigation, recovery time. Trade-offs make constraints explicit.""",
lab=dict(goal="Practise a design answer using the template.", prereq=["Paper/whiteboard or draw.io", "Timer (30 minutes)"],
steps=[("Pick: 'Design a highly available blog platform for 100k daily users'. Write 5 clarifying questions and quantified assumptions", "Practise requirement gathering."),
("Draw HLD with numbered request flow and label technology choices with one-line reasons", "Practise explaining WHY."),
("Add scaling, HA/DR, security, monitoring, cost; then list 5 failure scenarios and responses", "Cover the seniors' checklist."),
("Explain the design aloud in 5 minutes and record it", "Fluency for interviews.")]),
compare=[("Answer quality", ["Junior answer", "Senior answer"], [["Lists tools", "Maps each tool to a requirement"], ["Happy path only", "Failure modes and recovery"], ["No numbers", "RPS, SLO, RPO/RTO, cost estimates"], ["One option", "Alternatives and trade-offs"]])],
mnemonics=[("Design answer", "R-C-H-C-D-S-S-O-C-T")], hinglish="Design mein **pehle sawal poochho, numbers nikalo, phir boxes banao**. Har box ke liye bolo: kyun, aur **fail hua to kya hoga**.",
practices={"Development": ["Keep ADRs and Mermaid diagrams in Git."]}, mistakes={"Beginner mistakes": ["Starting with Kubernetes before requirements."]},
qa_extra=[("Intermediate", "How do you show trade-offs in a design answer?", "For each major choice state the alternative, why you chose this option under the given constraints, and what would make you change it.", "Senior thinking.", "Choose ECS over EKS for a small team, revisit if multi-cloud is needed.")]),

"hld-3tier-aws": dict(
define=dict(simple="The standard highly available web application on AWS: load balancer, app servers, database.",
technical="A three-tier architecture separates presentation/edge, application and data tiers across multiple AZs in a VPC with public, private and isolated subnets, managed database failover, caching, object storage and CDN.",
why="Scalability, security and availability by separating concerns.", without="Single server doing everything.", use="Most web applications.", avoid="Over-engineering tiny apps.", analogy="A restaurant: reception (LB), kitchen (app), pantry (DB), each with backups."),
internals="""User request resolves via Route 53 to CloudFront/WAF, then the ALB in public subnets. The ALB forwards to healthy app targets in private subnets (ASG/EKS). The app reads Redis; on a miss it queries RDS (primary in AZ-a, synchronous standby in AZ-b). Uploaded files go to S3; async work goes to SQS. If AZ-a fails, ALB and ASG shift to AZ-b and RDS fails over.""",
realworld=dict(diagram="""Route53 -> CloudFront/WAF -> ALB (pub a,b)
   -> App tier ASG/EKS (priv a,b) -> Redis
   -> RDS primary (db-a) <=sync=> standby (db-b)
   S3 (files) | SQS+workers | NAT per AZ | VPC endpoints""", text="A retail site serving 500 requests per second uses this layout. Static assets are cached at the CDN (70 percent hit ratio), the app tier autoscales on CPU/RPS, and Multi-AZ RDS meets a 99.9 percent SLO. Security groups chain ALB to app to DB, and monitoring alerts on 5xx rate, latency, CPU and replication health."),
lab=dict(goal="Sketch and cost a 3-tier design.", prereq=["AWS pricing calculator (calculator.aws)", "diagram tool"],
steps=[("Draw the HLD above with numbered flow", "Communicate clearly."), ("Add 2 AZs and mark the failure behaviour of each component", "Failure analysis."), ("Estimate monthly cost in the AWS calculator (ALB, 2x t3.medium, RDS Multi-AZ small, NAT x2, S3, CloudFront)", "Cost awareness: NAT and data transfer often surprise.")]),
mnemonics=[("Tiers", "Edge > App > Data; public > private > isolated")], hinglish="**ALB public subnet mein, app private mein, DB isolated mein.** Har tier 2 AZ mein. Security group ek dusre ko reference karte hain.",
practices={"Reliability": ["Multi-AZ everything; health checks; autoscaling."], "Security": ["SG chaining; WAF; encryption."]}, mistakes={"Production mistakes": ["Single NAT/AZ.", "DB in public subnet."]},
qa_extra=[("Advanced", "What are the bottlenecks as traffic grows 10x?", "Database first (connections/CPU): add caching, read replicas, pooling, query tuning; then NAT/egress and app tier autoscaling limits; CDN offload for static content.", "Scale reasoning.", "Introduce Redis before scaling the DB up.")]),

"hld-cicd-gitops-platform": dict(
define=dict(simple="An end-to-end delivery platform from code push to production, with security and rollback built in.",
technical="Git-based CI builds, tests, scans, signs and publishes immutable images; a GitOps repository holds environment state; ArgoCD reconciles clusters; progressive delivery and observability provide safe rollouts and rollback.",
why="Fast, safe, auditable releases across many teams.", without="Manual, inconsistent deployments.", use="Organisations with multiple services.", avoid="Excess complexity for one small app.", analogy="An automated factory line with inspection stations and a return chute."),
internals="""Developer opens a PR > CI runs unit tests, SAST/SCA/secrets > merge to main > CI builds image tagged with SHA, scans, signs, pushes to registry > CI updates the image tag in the GitOps repo (PR or commit) > ArgoCD detects the change, syncs to staging > smoke tests and analysis > promotion to production (approval) > progressive rollout monitored by metrics > auto rollback via Argo Rollouts or git revert.""",
realworld=dict(diagram="""Dev > GitHub PR > Actions (test, scan, build, sign) > ECR
   > GitOps repo (tag bump) > ArgoCD > EKS staging > tests > approval > EKS prod (canary)
   Prometheus analysis -> promote or rollback ; Slack notifications""", text="Twenty microservices share a pipeline template. Developers only push code; the platform handles images, environment promotion and rollbacks. Auditors can trace every production change to a reviewed commit and a signed image."),
lab=dict(goal="Draft the platform design and promotion rules.", prereq=["Diagram tool"],
steps=[("Draw the flow above and mark security controls at each stage", "Shift-left visualised."), ("Define promotion criteria: staging tests pass, no critical CVE, SLO burn OK, approval for prod", "Quality gates."), ("Write the rollback procedure: `git revert` GitOps commit or Argo Rollouts abort", "Recovery design.")]),
mnemonics=[("Platform", "Build once, sign, promote by Git, observe, rollback by revert")], hinglish="**Image ek baar build, Git se promote, ArgoCD se deploy, metrics se verify, aur rollback = git revert.** CI ko cluster credentials mat do.",
practices={"Security": ["Signed images, admission verification, OIDC, least privilege."], "Reliability": ["Progressive delivery with automated analysis."]}, mistakes={"DevOps mistakes": ["Rebuilding per environment.", "CI with cluster-admin."]},
qa_extra=[("Scenario-Based", "How do you promote from staging to prod safely?", "Promote the same image digest by changing the tag/digest in the prod GitOps overlay via PR with approval, after tests and policy checks; roll out progressively and monitor SLOs.", "Release governance.", "Prod overlay PR requires two reviewers.")]),

"hld-observability-platform": dict(
define=dict(simple="One central place to see metrics, logs, traces and alerts for all services and clusters.",
technical="A multi-cluster observability architecture: per-cluster collectors (Prometheus agents/OTel/Promtail) forward to central long-term storage (Thanos/Mimir, Loki, Tempo), visualised in Grafana with SLO dashboards and routed alerts.",
why="Fast detection and diagnosis across many systems.", without="Fragmented tools and blind spots.", use="Many services/clusters.", avoid="Collecting data with no owner or purpose.", analogy="A control tower seeing every runway."),
internals="""In each cluster, Prometheus scrapes services and remote-writes to central storage; OTel Collector receives traces/logs and exports to Tempo/Loki; labels (cluster, env, team, service) are added. Grafana queries all sources; alert rules evaluate centrally or per cluster and go to Alertmanager which routes by team label to Slack/PagerDuty. Retention tiers control cost.""",
realworld=dict(diagram="""Cluster A/B/C: Prometheus + OTel + Promtail --remote write--> Central: Mimir/Thanos, Loki, Tempo
                                                    v
                                              Grafana (SLO dashboards)  +  Alertmanager -> Slack/PagerDuty""", text="Twenty services across three clusters each expose standard RED metrics. Central dashboards show SLO burn per team; an alert links to a runbook and to a pre-filtered trace/log view."),
lab=dict(goal="Design retention and alert routing.", prereq=["Paper/whiteboard"],
steps=[("List signals per service (RED) and infrastructure (USE) and required labels", "Standardisation."), ("Set retention: metrics 15d raw + 13 months downsampled, logs 14d hot + 90d cold, traces 7d with tail sampling", "Cost control."), ("Draw alert routing: severity=page to PagerDuty by team label, warning to Slack", "Operational design.")]),
mnemonics=[("Platform labels", "cluster, env, team, service")], hinglish="Sab clusters ke **labels standard** rakho (cluster, env, team, service). **SLO burn** par alert lagao aur har alert mein **runbook link** do.",
practices={"Cost Optimization": ["Retention tiers, sampling, drop noisy logs."], "Reliability": ["HA Alertmanager; watchdog alert."]}, mistakes={"Production mistakes": ["No owner for dashboards/alerts."]},
qa_extra=[("Advanced", "How do you keep cardinality under control in a shared platform?", "Enforce label conventions, drop/relabel high-cardinality labels at the collector, per-tenant limits, review new metrics, and educate teams.", "Platform stability.", "Limits per tenant in Mimir.")]),

"lld-vpc-cidr-sg": dict(
define=dict(simple="The exact IP ranges and firewall rules for the network design.",
technical="LLD network specification: VPC and subnet CIDRs per AZ/tier, route tables, gateways, security group rules using SG references, NACL policy, endpoints and flow logs.",
why="Implementable, reviewable network.", without="Ad-hoc addressing and open rules.", use="Every VPC.", avoid="Overlapping CIDRs and 0.0.0.0/0 on internal tiers.", analogy="Street map with exact house numbers and gate rules."),
internals="""Route tables decide next hops per subnet: public to IGW, app to NAT (per AZ), DB local only. Security groups are stateful and evaluated at each ENI: ALB SG allows internet 443; app SG allows app port from ALB SG; DB SG allows DB port from app SG. NACLs are a coarse stateless second layer.""",
config=[("Terraform snippet for SG chaining explained", """resource "aws_security_group" "app" {
  name   = "app-sg"
  vpc_id = aws_vpc.main.id
  ingress {
    from_port       = 8080
    to_port         = 8080
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }
  egress { from_port = 0 to_port = 0 protocol = "-1" cidr_blocks = ["0.0.0.0/0"] }
}""", [("security_groups = [alb.id]", "Only traffic from the ALB's SG is allowed: no IP lists to maintain."), ("port 8080", "Application port only."), ("egress all", "Allows outbound (updates/APIs); tighten with endpoints/egress rules for strict environments.")])],
lab=dict(goal="Validate an address plan with Python.", prereq=["Python 3"],
steps=[("python3 -c \"import ipaddress as i; v=i.ip_network('10.0.0.0/16'); subs=['10.0.0.0/24','10.0.1.0/24','10.0.10.0/24','10.0.11.0/24','10.0.20.0/24','10.0.21.0/24']; print(all(i.ip_network(s).subnet_of(v) for s in subs))\"", "All subnets fit inside the VPC: True."), ("python3 -c \"import ipaddress as i, itertools; s=[i.ip_network(x) for x in ['10.0.0.0/24','10.0.1.0/24','10.0.10.0/24']]; print(any(a.overlaps(b) for a,b in itertools.combinations(s,2)))\"", "Checks for overlaps: False is good.")]),
mnemonics=[("SG chain", "internet > ALB SG > app SG > DB SG")], hinglish="Security group mein **IP nahi, SG ka reference** do (ALB SG se app SG). **DB ko internet route mat do.** CIDR overlap check karo.",
practices={"Security": ["Chain SGs; endpoints; flow logs."]}, mistakes={"DevOps mistakes": ["0.0.0.0/0 on DB SG."]},
qa_extra=[("Scenario-Based", "Why one NAT gateway per AZ?", "A single NAT is an AZ dependency and cross-AZ data path; per-AZ NATs keep each AZ independent at a higher fixed cost.", "HA vs cost.", "Prod uses 2 NATs, dev uses 1.")]),

"lld-cicd-pipeline": dict(
define=dict(simple="The actual workflow, Dockerfile and deploy configuration that implement the delivery design.",
technical="A concrete GitHub Actions workflow with cache, test, scan, build/push by SHA, sign, and a step that updates the GitOps repository; Dockerfile multi-stage non-root; ArgoCD Application per environment.",
why="Turns HLD into working automation.", without="Ideas without implementation.", use="Every service.", avoid="Copy-pasting without understanding.", analogy="The detailed wiring diagram after the electrical plan."),
internals="""On merge, the workflow authenticates to the registry via OIDC, builds the image with cache, scans with Trivy (fail on HIGH/CRITICAL), pushes `:sha`, signs with cosign, then clones the GitOps repo, updates `values.yaml` `image.tag`, and pushes. ArgoCD detects the commit and syncs.""",
config=[("Workflow explained", """name: release
on: { push: { branches: [main] } }
permissions: { id-token: write, contents: read }
jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: aws-actions/configure-aws-credentials@v4
        with: { role-to-assume: arn:aws:iam::123456789012:role/gha-ecr, aws-region: ap-south-1 }
      - uses: aws-actions/amazon-ecr-login@v2
      - run: docker build -t $ECR/app:${{ github.sha }} .
      - run: trivy image --exit-code 1 --severity HIGH,CRITICAL $ECR/app:${{ github.sha }}
      - run: docker push $ECR/app:${{ github.sha }}
      - run: cosign sign --yes $ECR/app:${{ github.sha }}""", [("id-token: write", "OIDC federation, no static AWS keys."), ("ecr-login", "Short-lived registry token."), ("tag = github.sha", "Immutable, traceable version."), ("trivy exit-code 1", "Blocks vulnerable images before push."), ("cosign sign", "Signature verified later at admission. Set `ECR` env to your registry URI and check current action versions.")])],
lab=dict(goal="Dry-run the pipeline locally.", prereq=["Docker", "Trivy", "Dockerfile"],
steps=[("docker build -t app:local .", "Build."), ("trivy image --severity HIGH,CRITICAL app:local", "Scan."), ("docker run --rm app:local id", "Verify it runs as non-root (uid not 0).")]),
mnemonics=[("Pipeline", "Test > Build > Scan > Push > Sign > GitOps bump")], hinglish="Pipeline mein **SHA tag**, **scan gate**, **signing** aur **GitOps repo update** zaroor rakho. Static AWS keys ki jagah **OIDC**.",
practices={"Security": ["OIDC, signed images, pinned actions."]}, mistakes={"Security mistakes": ["Long-lived registry passwords in secrets."]},
versions=["Action versions and cosign flags change: verify with each project's docs."],
qa_extra=[("Intermediate", "Why tag images with the commit SHA?", "It is immutable and links a running container to exact source; `latest` is mutable and hides what is deployed.", "Traceability.", "Roll back to a previous SHA.")]),

"lld-k8s-app-manifests": dict(
define=dict(simple="Production-ready Kubernetes YAML for one application: deployment, service, ingress, autoscaling and protections.",
technical="A complete manifest set with resource requests/limits, probes, rolling update strategy, PDB, HPA, NetworkPolicy, dedicated ServiceAccount and securityContext.",
why="Predictable, safe, secure workloads.", without="Defaults that allow outages and privilege.", use="Every production service.", avoid="Copy without adjusting numbers.", analogy="A pre-flight checklist for the application."),
internals="""Deployment maintains replicas and rolls out safely (maxUnavailable 0). Readiness gates traffic, liveness restarts hung pods, startup protects slow starts. HPA scales pods on CPU; PDB keeps minimum pods during node drains; NetworkPolicy restricts traffic; ServiceAccount + securityContext limit privileges.""",
config=[("Production Deployment explained", """apiVersion: apps/v1
kind: Deployment
metadata: { name: api, namespace: shop, labels: { app: api } }
spec:
  replicas: 3
  strategy: { type: RollingUpdate, rollingUpdate: { maxSurge: 1, maxUnavailable: 0 } }
  selector: { matchLabels: { app: api } }
  template:
    metadata: { labels: { app: api } }
    spec:
      serviceAccountName: api
      securityContext: { runAsNonRoot: true, seccompProfile: { type: RuntimeDefault } }
      topologySpreadConstraints:
      - { maxSkew: 1, topologyKey: topology.kubernetes.io/zone, whenUnsatisfiable: ScheduleAnyway, labelSelector: { matchLabels: { app: api } } }
      containers:
      - name: api
        image: registry.example.com/shop/api:3fa9c1d
        ports: [{ containerPort: 8080 }]
        resources: { requests: { cpu: 200m, memory: 256Mi }, limits: { memory: 512Mi } }
        readinessProbe: { httpGet: { path: /ready, port: 8080 }, periodSeconds: 5 }
        livenessProbe: { httpGet: { path: /live, port: 8080 }, initialDelaySeconds: 20, periodSeconds: 10 }
        startupProbe: { httpGet: { path: /live, port: 8080 }, failureThreshold: 30, periodSeconds: 2 }
        securityContext: { allowPrivilegeEscalation: false, readOnlyRootFilesystem: true, capabilities: { drop: [ALL] } }
        lifecycle: { preStop: { exec: { command: ["sleep","10"] } } }""", [("maxUnavailable: 0", "Never reduce capacity during updates."), ("serviceAccountName", "Dedicated identity for least-privilege RBAC/IRSA."), ("runAsNonRoot / seccomp", "Pod-level hardening."), ("topologySpreadConstraints", "Spread pods across zones for AZ failure tolerance."), ("image tag SHA", "Immutable version."), ("requests/limits", "Scheduling and protection; CPU limit omitted deliberately to avoid throttling (a design choice: adjust to policy)."), ("readiness/liveness/startup", "Traffic gating, self-healing, slow-start protection."), ("readOnlyRootFilesystem/drop ALL", "Container hardening."), ("preStop sleep", "Lets the load balancer drain connections before shutdown.")]),
("Companion objects explained", """apiVersion: policy/v1
kind: PodDisruptionBudget
metadata: { name: api, namespace: shop }
spec: { minAvailable: 2, selector: { matchLabels: { app: api } } }
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata: { name: api, namespace: shop }
spec:
  scaleTargetRef: { apiVersion: apps/v1, kind: Deployment, name: api }
  minReplicas: 3
  maxReplicas: 12
  metrics: [{ type: Resource, resource: { name: cpu, target: { type: Utilization, averageUtilization: 70 } } }]
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: { name: api, namespace: shop }
spec:
  podSelector: { matchLabels: { app: api } }
  policyTypes: [Ingress]
  ingress: [{ from: [{ namespaceSelector: { matchLabels: { name: ingress-nginx } } }], ports: [{ port: 8080 }] }]""", [("PDB minAvailable: 2", "Node drains cannot take the service below two pods."), ("HPA min 3 / max 12", "Baseline HA and burst capacity."), ("averageUtilization 70", "Scale before saturation (relative to requests)."), ("NetworkPolicy ingress", "Only the ingress controller namespace can reach the API pods (needs a policy-enforcing CNI).")])],
lab=dict(goal="Validate manifests without changing the cluster.", prereq=["kubectl", "Cluster or kind"],
steps=[("kubectl apply --dry-run=server -f k8s/", "Validates against the real API server schema/admission."), ("kubectl apply -f k8s/ && kubectl -n shop rollout status deploy/api", "Apply and watch rollout."), ("kubectl -n shop get pdb,hpa,networkpolicy", "Verify companion objects exist.")]),
mnemonics=[("Checklist", "Probes, Requests/limits, Replicas, PDB, HPA, Non-root, NetworkPolicy, SA")], hinglish="Production manifest mein **probes, requests/limits, 3 replicas, PDB, HPA, non-root, NetworkPolicy aur alag ServiceAccount** hamesha rakho.",
practices={"Production": ["Zone spread, PDB, HPA, graceful shutdown."], "Security": ["Non-root, drop caps, read-only FS, NetworkPolicy."]}, mistakes={"Production mistakes": ["No readiness probe.", "Single replica."]},
versions=["`autoscaling/v2` HPA is stable; `policy/v1` PDB; validate API versions with `kubectl api-resources` on your cluster version."],
qa_extra=[("Advanced", "Why is `preStop: sleep` used?", "Endpoints and load balancers update asynchronously; sleeping keeps the pod serving briefly after termination starts so in-flight requests/new connections still succeed while it is removed from rotation.", "Graceful shutdown.", "Eliminated 502s during rollouts.")]),

"lld-monitoring-alerts-runbook": dict(
define=dict(simple="The exact alert rules, dashboard panels and step-by-step runbook for the on-call engineer.",
technical="Symptom-based alert rules with `for` durations, severity labels and annotations linking dashboards/runbooks; dashboard panels for golden signals; runbooks with diagnosis commands, mitigation and escalation.",
why="Turn observability design into actionable operations.", without="Noisy alerts and improvised responses.", use="Every production service.", avoid="Alerts without runbooks.", analogy="An emergency checklist taped inside the cockpit."),
internals="""Prometheus evaluates rules each interval; a condition true for `for` duration becomes firing and goes to Alertmanager, which routes by severity/team. The annotation links the on-call to a dashboard and runbook. The runbook narrows the cause with specific commands and offers mitigations (rollback, scale, feature flag) and escalation.""",
config=[("Alert rules explained", """groups:
- name: api-slo
  rules:
  - alert: ApiHighErrorRate
    expr: sum(rate(http_requests_total{job="api",status=~"5.."}[5m])) / sum(rate(http_requests_total{job="api"}[5m])) > 0.02
    for: 10m
    labels: { severity: page, team: payments }
    annotations:
      summary: "API 5xx above 2% for 10m"
      dashboard: "https://grafana/d/api-overview"
      runbook: "https://wiki/runbooks/api-high-error-rate"
  - alert: ApiHighLatencyP95
    expr: histogram_quantile(0.95, sum by (le)(rate(http_request_duration_seconds_bucket{job="api"}[5m]))) > 0.5
    for: 10m
    labels: { severity: warning, team: payments }
  - alert: PodCrashLooping
    expr: increase(kube_pod_container_status_restarts_total{namespace="shop"}[15m]) > 3
    for: 5m
    labels: { severity: warning }""", [("expr error ratio", "Symptom: share of requests failing."), ("for: 10m", "Avoids paging on brief blips."), ("severity: page", "Routes to PagerDuty; warnings go to Slack/tickets."), ("team label", "Alertmanager routes to the owning team."), ("dashboard/runbook annotations", "The on-call gets context in the notification."), ("histogram_quantile 0.95", "Latency percentile, not average."), ("CrashLooping rule", "Cause-oriented warning with a threshold to avoid noise.")])],
lab=dict(goal="Write and test an alert rule.", prereq=["promtool (from Prometheus)"],
steps=[("Save the rules to api-rules.yml", "Rule file."), ("promtool check rules api-rules.yml", "Validates syntax: SUCCESS."), ("Add unit tests with promtool test rules and run them", "Proves the alert fires for synthetic data (see Prometheus docs for the test file format).")]),
mnemonics=[("Runbook", "Symptom > Check > Mitigate > Escalate > Record")], hinglish="Alert **symptom** par lagao, **runbook link** do, aur runbook mein **exact commands** likho: pehle dashboard, phir recent deploy, phir logs, mitigation (rollback), escalation.",
practices={"Monitoring & Logging": ["Every page has a runbook and dashboard."], "Reliability": ["Test alert rules with promtool."]}, mistakes={"DevOps mistakes": ["Alerts without runbooks."]},
qa_extra=[("Scenario-Based", "Write the first five steps of a runbook for 'API high error rate'.", "1) Open the API dashboard and confirm the error rate and affected endpoints. 2) Check deploys in the last hour and roll back if correlated. 3) Check dependencies (DB/cache) dashboards. 4) `kubectl -n shop logs deploy/api --since=15m | grep -i error`. 5) If unresolved in 15 minutes escalate to the service owner and open an incident channel.", "Practical runbook writing.", "Rollback fixed a bad config in 4 minutes.")]),

"real-problem-walkthroughs": dict(
define=dict(simple="Worked examples of real problems: what you see, how to investigate, how to fix and how to prevent.",
technical="Scenario-based practice using the structure symptom > hypotheses > investigation commands > fix > prevention, applied across Linux, network, Kubernetes, CI/CD, cloud and databases.",
why="Interviews and incidents reward systematic reasoning.", without="Random guessing.", use="Interview prep and on-call training.", avoid="Memorising fixes without understanding causes.", analogy="Doctor's case studies."),
internals="""General method: (1) define the symptom and scope (who, what, since when), (2) check what changed (deploys, config, traffic), (3) form hypotheses ordered by likelihood and cost of test, (4) test with the cheapest command, (5) mitigate first then fix root cause, (6) prevent with alerts/tests/automation and document.""",
config=[("Investigation template explained", """Symptom:   checkout returns 502 for 20% of users since 10:05
Scope:     only /pay endpoint, all regions
Changes:   deploy api v1.8.3 at 10:03
Hypotheses: (1) new version bug (2) DB connection exhaustion (3) dependency timeout
Tests:     kubectl rollout history; kubectl logs --since=15m; check DB connections; trace one failing request
Mitigation: kubectl rollout undo deploy/api
Root cause: new query without index -> DB CPU 95% -> timeouts
Prevention: query review, load test in CI, alert on DB CPU/latency""", [("Scope", "Narrowing scope points to the cause."), ("Changes", "Most incidents follow a change."), ("Hypotheses", "Ordered by likelihood."), ("Mitigation", "Restore service first."), ("Prevention", "Turns an incident into improvement.")])],
lab=dict(goal="Practise three walkthroughs.", prereq=["A local cluster or Docker"],
steps=[("Break a container on purpose: docker run --name w -d nginx:1.27 && docker exec w sh -c 'echo bad > /etc/nginx/conf.d/default.conf' && docker restart w; docker logs w", "Diagnose from logs: config error; fix by restoring config."), ("Kubernetes: kubectl run bad --image=nginx:doesnotexist; kubectl describe pod bad", "ImagePullBackOff analysis."), ("Disk full simulation in a container: docker run --rm alpine sh -c 'dd if=/dev/zero of=/tmp/big bs=1M count=100; df -h /tmp'", "Practise reading usage and cleaning up.")]),
mnemonics=[("Investigate", "Symptom, Scope, Changes, Hypotheses, Test, Mitigate, Root cause, Prevent")], hinglish="Har problem mein **symptom, scope, kya change hua, hypotheses, test, mitigation, root cause, prevention** ke order mein socho. **Pehle service restore, phir root cause.**",
practices={"Reliability": ["Write short incident notes for every real problem."]}, mistakes={"Beginner mistakes": ["Fixing symptoms without prevention."]},
qa_extra=[("Troubleshooting-Based", "Walk through: 'Website is slow, users complain'.", "Scope (all users or some), check golden signals and recent changes, find the slow tier (edge/app/DB/dependency) with metrics and traces, mitigate (rollback/scale/cache), fix root cause (index/query/limit), add alert and test.", "Structured troubleshooting.", "DB CPU from a missing index.")])
})
