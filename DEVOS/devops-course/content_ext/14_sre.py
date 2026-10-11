EXT = dict(
guide=dict(
bigpicture=dict(
problem="""**Problem it solves:** Development wants to ship features fast; operations wants stability. When they are separate teams, they fight: releases are slow, incidents cause blame, and reliability is nobody's clear responsibility. **DevOps culture** and **Site Reliability Engineering (SRE)** unite building and running software: shared ownership, automation, measurable reliability targets (SLOs), blameless learning from incidents.""",
chain=["PROBLEM: speed of change vs stability of service; handoffs and blame between teams",
       "TRADITIONAL APPROACH: developers 'throw code over the wall' to operations",
       "PAIN: slow releases, unclear ownership, repeated incidents, burnout",
       "TECHNOLOGY/PRACTICE: DevOps culture, SRE (SLOs, error budgets, toil reduction), incident management, chaos engineering, platform engineering",
       "SOLUTION: shared ownership, automation, data-driven reliability decisions, learning culture",
       "REAL-WORLD BENEFIT: faster and safer delivery, fewer/shorter incidents, sustainable on-call, lower cost"],
text="""SRE (coined at Google) treats operations as a software problem: define **SLIs/SLOs**, spend an **error budget** on change, automate **toil** (manual repetitive work), and run **blameless postmortems**. DevOps is the culture and practices; SRE is one concrete way to implement them. **Platform engineering** builds internal self-service platforms so product teams can deploy safely without deep infrastructure knowledge."""),
e2e=dict(diagram="""Plan (agile backlog, SLOs defined)
   v
Code + review (Git, PR)
   v
Build + test + security (CI)
   v
Release (CD, progressive delivery, feature flags)
   v
Operate (on-call, monitoring vs SLOs, error budget)
   v
Incident? -> detect > triage > mitigate > resolve > communicate
   v
Postmortem (blameless) -> action items -> backlog / automation (reduce toil)
   v
Learn + improve (chaos experiments, load tests, capacity planning) -> back to Plan""",
text="""Work flows in a loop, not a line. Teams **plan** with reliability targets (SLOs) in mind, then **build, test and release** through automated pipelines using safe strategies. In **operation** they watch SLIs against SLOs; the **error budget** says how much unreliability is acceptable, so if budget remains they can ship faster and if it is exhausted they prioritise reliability. When an **incident** occurs, a defined process (detect, triage, mitigate, resolve, communicate) limits impact. A **blameless postmortem** identifies systemic causes and creates action items that flow back into the backlog or into **automation**. **Chaos engineering** and **load testing** proactively find weaknesses before customers do."""),
tools=dict(rows=[
["Agile boards (Jira/Azure Boards)", "Plan and track work", "Requirements/stories", "Prioritised backlog", "Planning"],
["CI/CD (Actions/Jenkins/ArgoCD)", "Deliver changes safely", "Code", "Deployed release", "Delivery"],
["Prometheus/Grafana/SLO tools (Sloth, Nobl9)", "Measure SLIs/SLOs and burn rate", "Metrics", "SLO dashboards, alerts", "Operate"],
["PagerDuty/Opsgenie", "On-call and escalation", "Alerts", "Pages, schedules", "Incidents"],
["Incident tooling (Slack, Statuspage, Jira/incident.io)", "Coordinate and communicate", "Incident data", "Timeline, status updates", "Incidents"],
["Chaos Mesh / Litmus / Gremlin / AWS FIS", "Fault injection", "Experiment definition", "Resilience findings", "Game days"],
["k6 / JMeter / Locust", "Load and stress testing", "Scenarios", "Latency/throughput results", "Pre-release, capacity"],
["Backstage / Internal developer portal", "Self-service platform", "Templates/catalog", "Golden paths", "Platform engineering"],
["Kubecost / Cloud cost tools / FinOps dashboards", "Cost visibility", "Billing/usage", "Cost per team/service", "FinOps"]],
why="**DevOps vs SRE:** DevOps is a broad culture ('you build it, you run it'); SRE is a specific engineering discipline with quantified reliability (SLOs, error budgets) and often a dedicated team consulting with product teams. **SRE vs Platform Engineering:** SRE focuses on reliability of services; platform engineering builds the internal product (self-service tooling) that makes teams productive; they often overlap."),
compare=[
("DevOps vs SRE vs Platform Engineering", ["Topic", "DevOps", "SRE", "Platform Engineering"], [["Focus", "Culture, collaboration, automation", "Reliability with SLOs/error budgets", "Internal developer platform/golden paths"], ["Metric", "DORA metrics", "SLO attainment, MTTR", "Developer productivity/adoption"]]),
("SLI vs SLO vs SLA", ["Term", "Meaning", "Who cares"], [["SLI", "Measurement of service behavior", "Engineers"], ["SLO", "Internal target for an SLI", "Engineering + product"], ["SLA", "Contract with consequences", "Customers/business"]]),
("Agile vs Waterfall", ["Topic", "Agile", "Waterfall"], [["Delivery", "Iterative, small increments", "Big-bang, phase by phase"], ["Change", "Welcomed", "Costly"], ["Feedback", "Continuous", "At the end"]]),
("Scrum vs Kanban", ["Topic", "Scrum", "Kanban"], [["Cadence", "Fixed sprints", "Continuous flow"], ["Roles", "PO, Scrum Master, team", "No prescribed roles"], ["Limits", "Sprint scope", "WIP limits"]]),
("Load vs Stress vs Spike vs Soak testing", ["Type", "Goal"], [["Load", "Expected traffic behaviour"], ["Stress", "Find breaking point"], ["Spike", "Sudden surge handling"], ["Soak", "Long duration: leaks, degradation"]]),
("Blameful vs Blameless", ["Topic", "Blameful", "Blameless"], [["Question", "Who caused it?", "What conditions allowed it?"], ["Outcome", "Fear, hidden problems", "Learning, systemic fixes"]])],
troubleshooting=[
("Same incident keeps recurring", "Postmortem actions not completed, symptoms fixed but not root cause", "Review past postmortems, action-item status, incident tags", "Track actions with owners/due dates in the backlog; fix systemic cause; add tests/alerts.", "Review action completion in a regular reliability meeting."),
("Team burned out by on-call", "Noisy alerts, too much toil, small rotation", "Pages per shift, % non-actionable alerts, time on toil", "Prune alerts, automate toil, larger rotation, follow-the-sun, compensation/time off.", "Cap toil (<50%) and track pager load."),
("Incident response is chaotic", "No roles, no runbooks, many people acting at once", "Review last incident timeline", "Define roles (Incident Commander, Comms, Ops), single channel, runbooks, practice game days.", "Regular drills and clear severity definitions."),
("Releases still slow despite CI/CD", "Manual approvals, big batches, flaky tests, long-lived branches", "Value stream map, DORA metrics, pipeline durations", "Reduce batch size, automate tests, trunk-based development, feature flags.", "Track lead time and change failure rate."),
("Error budget always exhausted", "SLO too strict or unreliable dependencies/releases", "Burn-rate graphs, incident categories", "Fix top causes, add progressive delivery, renegotiate SLO if unrealistic.", "Set SLOs from user needs and data."),
("Cloud cost keeps growing", "No ownership, idle resources, over-provisioning", "Cost by team/tag, utilisation reports", "Tag and allocate, rightsizing, schedules, commitments, budgets.", "FinOps reviews and anomaly alerts.")],
practices={
"Development": ["Small batches, trunk-based development, automated tests, feature flags; 'you build it, you run it'."],
"Production": ["Define SLOs per critical user journey; error budget policy; runbooks for every page; progressive delivery; capacity planning."],
"Security": ["Security as shared responsibility; incident response plans include security events; least-privilege on-call access with audit."],
"Performance": ["Load test before major events; performance budgets in CI; capacity reviews."],
"Reliability": ["Redundancy across zones, graceful degradation, timeouts/retries/circuit breakers, chaos experiments, DR drills."],
"Cost Optimization": ["FinOps: tagging, showback/chargeback, rightsizing, commitment planning, kill idle resources."],
"Monitoring & Logging": ["Alert on SLO burn; symptoms over causes; tracked pager load; incident timelines preserved."],
"Backup & Disaster Recovery": ["Define RPO/RTO per service; rehearse restore and region failover; document runbooks."]},
mistakes={
"Beginner mistakes": ["Thinking DevOps is just tools or a job title.", "Automating a broken process."],
"Developer mistakes": ["Throwing code over the wall; no operational ownership.", "No runbook or alerts for new features."],
"DevOps mistakes": ["Hero culture: one person knows everything.", "Alerts without actions.", "Chasing 100% uptime."],
"Production mistakes": ["No incident roles; no status communication.", "Postmortem without follow-through."],
"Security mistakes": ["Treating security as a later phase.", "Sharing on-call credentials."]},
versions=[
"Frameworks evolve: Google's SRE books, DORA's yearly State of DevOps report, and the Agile/Scrum Guide (2020 version simplified roles) are references: check the latest editions.",
"DORA metrics: deployment frequency, lead time for changes, change failure rate, time to restore service (and newer reliability measures).",
"Chaos tools and platforms change: verify Kubernetes/cloud compatibility (Chaos Mesh, Litmus, AWS Fault Injection Service)."],
hinglish="""DevOps ka matlab sirf tools nahi, **culture** hai: **developers aur operations ek hi team ki tarah** kaam karte hain (**you build it, you run it**). **SRE** reliability ko numbers mein naapta hai: **SLI** (measurement), **SLO** (target), **error budget** (kitni galti allowed hai). Incident ke baad **blameless postmortem** karo: "kisne galti ki" nahi, "system mein kya kami thi". **Toil** (baar-baar ka manual kaam) ko automate karo. **Chaos engineering** mein hum jaan-boojh kar failure daalte hain taaki weakness pehle pata chale.""",
mnemonics=[("CALMS", "Culture, Automation, Lean, Measurement, Sharing"), ("Incident flow", "Detect > Triage > Mitigate > Resolve > Communicate > Learn"), ("Error budget", "1 - SLO"), ("DORA", "Deploy frequency, Lead time, Change failure rate, Time to restore"), ("Three Ways", "Flow, Feedback, Continual learning")],
client=dict(
s30="""DevOps and SRE are ways of working where the people who build software also take responsibility for running it. We set clear reliability targets, automate repetitive work and learn from every incident, so you get faster releases and a more dependable service.""",
m2="""Traditionally, developers and operations teams worked separately, which slowed delivery and created blame when things broke. We work as one team with shared ownership. We agree measurable reliability goals with the business, for example 99.9 percent availability, and use an error budget to balance speed and stability: while we are within budget we release quickly, and if we are not we prioritise reliability. Incidents follow a clear process with defined roles and communication, and every significant incident gets a blameless review with tracked improvements. We automate manual tasks and regularly test resilience with load tests and failure experiments. You see this as fewer outages, faster fixes and predictable delivery.""",
m5="""I will structure this in four parts. **Culture and flow:** small, frequent changes through automated pipelines, shared ownership, and metrics such as deployment frequency, lead time, change failure rate and recovery time. **Reliability engineering:** SLIs and SLOs per critical user journey, error budgets and burn-rate alerts to guide priorities, redundancy and graceful degradation in design, and capacity planning. **Operations:** a sustainable on-call with actionable alerts and runbooks, an incident management process with an incident commander, communications lead and status updates, and blameless postmortems whose actions are tracked to completion. **Continuous improvement:** chaos engineering and game days to verify resilience, load testing before peaks, toil reduction through automation, platform engineering to give teams self-service golden paths, and FinOps to keep cost visible. The outcome is a delivery system that is both faster and more reliable, with measurable evidence."""),
roadmap=[
("Beginner", ["SDLC, Agile/Scrum/Kanban basics", "DevOps principles (CALMS)", "Version control and CI basics", "What is on-call/incident"]),
("Intermediate", ["Monitoring and alerting basics", "SLI/SLO/SLA and error budgets", "Incident response roles and runbooks", "Postmortem writing"]),
("Advanced", ["Chaos engineering and game days", "Load/stress testing and capacity planning", "Progressive delivery, feature flags", "Platform engineering, developer portals"]),
("Production", ["On-call health and toil metrics", "DR drills, RPO/RTO", "FinOps practices", "Reliability reviews"]),
("Interview", ["Explain DevOps culture with examples", "Run a mock incident", "Define SLOs for a service", "Write a blameless postmortem"])],
miniproject=dict(title="Define SLOs, run a game day and write a postmortem for a demo service",
arch="""Service (API on Kubernetes) --> Prometheus SLIs --> SLO dashboard + burn-rate alerts
Load test (k6) + fault injection (kill pod / add latency) --> observe --> incident drill
--> blameless postmortem with action items --> backlog/automation""",
steps=[
("Step 1: Define SLIs and SLOs", """Service: checkout-api
SLI-availability = successful requests (non-5xx) / total requests
SLI-latency      = requests faster than 300 ms / total requests
SLO: 99.9% availability and 95% latency SLI over 30 days
Error budget (availability) = 0.1% = about 43 minutes of full outage per 30 days""", "SLOs are set per user journey with product input. The error budget is 1 minus the target: 0.1 percent of 30 days is about 43 minutes."),
("Step 2: Load test with k6", """// load.js
import http from 'k6/http';
import { check, sleep } from 'k6';
export const options = {
  stages: [{ duration: '2m', target: 50 }, { duration: '5m', target: 50 }, { duration: '1m', target: 0 }],
  thresholds: { http_req_failed: ['rate<0.01'], http_req_duration: ['p(95)<300'] },
};
export default function () {
  const r = http.get('http://checkout.example.internal/health');
  check(r, { 'status 200': (x) => x.status === 200 });
  sleep(1);
}
// run: k6 run load.js""", "Ramps to 50 virtual users. `thresholds` turn SLO-like targets into pass/fail criteria so the test can gate a release. Run only against systems you own."),
("Step 3: Inject a failure (game day)", """# announce the experiment, define abort conditions, then:
kubectl -n shop delete pod -l app=checkout-api --wait=false   # kill pods
# watch: kubectl get pods -w ; Grafana: error rate, latency, restarts
# expected: readiness + replicas keep SLO intact; if not, that is a finding""", "Hypothesis: with 3 replicas, killing pods does not breach the SLO. Run in staging first, with an abort plan and stakeholders informed. Tools like Chaos Mesh/Litmus/AWS FIS automate and schedule such experiments."),
("Step 4: Blameless postmortem template", """Title / Date / Severity / Duration / Incident Commander
Summary (2-3 sentences, customer impact)
Timeline (UTC): detection, escalation, mitigation, resolution
Root cause and contributing factors (systems and process, not people)
What went well / what went badly / where we got lucky
Action items: owner, priority, due date, ticket link (prevent, detect, mitigate)
Lessons learned""", "The purpose is learning: focus on conditions that allowed the failure. Action items must be tracked to completion or the same incident will repeat.")]),
interview=[
("Beginner", "What is DevOps?", "A culture and set of practices that unite development and operations to deliver software faster and more reliably through collaboration and automation.", "Foundation.", "One team owns build and run."),
("Beginner", "What is SDLC?", "Software Development Life Cycle: requirements, design, build, test, deploy, maintain.", "Basics.", "Agile iterates through it."),
("Beginner", "What is Agile?", "An iterative approach delivering small increments with continuous feedback.", "Process.", "Two-week sprints."),
("Beginner", "Scrum vs Kanban?", "Scrum uses time-boxed sprints and roles; Kanban is continuous flow with WIP limits.", "Frameworks.", "Ops teams often prefer Kanban."),
("Beginner", "What is SRE?", "Site Reliability Engineering: applying software engineering to operations to achieve reliability targets.", "Definition.", "SLOs and error budgets."),
("Beginner", "What is an incident?", "An unplanned event that degrades or interrupts a service.", "Terminology.", "Checkout errors."),
("Beginner", "What is on-call?", "Responsibility for responding to alerts outside normal hours on a rotation.", "Operations.", "PagerDuty rotation."),
("Beginner", "What is a postmortem?", "A written review of an incident: timeline, causes, actions.", "Learning.", "Blameless format."),
("Beginner", "What is toil?", "Manual, repetitive, automatable work that scales with service size and has no lasting value.", "SRE concept.", "Manually restarting a service."),
("Beginner", "What is CI/CD's role in DevOps?", "Automates build, test and delivery for fast, safe releases.", "Practice.", "Daily deploys."),
("Intermediate", "Explain SLI, SLO, SLA.", "SLI is a measurement, SLO a target for it, SLA a contractual promise with consequences; SLOs are stricter than SLAs.", "Core SRE.", "SLO 99.9%, SLA 99.5%."),
("Intermediate", "What is an error budget?", "The allowed unreliability (1 - SLO) over a period; it balances feature velocity and reliability work.", "Decision tool.", "Budget exhausted: freeze risky releases."),
("Intermediate", "DORA metrics?", "Deployment frequency, lead time for changes, change failure rate, time to restore service.", "Measuring delivery.", "Quarterly improvement."),
("Intermediate", "Incident management roles?", "Incident Commander coordinates, Communications lead updates stakeholders, Operations/SMEs fix, Scribe records timeline.", "Process.", "Sev1 bridge call."),
("Intermediate", "Severity levels?", "Defined levels (e.g. Sev1 critical customer-impacting to Sev4 minor) that set response urgency and communications.", "Triage.", "Sev1 pages immediately."),
("Intermediate", "What makes a good runbook?", "Clear trigger, diagnosis steps, commands, decision points, rollback and escalation contacts; kept current and linked from alerts.", "Operations.", "'Disk full' runbook."),
("Intermediate", "What is a blameless culture?", "Focus on systems and processes rather than individuals, encouraging open reporting and learning.", "Culture.", "Postmortem asks 'how did the system allow this'."),
("Intermediate", "MTTD, MTTA, MTTR?", "Mean time to detect, acknowledge, and recover/repair; used to measure incident response.", "Metrics.", "Reduce MTTR with rollbacks."),
("Intermediate", "What is chaos engineering?", "Deliberately injecting failures under controlled conditions to test and improve resilience.", "Resilience.", "Kill a pod/AZ."),
("Intermediate", "Load vs stress vs soak tests?", "Load: expected traffic; stress: beyond limits; soak: long duration to reveal leaks.", "Testing.", "Soak for memory leaks."),
("Intermediate", "What is capacity planning?", "Forecasting resource needs from growth and load tests to meet SLOs cost-effectively.", "Planning.", "Prepare for seasonal peak."),
("Intermediate", "What is a feature flag?", "A switch to enable/disable functionality at runtime without deploying.", "Safe releases.", "Gradual rollout."),
("Intermediate", "What is FinOps?", "Practice of managing cloud cost through visibility, accountability and optimisation across teams.", "Cost.", "Tag-based showback."),
("Intermediate", "What is a platform engineering team?", "A team building internal self-service platforms/golden paths for developers.", "Modern org design.", "Backstage templates."),
("Intermediate", "DevOps anti-patterns?", "DevOps team as silo, tool-only focus, blame culture, no measurement, manual heroics.", "Culture.", "'DevOps person' doing all deploys."),
("Advanced", "How do you set SLOs?", "Identify critical user journeys, choose SLIs that reflect user experience, measure baseline, agree targets with product, define error budget policy, review periodically.", "SRE practice.", "Checkout latency and success."),
("Advanced", "Explain multi-window burn-rate alerting.", "Alert when the error budget burns at a high rate over both a long and short window (e.g. 1h and 5m) to catch fast burns quickly and avoid noise.", "Modern alerting.", "14.4x for 1h pages."),
("Advanced", "How do you reduce toil systematically?", "Measure toil (target below about 50% of time), rank by frequency/effort, automate or eliminate the top items, track savings.", "Continuous improvement.", "Self-service restarts."),
("Advanced", "Design an incident process for a 24/7 service.", "Severity matrix, paging policy, IC role/rotation, war-room channel, status page, comms templates, runbooks, postmortem within days, action tracking.", "Process design.", "Follow-the-sun coverage."),
("Advanced", "How do you run a chaos experiment safely?", "Define steady state and hypothesis, limit blast radius, get approvals, monitor with abort conditions, start in staging, automate later in production, document learnings.", "Resilience practice.", "Game day with pod kill."),
("Advanced", "Explain graceful degradation.", "When dependencies fail, the system provides reduced functionality instead of total failure.", "Reliability design.", "Show cached recommendations."),
("Advanced", "Circuit breakers, retries, timeouts?", "Timeouts bound waiting; retries with backoff/jitter handle transient errors; circuit breakers stop calling failing dependencies to prevent cascading failure.", "Resilience patterns.", "Resilience4j/Envoy."),
("Advanced", "RPO and RTO?", "Recovery Point Objective is max acceptable data loss; Recovery Time Objective is max acceptable downtime.", "DR planning.", "RPO 5 min, RTO 30 min."),
("Advanced", "DR strategies?", "Backup/restore, pilot light, warm standby, multi-site active-active, balancing cost and RTO/RPO.", "DR design.", "Warm standby in second region."),
("Advanced", "How do you measure developer productivity/platform success?", "Adoption of golden paths, lead time, onboarding time, DORA, developer satisfaction, support tickets.", "Platform engineering.", "New service in a day."),
("Advanced", "Explain the Three Ways of DevOps.", "Flow (fast left-to-right delivery), Feedback (fast right-to-left), Continual learning and experimentation.", "Theory.", "The Phoenix Project."),
("Advanced", "How do you balance feature velocity and reliability?", "Error budgets: spend on change while within budget; when exhausted focus on reliability; agreed policy prevents arguments.", "SRE decision-making.", "Freeze on budget burn."),
("Advanced", "What is an incident postmortem quality bar?", "Clear timeline, systemic causes, detection/mitigation analysis, prioritised owned actions, shared broadly and reviewed.", "Learning quality.", "Action completion rate."),
("Advanced", "Metastable and cascading failures?", "Retries and overload amplify failure so it persists after the trigger; mitigate with load shedding, backoff, rate limits, capacity headroom.", "Advanced reliability.", "Retry storm."),
("Scenario-Based", "A Sev1 outage begins; what do you do first?", "Acknowledge, declare incident and roles, mitigate impact first (rollback/failover/scale), communicate status, gather data, then root cause later.", "Prioritisation.", "Rollback the release."),
("Scenario-Based", "Team says reliability work never gets prioritised.", "Introduce SLOs and error budgets with product agreement so reliability has a data-based claim on capacity.", "Influence.", "Budget policy."),
("Scenario-Based", "On-call engineers are getting paged 30 times a night.", "Audit alerts, remove non-actionable, group/inhibit, symptom-based SLO alerts, fix top noisy causes, automate remediations.", "Sustainability.", "Pages reduced by 80%."),
("Scenario-Based", "How to introduce DevOps in a siloed company?", "Start with a pilot team, shared goals/metrics, automate a painful process, celebrate wins, remove handoffs and blame, executive sponsorship.", "Change management.", "One product team owns pipeline."),
("Scenario-Based", "Prepare for a huge marketing event.", "Capacity model, load/spike tests, pre-scaling, cache/CDN, feature flags/kill switches, war room, runbooks, dependency contact list.", "Readiness.", "Sale day."),
("Scenario-Based", "Two incidents caused by the same missing alert.", "Add detection, update runbook, verify with a test; track postmortem actions with owners and deadlines.", "Learning loop.", "Disk space alert added."),
("Scenario-Based", "Executives ask for 100% uptime.", "Explain cost/benefit, propose SLO like 99.95% with error budget, design redundancy accordingly, clarify SLA vs SLO.", "Stakeholder communication.", "Each extra nine multiplies cost."),
("Scenario-Based", "Cloud bill grew 40% with no clear owner.", "Enable cost allocation tags, dashboards per team, budgets/alerts, rightsizing and commitments, review with owners monthly.", "FinOps.", "Idle GPU cluster."),
("Scenario-Based", "A postmortem reveals a human error (wrong command in prod).", "Focus on guardrails: confirmations, least privilege, dry-run, automation, staging parity; do not blame the individual.", "Blameless thinking.", "Add a `--dry-run` default."),
("Scenario-Based", "How to onboard a new developer to deploy safely?", "Golden path templates, self-service pipelines, guardrails via policy as code, documentation and paired first deploy.", "Platform engineering.", "Deploy in first week."),
("Scenario-Based", "Release frequency is low; how to improve?", "Measure lead time bottlenecks, shrink batch size, automate tests/approvals, trunk-based dev, feature flags, progressive delivery.", "Delivery improvement.", "Weekly to daily."),
("Scenario-Based", "A dependency team's service keeps failing you.", "Define SLOs and contracts, add timeouts/circuit breakers/fallbacks, joint reliability review, escalate with data.", "Dependency management.", "Third-party payment API."),
("Scenario-Based", "Design a game day for a region outage.", "Define scope and abort criteria, simulate region failure in staging or with FIS, verify DNS failover, data replication, runbooks, RTO/RPO, debrief.", "DR verification.", "Failover took 22 min vs 10 target."),
("Scenario-Based", "Developers resist being on-call.", "Reduce toil and noise, provide training/runbooks, fair rotation and compensation, make ownership benefits visible (fewer incidents).", "Culture.", "Better quality when developers carry pager."),
("Troubleshooting-Based", "Alerts fire but nobody responds.", "Check escalation policy, contact info, schedule gaps, alert routing and acknowledgement rules; test paging regularly.", "Process reliability.", "Wrong phone number."),
("Troubleshooting-Based", "Postmortem actions never completed.", "Lack of owner/priority/time; add tickets with owners, review in a recurring meeting, limit number of actions to meaningful ones.", "Follow-through.", "Track completion %."),
("Troubleshooting-Based", "SLO dashboard shows green but users complain.", "SLI does not represent user experience (wrong measurement point, missing journeys); measure at the edge/synthetic checks, refine SLIs.", "Measurement quality.", "Login flow missing from SLI."),
("Troubleshooting-Based", "Chaos experiment caused a real outage.", "Blast radius too large or missing abort conditions; start smaller, use staging, gradual rollout, communicate, add safeguards.", "Experiment safety.", "AZ-level fault without approvals."),
("Troubleshooting-Based", "Load test results differ from production.", "Test data/environment/traffic mix mismatch, caches cold/warm differences; use production-like data and realistic scenarios.", "Test validity.", "Only GET requests tested."),
("Troubleshooting-Based", "MTTR is increasing.", "Detection delays, unclear ownership, missing runbooks, complex deployments; analyse incident timelines and invest in observability and rollback speed.", "Diagnosis.", "Slow rollbacks."),
("Troubleshooting-Based", "Too many meetings, little improvement (DevOps 'theatre').", "Focus on measured outcomes (DORA), remove handoffs, automate; avoid ritual without change.", "Culture check.", "Renamed teams only."),
("Troubleshooting-Based", "Incident communications are inconsistent.", "Use templates, a single comms owner and update cadence (e.g. every 30 minutes) and a status page.", "Communication.", "Customers not informed."),
("Troubleshooting-Based", "Toil grows as the service grows.", "Measure and cap toil, automate the top offenders, build self-service tools, eliminate root causes.", "Scalability of ops.", "Ticket-driven access requests."),
("Troubleshooting-Based", "Cost anomalies found late.", "Set budgets and anomaly alerts, daily cost dashboards, tagging enforcement, owner notifications.", "FinOps operations.", "Runaway logging cost.")],
cheatsheet={
"Definitions": ["DevOps culture (CALMS); SRE; SLI/SLO/SLA; error budget = 1 - SLO; toil; MTTD/MTTA/MTTR; RPO/RTO; blameless postmortem; chaos engineering; platform engineering; FinOps."],
"Commands": ["`k6 run load.js` `kubectl delete pod -l app=x` `kubectl get pods -w` `amtool silence add`", "PromQL SLI: `sum(rate(http_requests_total{status!~\"5..\"}[30d])) / sum(rate(http_requests_total[30d]))`", "Error budget minutes = (1 - SLO) x 43,200 (30 days)"],
"Files": ["SLO definitions (YAML), runbooks, postmortem docs, on-call schedules, game day plans, cost dashboards"],
"Architecture": ["Plan > Build > Release > Operate > Incident > Postmortem > Improve (loop)."],
"Ports": ["N/A (process/culture topic); monitoring tools per their ports."],
"Differences": ["DevOps vs SRE vs Platform; Agile vs Waterfall; Scrum vs Kanban; SLI/SLO/SLA; load vs stress vs soak; blameful vs blameless."],
"Troubleshooting commands": ["Incident: dashboards (golden signals) > recent deploys > rollback/failover > logs/traces > communicate > postmortem"],
"Best practices": ["SLOs with error budgets, actionable alerts, runbooks, blameless postmortems with tracked actions, toil budget, chaos/game days, load tests, FinOps."]}
),
subs={
"devops-culture-sdlc": dict(
define=dict(simple="DevOps culture means developers and operations share responsibility for the whole life of the software.",
technical="DevOps combines cultural philosophies (CALMS: culture, automation, lean, measurement, sharing), practices (CI/CD, IaC, monitoring) and Agile methods to shorten lead time and improve reliability across the SDLC.",
why="Break down silos and speed up safe delivery.", without="Handoff delays and blame.", use="Any software organisation.", avoid="Tool-only 'DevOps' without culture change.", analogy="A relay team where everyone owns the finish line, not just their leg."),
internals="""The value stream (idea to production) is mapped to find waiting and rework; small batches, automation, fast feedback and shared metrics reduce delays. Agile frameworks (Scrum sprints, Kanban flow) organise work; CI/CD and IaC make releases routine; monitoring and postmortems close the feedback loop.""",
lab=dict(goal="Map your delivery value stream and compute lead time.", prereq=["A team project or sample project", "Whiteboard/spreadsheet"],
steps=[("Write each step from 'idea' to 'in production' with typical wait time and work time", "Reveals bottlenecks such as manual approvals or slow test environments."), ("Compute lead time = sum(work + wait) and flow efficiency = work / lead time", "Low efficiency (often under 20%) shows where automation helps."), ("Pick one bottleneck and define a small experiment (for example automate approval checks) with a measurable target", "Continuous improvement in practice.")]),
compare=[("Agile frameworks", ["Framework", "Cadence", "Best for"], [["Scrum", "Sprints (1-4 weeks)", "Product development with roles and ceremonies"], ["Kanban", "Continuous", "Ops/support, flow-based work"], ["XP", "Short iterations", "Engineering practices: TDD, pair programming"]])],
mnemonics=[("CALMS", "Culture, Automation, Lean, Measurement, Sharing"), ("Three Ways", "Flow, Feedback, Learning")], hinglish="DevOps **team aur mindset** ka badlav hai, sirf Jenkins ya Docker nahi. **Chhote batches, automation, feedback aur ownership** yahi core hai.",
practices={"Development": ["Small batches; definition of done includes monitoring and runbook."]}, mistakes={"Beginner mistakes": ["Creating a separate 'DevOps team' that becomes a new silo."]},
qa_extra=[("Intermediate", "What does 'you build it, you run it' mean?", "The team that develops a service is also responsible for operating it (on-call), which creates strong incentives for quality and observability.", "Ownership principle.", "Amazon's model.")]),

"incident-management": dict(
define=dict(simple="A clear way to respond to outages quickly and then learn from them.",
technical="Incident management defines detection, severity classification, roles (IC, comms, ops), communication, mitigation-first response, resolution, and blameless postmortem with tracked actions.",
why="Minimise customer impact and recurrence.", without="Chaos, duplicated effort and repeated failures.", use="Any production service.", avoid="Hunting for root cause before mitigating.", analogy="Emergency room triage: stabilise first, diagnose fully after."),
internals="""An alert pages on-call > they acknowledge and assess severity > for Sev1/2 an incident is declared with an Incident Commander who assigns roles in a dedicated channel > the priority is **mitigation** (rollback, failover, scale, disable feature) > communications updates on a cadence > when service is restored the incident is resolved > within days a postmortem is written and reviewed > action items are tracked.""",
config=[("Incident channel first message template explained", """:rotating_light: SEV1 declared - checkout errors > 5%
IC: @alice | Comms: @bob | Ops: @carol, @dave
Impact: ~30% of checkout requests failing since 10:12 UTC
Status: investigating; recent deploy 10:05 UTC is suspect
Next update: 10:45 UTC""", [("Severity + impact", "Sets urgency and shared understanding."), ("Roles", "IC coordinates; Comms handles stakeholders; Ops investigate."), ("Suspected cause/status", "Recent change is the first thing to check."), ("Next update time", "Regular cadence reduces interruptions and anxiety.")])],
lab=dict(goal="Run a tabletop incident exercise.", prereq=["2 to 4 people", "A sample architecture", "A timer"],
steps=[("Scenario: 'Error rate on checkout jumps to 20% at 10:00'. Assign IC, Comms, Ops", "Practise role clarity."), ("Walk through: acknowledge, assess severity, check dashboards/deploys, decide rollback, write two customer updates", "Mitigation before root cause."), ("Write a short postmortem with 3 action items (prevent, detect, mitigate)", "Close the learning loop.")]),
mnemonics=[("Incident flow", "Detect > Triage > Mitigate > Resolve > Communicate > Learn")], hinglish="Incident mein pehle **service restore** karo (rollback/failover), root cause baad mein. **IC, Comms, Ops** roles alag rakho aur **regular updates** do.",
practices={"Reliability": ["Practise with game days; keep runbooks updated."], "Monitoring & Logging": ["Preserve timelines and chat logs for postmortems."]}, mistakes={"Production mistakes": ["Everyone debugging, nobody communicating."]},
qa_extra=[("Scenario-Based", "You suspect a recent deploy caused the outage. What next?", "Roll back (or disable via feature flag) first to restore service, verify metrics recover, then investigate the change offline.", "Mitigation-first.", "Rollback restored service in 4 minutes.")]),

"chaos-load-testing": dict(
define=dict(simple="Load testing checks how the system behaves under traffic; chaos engineering checks how it behaves when parts fail.",
technical="Load/stress/spike/soak tests (k6, JMeter, Locust) validate capacity and latency SLOs; chaos experiments inject faults (pod/node/AZ failure, latency, packet loss) under a steady-state hypothesis with controlled blast radius.",
why="Find weaknesses before customers do.", without="Surprises during peaks or outages.", use="Before major releases/events and regularly.", avoid="Uncontrolled experiments in production without safeguards.", analogy="Fire drills and stress tests for a building."),
internals="""Chaos loop: define steady state (SLIs) > hypothesis ('killing one pod keeps error rate below 1%') > run experiment with limited blast radius and abort conditions > observe > learn/fix > repeat. Load tests generate concurrent virtual users, measure percentiles and error rates, and compare to thresholds; results guide autoscaling limits and capacity.""",
config=[("k6 script explained", """import http from 'k6/http';
import { check } from 'k6';
export const options = {
  scenarios: { spike: { executor: 'ramping-arrival-rate', startRate: 10, timeUnit: '1s', preAllocatedVUs: 100, stages: [{ target: 200, duration: '1m' }, { target: 10, duration: '1m' }] } },
  thresholds: { http_req_failed: ['rate<0.01'], http_req_duration: ['p(95)<500'] },
};
export default function () {
  check(http.get('https://staging.example.com/api/health'), { ok: (r) => r.status === 200 });
}""", [("ramping-arrival-rate", "Controls requests per second (open model), better for realistic load."), ("stages", "Ramp up to a 200 req/s spike then down."), ("thresholds", "Pass/fail SLO-like criteria."), ("staging URL", "Test only environments you own/are permitted to test.")])],
lab=dict(goal="Kill pods and observe recovery.", prereq=["Kubernetes cluster", "Deployment with 3 replicas and a Service"],
steps=[("kubectl get pods -w", "Watch in terminal 1."), ("while true; do curl -s -o /dev/null -w '%{http_code}\\n' http://<service>; sleep 0.5; done", "Terminal 2 shows responses."), ("kubectl delete pod <one-pod>", "The ReplicaSet recreates it; responses should stay 200 if readiness/replicas are right: hypothesis validated (or finding revealed).")]),
compare=[("Chaos tools", ["Tool", "Scope"], [["Chaos Mesh / Litmus", "Kubernetes fault injection"], ["AWS Fault Injection Service", "AWS resources (EC2, RDS, network)"], ["Gremlin", "Commercial, multi-platform"]])],
mnemonics=[("Chaos", "Hypothesis, Blast radius, Abort condition, Learn")], hinglish="Chaos engineering mein **chhoti failure jaan-boojh kar** daalte hain, **blast radius chhota** aur **abort condition** pehle se tay. Load test se pehle **thresholds** set karo.",
practices={"Reliability": ["Start in staging; automate experiments; fix findings."], "Performance": ["Load test before events; use production-like data."]}, mistakes={"Production mistakes": ["Chaos without abort criteria.", "Unrealistic load test data."]},
versions=["Tool APIs change (Chaos Mesh CRDs, Litmus, AWS FIS templates): use the current docs. Load-testing only systems you are authorised to test."],
qa_extra=[("Advanced", "Open vs closed load model?", "Closed model has fixed users who wait for responses (rate self-limits); open model sends arrivals at a fixed rate regardless of latency, exposing overload behaviour more realistically.", "Test design.", "Arrival-rate executors in k6.")]),

"platform-finops": dict(
define=dict(simple="Platform engineering builds easy self-service tools for developers; FinOps keeps cloud spending under control.",
technical="Platform engineering delivers an internal developer platform (IDP) with golden paths, templates, catalogs and guardrails; FinOps applies visibility, allocation, optimisation and governance to cloud costs through collaboration between engineering, finance and product.",
why="Reduce cognitive load and cost waste at scale.", without="Every team reinvents pipelines/infra and nobody owns spend.", use="Organisations with many teams/services.", avoid="Building a platform nobody asked for.", analogy="A company kitchen with ready recipes and a budget dashboard."),
internals="""A developer requests a new service via a portal template (Backstage) > scaffolder creates the repo, CI pipeline, Helm chart, monitoring dashboards and cloud resources through Terraform/Crossplane > guardrails via policy as code apply automatically > costs are tagged by team/service and shown in dashboards > budgets/anomaly alerts notify owners.""",
config=[("Cost tagging and budget example explained", """# Terraform: consistent tags for cost allocation
provider "aws" {
  default_tags { tags = { team = "payments", service = "checkout", env = "prod", cost-center = "cc-1042" } }
}
# CLI: monthly budget with alert at 80%
aws budgets create-budget --account-id 123456789012 --budget file://budget.json --notifications-with-subscribers file://notif.json""", [("default_tags", "Every resource gets team/service tags, enabling cost allocation."), ("cost-center", "Links spend to finance codes."), ("budgets", "Alerts owners before overspend; anomaly detection catches surprises.")])],
lab=dict(goal="Find cost waste in an AWS account (read-only).", prereq=["AWS CLI with read access to Cost Explorer/EC2"],
steps=[("aws ce get-cost-and-usage --time-period Start=2026-08-01,End=2026-09-01 --granularity MONTHLY --metrics UnblendedCost --group-by Type=DIMENSION,Key=SERVICE", "Cost by service (adjust dates)."), ("aws ec2 describe-volumes --filters Name=status,Values=available --query 'Volumes[].{ID:VolumeId,Size:Size}'", "Unattached EBS volumes are waste."), ("aws ec2 describe-addresses --query 'Addresses[?AssociationId==null]'", "Unassociated Elastic IPs cost money.")]),
compare=[("FinOps levers", ["Lever", "Example", "Typical effect"], [["Rightsizing", "Smaller instance types", "Medium"], ["Commitments", "Savings Plans/Reserved", "High for steady load"], ["Spot", "Batch/stateless on Spot", "High, with interruption risk"], ["Scheduling", "Stop dev at night", "Medium"], ["Architecture", "Serverless/caching/VPC endpoints", "Varies"]])],
mnemonics=[("FinOps loop", "Inform > Optimize > Operate")], hinglish="Cloud bill ko **tag** karo taaki pata chale kaun kitna use kar raha hai. **Budget alert, rightsizing, Savings Plans, Spot** aur idle resources delete karna: yeh main levers hain.",
practices={"Cost Optimization": ["Tagging policy, budgets, anomaly alerts, monthly reviews, commitments for baseline."], "Production": ["Golden paths with guardrails."]}, mistakes={"DevOps mistakes": ["No tagging.", "Building a platform without user feedback."]},
versions=["Cloud pricing and Savings Plan terms change: verify on the provider's pricing pages. Backstage and Crossplane APIs evolve quickly."],
qa_extra=[("Scenario-Based", "How to reduce cloud cost without hurting reliability?", "Start with waste (idle/unattached), rightsize using utilisation data, commit for baseline, Spot for fault-tolerant workloads, keep SLOs and redundancy for critical paths, and track savings.", "FinOps judgement.", "Dev environments scheduled off at night.")])
})
