TOPIC = dict(slug="06-cicd", title="CI/CD", intro="Code push se production tak sab kuch automatic: build, test, scan, deploy. DevOps ka heart.", subs=[

dict(slug="cicd-concepts", title="CI/CD Concepts & Pipeline Design", level="Basic",
intro="CI: har commit par build+test. Continuous Delivery: hamesha deployable, release manual approval se. Continuous Deployment: har pass hua change automatic prod mein.",
diagram="""
commit -> [Build] -> [Unit test] -> [Lint/SAST] -> [Package image] -> [Scan] -> [Deploy dev] -> [Integration/e2e] -> [Approve] -> [Deploy prod] -> [Smoke test]
  fail fast: koi bhi stage fail -> pipeline stop -> developer ko notify
""",
install="# Choose tool: GitHub Actions (cloud), Jenkins (self-hosted), GitLab CI",
examples=[("Pipeline design checklist","""1. Fast feedback (<10 min for CI)
2. Same artifact promoted across envs (build once, deploy many)
3. Immutable, versioned artifacts (image tag = git sha)
4. Config/secrets injected per env, not baked in
5. Automated rollback & smoke tests
6. Everything as code (Jenkinsfile / workflow yaml)""")],
problems=[("Works in staging, breaks in prod","Rebuilt artifact per env / config drift","Build once, promote same image; keep env config separate."),
("Pipeline takes 40 minutes","No caching / serial stages","Cache deps, parallelize tests, use path filters.")],
qa=[("CI vs CD vs Continuous Deployment?","CI = integrate+test often; Delivery = always releasable with manual gate; Deployment = fully automatic to prod."),
("What are DORA metrics?","Deployment frequency, lead time for changes, change failure rate, MTTR."),
("Why build once?","Guarantees what you tested is what you deploy."),
("What is a quality gate?","Automated threshold (coverage, vulnerabilities) that blocks promotion."),
("Artifact vs image?","Artifact is any build output (jar, binary, image); image is container artifact.")]),

dict(slug="github-actions", title="GitHub Actions", level="Basic",
intro="Repo ke andar `.github/workflows/*.yml`. Events (push/PR) par jobs run hote hain runners par. Free tier generous hai.",
diagram="""
Event (push/PR/schedule) -> Workflow -> Job(s) [parallel] -> Steps -> uses actions / run shell
Secrets: Settings -> Secrets and variables | Environments: approvals for prod
""",
install="# nothing to install: create .github/workflows/ci.yml and push. Local test: 'act' (https://github.com/nektos/act)",
examples=[("CI for Node app with cache and matrix","""name: ci
on:
  push: { branches: [main] }
  pull_request:
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix: { node: [18, 20] }
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: "${{ matrix.node }}", cache: npm }
      - run: npm ci
      - run: npm test -- --coverage
      - uses: actions/upload-artifact@v4
        with: { name: coverage, path: coverage/ }"""),
("Build & push image to GHCR, deploy on tag","""name: release
on: { push: { tags: ['v*'] } }
permissions: { contents: read, packages: write }
jobs:
  image:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/login-action@v3
        with: { registry: ghcr.io, username: "${{ github.actor }}", password: "${{ secrets.GITHUB_TOKEN }}" }
      - uses: docker/build-push-action@v6
        with:
          push: true
          tags: ghcr.io/${{ github.repository }}:${{ github.ref_name }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
  deploy:
    needs: image
    environment: production     # requires approval
    runs-on: ubuntu-latest
    steps:
      - run: echo "deploy ${{ github.ref_name }}""")],
problems=[("Secrets show in logs / leaked from forks","Printing secrets, pull_request_target misuse","Secrets are masked but never echo; forks don't get secrets; use environments."),
("Workflow doesn't trigger","YAML error / wrong branch filter / path filter","Check Actions tab syntax errors; validate with actionlint.")],
qa=[("Job vs step?","Job runs on a runner (parallel by default); steps run sequentially inside a job."),
("How to share workflows?","Reusable workflows (`workflow_call`) and composite actions."),
("How to authenticate to AWS securely?","OIDC with `role-to-assume`, no long-lived keys."),
("Self-hosted vs hosted runners?","Self-hosted: custom hardware/network access, you maintain; hosted: managed."),
("How to make deploy require approval?","Use Environments with required reviewers.")]),

dict(slug="jenkins", title="Jenkins", level="Intermediate",
intro="Sabse popular self-hosted CI server. Jenkinsfile (pipeline as code), agents, plugins. Enterprises mein abhi bhi bahut use hota hai.",
diagram="""
Git webhook -> Jenkins Controller -> schedules on Agents (VM/K8s pods)
                    |                      |
              Jenkinsfile stages     build, test, docker, deploy
""",
install="""# Docker (quick)
docker run -d --name jenkins -p 8080:8080 -p 50000:50000 -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword""",
examples=[("Declarative Jenkinsfile","""pipeline {
  agent any
  environment { IMAGE = "myrepo/app:${env.GIT_COMMIT[0..6]}" }
  options { timeout(time: 30, unit: 'MINUTES'); disableConcurrentBuilds() }
  stages {
    stage('Test')  { steps { sh 'npm ci && npm test' } }
    stage('Build') { steps { sh 'docker build -t $IMAGE .' } }
    stage('Push')  {
      steps { withCredentials([usernamePassword(credentialsId:'dockerhub', usernameVariable:'U', passwordVariable:'P')]) {
        sh 'echo $P | docker login -u $U --password-stdin && docker push $IMAGE' } }
    }
    stage('Deploy') {
      when { branch 'main' }
      steps { input 'Deploy to prod?'; sh './deploy.sh prod $IMAGE' }
    }
  }
  post { failure { echo 'Notify Slack' } always { cleanWs() } }
}""")],
problems=[("Jenkins slow / builds queue","Everything on controller, too few agents","Use ephemeral agents (K8s plugin), 0 executors on controller."),
("Plugin upgrade broke Jenkins","Uncontrolled plugin updates","Pin versions, test in staging, back up JENKINS_HOME, use JCasC.")],
qa=[("Declarative vs scripted pipeline?","Declarative: structured, simpler; Scripted: full Groovy flexibility."),
("How to store credentials?","Jenkins Credentials store + `withCredentials`, or external Vault."),
("What is a Jenkins agent?","Node executing jobs, connected via SSH/JNLP or spawned dynamically."),
("How to trigger builds?","SCM webhooks, cron, upstream jobs, manual."),
("What is JCasC?","Jenkins Configuration as Code YAML to reproduce setup.")]),

dict(slug="gitops-argocd", title="GitOps & ArgoCD", level="Advanced",
intro="Git = single source of truth for cluster state. ArgoCD Git repo watch karta hai aur cluster ko usse sync karta hai (pull-based CD). Drift auto-heal hota hai.",
diagram="""
Dev -> PR -> app repo CI -> builds image, updates tag in gitops repo
                                     |
                       ArgoCD (in cluster) watches gitops repo
                                     |  sync / self-heal
                               Kubernetes cluster
""",
install="""kubectl create ns argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath='{.data.password}' | base64 -d
kubectl port-forward svc/argocd-server -n argocd 8080:443""",
examples=[("Application manifest","""apiVersion: argoproj.io/v1alpha1
kind: Application
metadata: { name: myapp, namespace: argocd }
spec:
  project: default
  source: { repoURL: https://github.com/acme/gitops, targetRevision: main, path: charts/myapp }
  destination: { server: https://kubernetes.default.svc, namespace: prod }
  syncPolicy: { automated: { prune: true, selfHeal: true } }"""),
("Rollback = git revert","""git revert <bad-commit> && git push     # ArgoCD syncs the previous state
argocd app history myapp; argocd app rollback myapp <id>""")],
problems=[("Someone kubectl-edited prod and change vanished","selfHeal reverted manual drift (this is intended)","Make changes via Git PR; that's the point of GitOps."),
("Secrets in Git","GitOps needs all state in Git","Use Sealed Secrets, SOPS, or External Secrets Operator.")],
qa=[("Push vs pull deployment?","Push: CI runs kubectl (needs cluster creds). Pull: in-cluster agent pulls from Git (more secure)."),
("What is drift?","Live state differs from Git; GitOps detects and fixes."),
("App of apps pattern?","One Application that defines many child Applications for bootstrap."),
("ArgoCD vs Flux?","Both GitOps; Argo has rich UI and ApplicationSets; Flux is lighter, toolkit style."),
("How do you promote across envs?","Update env-specific values/overlays via PR, or Kargo/image-updater.")]),

dict(slug="deployment-strategies", title="Deployment Strategies & Pipeline Security", level="Advanced",
intro="Zero-downtime release techniques: rolling, blue-green, canary. Saath mein pipeline security (SAST, SCA, secrets, signing).",
diagram="""
Rolling:    v1 v1 v1 -> v2 v1 v1 -> v2 v2 v1 -> v2 v2 v2
Blue-Green: LB -> BLUE(v1) | GREEN(v2) idle -> switch LB to GREEN -> keep BLUE for rollback
Canary:     v1 100% -> v2 5% -> 25% -> 50% -> 100% (auto-rollback on error-rate rise)
""",
install="""kubectl create ns argo-rollouts
kubectl apply -n argo-rollouts -f https://github.com/argoproj/argo-rollouts/releases/latest/download/install.yaml""",
examples=[("Argo Rollouts canary","""apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata: { name: myapp }
spec:
  replicas: 5
  selector: { matchLabels: { app: myapp } }
  template:
    metadata: { labels: { app: myapp } }
    spec: { containers: [{ name: myapp, image: myapp:v2 }] }
  strategy:
    canary:
      steps:
      - setWeight: 10
      - pause: { duration: 5m }
      - setWeight: 50
      - pause: { duration: 10m }"""),
("Security stages in pipeline","""1 gitleaks (secrets)   2 SonarQube/Semgrep (SAST)
3 Trivy fs/deps (SCA)   4 Trivy image scan
5 cosign sign + SBOM    6 DAST (OWASP ZAP) on staging""")],
problems=[("Bad release hit all users at once","Big-bang deploy","Canary with metrics analysis + auto-rollback."),
("DB schema change breaks old version during rolling deploy","Non backward-compatible migration","Expand/contract pattern: add new columns first, deploy code, then remove old later.")],
qa=[("Blue-green vs canary?","Blue-green swaps all traffic at once with instant rollback (2x infra); canary shifts gradually to limit blast radius."),
("How to do DB migrations with zero downtime?","Backward-compatible, expand-contract, run migrations separately from app deploy."),
("What is SLSA?","Framework for supply chain integrity (provenance, build isolation)."),
("How to avoid long-lived cloud keys in CI?","OIDC federation to short-lived role credentials."),
("What is a feature flag benefit?","Deploy dark, release gradually, instant kill switch.")]),
])
