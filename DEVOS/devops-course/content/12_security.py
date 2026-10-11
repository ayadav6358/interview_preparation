TOPIC = dict(slug="12-devsecops", title="DevSecOps & Security", intro="Security ko end mein nahi, shuru se (shift-left) add karo. Code, dependencies, images, infra aur runtime sab cover karo.", subs=[

dict(slug="security-fundamentals", title="Security Fundamentals & Threat Thinking", level="Basic",
intro="CIA triad (Confidentiality, Integrity, Availability), least privilege, defense in depth. OWASP Top 10 awareness aur common DevOps mistakes.",
diagram="""
Defense in depth:
Code -> Dependencies -> Build/CI -> Image -> Registry -> Cluster/Network -> Cloud IAM -> Runtime -> Monitoring
Each layer has controls; assume one will fail.
""",
install="# concept; reading: owasp.org/www-project-top-ten",
examples=[("Top DevOps security mistakes","""1 Secrets in Git/images/env logs      2 Over-permissive IAM (*:*)
3 Public S3/DB/SG 0.0.0.0/0 on 22/3306   4 Running containers as root
5 No patching/old base images           6 No audit logs / MFA""")],
problems=[("AWS keys leaked on GitHub, crypto miners launched","Static keys committed","Revoke, rotate, check CloudTrail; use SSO/roles/OIDC; gitleaks + GitHub secret scanning.")],
qa=[("What is least privilege?","Grant only permissions needed for the task, nothing more."),
("What is shift-left security?","Detect issues early (IDE/PR/CI) when cheaper to fix."),
("OWASP Top 10 examples?","Broken access control, injection, cryptographic failures, insecure design, vulnerable components."),
("What is defense in depth?","Multiple layered controls."),
("What is zero trust?","Never trust by network location; verify identity and context every request.")]),

dict(slug="secrets-management", title="Secrets Management (Vault, Secrets Manager)", level="Intermediate",
intro="Passwords, tokens, keys ko Git ya env files mein mat rakho. Secret manager use karo: rotation, audit, dynamic short-lived credentials.",
diagram="""
App --auth (K8s SA / IAM role)--> Vault / AWS Secrets Manager --> secret (or dynamic DB creds, TTL 1h)
K8s: External Secrets Operator syncs store -> K8s Secret ; audit log of every read
""",
install="""# Vault dev server (learning only)
docker run -d --name vault -p 8200:8200 -e VAULT_DEV_ROOT_TOKEN_ID=root hashicorp/vault
export VAULT_ADDR=http://127.0.0.1:8200 VAULT_TOKEN=root
# External Secrets
helm repo add external-secrets https://charts.external-secrets.io && helm install eso external-secrets/external-secrets -n eso --create-namespace""",
examples=[("Vault KV + policy","""vault kv put secret/myapp db_password=S3cret
vault kv get -field=db_password secret/myapp
cat > app.hcl <<EOF
path "secret/data/myapp" { capabilities = ["read"] }
EOF
vault policy write myapp app.hcl"""),
("External Secret (AWS Secrets Manager -> K8s)","""apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata: { name: db }
spec:
  refreshInterval: 1h
  secretStoreRef: { name: aws, kind: ClusterSecretStore }
  target: { name: db-secret }
  data:
  - { secretKey: password, remoteRef: { key: prod/db, property: password } }"""),
("AWS CLI","""aws secretsmanager create-secret --name prod/db --secret-string '{"password":"S3cret"}'
aws secretsmanager get-secret-value --secret-id prod/db --query SecretString --output text""")],
problems=[("Secret rotation causes outage","Apps cache old password","Use dynamic secrets / reload on change / dual-credential rotation."),
("K8s Secrets visible to many","Broad RBAC, no encryption","Restrict RBAC, enable KMS encryption, use CSI/ESO.")],
qa=[("Why not env vars for secrets?","They leak in logs/process listings/crash dumps; prefer mounted files or fetch at runtime."),
("Dynamic secrets?","Generated on demand with TTL (e.g. DB user per app instance), auto-revoked."),
("SOPS/Sealed Secrets use?","Encrypt secrets so they can live in Git safely (GitOps)."),
("Vault auth methods?","Kubernetes, AWS IAM, AppRole, OIDC."),
("Envelope encryption?","Data key encrypts data; master key (KMS) encrypts data key.")]),

dict(slug="pipeline-security-scanning", title="Scanning: SAST, SCA, DAST, Image & IaC", level="Intermediate",
intro="Har stage ke liye scanner: code (SAST), dependencies (SCA), running app (DAST), images (Trivy), Terraform (Checkov). CI mein gate lagao.",
diagram="""
commit: gitleaks -> build: SAST (Semgrep/SonarQube) + SCA (Trivy fs/Dependabot)
  -> image: Trivy image + cosign sign + SBOM -> IaC: Checkov/tfsec
  -> staging: DAST (OWASP ZAP) -> prod: runtime (Falco)
""",
install="""docker run --rm -v $PWD:/src returntocorp/semgrep semgrep --config auto /src
docker run --rm -v $PWD:/src aquasec/trivy fs /src
pip install checkov""",
examples=[("GitHub Actions security job","""security:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
      with: { fetch-depth: 0 }
    - uses: gitleaks/gitleaks-action@v2
    - uses: aquasecurity/trivy-action@master
      with: { scan-type: fs, severity: 'HIGH,CRITICAL', exit-code: '1', ignore-unfixed: true }
    - run: pip install checkov && checkov -d infra --quiet
    - run: docker run --rm -v $PWD:/zap/wrk owasp/zap2docker-stable zap-baseline.py -t https://staging.example.com"""),
("Trivy usage","""trivy image --severity CRITICAL,HIGH --exit-code 1 myapp:1.0
trivy config .            # IaC / Dockerfile / K8s misconfig
trivy image --format cyclonedx -o sbom.json myapp:1.0""")],
problems=[("Scanner blocks every build with hundreds of findings","No triage/baseline","Fail only on HIGH/CRITICAL with fix available; baseline, ignore file with expiry, auto-update deps."),
("False positives waste time","Generic rules","Tune rules, suppress with justification, track in ticket.")],
qa=[("SAST vs DAST vs SCA?","SAST scans source; DAST attacks running app; SCA checks third-party dependency CVEs."),
("What is an SBOM?","Software bill of materials listing components for vulnerability tracking."),
("What is CVE/CVSS?","CVE identifies a vulnerability; CVSS scores severity."),
("How to secure the CI itself?","Least-privilege tokens, OIDC, pinned actions by SHA, isolated runners, no secrets on PRs from forks."),
("What is image signing?","cosign signs digest; admission controller verifies before running.")]),

dict(slug="cloud-k8s-security", title="Cloud, Network & Kubernetes Runtime Security", level="Advanced",
intro="IAM hygiene, network segmentation, encryption, K8s policies aur runtime detection (Falco). Compliance aur incident response.",
diagram="""
Cloud: SCPs | IAM roles+boundaries | KMS | CloudTrail | GuardDuty | Security Hub | Config rules
K8s: RBAC | NetworkPolicy default-deny | Pod Security (restricted) | Kyverno/OPA | Falco runtime | mTLS (mesh)
""",
install="""helm repo add falcosecurity https://falcosecurity.github.io/charts
helm install falco falcosecurity/falco -n falco --create-namespace
helm repo add kyverno https://kyverno.github.io/kyverno/ && helm install kyverno kyverno/kyverno -n kyverno --create-namespace""",
examples=[("Restricted pod spec","""securityContext:
  runAsNonRoot: true
  seccompProfile: { type: RuntimeDefault }
containers:
- name: app
  securityContext:
    allowPrivilegeEscalation: false
    readOnlyRootFilesystem: true
    capabilities: { drop: [ALL] }"""),
("Namespace Pod Security","""kubectl label ns prod pod-security.kubernetes.io/enforce=restricted"""),
("IRSA (pod IAM role) idea","""ServiceAccount annotation eks.amazonaws.com/role-arn -> pod gets scoped AWS creds, no node-wide role"""),
("Incident response steps","""Detect -> Contain (isolate SG/pod, revoke creds) -> Eradicate -> Recover -> Post-incident review (blameless)
Collect evidence: CloudTrail, VPC flow logs, K8s audit logs, memory/disk snapshot""")],
problems=[("Compromised pod could reach every service","Flat network","Default-deny NetworkPolicies + allow-lists; service mesh mTLS."),
("Node IAM role too broad, pods abuse it","All pods share node role","IRSA / Pod Identity, block IMDS from pods (hop limit 1, IMDSv2).")],
qa=[("How to secure EKS?","Private endpoint, IRSA, RBAC, network policies, PSS, image scanning, secrets encryption, audit logs, node patching."),
("What is IMDSv2?","Session-token based instance metadata service protecting against SSRF credential theft."),
("What is Falco?","Runtime threat detection via syscall rules (e.g. shell in container)."),
("Compliance frameworks?","SOC2, ISO 27001, PCI-DSS, HIPAA; automate evidence via policy-as-code."),
("Encryption at rest vs in transit?","At rest via KMS/EBS/S3 SSE; in transit via TLS/mTLS.")]),
])
