EXT = dict(
guide=dict(
bigpicture=dict(
problem="""**Problem it solves:** Manual releases are slow, risky and inconsistent: someone builds on a laptop, forgets to run tests, copies files to a server by hand, and a bug reaches users. **CI/CD** (Continuous Integration / Continuous Delivery or Deployment) automates the path from a code commit to a running application, with tests and checks at every step.""",
chain=["PROBLEM: releasing software by hand is slow and error-prone",
       "TRADITIONAL APPROACH: big releases every few weeks, manual build, manual tests, manual copy to servers",
       "PAIN: integration bugs found late, 'release nights', no traceability, hard rollbacks",
       "TECHNOLOGY: CI/CD pipelines (Jenkins, GitHub Actions, GitLab CI, ArgoCD)",
       "SOLUTION: every commit is built, tested, scanned and (after approval or automatically) deployed",
       "REAL-WORLD BENEFIT: small frequent safe releases, fast feedback, audit trail, quick rollback"],
text="""**CI** = Continuous Integration: merge code often and verify each change automatically (build + tests). **CD** = Continuous Delivery (every change is *ready* to deploy, a human approves) or Continuous Deployment (every passing change is deployed automatically)."""),
e2e=dict(diagram="""Developer
   | git push / Pull Request
   v
Git Repository (GitHub/GitLab)
   | webhook
   v
CI Server (Jenkins / GitHub Actions runner)
   v
Build (compile / npm ci)
   v
Unit Tests
   v
Code Quality (SonarQube) --> Quality Gate
   v
Docker Build
   v
Security Scan (Trivy, secrets, SCA)
   v
Push to Registry (Harbor / ECR)  [tag = git sha]
   v
Deploy to Staging (Helm / ArgoCD)
   v
Smoke / Integration Tests
   v
Approval Gate (for prod) --> Deploy to Production
   v
Kubernetes runs the application
   v
Monitoring (Prometheus/Grafana) + Notifications (Slack)  --> failure? Rollback""",
text="""A **push or pull request** triggers a **webhook**: Git tells the CI server something changed. The CI server allocates an **agent/runner**, checks out the code and runs the **pipeline** stages. **Build** compiles and installs dependencies; **unit tests** prove logic; **SonarQube** analyses code quality and the **quality gate** fails the pipeline if standards are not met. **Docker build** creates the image, **Trivy** scans it and dependency/secret scans run. The image is tagged with the commit SHA (immutable, traceable) and pushed to the **registry**. **CD** then deploys that same image to staging, runs smoke tests, waits for an **approval gate** for production and deploys with a safe strategy (rolling/canary/blue-green). **Monitoring** watches the new release; if error rate rises, the pipeline or ArgoCD rolls back, and **notifications** tell the team at every failure."""),
tools=dict(rows=[
["Git (GitHub/GitLab)", "Source of truth, triggers", "Commits/PRs", "Webhook events", "Start of pipeline"],
["Jenkins / GitHub Actions / GitLab CI", "Run pipeline stages", "Pipeline file (Jenkinsfile/workflow)", "Build results, artifacts", "CI orchestration"],
["Maven/npm/pip/go", "Build and dependency management", "Source", "Package/binary", "Build stage"],
["SonarQube", "Static code quality/SAST", "Source + coverage", "Quality gate result", "After tests"],
["Docker/BuildKit", "Package app", "Dockerfile + source", "Image", "Package stage"],
["Trivy / Snyk / Gitleaks", "Vulnerability and secret scan", "Image/deps/repo", "Report, exit code", "Security stage"],
["Harbor / ECR / Nexus / Artifactory", "Store images/artifacts", "Image/package", "Versioned artifact", "Between CI and CD"],
["Helm / ArgoCD / Flux", "Deploy to Kubernetes", "Chart/manifests in Git", "Running release", "CD stage"],
["Prometheus / Grafana / Slack", "Observe and notify", "Metrics/build events", "Alerts, dashboards", "After deploy"]],
why="**Jenkins vs GitHub Actions:** Jenkins is self-hosted, extremely flexible with many plugins but you maintain it; GitHub Actions is managed, YAML in the repo, easy start, great marketplace, cost per minute for private repos. **Push-based CD vs GitOps (ArgoCD):** push-based CD gives the CI system cluster credentials; GitOps pulls from Git inside the cluster (safer, auditable, self-healing drift)."),
compare=[
("CI vs CD", ["Topic", "CI", "CD"], [["Goal", "Integrate code often, verify automatically", "Release automatically or on approval"], ["Output", "Tested build/image", "Deployed application"], ["Key checks", "Build, unit tests, lint, scan", "Integration/smoke tests, approvals, rollout"]]),
("Continuous Delivery vs Continuous Deployment", ["Topic", "Delivery", "Deployment"], [["Prod release", "Manual approval click", "Fully automatic"], ["Needs", "Solid tests", "Excellent tests, monitoring, feature flags"], ["Typical", "Banks, regulated", "SaaS with strong automation"]]),
("Artifact vs Image", ["Topic", "Artifact", "Image"], [["Meaning", "Any build output (jar, zip, binary)", "Container image (special artifact)"], ["Stored in", "Nexus/Artifactory/S3", "Container registry"]]),
("Jenkins vs GitHub Actions", ["Topic", "Jenkins", "GitHub Actions"], [["Hosting", "Self-hosted", "SaaS (or self-hosted runners)"], ["Config", "Jenkinsfile (Groovy)", "YAML workflows"], ["Extensibility", "1800+ plugins", "Marketplace actions"], ["Maintenance", "You patch and scale", "Managed by GitHub"]]),
("Rolling vs Blue/Green vs Canary", ["Topic", "Rolling", "Blue/Green", "Canary"], [["Traffic", "Gradual replacement", "Instant switch", "Small % first"], ["Rollback speed", "Medium", "Fastest", "Fast"], ["Extra cost", "Low", "High", "Medium"], ["Risk exposure", "Medium", "Low (pre-test) but all-at-once", "Lowest"]]),
("Docker Hub vs Harbor", ["Topic", "Docker Hub", "Harbor"], [["Where", "Public SaaS", "Self-hosted private"], ["Extras", "Basic", "RBAC, replication, scanning, signing"]])],
troubleshooting=[
("Pipeline does not trigger on push", "Webhook not configured/failing, branch filter, path filter, wrong event", "Repo webhook delivery log; workflow `on:` / Jenkins multibranch scan log", "Fix webhook URL/secret or trigger config.", "Test webhook after setup; keep triggers simple."),
("Build works locally but fails in CI", "Different tool versions, missing env/secrets, cached files, OS differences", "Read the failing step log; compare versions; run in the same container image locally", "Pin versions; build in a container; provide required secrets.", "Use the same Docker image for local and CI."),
("Flaky tests", "Shared state, timing, external services, order dependence", "Re-run history; run test alone/in isolation", "Fix test isolation, use test containers/mocks, retry only as last resort.", "Quarantine flaky tests and track them."),
("Docker push denied/unauthorized", "Missing/expired registry credentials or wrong repo path", "`docker login` output; check secret; repo permissions", "Refresh credentials; use OIDC short-lived tokens.", "Avoid long-lived static credentials."),
("Deployment succeeded but app is broken", "No smoke test/readiness gate, config mismatch, bad migration", "App logs, `kubectl rollout status`, dashboards", "Roll back to previous image tag; fix forward.", "Add smoke tests, readiness probes, automatic rollback."),
("Secrets leaked in pipeline logs", "`echo` of variable, debug mode, unmasked secrets", "Search logs; secret scanner", "Rotate the secret immediately; mask/never print.", "Use masked secrets and secret managers; scanning in CI.")],
practices={
"Development": ["Small commits and short-lived branches; run the same checks locally (pre-commit)."],
"Production": ["Build once, deploy the same immutable image everywhere; tag with git SHA.", "Environment promotion: dev > staging > prod with the same artifact.", "Automatic rollback and post-deploy smoke tests."],
"Security": ["Least-privilege pipeline credentials; OIDC instead of static keys; secrets in a vault; never print secrets.", "SAST, SCA, secret scan, image scan, SBOM, signing; branch protection and required reviews; pin action versions/SHAs."],
"Performance": ["Cache dependencies and Docker layers; parallelise stages; use ephemeral/autoscaling agents."],
"Reliability": ["Timeouts and retries for infra steps; idempotent deploy scripts; pipeline as code with review."],
"Cost Optimization": ["Auto-scale runners, cancel superseded runs, spot agents, cleanup old artifacts."],
"Monitoring & Logging": ["Track lead time, deployment frequency, change failure rate, MTTR (DORA metrics); notify on failure."],
"Backup & Disaster Recovery": ["Back up Jenkins home/config as code (JCasC); keep pipeline definitions in Git."]},
mistakes={
"Beginner mistakes": ["Hard-coding secrets in the pipeline file.", "One giant stage that does everything."],
"Developer mistakes": ["Skipping tests to 'get it green'.", "Committing to main directly with no PR."],
"DevOps mistakes": ["Rebuilding a different image per environment.", "No rollback plan.", "Snowflake Jenkins servers without config as code."],
"Production mistakes": ["Deploying on Friday without monitoring/automatic rollback.", "No approval gate for prod when required by policy."],
"Security mistakes": ["Running pipelines from forks with secrets.", "Using `latest` and unpinned third-party actions/plugins.", "Over-privileged deploy credentials."]},
versions=[
"GitHub Actions: pin actions by major version or commit SHA (for example `actions/checkout@v4`); check the marketplace for current versions; Node runtime versions of actions change.",
"Jenkins: use LTS releases; Declarative Pipeline is preferred over Scripted for most cases; plugins need regular updates; check the security advisories.",
"ArgoCD: Application CRD fields and sync options change between versions; check argo-cd docs for your version.",
"Deprecated: Docker `latest`-only deployments, Jenkins freestyle-only jobs and storing credentials in job config; use pipeline as code and credential stores."],
hinglish="""**CI** ka matlab hai har code change par **automatic build + test**. **CD** ka matlab hai wo tested build **automatically (ya approval ke baad) deploy** hona. Pipeline mein stages hote hain: build, test, scan, package, push, deploy. Ek hi **image ek baar build** karo aur usi ko dev se prod tak promote karo. **Webhook** Git ko CI se jodta hai. Rollback ka matlab pichli working image dobara deploy karna.""",
mnemonics=[
("Pipeline order", "B-T-Q-S-P-D: Build, Test, Quality, Security, Package, Deploy"),
("Delivery vs Deployment", "Delivery = a human presses the button; Deployment = the pipeline presses it"),
("DORA metrics", "Deploy frequency, Lead time, Change failure rate, MTTR"),
("Fail fast", "Cheapest checks first (lint, unit) then expensive ones (integration, scan)")],
client=dict(
s30="""CI/CD is an automated assembly line for software. Every code change is automatically built, tested, security-checked and delivered, so we release faster, with fewer errors, and can roll back quickly if something goes wrong.""",
m2="""Without CI/CD, releases depend on manual steps: someone builds, tests and copies files by hand, which is slow and error-prone. With CI/CD, when a developer pushes code, a pipeline automatically builds the application, runs tests, checks code quality and security, packages it as a container image and stores it in a registry. Then the same image is deployed to staging and, after approval or automatically, to production with a safe strategy such as rolling or canary. You get faster releases, consistent quality, a full audit trail of who released what, and a one-step rollback. We also track delivery metrics so you can see improvement over time.""",
m5="""Think of four layers. **First, integration:** developers merge small changes often; each change triggers a pipeline that builds and runs automated tests, and a quality gate blocks poor code. **Second, security and packaging:** the pipeline scans dependencies, secrets and the container image, then produces one immutable, versioned image in a private registry. **Third, delivery:** the same image is promoted through environments. In Kubernetes we use GitOps with ArgoCD, so the desired state lives in Git, deployments are pull-based and auditable, and drift is corrected automatically. Production releases use rolling, blue/green or canary strategies with automatic rollback based on monitoring. **Fourth, governance and improvement:** approvals for regulated environments, secrets in a vault, notifications, and DORA metrics (deployment frequency, lead time, change failure rate, recovery time). The outcome is shorter time to market, lower release risk and predictable operations."""),
roadmap=[
("Beginner", ["Git basics and branching", "What is CI vs CD", "First pipeline: build + test", "Docker basics"]),
("Intermediate", ["GitHub Actions/Jenkins in depth", "Caching, artifacts, matrix builds", "Docker build + push", "Secrets and credentials", "SonarQube + Trivy"]),
("Advanced", ["Deployment strategies", "GitOps with ArgoCD", "Environment promotion, approvals", "Pipeline security and OIDC", "Shared libraries / reusable workflows"]),
("Production", ["Rollback automation", "Monitoring after deploy, DORA metrics", "Scaling runners, cost control", "Compliance/audit"]),
("Interview", ["Design a pipeline end to end", "Explain Jenkins architecture", "Blue/green vs canary", "Debug a failing pipeline"])],
miniproject=dict(title="GitHub Actions pipeline: build, test, scan, push, deploy via ArgoCD",
arch="""Git push --> GitHub Actions
   build+test -> SonarQube gate -> docker build -> Trivy scan -> push to Harbor/ECR (tag=SHA)
   -> update image tag in GitOps repo (PR/commit)
   -> ArgoCD detects change -> syncs to Kubernetes (staging, then prod after approval)
   -> Prometheus/Grafana + Slack notification""",
steps=[
("Step 1: Workflow file .github/workflows/ci.yml", """name: ci
on:
  push: { branches: [main] }
  pull_request:
permissions: { contents: read }
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20, cache: npm }
      - run: npm ci
      - run: npm test
      - name: Build image
        run: docker build -t registry.example.com/shop/api:${{ github.sha }} .
      - name: Scan image
        uses: aquasecurity/trivy-action@0.28.0
        with:
          image-ref: registry.example.com/shop/api:${{ github.sha }}
          severity: HIGH,CRITICAL
          exit-code: '1'
      - name: Login and push
        if: github.ref == 'refs/heads/main'
        run: |
          echo "${{ secrets.REGISTRY_PASSWORD }}" | docker login registry.example.com -u "${{ secrets.REGISTRY_USER }}" --password-stdin
          docker push registry.example.com/shop/api:${{ github.sha }}""", "`on` defines triggers; `permissions` limits the token; `checkout` gets code; `setup-node` with `cache` speeds installs; tests run before build; the image is tagged with the commit SHA so every deployment is traceable; Trivy fails the job (`exit-code: 1`) on HIGH/CRITICAL findings; push happens only on `main`. Secrets come from repository secrets (or use OIDC in production). Action versions vary: check the marketplace for current tags."),
("Step 2: Update GitOps repo", """git clone https://github.com/acme/gitops.git && cd gitops
yq -i '.image.tag = "'$GITHUB_SHA'"' apps/api/values-staging.yaml
git commit -am "api: deploy $GITHUB_SHA" && git push""", "CI does not touch the cluster. It changes the desired state in Git; ArgoCD pulls and applies it (auditable and reversible with `git revert`)."),
("Step 3: ArgoCD Application", """apiVersion: argoproj.io/v1alpha1
kind: Application
metadata: { name: api-staging, namespace: argocd }
spec:
  project: default
  source: { repoURL: https://github.com/acme/gitops.git, path: apps/api, targetRevision: main, helm: { valueFiles: [values-staging.yaml] } }
  destination: { server: https://kubernetes.default.svc, namespace: staging }
  syncPolicy: { automated: { prune: true, selfHeal: true } }""", "`automated` sync applies Git changes; `selfHeal` reverts manual drift; `prune` removes deleted resources. For production use manual sync or an approval step."),
("Step 4: Verify and roll back", """argocd app get api-staging
kubectl -n staging rollout status deploy/api
git revert HEAD && git push   # rollback = revert the commit""", "Check sync/health, confirm rollout and roll back by reverting the Git commit.")]),
interview=[
("Beginner", "What is CI/CD?", "CI automatically builds and tests every code change; CD automatically delivers/deploys tested changes to environments.", "Foundation.", "Push triggers build, tests and deployment to staging."),
("Beginner", "What is a pipeline?", "An automated sequence of stages (build, test, scan, deploy) defined as code.", "Basic vocabulary.", "Jenkinsfile or workflow YAML."),
("Beginner", "What is a webhook?", "An HTTP callback that Git sends to the CI server on events like push.", "How triggers work.", "GitHub webhook to Jenkins."),
("Beginner", "What is an artifact?", "A build output such as a jar, zip or Docker image stored for later stages.", "Build once, deploy many.", "Image in Harbor."),
("Beginner", "What is Jenkins?", "An open-source, self-hosted automation server for CI/CD with a large plugin ecosystem.", "Very common tool.", "Multibranch pipeline building on each PR."),
("Beginner", "What is GitHub Actions?", "GitHub's built-in CI/CD using YAML workflows run on hosted or self-hosted runners.", "Modern default.", "`.github/workflows/ci.yml`."),
("Beginner", "What is a stage vs a job/step?", "Stage: logical phase; job: unit run on one runner; step: single command/action.", "Terminology.", "Job `build` with steps checkout, test."),
("Beginner", "Why run tests in CI?", "Catch bugs early before merge and keep main releasable.", "Quality gate.", "PR blocked when tests fail."),
("Beginner", "What is a rollback?", "Returning to the previous known-good version.", "Safety.", "Deploy previous image tag."),
("Beginner", "What is a quality gate?", "A rule (for example coverage, no critical issues) that must pass or the pipeline fails.", "Quality control.", "SonarQube gate."),
("Intermediate", "Continuous Delivery vs Deployment?", "Delivery keeps every change deployable but prod release needs approval; Deployment automatically releases every passing change.", "Common question.", "Bank: delivery; SaaS: deployment."),
("Intermediate", "Describe a full CI/CD flow for a containerised app.", "Push > webhook > build/test > Sonar > docker build > scan > push registry > deploy staging > smoke test > approval > prod > monitor/rollback.", "Big-picture skill.", "See e2e diagram."),
("Intermediate", "How do you handle secrets in pipelines?", "Store in the CI secret store or a vault, inject at runtime, mask in logs, prefer OIDC/short-lived credentials, rotate.", "Security basics.", "GitHub OIDC to AWS role."),
("Intermediate", "How to speed up pipelines?", "Cache dependencies/layers, parallel jobs, matrix builds, incremental builds, smaller images, ephemeral autoscaled runners.", "Efficiency.", "Cache npm and Docker layers."),
("Intermediate", "What is a Jenkins agent?", "A node that executes pipeline stages, keeping the controller free; can be static or dynamic (Kubernetes Pods).", "Jenkins architecture.", "Pod agents per build."),
("Intermediate", "Jenkinsfile: Declarative vs Scripted?", "Declarative has a structured `pipeline {}` syntax and validation; Scripted is free-form Groovy. Prefer Declarative.", "Jenkins depth.", "Use script blocks sparingly."),
("Intermediate", "What is environment promotion?", "Moving the same artifact through dev, staging, prod with increasing gates.", "Release management.", "Same image SHA in all environments."),
("Intermediate", "How do you version images?", "Immutable tags (git SHA or semver), avoid `latest`, optionally digest pinning.", "Traceability.", "`api:1.4.2-3fa9c1d`."),
("Intermediate", "What is a matrix build?", "Running the same job with multiple parameters (OS, language versions) in parallel.", "Compatibility testing.", "Node 18/20/22."),
("Intermediate", "What is a reusable workflow / shared library?", "Central pipeline templates reused across repos (GitHub reusable workflows, Jenkins shared libraries).", "Standardisation.", "Company-wide build template."),
("Intermediate", "How do you protect the main branch?", "Branch protection: required reviews, status checks, no force-push, signed commits.", "Governance.", "PR must pass CI."),
("Intermediate", "What is GitOps?", "Git holds the desired state; an in-cluster agent (ArgoCD/Flux) continuously reconciles the cluster to Git.", "Modern CD.", "Rollback with git revert."),
("Intermediate", "Push-based vs pull-based deployment?", "Push: CI has cluster credentials and applies; Pull: agent in cluster pulls from Git (no inbound credentials, drift correction).", "Security trade-off.", "ArgoCD pull model."),
("Intermediate", "Explain Jenkins architecture.", "Controller (schedules, UI, config) and agents (execute builds), plugins, credentials store, jobs/pipelines.", "Common Jenkins question.", "Kubernetes plugin spins agent Pods."),
("Advanced", "Design a secure pipeline.", "Least privilege runners, OIDC, secret scanning, SAST/SCA/image scan, SBOM, signing, provenance (SLSA), branch protection, no secrets for forks, pinned dependencies, audit logs.", "DevSecOps.", "Cosign-signed images verified at admission."),
("Advanced", "Blue/green vs canary vs rolling?", "Rolling replaces gradually (simple); blue/green switches all traffic between two environments (fast rollback, 2x cost); canary sends small traffic share and observes metrics before increasing.", "Release strategy.", "Canary 5% > 25% > 100% with Argo Rollouts."),
("Advanced", "How do you achieve zero-downtime deployment with DB changes?", "Expand/contract migrations: backward-compatible schema first, deploy code, then remove old columns later; feature flags.", "Hard real-world problem.", "Add nullable column first."),
("Advanced", "How do you implement automatic rollback?", "Health checks and metrics analysis (Argo Rollouts analysis, Helm `--atomic`, Kubernetes rollout status) trigger rollback on failure.", "Reliability.", "`helm upgrade --atomic --timeout 5m`."),
("Advanced", "Monorepo vs polyrepo CI strategy?", "Monorepo: path filters and affected-build tooling to avoid rebuilding everything; polyrepo: simpler pipelines but cross-repo changes harder.", "Scale design.", "Trigger only changed service paths."),
("Advanced", "What is SLSA/supply chain security?", "Framework for build integrity: provenance, signed artifacts, hermetic builds, verified dependencies.", "Modern security.", "Cosign + provenance attestation."),
("Advanced", "How do you scale Jenkins?", "Distributed agents (Kubernetes/EC2 spot), controller HA practices, JCasC, plugin hygiene, separate controllers per team.", "Ops maturity.", "Ephemeral Pod agents."),
("Advanced", "Explain OIDC authentication from CI to cloud.", "CI issues a short-lived signed token; the cloud trusts it via an identity provider and grants a role without stored keys.", "Removes static secrets.", "GitHub Actions to AWS IAM role."),
("Advanced", "How do you manage database migrations in pipelines?", "Versioned tools (Flyway/Liquibase), run as a job before/with deploy, idempotent, tested in staging, backup/rollback plan.", "Data safety.", "Flyway job in Helm hook."),
("Advanced", "Feature flags vs deployment?", "Decouple deployment from release: deploy dark, enable per user segment; reduces risk.", "Modern delivery.", "LaunchDarkly/Unleash."),
("Advanced", "What are DORA metrics?", "Deployment frequency, lead time for changes, change failure rate, time to restore service.", "Measuring DevOps.", "Weekly dashboard."),
("Advanced", "Ephemeral vs long-lived agents?", "Ephemeral agents are clean and secure per job; long-lived accumulate state and risk.", "Security and reproducibility.", "Kubernetes agent Pods."),
("Advanced", "How do you promote artifacts securely across environments?", "Immutable image, signature verification, environment-specific config only, approvals, audit trail.", "Governance.", "Same digest from staging to prod."),
("Advanced", "Progressive delivery?", "Automated gradual rollout guided by metrics (canary analysis), using Argo Rollouts/Flagger.", "Advanced CD.", "Rollback on error-rate SLO breach."),
("Advanced", "Handling long-running or flaky integration tests?", "Parallelise, split suites, test containers, retry with limits, nightly runs, quarantine flakies.", "Pipeline health.", "Smoke tests on PR, full suite nightly."),
("Scenario-Based", "Design CI/CD for 20 microservices.", "Shared pipeline templates, per-service pipelines with path filters, common registry, GitOps repo per env, ArgoCD ApplicationSets, standard quality/security gates, DORA dashboards.", "Scale design.", "Reusable workflow + Helm chart."),
("Scenario-Based", "Prod deploy broke the site at 2am.", "Roll back immediately (previous tag/revert), communicate, gather logs/metrics, postmortem, add tests/gates, improve rollout strategy.", "Incident handling.", "`git revert` then ArgoCD sync."),
("Scenario-Based", "Audit requires approvals and traceability.", "Continuous delivery with environment approval gates, signed commits, PR reviews, immutable artifacts, logs retained.", "Compliance.", "GitHub environment protection rules."),
("Scenario-Based", "Pipeline takes 40 minutes.", "Profile stages, cache, parallelise, split tests, use faster runners, skip unchanged components.", "Optimisation.", "Reduced to 12 minutes."),
("Scenario-Based", "A dependency has a critical CVE.", "SCA scan fails build, update/pin dependency, rebuild, rescan, redeploy; automate with Dependabot/Renovate.", "Security response.", "log4j style incident."),
("Scenario-Based", "Developers deploy from laptops.", "Remove direct access, enforce pipeline-only deploys, RBAC, GitOps, audit.", "Governance.", "Only the CI ServiceAccount can deploy."),
("Scenario-Based", "Need multi-region deployments.", "Pipeline promotes to region A then B, health check between, global traffic routing, per-region GitOps apps.", "Scale/HA.", "Staged region rollout."),
("Scenario-Based", "Secrets exposed in a public repo.", "Revoke/rotate immediately, purge history, add pre-commit and CI secret scanning, move to a vault.", "Security response.", "Gitleaks."),
("Scenario-Based", "Migrate from Jenkins to GitHub Actions.", "Inventory jobs, map stages to workflows, replace plugins with actions, move secrets, run both in parallel, cut over gradually.", "Migration planning.", "Start with simplest services."),
("Scenario-Based", "Different config per environment.", "Same image; config via Helm values/Kustomize overlays/secrets per environment.", "Twelve-factor.", "values-prod.yaml."),
("Scenario-Based", "How to deploy to Kubernetes securely from CI?", "Prefer GitOps; otherwise short-lived credentials/OIDC, namespaced RBAC, no cluster-admin.", "Least privilege.", "ArgoCD instead of kubectl in CI."),
("Scenario-Based", "Reduce failed deployments.", "More automated tests, staging parity, progressive delivery, feature flags, health-gated rollouts, rollback automation.", "Change failure rate.", "Canary with analysis."),
("Scenario-Based", "Team wants to release on demand.", "Trunk-based development, feature flags, automated tests, continuous delivery.", "Process design.", "Short-lived branches."),
("Scenario-Based", "Build agents are overloaded.", "Autoscaling ephemeral agents, queue metrics, parallelism limits, cache layers.", "Capacity planning.", "Kubernetes-based Jenkins agents."),
("Scenario-Based", "Third-party action compromised.", "Pin to commit SHAs, allowlist actions, review updates, minimal permissions, rotate exposed secrets.", "Supply chain.", "tj-actions incident style."),
("Troubleshooting-Based", "Webhook delivered but pipeline did not start.", "Check branch/path filters, Jenkins job type/multibranch scan, webhook secret/response code, permissions.", "Trigger debugging.", "Response 403 from Jenkins."),
("Troubleshooting-Based", "Pipeline fails only on CI: 'command not found'.", "Tool not installed on agent/runner; use container agent or setup step and pin versions.", "Environment parity.", "node/npm version missing."),
("Troubleshooting-Based", "Docker build fails in CI with 'permission denied /var/run/docker.sock'.", "Agent user lacks Docker access or Docker-in-Docker not set; use a Docker-enabled agent or Kaniko/BuildKit.", "Common CI issue.", "Add user to docker group or use rootless builder."),
("Troubleshooting-Based", "Cache not restored.", "Key changed, cache scope/branch mismatch, size limit; check restore logs.", "Speed issues.", "Key uses lockfile hash."),
("Troubleshooting-Based", "Deploy step hangs.", "Rollout stuck (readiness), missing timeout, cluster unreachable; add `--timeout` and inspect Pods.", "Deployment debugging.", "kubectl rollout status hangs."),
("Troubleshooting-Based", "Pipeline passes but wrong image deployed.", "Tag mismatch/`latest`, GitOps repo not updated, ArgoCD out-of-sync; verify digest.", "Traceability.", "Use SHA tags."),
("Troubleshooting-Based", "Jenkins is slow/out of memory.", "Too many builds on controller, plugin issues, heap size, disk; move builds to agents, tune JVM, clean workspace.", "Jenkins ops.", "Run zero executors on controller."),
("Troubleshooting-Based", "Secrets unavailable in PR from fork.", "By design forks do not receive secrets; use pull_request_target carefully or run trusted checks after review.", "Security model.", "GitHub Actions fork rules."),
("Troubleshooting-Based", "SonarQube gate fails unexpectedly.", "New-code coverage threshold, new issues, wrong baseline; view the Sonar report.", "Quality gate.", "Coverage on new code < 80%."),
("Troubleshooting-Based", "ArgoCD stuck OutOfSync/Degraded.", "Check diff, resource health, hooks, RBAC and events in the Application; hard refresh; fix manifest.", "GitOps debugging.", "Immutable field changed.")],
cheatsheet={
"Definitions": ["CI: build+test every change. Continuous Delivery: releasable + approval. Continuous Deployment: auto release.", "Artifact: build output. Quality gate: pass/fail standard. GitOps: Git is source of truth.", "Rolling/Blue-Green/Canary: release strategies."],
"Commands": ["`git push` (trigger) | `docker build -t reg/app:$SHA .` | `docker push reg/app:$SHA`", "`trivy image --severity HIGH,CRITICAL --exit-code 1 img`", "`helm upgrade --install app ./chart -f values.yaml --atomic --timeout 5m`", "`kubectl rollout status|undo deploy/app` | `argocd app sync|get|rollback app`", "`gitleaks detect` | `sonar-scanner`"],
"Files": ["Jenkinsfile", ".github/workflows/*.yml", ".gitlab-ci.yml", "Dockerfile", "Helm values-*.yaml", "ArgoCD Application YAML"],
"Architecture": ["Git > webhook > CI runner > build > test > quality > scan > registry > CD (GitOps) > cluster > monitoring."],
"Ports": ["Jenkins 8080 (agents 50000), SonarQube 9000, Harbor 80/443, ArgoCD UI 443/8080, Registry 5000"],
"Differences": ["CI vs CD; Delivery vs Deployment; Jenkins vs Actions; push vs pull CD; blue/green vs canary; artifact vs image."],
"Troubleshooting commands": ["Read failing step log > reproduce locally in same container > check secrets/permissions > `kubectl rollout status/describe` > `argocd app diff`"],
"Best practices": ["Build once/deploy many, SHA tags, pipeline as code, OIDC, scan + sign, approvals for prod, automated rollback, DORA metrics."]}
),
subs={
"cicd-concepts": dict(
define=dict(simple="CI/CD is an automatic path from code commit to running application.",
technical="CI verifies each change via automated build/test/analysis in a shared pipeline; CD automates packaging and release to environments with gates and strategies.",
why="Reduce risk by releasing small changes frequently with fast feedback.", without="Big-bang releases and manual mistakes.", use="Any team shipping software regularly.", avoid="Never 'avoid' but start simple: a small pipeline beats none.", analogy="Factory assembly line with quality inspection at each station."),
internals="""Trigger (push/PR/schedule/manual) > CI server allocates an agent > checkout > run stages in order; each stage is a set of commands returning an exit code. Non-zero fails the pipeline and stops later stages (fail fast). Outputs (artifacts, test reports, images) are stored and reused by later stages/environments.""",
lab=dict(goal="Create a minimal CI pipeline for a Node app on GitHub.", prereq=["GitHub account and repo", "A Node project with npm test"],
steps=[("mkdir -p .github/workflows", "Workflows must be in this folder."),
("cat > .github/workflows/ci.yml <<'EOF'\nname: ci\non: [push, pull_request]\njobs:\n  test:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - uses: actions/setup-node@v4\n        with: { node-version: 20 }\n      - run: npm ci\n      - run: npm test\nEOF", "Defines a two-trigger workflow that installs and tests."),
("git add . && git commit -m 'add ci' && git push", "Push triggers the workflow. Open the Actions tab: green check = pass."),
("Break a test, push again", "The pipeline fails and blocks the PR: that is the value of CI.")]),
compare=[("Pipeline terms", ["Term", "Meaning"], [["Pipeline", "Whole automated flow"], ["Stage", "Logical phase (build/test/deploy)"], ["Job", "Unit executed on a runner"], ["Step", "Single command/action"], ["Agent/Runner", "Machine running the job"], ["Artifact", "Saved output"]])],
mnemonics=[("Pipeline order", "B-T-Q-S-P-D")],
hinglish="CI = code push par **automatic build aur test**. CD = tested code ka **automatic deploy**. Jo bhi stage fail ho, pipeline wahin ruk jati hai (**fail fast**).",
practices={"Production": ["Build once, deploy everywhere.", "Fast pipelines (<10 min for PR checks)."], "Security": ["Least privilege credentials."]},
mistakes={"Beginner mistakes": ["No tests in the pipeline.", "Secrets in YAML."]},
qa_extra=[("Intermediate", "Why 'build once, deploy many'?", "Ensures the exact tested artifact reaches production; rebuilding can change dependencies and behavior.", "Reliability.", "Same image SHA from staging to prod.")]),

"github-actions": dict(
define=dict(simple="GitHub Actions runs automation (build, test, deploy) directly from your GitHub repository.",
technical="A workflow (YAML in .github/workflows) is triggered by events, contains jobs that run on runners; each job has steps that run commands or reusable actions. Contexts, secrets, caches and artifacts support pipelines.",
why="Integrated CI/CD without managing servers.", without="Separate CI server to operate.", use="Repos on GitHub.", avoid="Long heavy builds on hosted minutes without cost planning (use self-hosted runners).", analogy="A robot that reacts to events in your repo."),
internals="""Event (push) > GitHub schedules a job > a runner (VM) picks it up > checks out code > runs steps in order > uploads logs/artifacts > reports a status check on the commit/PR. Jobs run in parallel unless `needs:` creates dependencies. Secrets are injected as masked env values.""",
config=[("Workflow with cache, matrix and OIDC explained", """name: ci
on: { push: { branches: [main] }, pull_request: {} }
permissions: { id-token: write, contents: read }
jobs:
  test:
    runs-on: ubuntu-latest
    strategy: { matrix: { node: [18, 20] } }
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: "${{ matrix.node }}", cache: npm }
      - run: npm ci && npm test
  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: aws-actions/configure-aws-credentials@v4
        with: { role-to-assume: arn:aws:iam::123456789012:role/gha-deploy, aws-region: ap-south-1 }""", [
("on:", "Triggers: push to main and any pull request."),
("permissions: id-token: write", "Allows the job to request an OIDC token so AWS can trust it without stored keys; `contents: read` is least privilege."),
("strategy.matrix", "Runs the test job for each Node version in parallel."),
("cache: npm", "Caches dependencies keyed on the lockfile to speed up runs."),
("needs: test", "Deploy job waits for test job success."),
("if: github.ref == ...", "Deploy only from main."),
("environment: production", "Enables required reviewers/approval and environment secrets."),
("role-to-assume", "OIDC role; no long-lived AWS keys in secrets.")])],
lab=dict(goal="Build, test and push a Docker image from Actions.", prereq=["GitHub repo with Dockerfile", "Container registry (GHCR works with GITHUB_TOKEN)"],
steps=[("Create .github/workflows/docker.yml with checkout, docker/login-action (registry ghcr.io, password ${{ secrets.GITHUB_TOKEN }}) and docker/build-push-action (tags ghcr.io/OWNER/app:${{ github.sha }})", "Builds the image and pushes it tagged with the commit SHA. Check action versions in the marketplace."),
("git push and open Actions > run", "Watch each step log. Expected: image appears under Packages."),
("Add an aquasecurity/trivy-action step before push with exit-code: 1", "Vulnerable images now fail the build.")]),
compare=[("Hosted vs self-hosted runners", ["Topic", "GitHub-hosted", "Self-hosted"], [["Maintenance", "None", "You patch/scale"], ["Cost", "Per minute", "Your infrastructure"], ["Network access", "Public internet", "Inside your VPC"], ["Security", "Ephemeral VM", "Must harden and isolate"]])],
mnemonics=[("Actions hierarchy", "Workflow > Job > Step (Event triggers workflow)")],
hinglish="Actions mein **event → workflow → job → step**. Cloud ke liye **OIDC** use karo taaki AWS keys secrets mein store na karni pade.",
practices={"Security": ["Pin actions to SHA; least-privilege `permissions`; OIDC; do not expose secrets to fork PRs."], "Performance": ["Cache, concurrency groups to cancel old runs."]},
mistakes={"Security mistakes": ["`pull_request_target` with untrusted code.", "Unpinned third-party actions."]},
versions=["Action versions (checkout@v4, setup-node@v4...) evolve; verify current versions. Runner images (ubuntu-latest) change over time: pin `ubuntu-24.04` if you need stability."],
qa_extra=[("Intermediate", "How do you require manual approval for prod?", "Use `environment: production` with required reviewers configured in repository settings.", "Governance.", "Delivery model.")]),

"jenkins": dict(
define=dict(simple="Jenkins is a server you host that runs your build and deploy jobs.",
technical="Jenkins is a Java-based automation server: a controller manages jobs, credentials and plugins; agents execute builds. Pipelines are defined in a Jenkinsfile (Declarative or Scripted Groovy).",
why="Flexible, self-hosted CI/CD with a huge plugin ecosystem.", without="Custom scripts and cron jobs.", use="Complex/legacy or on-premises environments.", avoid="If you want zero maintenance: use a managed CI.", analogy="A factory manager (controller) assigning work to workers (agents)."),
internals="""SCM webhook/poll > controller queues the build > allocates an executor on a matching agent (label) > agent checks out code and runs stages > results, artifacts and reports are sent to the controller > post actions (notify). Credentials are stored encrypted on the controller and injected into builds with masking. Kubernetes plugin can create a Pod per build as an ephemeral agent.""",
config=[("Declarative Jenkinsfile explained", """pipeline {
  agent { label 'docker' }
  environment { IMAGE = "registry.example.com/shop/api:${env.GIT_COMMIT}" }
  options { timeout(time: 30, unit: 'MINUTES'); disableConcurrentBuilds() }
  stages {
    stage('Test')  { steps { sh 'npm ci && npm test' } }
    stage('Sonar') { steps { withSonarQubeEnv('sonar') { sh 'sonar-scanner' } } }
    stage('Gate')  { steps { timeout(time: 5, unit: 'MINUTES') { waitForQualityGate abortPipeline: true } } }
    stage('Build') { steps { sh 'docker build -t $IMAGE .' } }
    stage('Scan')  { steps { sh 'trivy image --exit-code 1 --severity HIGH,CRITICAL $IMAGE' } }
    stage('Push')  { steps { withCredentials([usernamePassword(credentialsId: 'registry', usernameVariable: 'U', passwordVariable: 'P')]) {
      sh 'echo $P | docker login registry.example.com -u $U --password-stdin && docker push $IMAGE' } } }
  }
  post { failure { echo 'notify Slack' } always { cleanWs() } }
}""", [
("agent { label 'docker' }", "Run on an agent that has Docker; keeps builds off the controller."),
("environment", "Pipeline-wide variables; tagged with the commit SHA."),
("options timeout/disableConcurrentBuilds", "Prevents hung builds and overlapping deployments."),
("withSonarQubeEnv + waitForQualityGate", "Runs analysis and blocks the pipeline until the quality gate returns."),
("trivy --exit-code 1", "Fails the build on HIGH/CRITICAL vulnerabilities."),
("withCredentials", "Injects registry credentials securely and masks them in logs."),
("post", "Runs after stages: notify on failure, always clean the workspace.")])],
lab=dict(goal="Run Jenkins in Docker and create a first pipeline.", prereq=["Docker installed"],
steps=[("docker run -d --name jenkins -p 8080:8080 -p 50000:50000 -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts", "Starts Jenkins LTS with data in a named volume so it survives restarts."),
("docker logs jenkins | grep -A2 'password'", "Prints the initial admin password. Open http://localhost:8080, install suggested plugins."),
("New Item > Pipeline > paste a simple Jenkinsfile (`pipeline { agent any stages { stage('Hello') { steps { echo 'hi' } } } }`) > Build Now", "Green build with logs in Console Output."),
("Connect to a Git repo via Multibranch Pipeline", "Jenkins scans branches with a Jenkinsfile and builds each automatically.")]),
compare=[("Jenkins components", ["Component", "Role"], [["Controller", "UI, scheduling, config, credentials"], ["Agent", "Runs builds"], ["Plugin", "Adds integrations"], ["Shared library", "Reusable Groovy pipeline code"]])],
mnemonics=[("Jenkins", "Controller thinks, Agent works")],
hinglish="Jenkins mein **controller sirf manage karta hai, build agent par chalta hai**. Credentials `withCredentials` se use karo, kabhi Jenkinsfile mein password mat likho.",
practices={"Security": ["Keep Jenkins and plugins updated; disable script approvals abuse; use RBAC/SSO; zero executors on controller."], "Reliability": ["Configuration as Code (JCasC), backup JENKINS_HOME, Pipeline as code."]},
mistakes={"DevOps mistakes": ["Manual UI config (snowflake)", "Building on the controller", "Never updating plugins"]},
versions=["Use the current LTS release and check plugin compatibility; the Blue Ocean UI is in maintenance mode; controller Java version requirements change between LTS lines."],
qa_extra=[("Troubleshooting-Based", "Jenkins build stuck 'waiting for next available executor'.", "No agent with the required label/free executor; check node status, labels and agent connectivity or add dynamic agents.", "Capacity issue.", "Label typo `dokcer`.")]),

"gitops-argocd": dict(
define=dict(simple="GitOps means Git is the single source of truth and a tool in the cluster keeps the cluster equal to Git.",
technical="ArgoCD is a Kubernetes controller that continuously compares the desired state defined in Git (manifests/Helm/Kustomize) with live cluster state and syncs differences, optionally self-healing drift.",
why="Auditable, reversible, secure (pull-based) deployments.", without="CI with cluster admin credentials and undocumented manual changes.", use="Kubernetes deployments.", avoid="Non-Kubernetes targets.", analogy="A thermostat: you set the target in Git; ArgoCD keeps the room at that temperature."),
internals="""Repo server renders manifests (Helm/Kustomize). The application controller compares rendered manifests with live objects; result is Synced/OutOfSync and Healthy/Degraded. With automated sync it applies changes; selfHeal reverts manual edits; prune deletes resources removed from Git. Rollback = revert Git commit.""",
lab=dict(goal="Install ArgoCD and deploy an app from Git.", prereq=["kubectl + cluster"],
steps=[("kubectl create namespace argocd && kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml", "Installs ArgoCD (check the official docs for the current install method)."),
("kubectl -n argocd port-forward svc/argocd-server 8443:443", "UI at https://localhost:8443. Initial password: `kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath='{.data.password}' | base64 -d`."),
("argocd app create guestbook --repo https://github.com/argoproj/argocd-example-apps.git --path guestbook --dest-server https://kubernetes.default.svc --dest-namespace default && argocd app sync guestbook", "Creates and syncs an Application. Then edit a replica count in the cluster and watch selfHeal (if enabled) revert it.")]),
compare=[("Push vs pull CD", ["Topic", "Push (kubectl in CI)", "Pull (GitOps)"], [["Cluster credentials", "Stored in CI", "Stay inside cluster"], ["Drift", "Not detected", "Detected/corrected"], ["Audit", "CI logs", "Git history"]]), ("ArgoCD vs Flux", ["Topic", "ArgoCD", "Flux"], [["UI", "Rich web UI", "CLI/controllers (UI via add-ons)"], ["Model", "Application CRD", "GitRepository + Kustomization"]])],
mnemonics=[("GitOps loop", "Declare in Git > Detect diff > Sync > Self-heal")],
hinglish="GitOps mein **Git hi truth hai**. Cluster mein manual change karoge to ArgoCD **wapas Git jaisa kar dega** (selfHeal). Rollback = `git revert`.",
practices={"Security": ["Do not give CI cluster credentials; RBAC on ArgoCD projects; separate app and config repos."], "Reliability": ["Use sync waves/hooks for migrations; manual sync for prod."]},
mistakes={"DevOps mistakes": ["Editing live objects with kubectl.", "Secrets in Git without encryption (use Sealed Secrets/SOPS/External Secrets)."]},
versions=["Install manifest URL and CRD fields change by version; consult the ArgoCD docs. ApplicationSet is available for multi-cluster/multi-app generation."],
qa_extra=[("Scenario-Based", "ArgoCD shows OutOfSync every time even after sync.", "Fields mutated by controllers/HPA (replicas) or defaults; add `ignoreDifferences` or remove conflicting fields from Git.", "Real GitOps issue.", "HPA changes `spec.replicas`.")]),

"deployment-strategies": dict(
define=dict(simple="Deployment strategies are safe ways to release a new version to users.",
technical="Rolling update, recreate, blue/green, canary, A/B and shadow deployments trade off risk, cost and speed; progressive delivery automates metric-based promotion and rollback.",
why="Minimise downtime and blast radius of bad releases.", without="Big-bang releases causing outages.", use="Every production release.", avoid="Blue/green for very expensive or stateful environments without planning.", analogy="Opening a new bridge lane by lane vs closing the whole bridge."),
internals="""Rolling: Deployment replaces Pods gradually while readiness gates traffic. Blue/green: two full environments; a Service selector/load balancer switches all traffic. Canary: traffic split (ingress weights, service mesh, Argo Rollouts) sends 5% > 25% > 100% while analysis compares error rate/latency; failure aborts and shifts traffic back.""",
realworld=dict(diagram="""Users --> Ingress --95%--> api v1 (stable)
             \\--5%---> api v2 (canary) --> metrics (errors, latency) --> promote or rollback""", text="A payments API releases v2 as a 5% canary. Prometheus queries compare error rate and p95 latency; if error rate stays below the SLO for 10 minutes traffic goes to 25%, then 100%. If it breaches, Argo Rollouts automatically reverts to v1."),
compare=[("Strategy summary", ["Strategy", "Downtime", "Rollback", "Cost", "Best for"], [["Recreate", "Yes", "Redeploy old", "Low", "Dev, apps that cannot run 2 versions"], ["Rolling", "None", "Undo rollout", "Low", "Default stateless apps"], ["Blue/Green", "None", "Instant switch", "High", "Critical apps needing fast rollback"], ["Canary", "None", "Set weight 0", "Medium", "Risk-sensitive with good metrics"]])],
lab=dict(goal="Practise blue/green with Kubernetes Services.", prereq=["Cluster", "kubectl"],
steps=[("""cat > bg.yaml <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata: { name: app-blue }
spec:
  replicas: 2
  selector: { matchLabels: { app: app, ver: blue } }
  template:
    metadata: { labels: { app: app, ver: blue } }
    spec: { containers: [{ name: web, image: "nginx:1.26" }] }
---
apiVersion: apps/v1
kind: Deployment
metadata: { name: app-green }
spec:
  replicas: 2
  selector: { matchLabels: { app: app, ver: green } }
  template:
    metadata: { labels: { app: app, ver: green } }
    spec: { containers: [{ name: web, image: "nginx:1.27" }] }
---
apiVersion: v1
kind: Service
metadata: { name: app }
spec:
  selector: { app: app, ver: blue }
  ports: [{ port: 80 }]
EOF
kubectl apply -f bg.yaml""", "Creates both versions (blue = nginx 1.26, green = nginx 1.27) and a Service that currently selects blue only."),
("kubectl get endpoints app", "Endpoints list only the blue Pod IPs, so all traffic goes to blue."),
("""kubectl patch svc app -p '{"spec":{"selector":{"app":"app","ver":"green"}}}'""", "Instant switch of ALL traffic to green. Run `kubectl get endpoints app` again to see the green IPs."),
("""kubectl patch svc app -p '{"spec":{"selector":{"app":"app","ver":"blue"}}}'""", "Rollback is the same one-line switch back to blue.")]),
mnemonics=[("Strategies", "Rolling = replace slowly; Blue/Green = swap; Canary = taste test")],
hinglish="**Rolling** = dheere dheere replace; **Blue/Green** = ek dum switch (rollback instant); **Canary** = pehle thode users par test, metrics theek to aage badhao.",
practices={"Production": ["Readiness probes + PDB for rolling; metrics-based canary analysis; automated rollback; DB migrations backward compatible."], "Security": ["Scan and sign before promote; verify signature at admission."]},
mistakes={"Production mistakes": ["Canary without metrics.", "Schema changes that break the old version."]},
versions=["Kubernetes has no native canary/blue-green object: use Argo Rollouts, Flagger, ingress annotations or a service mesh; features differ by tool version."],
qa_extra=[("Scenario-Based", "How do you handle DB schema changes with blue/green?", "Use backward-compatible expand/contract migrations so both versions work against the same database, then clean up later.", "Real blocker for blue/green.", "Add column first, remove old column in a later release.")])
})
