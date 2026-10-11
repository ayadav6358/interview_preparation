TOPIC = dict(slug="14-sre-culture", title="SRE, Reliability & DevOps Culture", intro="Tools se aage: reliability engineering, incident management, chaos testing, platform engineering aur DevOps mindset.", subs=[

dict(slug="devops-culture-sdlc", title="DevOps Culture, SDLC & Agile", level="Basic",
intro="DevOps = culture + practices + tools. Dev aur Ops ke beech ki deewar todna. CALMS: Culture, Automation, Lean, Measurement, Sharing.",
diagram="""
Plan -> Code -> Build -> Test -> Release -> Deploy -> Operate -> Monitor -> (feedback) -> Plan
Waterfall (slow, big-bang)  vs  Agile/Scrum sprints  vs  DevOps continuous flow
""",
install="# tools: Jira/Linear (tracking), Confluence/Notion (docs), Slack (chatops)",
examples=[("Scrum vs Kanban","""Scrum: sprints (2 wk), roles PO/SM/team, ceremonies (planning, standup, review, retro)
Kanban: continuous flow, WIP limits, board columns""")],
problems=[("Dev throws code over the wall, Ops firefights","Silos, no shared ownership","You build it, you run it; shared on-call, shared dashboards.")],
qa=[("What is DevOps?","Culture and practices that unify development and operations to deliver software faster and more reliably."),
("What is CALMS?","Culture, Automation, Lean, Measurement, Sharing."),
("Agile vs DevOps?","Agile focuses on iterative development; DevOps extends to delivery and operations."),
("What is a retrospective?","Team meeting to improve process."),
("What is ChatOps?","Operating via chat tools with bots.")]),

dict(slug="incident-management", title="Incident Management & Postmortems", level="Intermediate",
intro="Production down ho to panic nahi, process. Detect -> triage -> mitigate -> resolve -> blameless postmortem. MTTR kam karna goal hai.",
diagram="""
Alert -> On-call ack -> Severity (SEV1-4) -> Incident channel + roles (IC, Ops, Comms)
   -> MITIGATE first (rollback/scale/failover) -> RCA later -> Postmortem + action items
""",
install="# tools: PagerDuty/Opsgenie, Statuspage, Slack, Jira, runbooks in wiki",
examples=[("First 10 minutes runbook","""1 Ack alert, open #inc-YYYYMMDD channel, assign Incident Commander
2 What changed? (deploys, config, traffic, dependency) -> check deploy annotations
3 Mitigate: rollback / scale up / failover / disable feature flag
4 Communicate status every 15-30 min; update status page
5 Verify recovery with SLI dashboards"""),
("Postmortem template","""Summary | Impact (users, duration, $) | Timeline | Root cause (5 whys) | What went well/badly | Action items (owner, due) | Lessons""")],
problems=[("Same incident repeats","Postmortem actions never done","Track actions as tickets with owners; review in weekly ops meeting.")],
qa=[("Mitigation vs root cause fix?","Mitigation restores service fast; root cause fix prevents recurrence."),
("What is a blameless postmortem?","Focus on systems and process, not individuals."),
("MTTD/MTTA/MTTR?","Mean time to detect/acknowledge/recover."),
("Severity levels?","SEV1 critical outage ... SEV4 minor; determine response."),
("Production is down after deploy - what do you do?","Confirm impact, check recent changes, rollback quickly, communicate, then investigate.")]),

dict(slug="chaos-load-testing", title="Chaos Engineering & Load Testing", level="Advanced",
intro="Failure ka wait mat karo, khud inject karo (controlled). Load test se capacity aur bottlenecks pata karo.",
diagram="""
Hypothesis: 'If 1 pod dies, users see no errors'
 -> run experiment (Chaos Mesh/Litmus kills pod) -> observe SLO dashboards -> fix gaps -> repeat
Load test: k6 ramps users -> watch latency/errors/saturation -> find breaking point
""",
install="""# k6
winget install k6   # or docker run -i grafana/k6 run - <script.js
# Chaos Mesh
helm repo add chaos-mesh https://charts.chaos-mesh.org && helm install chaos-mesh chaos-mesh/chaos-mesh -n chaos-mesh --create-namespace""",
examples=[("k6 load test","""import http from 'k6/http'; import { check, sleep } from 'k6';
export const options = {
  stages: [{ duration: '2m', target: 100 }, { duration: '5m', target: 100 }, { duration: '1m', target: 0 }],
  thresholds: { http_req_duration: ['p(95)<500'], http_req_failed: ['rate<0.01'] },
};
export default function () {
  const r = http.get('https://staging.example.com/api/products');
  check(r, { 'status 200': (x) => x.status === 200 });
  sleep(1);
}"""),
("Chaos Mesh pod kill","""apiVersion: chaos-mesh.org/v1alpha1
kind: PodChaos
metadata: { name: kill-web, namespace: chaos-mesh }
spec:
  action: pod-kill
  mode: one
  selector: { namespaces: [staging], labelSelectors: { app: web } }
  duration: 30s""")],
problems=[("System falls over at 2x traffic on launch day","Never load tested","Regular load tests in staging, autoscaling tuned, capacity plan with headroom.")],
qa=[("What is chaos engineering?","Deliberate failure experiments to build confidence in resilience."),
("Load vs stress vs soak test?","Load: expected traffic; stress: beyond limits; soak: long duration for leaks."),
("Game day?","Planned team exercise simulating failures."),
("What is graceful degradation?","Reduced functionality instead of total failure."),
("Circuit breaker pattern?","Stop calling failing dependency temporarily to prevent cascading failures.")]),

dict(slug="platform-finops", title="Platform Engineering, FinOps & Career", level="Advanced",
intro="Internal Developer Platform (golden paths), cost governance aur DevOps career path aur certifications.",
diagram="""
Developers -> Portal (Backstage) -> templates/golden path -> auto CI/CD + infra + monitoring
Platform team = product team serving internal developers
FinOps: tag -> allocate -> optimize (rightsizing, savings plans, spot) -> budget alerts
""",
install="npx @backstage/create-app@latest    # Backstage portal",
examples=[("Career roadmap","""0-6m Linux, Git, Docker, Bash/Python, AWS basics
6-12m CI/CD, Terraform, K8s, monitoring   -> Junior DevOps / Cloud engineer
1-3y  EKS in prod, GitOps, security, SRE practices -> DevOps Engineer
3y+   Architecture, platform eng, cost, leadership -> Senior/Staff/SRE/Architect
Certs: AWS SAA -> CKA -> Terraform Associate -> CKS/AWS DevOps Pro"""),
("Portfolio ideas","""1 3-tier app on EKS w/ Terraform + ArgoCD  2 Full observability stack  3 Secure pipeline with scanning  4 Chaos + postmortem write-up
Put README + architecture diagram + cost estimate in each repo""")],
problems=[("Every team builds pipelines differently","No standards","Golden-path templates and shared modules maintained by platform team.")],
qa=[("What is platform engineering?","Building self-service internal platforms to improve developer productivity."),
("What is FinOps?","Practice of cloud financial accountability across engineering and finance."),
("DevOps vs SRE vs Platform?","DevOps culture/practices; SRE applies software engineering to reliability with SLOs; Platform builds internal products."),
("How do you measure DevOps success?","DORA metrics."),
("What is toil?","Manual, repetitive, automatable work that scales with service growth; SRE aims to keep it under 50%.")]),
])
