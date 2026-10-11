TOPIC = dict(slug="04-python-automation", title="Python & Automation", intro="Bash chhoti tasks ke liye; Python bade automation, AWS SDK, APIs aur tools ke liye. DevOps mein Python sabse useful language hai.", subs=[

dict(slug="python-basics", title="Python Basics for DevOps", level="Basic",
intro="Variables, lists, dicts, functions, files, virtualenv. JSON/YAML parsing DevOps ka daily kaam hai.",
diagram="""
project/
├── .venv/            (isolated deps)
├── requirements.txt
└── main.py
python -m venv .venv -> activate -> pip install -r requirements.txt
""",
install="""# Windows: winget install Python.Python.3.12 ; Ubuntu: sudo apt install python3 python3-venv python3-pip -y
python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\\Scripts\\activate
pip install requests pyyaml boto3""",
examples=[("Read YAML/JSON, write report","""import json, yaml
with open("config.yaml") as f:
    cfg = yaml.safe_load(f)
servers = cfg["servers"]
report = {s["name"]: s["port"] for s in servers if s.get("enabled")}
print(json.dumps(report, indent=2))"""),
("Functions and error handling","""def read_file(path):
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        print(f"missing: {path}")
        return None""")],
problems=[("'ModuleNotFoundError' on server","Packages installed globally on another interpreter","Use venv, pin deps in requirements.txt, run `python -m pip`."),
("Script works locally, fails in CI","Different Python version","Pin version in CI (`actions/setup-python`), use `pyproject`/lockfile.")],
qa=[("List vs tuple vs set vs dict?","List ordered mutable; tuple immutable; set unique unordered; dict key-value."),
("What is a virtualenv?","Isolated environment with its own packages."),
("`yaml.load` vs `safe_load`?","safe_load avoids arbitrary code execution; always use it."),
("What is a context manager (`with`)?","Ensures cleanup (closing files) even on errors."),
("How to handle secrets in scripts?","Env vars / secret manager, never hard-code.")]),

dict(slug="boto3-aws-automation", title="AWS Automation with boto3", level="Intermediate",
intro="boto3 se AWS resources programmatically manage karo: cost saving scripts, backups, audits.",
diagram="""
script --(credentials: role/profile)--> boto3 client --> AWS API (EC2, S3, IAM...)
""",
install="pip install boto3\naws configure   # or use SSO / IAM role; NEVER hard-code keys",
examples=[("Stop dev instances outside office hours","""import boto3
ec2 = boto3.client("ec2", region_name="ap-south-1")
resp = ec2.describe_instances(Filters=[
    {"Name": "tag:Env", "Values": ["dev"]},
    {"Name": "instance-state-name", "Values": ["running"]}])
ids = [i["InstanceId"] for r in resp["Reservations"] for i in r["Instances"]]
if ids:
    ec2.stop_instances(InstanceIds=ids)
    print("stopped", ids)"""),
("Find public S3 buckets","""s3 = boto3.client("s3")
for b in s3.list_buckets()["Buckets"]:
    try:
        st = s3.get_public_access_block(Bucket=b["Name"])["PublicAccessBlockConfiguration"]
        if not all(st.values()): print("REVIEW", b["Name"])
    except Exception:
        print("NO BLOCK", b["Name"])"""),
("Lambda handler running nightly (EventBridge cron)","""def handler(event, context):
    # call the stop-dev-instances logic here
    return {"status": "ok"}""")],
problems=[("Throttling errors (RequestLimitExceeded)","Too many API calls","Use paginators + exponential backoff (`botocore.config.Config(retries={'max_attempts':10,'mode':'adaptive'})`)."),
("Script stopped prod by mistake","No filter/dry-run","Use tags filter, `DryRun=True`, and confirm prompt.")],
qa=[("client vs resource in boto3?","client low-level 1:1 with API; resource higher-level OOP (being deprecated)."),
("How to handle pagination?","`client.get_paginator('describe_instances')`."),
("How do you authenticate boto3 on EC2?","Instance profile IAM role; no keys stored."),
("How to test automation safely?","DryRun flag, moto for mocks, non-prod account."),
("What is idempotency in automation?","Running multiple times yields same end state.")]),

dict(slug="apis-cli-tools", title="APIs, CLI Tools & Monitoring Scripts", level="Intermediate",
intro="REST APIs se baat karna (requests), CLI tool banana (argparse), aur Slack alerts bhejna.",
diagram="""
cron/CI --> python check.py --> requests.get(url) --> compare --> Slack webhook alert
""",
install="pip install requests click",
examples=[("Health checker with Slack alert","""import os, sys, requests
URLS = ["https://example.com/health", "https://api.example.com/health"]
hook = os.environ["SLACK_WEBHOOK"]
bad = []
for u in URLS:
    try:
        r = requests.get(u, timeout=5)
        if r.status_code != 200: bad.append(f"{u} -> {r.status_code}")
    except requests.RequestException as e:
        bad.append(f"{u} -> {e}")
if bad:
    requests.post(hook, json={"text": "ALERT:\\n" + "\\n".join(bad)})
    sys.exit(1)"""),
("CLI with argparse","""import argparse
p = argparse.ArgumentParser(description="Deploy helper")
p.add_argument("env", choices=["dev", "prod"])
p.add_argument("--dry-run", action="store_true")
a = p.parse_args()
print(a.env, a.dry_run)"""),
("Retry with backoff","""import time
def retry(fn, n=5):
    for i in range(n):
        try: return fn()
        except Exception:
            time.sleep(2 ** i)
    raise RuntimeError("failed")""")],
problems=[("Script hangs forever","No timeout on requests","Always set `timeout=`."),
("Duplicate alerts flood Slack","No dedup/state","Store last state (file/Redis) and alert on change only.")],
qa=[("How to make HTTP calls resilient?","Timeouts, retries with exponential backoff and jitter, circuit breaker."),
("subprocess vs os.system?","subprocess safer and gives output/exit code; avoid shell=True with untrusted input."),
("How to package a CLI?","pyproject.toml with entry point, publish to PyPI or container."),
("logging vs print?","logging has levels, handlers, formats; use in production."),
("What is a webhook?","HTTP callback URL that receives event POSTs.")]),

dict(slug="go-and-operators", title="Go for DevOps & Kubernetes Operators (Intro)", level="Advanced",
intro="Docker, Kubernetes, Terraform, Prometheus sab Go mein bane hain. Go static binary deta hai, isliye tools ke liye best. Operators custom controllers hote hain.",
diagram="""
Custom Resource (YAML) --> Controller (watch loop) --> creates/updates K8s objects
      desired state           reconcile(): observe -> diff -> act
""",
install="# https://go.dev/dl/  then: go version\ngo mod init mytool",
examples=[("Tiny Go CLI (health checker)","""package main
import ("fmt";"net/http";"os";"time")
func main() {
    c := http.Client{Timeout: 5 * time.Second}
    r, err := c.Get(os.Args[1])
    if err != nil || r.StatusCode != 200 { fmt.Println("DOWN"); os.Exit(1) }
    fmt.Println("UP")
}
// go build -o check && ./check https://example.com  (cross-compile: GOOS=linux GOARCH=amd64 go build)"""),
("Reconcile idea (pseudo)","""for {
  desired := getCR()
  actual  := getDeployment()
  if actual != desired { apply(desired) }
  sleep()
}""")],
problems=[("Need a tool distributed to all servers without runtime","Python deps hassle","Write in Go, ship single static binary.")],
qa=[("Why Go for DevOps tooling?","Static binaries, fast, great concurrency, cross-compile, strong stdlib."),
("What is an operator?","Controller + CRD encoding operational knowledge to manage an app on K8s."),
("What is reconciliation loop?","Continuously drive actual state to desired state."),
("Goroutine vs thread?","Lightweight user-space concurrency managed by Go runtime."),
("Tools for operators?","kubebuilder, operator-sdk, kopf (Python).")]),
])
