EXT = dict(
guide=dict(
bigpicture=dict(
problem="""**Problem it solves:** If security checks happen only at the end (a penetration test before go-live), vulnerabilities are found late, fixes are expensive and releases are blocked. **DevSecOps** builds security into every step of the delivery pipeline ("shift left") and into runtime, so problems are caught early, automatically and continuously.""",
chain=["PROBLEM: software and infrastructure ship with vulnerabilities and leaked secrets",
       "TRADITIONAL APPROACH: separate security team reviews at the end",
       "PAIN: late findings, delays, friction, breaches from known issues",
       "TECHNOLOGY: DevSecOps (SAST, SCA, secret scan, image/IaC scan, DAST, policy, runtime security)",
       "SOLUTION: automated checks in pipeline + least privilege + secrets management + monitoring",
       "REAL-WORLD BENEFIT: fewer incidents, faster compliant releases, security as shared responsibility"],
text="""Core principles: **least privilege**, **defence in depth** (multiple layers), **zero trust** (verify every request), **secure by default**, and **assume breach** (detect and respond). The **CIA triad** (Confidentiality, Integrity, Availability) frames what we protect."""),
e2e=dict(diagram="""Developer IDE / pre-commit (secret scan, lint)
   v
Git PR (branch protection, code review, signed commits)
   v
CI pipeline:
   SAST (code)  +  SCA (dependencies)  +  Secret scan  +  IaC scan (Terraform/K8s YAML)
   v
Build image (minimal base) -> Image scan (Trivy) -> SBOM (Syft) -> Sign (cosign)
   v
Registry (private, scanning, immutable tags)
   v
Deploy gate: policy admission (Kyverno/OPA) verifies signature, non-root, no privileged
   v
Runtime: NetworkPolicy, Pod Security, RBAC, secrets from Vault/Secrets Manager, WAF
   v
DAST on staging, runtime detection (Falco/GuardDuty), logging/SIEM
   v
Vulnerability management: patch, rotate, incident response, audit""",
text="""Security starts **before commit** with local secret scanning and continues in **CI**: **SAST** analyses source code, **SCA** checks third-party dependencies for known CVEs, **secret scanning** blocks leaked credentials, **IaC scanning** checks Terraform/Kubernetes files for misconfiguration. The built **image** is scanned, an **SBOM** (Software Bill of Materials) is produced and the image is **signed**. At deploy time an **admission controller** enforces policies (only signed images, non-root, no privileged containers). At **runtime**, NetworkPolicies limit traffic, RBAC limits API access, secrets come from a vault, and tools such as Falco/GuardDuty detect suspicious behaviour. **DAST** tests the running staging app. Findings feed a patching and incident-response process."""),
tools=dict(rows=[
["Gitleaks / trufflehog", "Secret detection", "Repo/commits", "Findings", "Pre-commit + CI"],
["SonarQube / Semgrep / CodeQL", "SAST", "Source code", "Code vulnerabilities", "CI"],
["Dependabot / Snyk / OWASP Dependency-Check / pip-audit", "SCA", "Dependency manifests", "CVE list + fix versions", "CI/scheduled"],
["Trivy / Grype", "Image and IaC scanning", "Image/IaC", "CVE/misconfig report", "CI + registry"],
["Checkov / tfsec / kube-linter", "IaC misconfiguration", "Terraform/K8s YAML", "Policy violations", "CI"],
["Syft / cosign", "SBOM / signing", "Image", "SBOM, signature", "CI"],
["HashiCorp Vault / AWS Secrets Manager", "Secrets storage and rotation", "Secrets", "Short-lived credentials", "Runtime"],
["OWASP ZAP", "DAST", "Running app URL", "Web vulnerabilities", "Staging"],
["Kyverno / OPA Gatekeeper", "Admission policy", "K8s requests", "Allow/deny", "Cluster"],
["Falco / GuardDuty / Security Hub", "Runtime threat detection", "Syscalls/logs", "Alerts", "Production"]],
why="**SAST vs DAST:** SAST reads source without running it (early, code-level, false positives); DAST attacks the running app from outside (finds runtime/config issues, later in cycle). **SCA vs SAST:** SCA checks *third-party* libraries; SAST checks *your* code. **Vault vs Secrets Manager:** Vault is cloud-agnostic with dynamic secrets; Secrets Manager is AWS-managed with native rotation."),
compare=[
("SAST vs DAST vs SCA vs IAST", ["Type", "What it tests", "When", "Example"], [["SAST", "Source code", "Build time", "SonarQube, Semgrep"], ["DAST", "Running application", "Staging/test", "OWASP ZAP"], ["SCA", "Dependencies", "Build time", "Snyk, Dependabot"], ["IAST", "App instrumented at runtime during tests", "Test", "Contrast"]]),
("Authentication vs Authorization", ["Topic", "AuthN", "AuthZ"], [["Question", "Who are you?", "What may you do?"], ["Example", "Login, MFA, OIDC", "RBAC, IAM policy"]]),
("Symmetric vs Asymmetric encryption", ["Topic", "Symmetric", "Asymmetric"], [["Keys", "One shared key", "Public/private pair"], ["Speed", "Fast", "Slower"], ["Use", "Bulk data (AES)", "Key exchange, signatures (RSA/ECC)"]]),
("Secrets vs ConfigMap vs Vault", ["Topic", "K8s Secret", "External vault"], [["Encryption", "Base64 (enable etcd encryption)", "Encrypted, audited, rotated"], ["Dynamic creds", "No", "Yes (Vault)"]]),
("Hashing vs Encryption vs Encoding", ["Topic", "Hashing", "Encryption", "Encoding"], [["Reversible", "No", "Yes (with key)", "Yes (no key)"], ["Purpose", "Integrity, password storage (bcrypt/argon2)", "Confidentiality", "Data format (base64)"]])],
troubleshooting=[
("Secret found in Git history", "Committed key/token", "`gitleaks detect`, `git log -S`", "Rotate immediately, remove from history, invalidate sessions, audit usage in CloudTrail.", "Pre-commit hook + push protection + secret manager."),
("Pipeline blocked by a critical CVE", "Vulnerable base image or library", "Trivy/Snyk report shows package and fixed version", "Update package/base image, rebuild; if no fix, assess exploitability and add time-boxed exception.", "Automated dependency updates; regular base image rebuilds."),
("Too many false positives from scanners", "Default rules too broad", "Review findings and rule IDs", "Tune rules, baseline, suppress with justification and expiry.", "Security champions review exceptions."),
("Pod blocked by admission policy", "Policy violation (root, privileged, unsigned image)", "`kubectl describe`, event message from Kyverno/Gatekeeper", "Fix the manifest (runAsNonRoot, drop capabilities, sign image).", "Provide compliant templates/Helm charts."),
("Suspicious outbound traffic from a container", "Compromised container or cryptominer", "Falco alerts, `kubectl exec` inspection, flow logs, NetworkPolicy", "Isolate (NetworkPolicy/quarantine), collect evidence, redeploy from clean image, rotate secrets.", "Default-deny egress, runtime detection."),
("IAM key exposed", "Key in code/log/public repo", "CloudTrail activity for the key, IAM credential report", "Deactivate and rotate key, review activity, revoke sessions.", "Use roles/OIDC, no long-lived keys.")],
practices={
"Development": ["Threat model new features; input validation; parameterised queries; dependency updates; pre-commit secret scan."],
"Production": ["Patch regularly; least-privilege IAM; network segmentation; WAF; backups; incident response plan."],
"Security": ["Encrypt in transit and at rest; MFA; rotate secrets; sign artifacts; verify at admission; audit logging; CIS benchmarks; scan continuously; vulnerability SLAs (e.g. critical in 7 days)."],
"Performance": ["Run scans incrementally/cached and in parallel; scan schedule for heavy DAST."],
"Reliability": ["Security controls should fail closed but with break-glass; test policies in audit mode before enforce."],
"Cost Optimization": ["Prioritise by risk (exploitability, exposure); avoid tool sprawl; use open-source scanners where suitable."],
"Monitoring & Logging": ["Central audit logs (CloudTrail, K8s audit), SIEM alerts, GuardDuty; retention per compliance."],
"Backup & Disaster Recovery": ["Immutable/offline backups (ransomware); tested restore; runbooks for incident response."]},
mistakes={
"Beginner mistakes": ["Hard-coding passwords.", "Using default credentials."],
"Developer mistakes": ["String-concatenated SQL.", "Ignoring dependency alerts.", "Logging sensitive data."],
"DevOps mistakes": ["Scanning but never fixing (no ownership/SLAs).", "Over-privileged CI credentials.", "Running containers as root."],
"Production mistakes": ["Unpatched systems.", "No incident response plan.", "Public S3/DB."],
"Security mistakes": ["Security only at the end.", "Sharing accounts.", "Disabling security tools to 'get it working'."]},
versions=[
"OWASP Top 10 is updated periodically (2021 edition current at time of writing): check owasp.org for the latest.",
"Kubernetes Pod Security Admission replaced PodSecurityPolicy (removed in v1.25).",
"Sigstore/cosign supports keyless signing (OIDC) as well as key-based; check current CLI syntax.",
"Scanner databases update continuously: always run the latest DB and pin scanner versions in CI; some tools changed licences (verify for your use).",
"Compliance frameworks (SOC 2, ISO 27001, PCI DSS, HIPAA, GDPR) have their own requirements: consult your compliance owner."],
hinglish="""**Shift-left** ka matlab security ko **shuru se** lagana, end mein nahi. Pipeline mein **secret scan, SAST (apna code), SCA (dependencies), image scan, IaC scan** lagao aur deploy par **admission policy** se check karo. **Least privilege** rakho, secrets **Vault/Secrets Manager** mein rakho, **MFA** lagao. Secret leak ho to **pehle rotate** karo. **Defence in depth** = ek layer fail ho to doosri bacha le.""",
mnemonics=[("CIA triad", "Confidentiality, Integrity, Availability"), ("STRIDE", "Spoofing, Tampering, Repudiation, Information disclosure, DoS, Elevation of privilege"), ("Shift-left scans", "S-S-S-I-D: Secrets, SAST, SCA, Image/IaC, DAST"), ("Least privilege", "Give the minimum, for the minimum time"), ("Incident", "Contain > Eradicate > Recover > Learn")],
client=dict(
s30="""DevSecOps means security is built into every step of how we build and run software, automatically. That finds problems early, keeps secrets safe and lowers the risk of breaches without slowing down releases.""",
m2="""Instead of a security review at the end, we run automatic checks throughout the pipeline: scanning for leaked passwords, vulnerabilities in our code and in third-party libraries, and weaknesses in container images and infrastructure code. Only images that pass and are digitally signed can be deployed. In production we use least-privilege access, encrypted data, network segmentation and monitoring for suspicious activity. Secrets live in a vault, not in code. This reduces the chance and impact of an incident and gives you evidence for audits.""",
m5="""I will describe four layers. **Code:** pre-commit secret scanning, code review, SAST and dependency scanning with automated update pull requests. **Build and supply chain:** minimal container images, image and infrastructure-as-code scanning, an SBOM for each release and cryptographic signing, with policies that fail the build on critical findings. **Deployment and runtime:** admission controls that only allow signed, non-root images, RBAC and network policies, encrypted secrets from a vault with rotation, WAF and runtime threat detection. **Governance:** centralised audit logs, vulnerability SLAs, tested incident-response and backup procedures, and mapping of controls to compliance frameworks such as ISO 27001 or SOC 2. Security becomes a repeatable, measured process instead of a last-minute gate."""),
roadmap=[
("Beginner", ["CIA triad and basic threats (OWASP Top 10)", "Passwords, MFA, TLS", "Least privilege", "Secret hygiene"]),
("Intermediate", ["SAST, SCA, secret scanning in CI", "Image scanning with Trivy", "Vault/Secrets Manager", "Cloud IAM security"]),
("Advanced", ["Threat modelling (STRIDE)", "Kubernetes security (RBAC, NetworkPolicy, PSA, Kyverno)", "Supply chain security (SBOM, cosign, SLSA)", "Runtime detection (Falco/GuardDuty)"]),
("Production", ["Vulnerability management SLAs", "Incident response", "Compliance automation", "Security monitoring/SIEM"]),
("Interview", ["Design a secure pipeline", "Handle a leaked secret", "SAST vs DAST vs SCA", "Secure a Kubernetes cluster"])],
miniproject=dict(title="Secure pipeline: secret scan + SAST/SCA + Trivy + SBOM + signing",
arch="""PR --> gitleaks --> unit tests --> semgrep (SAST) + dependency audit (SCA)
    --> docker build --> trivy image (fail on HIGH/CRITICAL) --> syft SBOM --> cosign sign
    --> push registry --> Kyverno verifies signature at admission""",
steps=[
("Step 1: Secret scanning", """gitleaks detect --source . --verbose
# CI: fail the job on any finding (exit code 1)""", "Detects API keys and tokens in the working tree and history. Rotate anything found before cleaning up."),
("Step 2: SAST and SCA", """pip install semgrep pip-audit
semgrep --config auto --error .
pip-audit -r requirements.txt
# JS: npm audit --audit-level=high""", "`--error` returns non-zero when findings exist. `pip-audit`/`npm audit` find known vulnerable dependencies. Tune rules to control false positives."),
("Step 3: Image scan, SBOM, sign", """docker build -t registry.example.com/app:${GIT_SHA} .
trivy image --severity HIGH,CRITICAL --exit-code 1 registry.example.com/app:${GIT_SHA}
syft registry.example.com/app:${GIT_SHA} -o spdx-json > sbom.json
docker push registry.example.com/app:${GIT_SHA}
cosign sign --yes registry.example.com/app:${GIT_SHA}""", "Trivy blocks vulnerable images; Syft records what is inside; cosign signs the pushed image (keyless signing uses the CI's OIDC identity: verify CLI flags for your cosign version). Sign after push because signatures attach to the registry digest."),
("Step 4: Enforce at admission (Kyverno)", """apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata: { name: require-nonroot }
spec:
  validationFailureAction: Enforce
  rules:
  - name: run-as-non-root
    match: { any: [{ resources: { kinds: [Pod] } }] }
    validate:
      message: "Containers must run as non-root."
      pattern:
        spec:
          securityContext: { runAsNonRoot: true }""", "The cluster rejects Pods that do not declare `runAsNonRoot: true`. Start with `Audit` mode to measure impact, then switch to `Enforce`. A second policy (`verifyImages`) can require valid cosign signatures.")]),
interview=[
("Beginner", "What is DevSecOps?", "Integrating security practices into DevOps: automated, continuous, shared responsibility.", "Definition.", "Scanners in the CI pipeline."),
("Beginner", "What is shift-left security?", "Moving security checks earlier in the development lifecycle.", "Key idea.", "Secret scan before commit."),
("Beginner", "What is the CIA triad?", "Confidentiality, Integrity, Availability.", "Foundations.", "Encryption = confidentiality."),
("Beginner", "What is least privilege?", "Granting only the permissions needed for a task.", "Principle.", "Read-only role for reports."),
("Beginner", "What is MFA?", "Multi-factor authentication: two or more proofs (password + device).", "Account security.", "TOTP on AWS root."),
("Beginner", "What is a vulnerability vs a threat vs risk?", "Vulnerability is a weakness; threat is a potential attacker/event; risk is likelihood times impact.", "Terminology.", "Unpatched server = vulnerability."),
("Beginner", "What is encryption at rest and in transit?", "Protecting stored data (disk/DB) and data moving over networks (TLS).", "Data protection.", "S3 SSE-KMS and HTTPS."),
("Beginner", "What is OWASP Top 10?", "List of the most critical web application security risks.", "Awareness.", "Injection, broken access control."),
("Beginner", "Why not store secrets in Git?", "History keeps them, repos are widely accessible, bots scan for leaks.", "Secrets.", "AWS key abused in minutes."),
("Beginner", "What is a CVE?", "Common Vulnerabilities and Exposures: a public identifier for a known vulnerability.", "Vulnerability mgmt.", "CVE-2021-44228 (Log4Shell)."),
("Intermediate", "SAST vs DAST vs SCA?", "SAST analyses source; DAST tests running app; SCA finds vulnerable dependencies.", "Tool coverage.", "SonarQube, ZAP, Snyk."),
("Intermediate", "What is an SBOM and why?", "A list of components in software; helps find affected systems when a new CVE appears.", "Supply chain.", "Log4Shell impact query."),
("Intermediate", "How do you scan container images?", "Trivy/Grype against OS packages and language dependencies; fail on severity thresholds; rescan registry images regularly.", "Container security.", "`trivy image --exit-code 1`."),
("Intermediate", "Explain secrets management best practices.", "Central vault, dynamic short-lived credentials, rotation, least-privilege access, audit logs, never in code/images.", "Secrets.", "Vault database secrets engine."),
("Intermediate", "What is RBAC?", "Role-based access control assigns permissions to roles, roles to users.", "AuthZ.", "K8s Role/RoleBinding."),
("Intermediate", "What is SQL injection and prevention?", "Attacker input alters a query; prevent with parameterised queries/ORM, validation and least-privilege DB accounts.", "App security.", "`' OR 1=1 --`."),
("Intermediate", "What is XSS/CSRF?", "XSS injects scripts into pages; CSRF tricks a browser into unwanted authenticated requests; prevent with output encoding/CSP and CSRF tokens/SameSite cookies.", "Web security.", "Stored XSS in comments."),
("Intermediate", "How do you secure Docker containers?", "Non-root user, minimal image, read-only FS, drop capabilities, no privileged/docker.sock, scan/sign images, resource limits.", "Container hardening.", "See Docker guide."),
("Intermediate", "What is a WAF?", "Web application firewall filtering HTTP traffic for attacks (SQLi, XSS, bots).", "Perimeter.", "AWS WAF on ALB."),
("Intermediate", "What is TLS/mTLS?", "TLS encrypts and authenticates server; mTLS authenticates both sides.", "Transport security.", "Service mesh mTLS."),
("Intermediate", "How to secure CI/CD?", "Least-privilege runners, OIDC not static keys, protected branches, secret scanning, pinned actions/plugins, isolated ephemeral agents, signed artifacts.", "Pipeline security.", "GitHub Actions hardening."),
("Intermediate", "What is IaC scanning?", "Checking Terraform/CloudFormation/K8s manifests for misconfigurations before deployment.", "Prevent misconfig.", "Checkov finds open SG."),
("Intermediate", "What is a security group misconfiguration example?", "Allowing 0.0.0.0/0 to SSH/DB ports.", "Cloud security.", "Exposed MongoDB."),
("Intermediate", "What is IAM best practice?", "No root use, MFA, roles instead of keys, least privilege, rotate, review with Access Analyzer.", "Cloud IAM.", "Assume-role for admins."),
("Advanced", "How would you design a secure CI/CD pipeline end to end?", "Pre-commit + protected branches; CI with SAST/SCA/secret/IaC/image scans; SBOM+signing; private registry; admission verification; OIDC creds; approvals; audit logs.", "Architecture.", "See mini project."),
("Advanced", "Explain supply chain attacks and mitigations.", "Compromising dependencies, build systems or registries; mitigate with pinning, provenance (SLSA), signed artifacts, SBOM, private mirrors, review of updates, least privilege builds.", "Modern threat.", "SolarWinds/xz-style incidents."),
("Advanced", "How do you secure a Kubernetes cluster?", "RBAC least privilege, NetworkPolicy default deny, Pod Security Standards, admission policies, secrets encryption/external, image signing, audit logs, runtime detection, node hardening, regular upgrades.", "K8s security.", "Kyverno + Falco."),
("Advanced", "What is threat modelling (STRIDE)?", "Systematic identification of threats using data-flow diagrams and categories: Spoofing, Tampering, Repudiation, Information disclosure, DoS, Elevation of privilege.", "Design security.", "Model login flow."),
("Advanced", "What is zero trust?", "Never trust by network location; authenticate, authorise and encrypt every request with least privilege and continuous verification.", "Architecture.", "BeyondCorp-style access."),
("Advanced", "Vault dynamic secrets?", "Vault generates short-lived credentials on demand (DB users/AWS keys) with TTL and automatic revocation.", "Secrets depth.", "DB user valid 1 hour."),
("Advanced", "How do you handle a compromised credential?", "Revoke/rotate, determine scope via audit logs, contain, eradicate persistence, recover, communicate, postmortem, add prevention.", "Incident response.", "Leaked AWS key."),
("Advanced", "Explain IAM policy evaluation and privilege escalation risks.", "Explicit deny wins; risky permissions (iam:PassRole, iam:CreatePolicyVersion, sts:AssumeRole broadly) allow escalation; use boundaries/SCPs.", "Cloud security depth.", "PassRole to admin role."),
("Advanced", "What is container escape and how to prevent it?", "Breaking out of isolation to the host via kernel bugs or misconfig (privileged, docker.sock, hostPath); prevent by hardening, updates, seccomp/AppArmor, gVisor/Kata for untrusted workloads.", "Container internals.", "Privileged Pod."),
("Advanced", "SLSA framework?", "Levels of supply-chain assurance: scripted builds, provenance, hardened isolated builds, verification.", "Supply chain.", "Provenance attestation with GitHub."),
("Advanced", "How to manage vulnerabilities at scale?", "Inventory (SBOM), prioritise by exploitability/exposure (EPSS/KEV), SLAs, ownership, automated updates, exceptions with expiry, metrics.", "Vuln mgmt.", "Critical in 7 days."),
("Advanced", "Explain secure secret injection in Kubernetes.", "External Secrets Operator/CSI driver/Vault agent fetching at runtime, avoiding Git-stored secrets; encrypt etcd; short-lived tokens.", "K8s secrets.", "ESO syncing from Secrets Manager."),
("Advanced", "What is a security incident lifecycle?", "Preparation, detection, containment, eradication, recovery, lessons learned (NIST).", "IR process.", "Runbooks and drills."),
("Advanced", "How do you audit and monitor for threats?", "CloudTrail, K8s audit, VPC flow logs, GuardDuty, SIEM correlation, alerts on anomalies, retention.", "Detection.", "Alert on root login."),
("Scenario-Based", "A developer pushed an AWS key to GitHub.", "Deactivate/rotate key immediately, check CloudTrail for use, purge history, enable push protection, move to role/OIDC.", "Classic incident.", "See troubleshooting."),
("Scenario-Based", "Critical CVE in a base image used by 30 services.", "Identify via SBOM/registry scan, update base image centrally, rebuild and redeploy in priority order, verify, add gate.", "Scale response.", "Renovate opens PRs across repos."),
("Scenario-Based", "Auditor asks for proof of change control.", "Show PR approvals, signed commits, pipeline logs, artifact signatures, deployment history and CloudTrail.", "Compliance.", "GitOps audit trail."),
("Scenario-Based", "Security scans slow the pipeline.", "Cache DBs, run in parallel, incremental SAST, full scans nightly, gate only on new findings.", "Balance speed/safety.", "Trivy DB cache."),
("Scenario-Based", "Developers bypass security gates.", "Make secure path easiest (templates), enforce server-side (branch protection, admission), educate, measure exceptions.", "Culture.", "Golden pipeline."),
("Scenario-Based", "Database credentials shared in chat.", "Rotate, move to secret manager with dynamic creds, restrict access, policy and training.", "Secrets hygiene.", "Vault DB engine."),
("Scenario-Based", "Public S3 bucket with customer data.", "Block access immediately, assess exposure via access logs, notify per policy/regulation, enable account-level Block Public Access and Config rules.", "Data breach response.", "Config auto-remediation."),
("Scenario-Based", "Ransomware risk mitigation.", "Immutable/offline backups, least privilege, patching, MFA, EDR, network segmentation, tested restores.", "Resilience.", "S3 Object Lock backups."),
("Scenario-Based", "Third-party library compromised (new malicious version).", "Pin versions/lockfiles, use private proxy with delay/allowlist, monitor advisories, rebuild from known-good, rotate secrets touched by builds.", "Supply chain response.", "npm typosquat."),
("Scenario-Based", "Design secure access for contractors.", "Time-bound least-privilege roles via SSO, MFA, session logging, no shared accounts, access reviews.", "Access governance.", "Identity Center."),
("Scenario-Based", "Prevent privileged containers cluster-wide.", "Pod Security Admission restricted or Kyverno/Gatekeeper policy, exceptions by namespace with review.", "Guardrails.", "Enforce non-root."),
("Scenario-Based", "How to secure an internal admin panel?", "Not public; SSO+MFA behind VPN/zero-trust proxy, RBAC, audit logs, IP allow-list.", "Access design.", "Grafana admin."),
("Scenario-Based", "Log4Shell-style zero-day announced.", "Identify affected assets via SBOM, apply mitigations/WAF rules, patch/upgrade, monitor for exploitation, communicate.", "Zero-day response.", "Search images for log4j."),
("Scenario-Based", "Encrypt data for a new service.", "TLS in transit; KMS-managed keys at rest; key policies/rotation; app-level encryption for highly sensitive fields.", "Data protection.", "RDS with KMS."),
("Troubleshooting-Based", "Gitleaks flags a false positive.", "Verify it is not a real secret, add a baseline/allowlist entry with justification, avoid disabling the rule globally.", "Tuning.", "Test fixtures."),
("Troubleshooting-Based", "Trivy fails on unfixable CVE.", "Assess exploitability; use `.trivyignore` with expiry and reasoning, switch base image, or apply mitigations.", "Exceptions.", "No upstream fix yet."),
("Troubleshooting-Based", "Kyverno blocks all deployments unexpectedly.", "Policy in Enforce too broad or webhook failing; check policy reports/events, switch to Audit, fix policy or exclude system namespaces.", "Policy ops.", "kube-system excluded."),
("Troubleshooting-Based", "Vault agent cannot fetch secrets.", "Auth method/role/policy mismatch, token TTL, network; inspect agent logs and Vault audit log.", "Secrets integration.", "Kubernetes auth role wrong SA."),
("Troubleshooting-Based", "Cosign verification fails at admission.", "Wrong identity/issuer/public key, unsigned digest vs tag mismatch, registry access; verify with `cosign verify` manually.", "Signing.", "Signed tag, deployed different digest."),
("Troubleshooting-Based", "TLS handshake errors after cert rotation.", "Chain/intermediate missing or clients pinned to old cert; test with openssl and update trust.", "PKI.", "Expired intermediate."),
("Troubleshooting-Based", "AccessDenied for a role that should work.", "SCP/boundary/resource policy/KMS key policy denies; analyse with CloudTrail and policy simulator.", "IAM debugging.", "KMS key policy lacks role."),
("Troubleshooting-Based", "SAST finds too many issues on legacy code.", "Baseline existing findings, gate on new/changed code, schedule remediation.", "Adoption.", "Sonar new-code period."),
("Troubleshooting-Based", "Falco alert 'Terminal shell in container'.", "Determine if legitimate (debug) or intrusion; check exec audit logs, isolate/redeploy, restrict exec via RBAC.", "Runtime response.", "kubectl exec by unknown user."),
("Troubleshooting-Based", "Secrets show in application logs.", "Add redaction/log filters, rotate exposed secrets, review logging code and retention.", "Data leak.", "Logging full request headers.")],
cheatsheet={
"Definitions": ["CIA; least privilege; defence in depth; zero trust; SAST/DAST/SCA; SBOM; CVE; MFA; RBAC; encryption at rest/in transit; STRIDE."],
"Commands": ["`gitleaks detect` `semgrep --config auto` `pip-audit` `npm audit` `trivy image|fs|config` `checkov -d .` `tfsec .`", "`syft img -o spdx-json` `cosign sign|verify img` `zap-baseline.py -t URL`", "`vault kv put|get` `vault token lookup` `kubectl auth can-i` `kubectl get networkpolicy`", "`aws iam get-account-authorization-details` `aws cloudtrail lookup-events`"],
"Files": [".gitleaks.toml .trivyignore .pre-commit-config.yaml Kyverno/Gatekeeper policies NetworkPolicy IAM policy JSON sbom.json"],
"Architecture": ["Pre-commit > PR > CI scans > sign > registry > admission policy > runtime detection > audit/SIEM."],
"Ports": ["HTTPS 443, Vault 8200, SonarQube 9000, ZAP API 8080, SSH 22 (restrict), DB ports private only"],
"Differences": ["SAST vs DAST vs SCA; AuthN vs AuthZ; hash vs encrypt vs encode; Secret vs Vault; symmetric vs asymmetric."],
"Troubleshooting commands": ["`gitleaks` > `trivy` > CloudTrail lookup > `kubectl describe` (policy events) > `openssl s_client` > Vault audit log"],
"Best practices": ["Shift-left scans, least privilege, MFA, secret manager, sign+verify, non-root, network policies, patch SLAs, audit logs, tested IR plan."]}
),
subs={
"security-fundamentals": dict(
define=dict(simple="Security is protecting systems and data from misuse; fundamentals are the basic principles everything else builds on.",
technical="Security engineering applies CIA, least privilege, defence in depth, secure defaults and threat modelling; authentication, authorisation, cryptography (hashing, symmetric/asymmetric, TLS, PKI) and OWASP risks form the base.",
why="Breaches damage data, trust and money.", without="Reactive firefighting.", use="Every system.", avoid="Security by obscurity.", analogy="A building with locks, guards, cameras and alarms: several layers."),
internals="""Threat modelling draws data flows, marks trust boundaries and asks 'what can go wrong' using STRIDE; each threat gets a control (authN, encryption, validation, logging). Authentication proves identity (password + MFA/OIDC); authorisation evaluates policy for each request; cryptography protects confidentiality/integrity; logging detects misuse.""",
lab=dict(goal="Practise hashing, encryption and TLS inspection.", prereq=["Linux/WSL with openssl"],
steps=[("echo -n 'password' | sha256sum", "Hashing: one-way, same input gives the same hash (passwords need salted slow hashes such as bcrypt/argon2 instead)."), ("echo 'secret' | openssl enc -aes-256-cbc -pbkdf2 -salt -out s.enc -pass pass:demo && openssl enc -d -aes-256-cbc -pbkdf2 -in s.enc -pass pass:demo", "Symmetric encryption and decryption with the same key."), ("echo | openssl s_client -connect example.com:443 -servername example.com 2>/dev/null | openssl x509 -noout -subject -issuer -dates", "Inspect a real TLS certificate chain.")]),
compare=[("OWASP Top 10 themes", ["Risk", "Prevention"], [["Broken access control", "Server-side authorisation checks, deny by default"], ["Cryptographic failures", "TLS, strong algorithms, key management"], ["Injection", "Parameterised queries, input validation"], ["Vulnerable components", "SCA and updates"], ["Security misconfiguration", "Hardened defaults, IaC scanning"]])],
mnemonics=[("CIA", "Confidentiality, Integrity, Availability"), ("STRIDE", "S-T-R-I-D-E")], hinglish="Security ka base: **least privilege, defence in depth, encryption, MFA**. Password hash karo (bcrypt/argon2), encrypt nahi.",
practices={"Security": ["Secure defaults, validate input, parameterised queries."]}, mistakes={"Developer mistakes": ["Rolling your own crypto.", "MD5/SHA1 for passwords."]},
qa_extra=[("Intermediate", "Why hash passwords with bcrypt/argon2 instead of SHA-256?", "They are deliberately slow and salted, resisting brute force and rainbow tables; plain fast hashes are easy to crack.", "Crypto practice.", "Credential dump defence.")]),

"secrets-management": dict(
define=dict(simple="Keeping passwords, tokens and keys out of code and giving them to apps safely at runtime.",
technical="Secrets managers (Vault, AWS Secrets Manager, Parameter Store) store encrypted secrets with access policies, audit logs, versioning and rotation; apps authenticate with machine identity (IAM role/K8s SA) to fetch them.",
why="Leaked secrets are a top breach cause.", without="Passwords in Git and env files.", use="All credentials.", avoid="Long-lived shared secrets.", analogy="A bank vault with a logbook: you sign to borrow and it records everything."),
internals="""App identity (IAM role or Kubernetes ServiceAccount token) > authenticates to Vault/Secrets Manager > policy checks > returns secret (or generates a dynamic credential with TTL) > audit log entry. Rotation replaces the secret and updates consumers; short TTL limits blast radius.""",
config=[("Vault policy and read explained", """path "secret/data/app/prod/*" {
  capabilities = ["read"]
}
# CLI
vault kv put secret/app/prod/db username=app password=S3cr3t
vault kv get -field=password secret/app/prod/db""", [("path secret/data/...", "KV v2 paths include `data/` in policies."), ("capabilities read", "Least privilege: read only."), ("vault kv put/get", "Write and fetch a secret; never put real secrets in shell history in real environments.")])],
lab=dict(goal="Try Vault in dev mode (never for production).", prereq=["Docker"],
steps=[("docker run -d --name vault -p 8200:8200 -e VAULT_DEV_ROOT_TOKEN_ID=root hashicorp/vault", "Starts an in-memory dev Vault."), ("export VAULT_ADDR=http://127.0.0.1:8200 VAULT_TOKEN=root && vault kv put secret/demo password=abc123", "Stores a secret."), ("vault kv get secret/demo", "Reads it back; versions and metadata are kept.")]),
mnemonics=[("Secrets", "Central, Short-lived, Audited, Rotated")], hinglish="Secret **Git mein nahi**, vault mein. App ko **identity (role)** se secret milna chahiye, aur secret **short-lived** ho toh behtar.",
practices={"Security": ["Rotation, dynamic secrets, audit logs, least-privilege policies."]}, mistakes={"Security mistakes": ["Secrets in env files in Git.", "Root token usage."]},
versions=["Vault dev mode is for learning only; KV v1 vs v2 paths differ; check the current Vault docs for CLI and Kubernetes auth syntax."],
qa_extra=[("Scenario-Based", "How does an app running on EKS get DB credentials safely?", "Use IRSA to assume a role that reads Secrets Manager (or Vault Kubernetes auth), inject via External Secrets/CSI at runtime, rotate automatically.", "Cloud-native secrets.", "No static credentials in manifests.")]),

"pipeline-security-scanning": dict(
define=dict(simple="Automatic scanners in the pipeline that find secrets, vulnerable code, libraries, images and bad infrastructure config.",
technical="Layered scanning: secrets (gitleaks), SAST (Semgrep/SonarQube/CodeQL), SCA (Snyk/Dependabot/pip-audit), container/IaC (Trivy/Checkov), DAST (ZAP), with quality gates based on severity and policy.",
why="Find issues early when they are cheap to fix.", without="Vulnerabilities reach production.", use="Every pipeline.", avoid="Gates so strict that teams bypass them.", analogy="Airport security: bags, body scanner, passport check: different tests."),
internals="""Each scanner parses artifacts (source AST, dependency manifests, image layers, IaC files) and matches against rules or vulnerability databases (NVD, GitHub Advisory). Results (SARIF/JSON) are uploaded to the CI/security dashboard; a gate compares severities against thresholds and fails the build.""",
config=[("GitHub Actions security stage explained", """  security:
    runs-on: ubuntu-latest
    permissions: { contents: read, security-events: write }
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - name: Secret scan
        uses: gitleaks/gitleaks-action@v2
      - name: SCA + IaC + image scan
        uses: aquasecurity/trivy-action@0.28.0
        with: { scan-type: fs, severity: 'HIGH,CRITICAL', exit-code: '1' }""", [("fetch-depth: 0", "Full history so gitleaks can scan past commits."), ("permissions", "Least privilege token; `security-events: write` allows uploading SARIF."), ("gitleaks-action", "Secret detection."), ("trivy fs", "Scans dependencies, IaC and secrets in the repo; `exit-code: 1` fails on findings.")])],
lab=dict(goal="Scan a project locally.", prereq=["Docker", "A sample repo"],
steps=[("docker run --rm -v $PWD:/src zricethezav/gitleaks:latest detect --source=/src -v", "Secret scan."), ("docker run --rm -v $PWD:/src aquasec/trivy fs /src --severity HIGH,CRITICAL", "Dependency/IaC scan."), ("docker run --rm -t ghcr.io/zaproxy/zaproxy:stable zap-baseline.py -t https://your-staging-url", "Baseline DAST (only against systems you own/are authorised to test).")]),
compare=[("Scan placement", ["Stage", "Scan", "Fail on"], [["Pre-commit", "Secrets, lint", "Any secret"], ["PR", "SAST, SCA, IaC", "New high/critical"], ["Build", "Image scan, SBOM, sign", "Critical CVE"], ["Staging", "DAST", "High findings"], ["Runtime", "Registry rescans, Falco", "New CVEs / anomalies"]])],
mnemonics=[("Scan stack", "Secrets, Code, Deps, Image, IaC, Running app")], hinglish="Har scan alag cheez dekhta hai: **secret, code, dependency, image, IaC, running app**. Sirf **new high/critical** par build fail karo taaki team scanners ko bypass na kare.",
practices={"Security": ["Gate on new critical/high; baseline old issues; review exceptions."], "Performance": ["Cache vulnerability DB; parallel scans."]}, mistakes={"DevOps mistakes": ["Scan reports nobody owns."]},
versions=["Action versions and scanner flags change; verify current versions/syntax in each project's documentation. Only run DAST on systems you are authorised to test."],
qa_extra=[("Intermediate", "How do you introduce scanners into a legacy project?", "Baseline existing findings, gate only on new issues, assign owners and SLAs, tune rules and remediate gradually.", "Adoption strategy.", "Sonar new-code gate.")]),

"cloud-k8s-security": dict(
define=dict(simple="Protect cloud accounts, networks and Kubernetes clusters at runtime.",
technical="Cloud: IAM least privilege, private networking, encryption (KMS), logging (CloudTrail/GuardDuty), Config rules. Kubernetes: RBAC, NetworkPolicy, Pod Security Standards, admission policies, runtime detection, secrets protection and image verification.",
why="Attackers target misconfigurations and exposed services.", without="Open buckets, root pods, flat networks.", use="All cloud/Kubernetes environments.", avoid="Default settings unchanged.", analogy="Securing a whole campus: gates, badges, cameras and room locks."),
internals="""Layered controls: perimeter (WAF, security groups) > identity (IAM/OIDC/RBAC) > workload (Pod Security, non-root, seccomp, read-only FS) > network (NetworkPolicy default-deny, mTLS) > data (KMS encryption, secrets manager) > detection (audit logs, GuardDuty, Falco) > response (isolate, rotate, redeploy).""",
config=[("Default-deny NetworkPolicy and a Pod securityContext explained", """apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: { name: default-deny, namespace: prod }
spec:
  podSelector: {}
  policyTypes: [Ingress, Egress]
---
apiVersion: v1
kind: Pod
metadata: { name: hardened }
spec:
  securityContext: { runAsNonRoot: true, seccompProfile: { type: RuntimeDefault } }
  containers:
  - name: app
    image: registry.example.com/app:1.0.0
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities: { drop: [ALL] }""", [("podSelector: {}", "Selects all pods in the namespace."), ("policyTypes Ingress, Egress", "Blocks all traffic until allowed by other policies (needs a CNI that enforces policies)."), ("runAsNonRoot", "Refuses to start as root."), ("seccompProfile RuntimeDefault", "Filters dangerous syscalls."), ("allowPrivilegeEscalation false", "Prevents gaining more privileges."), ("readOnlyRootFilesystem", "Blocks writing malware to the FS."), ("capabilities drop ALL", "Removes Linux capabilities.")])],
lab=dict(goal="Test a default-deny policy.", prereq=["Cluster with a policy-enforcing CNI (Calico/Cilium)", "kubectl"],
steps=[("kubectl create ns lab && kubectl -n lab run web --image=nginx:1.27 --port=80 && kubectl -n lab expose pod web --port=80", "A web pod and service."), ("kubectl -n lab run tmp --rm -it --image=busybox -- wget -qO- -T 3 http://web", "Works before the policy."), ("kubectl -n lab apply -f default-deny.yaml && repeat the wget", "Now times out: traffic is blocked until you add an allow rule.")]),
mnemonics=[("K8s hardening", "R-N-P-S-I: RBAC, NetworkPolicy, Pod security, Secrets, Image verification")], hinglish="Cluster mein **default-deny NetworkPolicy** lagao, pods **non-root** chalao aur RBAC **least privilege** rakho. Cloud mein **CloudTrail + GuardDuty** on rakho.",
practices={"Security": ["Pod Security restricted, NetworkPolicy, RBAC review, audit logs, image verification, node patching."]}, mistakes={"Security mistakes": ["cluster-admin for everyone.", "No egress control."]},
versions=["NetworkPolicy needs a CNI that enforces it (Calico, Cilium); default AWS VPC CNI needs the network policy feature enabled. Pod Security Admission labels and levels (privileged/baseline/restricted) apply from Kubernetes 1.23+ (stable in 1.25)."],
qa_extra=[("Advanced", "How would you detect a compromised pod?", "Runtime detection (Falco) for shells/unexpected processes, egress anomalies from flow logs, audit logs for API calls with its ServiceAccount, image drift; isolate and redeploy.", "Detection and response.", "Cryptominer in a container.")])
})
