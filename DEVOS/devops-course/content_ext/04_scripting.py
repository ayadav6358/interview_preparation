EXT = dict(
guide=dict(
bigpicture=dict(
problem="""**Problem it solves:** Repeating tasks by hand (creating servers, rotating keys, checking health, cleaning resources, calling APIs) is slow and error-prone. **Python (and Go)** let you automate these tasks with real programming features: data structures, error handling, libraries for AWS, APIs and files.""",
chain=["PROBLEM: repetitive operational tasks across many resources",
       "TRADITIONAL APPROACH: manual console clicks or long fragile bash scripts",
       "PAIN: errors, no reuse, no tests, hard to read",
       "TECHNOLOGY: Python (boto3, requests, argparse, logging) and Go for tools/operators",
       "SOLUTION: small tested scripts and CLIs, run by cron/CI/Lambda",
       "REAL-WORLD BENEFIT: consistent, auditable, repeatable operations and cost savings"],
text="""Rule of thumb: **Bash** for short glue commands (under ~50 lines), **Python** for logic, APIs and cloud SDKs, **Go** for fast single-binary tools and Kubernetes controllers/operators."""),
e2e=dict(diagram="""Trigger (cron / CI / EventBridge / manual)
   v
Python script (venv + pinned dependencies)
   v
Read config (env vars / args / Secrets Manager)
   v
Call APIs (boto3 -> AWS, requests -> HTTP, kubernetes client)
   v
Process data (filter, transform, decide)
   v
Act (stop idle EC2, tag resources, send Slack alert, write report)
   v
Log + exit code (0 ok / non-zero fail) -> CI/monitoring sees the result""",
text="""A **trigger** starts the script. It runs in an isolated **virtual environment** so dependency versions are controlled. Configuration comes from **environment variables/arguments**, never hard-coded; credentials come from an IAM role or a secrets manager. The script **calls APIs** (for example `boto3` for AWS), **processes** the response and **acts**. Good scripts **log** what they did, handle errors with `try/except`, are **idempotent** (safe to run twice) and return a proper **exit code** so schedulers know if it succeeded."""),
tools=dict(rows=[
["Python 3 + venv/pip/uv", "Language runtime and packages", "Source + requirements", "Running script", "Automation host/CI"],
["boto3", "AWS SDK", "AWS credentials + API calls", "AWS resources/data", "Cloud automation"],
["requests / httpx", "HTTP client", "URL + payload", "API responses", "REST/webhooks"],
["argparse / click / typer", "CLI building", "Arguments", "Structured CLI", "Internal tools"],
["pytest", "Testing", "Test files", "Pass/fail", "CI"],
["Go", "Compiled language", "Source", "Single static binary", "CLIs, operators, exporters"],
["kubernetes client / kubebuilder", "Talk to/extend Kubernetes", "Kubeconfig / CRDs", "Controllers", "Platform tooling"],
["Lambda / cron / GitHub Actions", "Run scripts", "Schedule/event", "Executions", "Scheduling"]],
why="**Python vs Bash:** Python has data structures, exceptions, libraries and tests; Bash is faster to write for one-liners. **Python vs Go:** Python is quicker to develop; Go compiles to one static binary with high performance and is the language of Kubernetes/Terraform providers."),
compare=[
("Python vs Bash vs Go", ["Topic", "Bash", "Python", "Go"], [["Best for", "Glue commands", "Automation logic, APIs", "Tools, operators, high performance"], ["Deployment", "Needs shell", "Needs interpreter/venv", "Single binary"], ["Error handling", "Weak", "Exceptions", "Explicit errors"], ["Learning curve", "Low", "Low", "Medium"]]),
("list vs tuple vs dict vs set", ["Type", "Ordered", "Mutable", "Use"], [["list", "Yes", "Yes", "Sequence of items"], ["tuple", "Yes", "No", "Fixed records"], ["dict", "Insertion-ordered", "Yes", "Key/value lookup"], ["set", "No", "Yes", "Unique items"]]),
("boto3 client vs resource", ["Topic", "client", "resource"], [["Level", "Low-level, 1:1 with API", "Higher-level objects (limited services, in maintenance mode)"], ["Recommendation", "Use client (and paginators)", "Avoid for new code"]])],
troubleshooting=[
("`ModuleNotFoundError`", "Package not installed in the active environment", "`which python`, `pip list`, `python -m pip show pkg`", "Activate the venv and `pip install -r requirements.txt`.", "Pin dependencies and use venv per project."),
("`botocore.exceptions.NoCredentialsError`", "No AWS credentials/role/profile", "`aws sts get-caller-identity`, `env | grep AWS`", "Set profile/role (`AWS_PROFILE`), attach IAM role, use SSO.", "Use IAM roles instead of keys."),
("`AccessDenied` from AWS", "IAM policy lacks the action or resource", "CloudTrail event, error message names the action", "Add least-privilege permission for that action/ARN.", "Test with policy simulator."),
("Script only returns first 50/1000 items", "No pagination", "Look for `NextToken`/`IsTruncated`", "Use `get_paginator()`.", "Always paginate list calls."),
("Script works locally, fails in cron", "Environment/PATH/venv differences", "Cron log, absolute paths", "Use absolute python path (`/opt/venv/bin/python`) and set env.", "Log environment on start."),
("API rate limit / throttling", "Too many calls", "HTTP 429, `ThrottlingException`", "Retry with exponential backoff, reduce calls, batch.", "Configure boto3 retries.")],
practices={
"Development": ["Virtual environments; type hints; small functions; `argparse`; unit tests with pytest; format with black/ruff."],
"Production": ["Idempotent scripts, dry-run flag, structured logging, timeouts on every network call, exit codes."],
"Security": ["No secrets in code; use IAM roles/Secrets Manager; least-privilege policies; validate inputs; pin dependencies and scan (pip-audit)."],
"Performance": ["Paginate and filter server-side; use threads/async for many API calls; cache."],
"Reliability": ["Retries with backoff, error handling, alert on failure."],
"Cost Optimization": ["Automate stopping idle resources, deleting unattached volumes, tagging."],
"Monitoring & Logging": ["Use `logging` (JSON) not `print`; send metrics/alerts."]},
mistakes={
"Beginner mistakes": ["Global Python without venv.", "Bare `except:` hiding errors."],
"Developer mistakes": ["Hard-coded credentials/regions.", "No pagination.", "Mutable default arguments."],
"DevOps mistakes": ["Scripts that are not idempotent.", "No dry-run for destructive scripts."],
"Production mistakes": ["No timeouts on `requests` (hangs forever).", "Deleting resources based on name match only."],
"Security mistakes": ["Committing `.env`/keys.", "Logging secrets."]},
versions=[
"Use Python 3.9+ (check supported versions: older ones are end-of-life). `python3` and `python` may differ by OS; on Windows use `py -3`.",
"boto3 `resource` interfaces are feature-frozen: prefer `client`. Check boto3 docs for current APIs.",
"`pip` can be replaced by `uv` for faster installs; both read requirements files.",
"Go modules (`go mod`) replaced GOPATH workflows; check the current stable Go release."],
hinglish="""Chhote kaam ke liye **Bash**, logic/API/AWS ke liye **Python**, aur fast single-binary tools ya Kubernetes operators ke liye **Go**. Script hamesha **idempotent** rakho (do baar chalane se problem na ho), **credentials code mein mat likho**, aur AWS list calls mein **pagination** zaroor lagao.""",
mnemonics=[("Good script", "I-L-E-T: Idempotent, Logged, Error-handled, Tested"), ("boto3 flow", "session > client > paginator > filter > act"), ("Python data", "list [] , tuple (), dict {k:v}, set {}")],
client=dict(
s30="""We automate operational tasks with Python and Go: creating and cleaning cloud resources, checking health, generating reports. That replaces manual work, reduces mistakes and lowers cloud cost.""",
m2="""Manual cloud operations do not scale and cause human error. We write small, tested automation tools in Python that use the AWS SDK and other APIs to do routine work: for example stop unused development servers at night, delete unattached disks, enforce tags and send daily cost or compliance reports. These run on a schedule or in the pipeline using secure roles instead of stored passwords, and log every action for auditing. Where we need a fast standalone tool or a Kubernetes controller we use Go. The benefit is consistency, lower cost and engineers freed for higher-value work.""",
m5="""I will cover why, how, and safety. **Why:** repeated tasks should be code, so they are versioned, reviewed and repeatable. **How:** Python scripts use boto3 to call AWS APIs with pagination and retries, requests for other services, argparse for a clean interface, and pytest for tests; they run from cron, CI or Lambda. Go is chosen for distributable single binaries and for Kubernetes operators built with controller-runtime. **Safety:** idempotent operations, a dry-run mode for destructive actions, least-privilege IAM roles, no secrets in code, timeouts and structured logs. **Governance:** code in Git with pull requests, dependency scanning and alerts on failures. The result is reliable automation you can audit and trust."""),
roadmap=[
("Beginner", ["Variables, types, control flow", "Functions, files, exceptions", "venv and pip", "Reading JSON/YAML"]),
("Intermediate", ["requests and REST APIs", "argparse/click CLIs", "boto3 basics + pagination", "logging, testing with pytest"]),
("Advanced", ["Concurrency (threads/asyncio)", "Packaging CLIs", "Kubernetes Python client", "Go basics and controller-runtime"]),
("Production", ["Idempotency, retries, dry-run", "Secrets and IAM roles", "Scheduling in Lambda/CI", "Observability of scripts"]),
("Interview", ["Write a script to find idle EC2", "Explain pagination and retries", "Python vs Bash vs Go", "Handle secrets safely"])],
miniproject=dict(title="Cost-saver CLI: stop idle dev EC2 instances and alert Slack",
arch="""EventBridge (nightly) --> Lambda/cron --> Python (boto3)
   describe_instances (tag env=dev, state=running)  --paginate-->
   dry-run? print : stop_instances
   --> Slack webhook summary ; logs to CloudWatch ; non-zero exit on error""",
steps=[
("Step 1: Setup", """python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\\Scripts\\activate
pip install boto3 requests
aws sts get-caller-identity""", "Isolated environment and a check that credentials work."),
("Step 2: The script (stopper.py)", """import argparse, logging, os, sys
import boto3, requests

log = logging.getLogger("stopper")

def find_running(ec2):
    ids = []
    for page in ec2.get_paginator("describe_instances").paginate(
        Filters=[{"Name": "tag:env", "Values": ["dev"]},
                 {"Name": "instance-state-name", "Values": ["running"]}]):
        for r in page["Reservations"]:
            ids += [i["InstanceId"] for i in r["Instances"]]
    return ids

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--region", default=os.getenv("AWS_REGION", "ap-south-1"))
    p.add_argument("--apply", action="store_true", help="really stop instances")
    a = p.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    ec2 = boto3.client("ec2", region_name=a.region)
    ids = find_running(ec2)
    log.info("running dev instances: %s", ids)
    if ids and a.apply:
        ec2.stop_instances(InstanceIds=ids)
    hook = os.getenv("SLACK_WEBHOOK")
    if hook:
        requests.post(hook, json={"text": f"stopper: {len(ids)} dev instances {'stopped' if a.apply else 'found (dry-run)'}"}, timeout=10)
    return 0

if __name__ == "__main__":
    sys.exit(main())""", "`paginator` handles more than one page of results; the tag filter limits the blast radius to `env=dev`; **dry-run is the default** and `--apply` is needed to act; the Slack webhook comes from an environment variable; `timeout=10` avoids hanging; `sys.exit(main())` returns a proper exit code."),
("Step 3: Run and schedule", """python stopper.py                 # dry run
python stopper.py --apply
# cron (absolute paths!): 0 20 * * 1-5 /opt/stopper/.venv/bin/python /opt/stopper/stopper.py --apply""", "Always run dry first. Cron needs absolute paths because its environment is minimal."),
("Step 4: Test", """# test_stopper.py
def test_find_running_empty(monkeypatch):
    class Fake:
        def get_paginator(self, n):
            class P:
                def paginate(self, **kw): return [{"Reservations": []}]
            return P()
    import stopper
    assert stopper.find_running(Fake()) == []""", "Unit tests use a fake client, so no real AWS calls are made. Run with `pytest -q`.")]),
interview=[
("Beginner", "Why Python for DevOps?", "Readable, huge library ecosystem (boto3, requests), good for automation and glue code.", "Language choice.", "AWS automation scripts."),
("Beginner", "What is a virtual environment?", "An isolated Python environment with its own packages.", "Dependency control.", "`python -m venv .venv`."),
("Beginner", "list vs dict?", "List is ordered sequence; dict maps keys to values.", "Data structures.", "Instances list, tag dict."),
("Beginner", "What is `pip`?", "Python package installer.", "Dependencies.", "`pip install boto3`."),
("Beginner", "How to read a JSON file?", "`import json; json.load(open('f.json'))`.", "Config handling.", "Parse `aws` output."),
("Beginner", "What is `try/except`?", "Handles exceptions so errors do not crash the script.", "Robustness.", "Catch `ClientError`."),
("Beginner", "What is `requests`?", "HTTP library for calling APIs.", "API integration.", "Post to Slack."),
("Beginner", "What is boto3?", "AWS SDK for Python.", "Cloud automation.", "`boto3.client('s3')`."),
("Beginner", "What are environment variables used for?", "Config and secrets injected at runtime.", "12-factor.", "`os.getenv('DB_URL')`."),
("Beginner", "What is `if __name__ == '__main__'`?", "Runs code only when the file is executed directly, not imported.", "Script structure.", "Testable modules."),
("Intermediate", "Explain pagination in boto3.", "List APIs return limited pages with tokens; use paginators to iterate all results.", "Correctness.", "Listing S3 objects > 1000."),
("Intermediate", "Client vs resource in boto3?", "Client is low-level and complete; resource is higher-level object API but feature-frozen.", "SDK use.", "Prefer client."),
("Intermediate", "How do you handle AWS credentials in scripts?", "Never hard-code; use IAM roles, SSO/profile, env vars or Secrets Manager.", "Security.", "EC2 instance role."),
("Intermediate", "What is idempotency?", "Running an operation multiple times gives the same result.", "Safe automation.", "Create-if-not-exists."),
("Intermediate", "How to build a CLI?", "argparse, click or typer with subcommands and help.", "Tooling.", "`tool stop --apply`."),
("Intermediate", "How to log properly?", "Use the `logging` module with levels and structured output instead of print.", "Observability.", "JSON logs to CloudWatch."),
("Intermediate", "How do you test scripts that call AWS?", "Mock clients (unittest.mock/moto), separate logic from I/O, pytest.", "Quality.", "moto simulates S3/EC2."),
("Intermediate", "How to call an API with retries?", "Use `requests` with `Retry` adapter or tenacity; exponential backoff; timeouts.", "Reliability.", "429 handling."),
("Intermediate", "What are decorators/context managers used for?", "Decorators wrap functions; context managers manage resources (`with open`).", "Python idioms.", "Timing decorator."),
("Intermediate", "Threads vs asyncio vs multiprocessing?", "Threads/async for I/O-bound (API calls), multiprocessing for CPU-bound (GIL).", "Performance.", "Threadpool to query 20 regions."),
("Intermediate", "How to pin dependencies?", "`requirements.txt` with versions or lock files (pip-tools/uv/poetry).", "Reproducibility.", "`pip freeze`."),
("Intermediate", "How to parse YAML safely?", "`yaml.safe_load`, not `yaml.load`.", "Security.", "Read k8s manifests."),
("Advanced", "Design a script to find and delete unattached EBS volumes safely.", "Paginate describe_volumes filter `status=available`, exclude tagged 'keep', age threshold, snapshot first (optional), dry-run default, log actions, IAM least privilege, notify.", "Safe destructive automation.", "Monthly cost cleanup."),
("Advanced", "Explain Python's GIL.", "Global Interpreter Lock lets only one thread execute Python bytecode at a time; affects CPU-bound threading, not I/O-bound.", "Concurrency.", "Use multiprocessing for CPU tasks."),
("Advanced", "Why choose Go for Kubernetes tooling?", "Static single binary, strong concurrency, Kubernetes libraries (client-go, controller-runtime) are Go.", "Ecosystem.", "Operators."),
("Advanced", "What is a Kubernetes Operator?", "A controller with a custom resource that encodes operational knowledge and reconciles desired state.", "Platform engineering.", "Database operator."),
("Advanced", "How to package and distribute a Python tool?", "pyproject.toml, entry points, wheel, private PyPI/artifact registry, container image.", "Tooling.", "`pipx install`."),
("Advanced", "How do you secure a script that runs in CI?", "OIDC roles, least privilege, no secrets in logs, pinned dependencies, pip-audit, read-only tokens.", "Supply chain.", "GitHub OIDC to AWS."),
("Advanced", "Handling partial failures in bulk operations?", "Collect errors per item, continue, report summary, non-zero exit if any failed, retry failed subset.", "Robustness.", "Tagging 500 resources."),
("Advanced", "What is a generator and why use it?", "Lazy iterator using `yield`; processes large data without loading it all.", "Memory.", "Stream a big log file."),
("Advanced", "Explain reconciliation loop in operators.", "Observe current state, compare to desired, act to converge, repeat on events.", "Kubernetes pattern.", "Scale replicas to spec."),
("Advanced", "How to schedule Python automation in AWS?", "EventBridge rule triggering Lambda (or ECS task/Step Functions), IAM role, CloudWatch logs.", "Serverless ops.", "Nightly stop dev instances."),
("Scenario-Based", "Write logic to list all EC2 instances across regions.", "Get regions via `ec2.describe_regions()`, loop with a client per region, paginate, aggregate; use threads.", "Multi-region.", "Inventory report."),
("Scenario-Based", "Your script deleted the wrong resources.", "Add dry-run, tag-based allowlist, confirmation, snapshots/backups, peer review, restrict IAM, audit logs.", "Safety design.", "Name-match delete gone wrong."),
("Scenario-Based", "Script is too slow across 1000 resources.", "Filter server-side, paginate with larger pages, concurrency, caching, avoid N+1 calls.", "Performance.", "Batch describe calls."),
("Scenario-Based", "Need daily compliance report for untagged resources.", "Use Resource Groups Tagging API/AWS Config, generate CSV, email/Slack, schedule with Lambda.", "Governance.", "Cost allocation tags."),
("Scenario-Based", "Automate onboarding of a new developer (IAM user/group, repo access).", "Idempotent script/Terraform, least privilege group membership, audit, offboarding path.", "Automation.", "SSO where possible."),
("Troubleshooting-Based", "`ClientError: Throttling`.", "Too many API calls; add backoff/retries, reduce calls, spread over time.", "Rate limits.", "Config(retries={'max_attempts': 10, 'mode': 'adaptive'})."),
("Troubleshooting-Based", "Script hangs forever.", "Missing timeout on network call; add `timeout=`; inspect with `py-spy`/logging.", "Reliability.", "requests without timeout."),
("Troubleshooting-Based", "Works on my machine but not in CI.", "Python/dependency versions or env differences; pin and use same container image.", "Reproducibility.", "requirements without versions."),
("Troubleshooting-Based", "`UnicodeDecodeError` reading file.", "Wrong encoding: open with `encoding='utf-8'` or handle errors.", "Files.", "Windows default codepage."),
("Troubleshooting-Based", "`InvalidClientTokenId`/expired token.", "Expired temporary credentials or wrong profile/region; refresh SSO/role.", "AWS auth.", "`aws sso login`.")],
cheatsheet={
"Definitions": ["venv=isolated env; idempotent=safe to repeat; paginator=iterate all pages; dry-run=preview changes."],
"Commands": ["`python -m venv .venv` `pip install -r requirements.txt` `pip freeze > requirements.txt`", "`python script.py --help` `pytest -q` `python -m json.tool`", "`aws sts get-caller-identity` `aws configure sso` `go build` `go run .` `go mod tidy`"],
"Files": ["requirements.txt/pyproject.toml, .env (not in Git), main.py, tests/, go.mod, Makefile"],
"Architecture": ["Trigger > script (venv) > config/secrets > API calls (boto3) > action > logs/exit code."],
"Ports": ["HTTPS APIs 443; Slack webhook 443; Prometheus exporter often 8000/9100"],
"Differences": ["Python vs Bash vs Go; client vs resource; list/tuple/dict/set; thread vs process vs async."],
"Troubleshooting commands": ["`which python` > `pip list` > `aws sts get-caller-identity` > enable DEBUG logging > CloudTrail for AccessDenied"],
"Best practices": ["venv, pinned deps, argparse, logging, timeouts, retries, dry-run, IAM roles, tests, idempotency."]}
),
subs={
"python-basics": dict(
define=dict(simple="Python is an easy programming language used to automate tasks.",
technical="Python is a dynamically typed, interpreted language with rich standard library (os, subprocess, json, logging, pathlib) and a large package ecosystem via PyPI.",
why="Readable automation with strong libraries.", without="Fragile shell scripts for complex logic.", use="Automation, tooling, glue code.", avoid="Very performance-critical tools (consider Go).", analogy="A Swiss army knife for operations."),
internals="""Python compiles source to bytecode and runs it in the interpreter. `import` finds modules on `sys.path` (including the active venv's site-packages). `subprocess.run` starts a child process; exceptions propagate up the call stack until caught.""",
config=[("Small utility script explained", """import json, logging, subprocess, sys

logging.basicConfig(level=logging.INFO)

def disk_usage_percent(path="/"):
    out = subprocess.run(["df", path, "--output=pcent"], capture_output=True, text=True, check=True).stdout
    return int(out.splitlines()[1].strip().rstrip("%"))

if __name__ == "__main__":
    pct = disk_usage_percent()
    logging.info("disk usage %s%%", pct)
    sys.exit(1 if pct > 80 else 0)""", [("subprocess.run([...], check=True)", "List form avoids shell injection; `check=True` raises on failure."), ("capture_output/text", "Captures stdout as a string."), ("logging", "Structured levels instead of print."), ("sys.exit(1 if pct > 80 else 0)", "Exit code lets cron/CI detect a problem.")])],
lab=dict(goal="Create a venv and run a JSON-processing script.", prereq=["Python 3"],
steps=[("python3 -m venv .venv && source .venv/bin/activate && python -V", "Creates and activates an isolated environment (Windows: `.venv\\Scripts\\activate`)."),
("pip install requests && python -c \"import requests;print(requests.get('https://api.github.com', timeout=10).status_code)\"", "Installs a package and calls an API: prints 200."),
("echo '{\"a\":[1,2]}' | python -m json.tool", "Pretty-prints JSON.")]),
mnemonics=[("Basics", "Types, Control flow, Functions, Files, Errors")], hinglish="Python mein **venv** zaroor use karo aur **check=True** ke saath subprocess chalao taaki failure chhupe nahi.",
practices={"Development": ["Type hints, small functions, pytest, ruff/black."]}, mistakes={"Developer mistakes": ["Bare except.", "shell=True with user input."]},
qa_extra=[("Intermediate", "Why avoid `shell=True`?", "It passes the string through a shell, enabling command injection and quoting bugs; pass a list instead.", "Security.", "User-supplied filenames.")]),

"boto3-aws-automation": dict(
define=dict(simple="boto3 lets Python control AWS: create, list, stop, delete resources.",
technical="boto3 is the AWS SDK: it signs API requests (SigV4) using credentials from the default provider chain (env, profile/SSO, container/instance role) and returns Python dicts.",
why="Automate cloud operations.", without="Console clicks.", use="Inventory, cleanup, tagging, backups.", avoid="Long-lived access keys.", analogy="A remote control for the whole AWS console."),
internals="""`boto3.client('ec2')` loads the service model, resolves credentials through the provider chain, signs each HTTPS request with SigV4 and parses the JSON/XML response. Paginators call the API repeatedly with the continuation token. Retries with backoff handle throttling.""",
config=[("boto3 snippet explained", """import boto3
from botocore.config import Config

cfg = Config(retries={"max_attempts": 10, "mode": "standard"})
s3 = boto3.client("s3", config=cfg)
for page in s3.get_paginator("list_objects_v2").paginate(Bucket="my-bucket"):
    for obj in page.get("Contents", []):
        print(obj["Key"])""", [("Config(retries=...)", "Automatic retries with backoff for throttling."), ("get_paginator", "Iterates all pages instead of only the first 1000 keys."), ("page.get('Contents', [])", "Empty buckets have no Contents key.")])],
lab=dict(goal="List and tag resources safely.", prereq=["AWS account", "aws cli configured (`aws sts get-caller-identity` works)", "pip install boto3"],
steps=[("python -c \"import boto3;print([b['Name'] for b in boto3.client('s3').list_buckets()['Buckets']])\"", "Lists buckets using default credentials."),
("python -c \"import boto3;e=boto3.client('ec2');print(e.describe_regions()['Regions'][0]['RegionName'])\"", "Region call."),
("Write the stopper.py from the mini project and run it without --apply", "Dry-run output lists instances that would be stopped.")]),
mnemonics=[("Credential chain", "Env > Profile/SSO > Role")], hinglish="boto3 mein **credentials role/SSO se** lo, code mein keys mat likho, aur list calls par **paginator** lagao.",
practices={"Security": ["Least-privilege IAM roles; short-lived credentials."], "Reliability": ["Retries, pagination, dry-run."]}, mistakes={"Developer mistakes": ["Ignoring pagination.", "Hard-coded region and keys."]},
versions=["Use `boto3.client`; `resource` is not receiving new features. Check botocore docs for API names; regions/services vary by account."],
qa_extra=[("Scenario-Based", "How to safely run destructive AWS scripts?", "Dry-run default, allow-list by tag, small IAM role, snapshots, confirmation, logs and peer review.", "Blast radius control.", "Only env=dev tagged resources.")]),

"apis-cli-tools": dict(
define=dict(simple="Use Python to call web APIs and build small command-line tools and monitoring checks.",
technical="REST APIs use HTTP verbs and JSON; `requests` provides sessions, timeouts and retries; `argparse/click` create CLIs; health-check scripts return exit codes for schedulers and monitoring.",
why="Integrate tools (Slack, GitHub, monitoring) and automate checks.", without="Manual copy-paste between systems.", use="ChatOps, notifications, inventory, health checks.", avoid="Polling too frequently without limits.", analogy="A messenger carrying data between systems."),
internals="""`requests.get(url, timeout=5)` opens a TCP/TLS connection, sends HTTP, returns a Response with status and body. `raise_for_status()` turns 4xx/5xx into exceptions. A Session reuses connections. CLI parsing converts arguments to a namespace and dispatches to functions.""",
config=[("Health check tool explained", """import argparse, sys, requests

def check(url, expect=200):
    r = requests.get(url, timeout=5)
    return r.status_code == expect, r.elapsed.total_seconds()

if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("url"); a = p.parse_args()
    ok, secs = check(a.url)
    print(f"{'OK' if ok else 'FAIL'} {a.url} {secs:.3f}s")
    sys.exit(0 if ok else 1)""", [("timeout=5", "Never wait forever."), ("elapsed", "Response time for latency checks."), ("sys.exit(0/1)", "Nagios-style exit code; cron/CI can alert.")])],
lab=dict(goal="Build a mini health-check CLI.", prereq=["Python, pip install requests"],
steps=[("Save the code above as check.py", "Simple tool."), ("python check.py https://example.com; echo $?", "Prints OK and exit code 0."), ("python check.py https://example.com/404; echo $?", "Prints FAIL and exit code 1.")]),
mnemonics=[("API call", "URL, Verb, Headers, Body, Timeout, Status")], hinglish="Har API call mein **timeout** lagao aur **status code check** karo. Tool ka **exit code** monitoring ke kaam aata hai.",
practices={"Reliability": ["Timeouts, retries with backoff, rate-limit respect."], "Security": ["Tokens from env/secret manager; never log them."]}, mistakes={"Production mistakes": ["No timeout.", "Ignoring non-200 responses."]},
qa_extra=[("Intermediate", "How do you handle API pagination and rate limits?", "Follow `next` links/cursors, respect `Retry-After` and 429, use backoff.", "API integration.", "GitHub API listing repos.")]),

"go-and-operators": dict(
define=dict(simple="Go is a fast compiled language used for DevOps tools; operators are programs that manage apps inside Kubernetes.",
technical="Go compiles to a static binary with built-in concurrency (goroutines, channels). Kubernetes controllers use client-go/controller-runtime to watch resources and reconcile actual to desired state via Custom Resource Definitions.",
why="Portable tools and native Kubernetes extension.", without="Manual operational runbooks for complex apps.", use="CLIs, exporters, operators, high-performance services.", avoid="Quick one-off scripts (use Python/Bash).", analogy="An operator is an automated site-reliability engineer living inside the cluster."),
internals="""An operator registers a CRD (for example `Database`). The controller watches those objects through the API server (informers/caches), and on each event runs `Reconcile()`: read desired spec, inspect actual resources (Deployments, PVCs), create/update/delete to match, update `status`, and requeue if needed. Reconcile must be idempotent.""",
config=[("Minimal Go CLI explained", """package main

import (
    "fmt"
    "net/http"
    "os"
    "time"
)

func main() {
    c := http.Client{Timeout: 5 * time.Second}
    resp, err := c.Get(os.Args[1])
    if err != nil {
        fmt.Println("FAIL:", err)
        os.Exit(1)
    }
    defer resp.Body.Close()
    fmt.Println("status:", resp.StatusCode)
}""", [("http.Client{Timeout}", "Always set a timeout."), ("err != nil", "Go returns errors explicitly; handle them."), ("defer resp.Body.Close()", "Guarantees cleanup."), ("os.Exit(1)", "Non-zero exit for automation.")])],
lab=dict(goal="Build and run a Go binary.", prereq=["Go installed (`go version`)"],
steps=[("mkdir hc && cd hc && go mod init example.com/hc", "Creates a module."), ("Save the code as main.go, then: go build -o hc && ./hc https://example.com", "Produces a single static binary and prints status: 200."), ("GOOS=linux GOARCH=arm64 go build -o hc-arm64", "Cross-compile for another platform: a big Go advantage.")]),
mnemonics=[("Operator loop", "Watch > Compare > Act > Update status")], hinglish="Go ka binary **ek file** hota hai aur kahin bhi chalta hai. **Operator** cluster ke andar chalne wala controller hai jo desired state ko actual state banata rehta hai.",
practices={"Production": ["Idempotent reconcile, leader election, metrics, RBAC least privilege for operator."]}, mistakes={"Developer mistakes": ["Non-idempotent reconcile loops.", "Ignoring errors in Go."]},
versions=["Check the current stable Go version and Kubernetes client-go / controller-runtime version compatibility with your cluster."],
qa_extra=[("Advanced", "Why must Reconcile be idempotent?", "It may run many times for the same object (retries, resyncs); repeated runs must converge without side effects.", "Operator design.", "Create-if-missing, update-if-different.")])
})
