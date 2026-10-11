EXT = dict(
guide=dict(
bigpicture=dict(
problem="""**Problem it solves:** Creating cloud infrastructure by clicking in a console is slow, undocumented and impossible to reproduce exactly. **Terraform** (Infrastructure as Code, IaC) lets you describe infrastructure in files, review it like code, and create, change or destroy it repeatably with one workflow.""",
chain=["PROBLEM: infrastructure must be created and changed consistently",
       "TRADITIONAL APPROACH: console clicking ('click-ops') or ad-hoc scripts",
       "PAIN: drift, no review, no history, can't recreate environments, mistakes in production",
       "TECHNOLOGY: Terraform (declarative HCL, providers, state, plan/apply)",
       "SOLUTION: code in Git > plan (preview) > review > apply",
       "REAL-WORLD BENEFIT: repeatable environments, audit trail, safe changes, disaster recovery"],
text="""Terraform is **declarative**: you state the desired end result and Terraform works out the steps. It keeps a **state file** mapping your code to real resources and uses **providers** (plugins) to talk to AWS, Azure, Kubernetes and hundreds of other APIs."""),
e2e=dict(diagram="""Engineer writes main.tf (HCL)
   | git push / PR
   v
CI: terraform fmt + validate + tflint + security scan (tfsec/checkov)
   v
terraform init  (download providers, configure backend)
   v
terraform plan  (compare code vs state vs real world -> preview)
   v
Review / approval (policy checks: OPA/Sentinel)
   v
terraform apply (provider API calls create/update/destroy)
   v
State updated in remote backend (S3 + DynamoDB lock / Terraform Cloud)
   v
Infrastructure ready -> outputs used by CI/CD, Ansible, Kubernetes""",
text="""`init` prepares the working directory: it downloads **providers** and configures the **backend** where state is stored. `plan` reads your code, the **state** and the real infrastructure (refresh) and prints exactly what will be added, changed or destroyed, without doing it. After review, `apply` executes the plan by calling the provider APIs in dependency order (Terraform builds a dependency graph). The **state** is updated; a **lock** prevents two people from applying at once. **Outputs** expose values (like a load balancer DNS) to other tools."""),
tools=dict(rows=[
["Terraform / OpenTofu", "Provision infrastructure", "HCL code + variables", "Real resources + state", "Provisioning"],
["Providers (aws, kubernetes, helm)", "Talk to APIs", "Resource config", "API calls", "Inside Terraform"],
["Remote backend (S3+DynamoDB, TFC)", "Store state and locks", "State", "Shared locked state", "Team usage"],
["Modules", "Reusable building blocks", "Inputs", "Resources + outputs", "Standard patterns"],
["tflint / tfsec / checkov", "Lint and security scan", "Terraform code", "Findings", "CI"],
["Terragrunt / workspaces", "Environment management / DRY", "Config", "Per-env stacks", "Multi-env"],
["Ansible", "Configure servers after creation", "Inventory from outputs", "Configured hosts", "After provisioning"],
["Atlantis / GitHub Actions", "PR-driven plan/apply", "PR", "Plan comments, apply", "Team automation"]],
why="**Terraform vs CloudFormation:** Terraform is multi-cloud with a large provider ecosystem; CloudFormation is AWS-native with deep integration and no state file to manage. **Terraform vs Ansible:** Terraform provisions infrastructure (declarative, stateful); Ansible configures software inside servers (procedural/idempotent, agentless). **Terraform vs OpenTofu:** OpenTofu is a community-driven open-source fork after Terraform's licence change; syntax is largely compatible: check versions."),
compare=[
("Terraform vs CloudFormation vs Pulumi", ["Topic", "Terraform", "CloudFormation", "Pulumi"], [["Language", "HCL", "YAML/JSON", "Python/TS/Go etc."], ["Clouds", "Many", "AWS only", "Many"], ["State", "State file/backend", "Managed by AWS", "Backend/service"]]),
("Terraform vs Ansible", ["Topic", "Terraform", "Ansible"], [["Purpose", "Create infrastructure", "Configure servers/apps"], ["Model", "Declarative + state", "Procedural tasks, idempotent modules"], ["Agent", "None", "Agentless (SSH/WinRM)"]]),
("variable vs local vs output", ["Type", "Purpose"], [["variable", "Input from user/environment"], ["local", "Computed value inside module"], ["output", "Value exposed to caller/CLI"]]),
("count vs for_each", ["Topic", "count", "for_each"], [["Index", "Numeric index", "Map/set key"], ["Removal problem", "Shifts indexes and may recreate resources", "Stable per key"], ["Use", "Simple on/off (0/1)", "Multiple named resources"]]),
("Workspaces vs separate directories", ["Topic", "Workspaces", "Directories/Stacks"], [["State", "Same backend, different state key", "Separate backend/state per env"], ["Isolation", "Weaker", "Stronger (recommended for prod)"]])],
troubleshooting=[
("`Error acquiring the state lock`", "Another apply running or a crashed run left a lock", "Check who holds it (lock info), CI runs", "Wait; if stale, `terraform force-unlock <ID>` after confirming no run is active.", "Run applies only via CI with concurrency limits."),
("Plan wants to destroy/recreate a resource unexpectedly", "Immutable attribute changed, renamed resource, count index shift", "Read `# forces replacement` in the plan", "Use `moved` blocks / `terraform state mv`, avoid changing immutable fields, use `for_each`.", "Always review plan; use `prevent_destroy` for critical resources."),
("Drift: real resources differ from code", "Manual console changes", "`terraform plan` shows changes", "Apply to restore, or import/update code if the change is desired.", "Restrict console write access; scheduled drift detection."),
("`resource already exists`", "Resource created outside Terraform", "Cloud console / CLI", "`terraform import` (or `import` block) then adjust code.", "Create everything through IaC."),
("Provider auth errors", "Missing/expired credentials or wrong region/profile", "`aws sts get-caller-identity`, env vars", "Fix credentials/role; use OIDC in CI.", "No static keys in code."),
("State corrupted/lost", "Local state deleted or backend misconfigured", "Backend config, bucket versioning", "Restore from versioned S3 bucket; re-import if necessary.", "Remote backend with versioning, encryption and locking.")],
practices={
"Development": ["`terraform fmt`, `validate`, small modules, meaningful variable descriptions/types, pin provider and Terraform versions."],
"Production": ["Remote state with locking; separate state per environment/component; plan in PR, apply from CI after approval; modules versioned with tags."],
"Security": ["Never commit `*.tfstate` or secrets; mark variables `sensitive`; encrypt state; least-privilege IAM/OIDC for CI; scan with tfsec/checkov; policy as code."],
"Performance": ["Split large stacks; use `-target` only for emergencies; parallelism tuned; avoid huge monoliths."],
"Reliability": ["`prevent_destroy` on data stores; backups of state; `create_before_destroy` for zero-downtime replacement."],
"Cost Optimization": ["Tagging via `default_tags`; scheduled dev environments; cost estimation (Infracost) in PRs."],
"Monitoring & Logging": ["Log plan/apply output in CI; alert on drift."],
"Backup & Disaster Recovery": ["Versioned state bucket with replication; IaC allows rebuilding an environment in a new region."]},
mistakes={
"Beginner mistakes": ["Editing infrastructure manually after Terraform created it.", "Using `apply -auto-approve` locally without reading the plan."],
"Developer mistakes": ["Hard-coded values instead of variables.", "Copy-pasting instead of modules."],
"DevOps mistakes": ["One giant state file for everything.", "No provider version pinning.", "Local state in a team."],
"Production mistakes": ["Applying without review.", "No `prevent_destroy` on databases."],
"Security mistakes": ["Secrets or state in Git.", "Over-privileged CI credentials."]},
versions=[
"Terraform 1.x is stable; features like `moved`, `import` blocks, `check` blocks need recent 1.x versions. Pin with `required_version`.",
"Licence change in 2023 (BSL) led to OpenTofu, a compatible open-source fork: verify compatibility for your version and providers.",
"Provider versions change resource arguments (e.g. AWS provider v4/v5 split S3 bucket settings into separate resources): pin `~>` versions and read upgrade guides.",
"`terraform workspace` semantic differs in Terraform Cloud vs CLI workspaces."],
hinglish="""Terraform mein tum **HCL code** likhte ho jo batata hai infrastructure **kaisa hona chahiye**. **`plan`** preview dikhata hai, **`apply`** actual changes karta hai. **State file** yaad rakhti hai ki kaunsa code kaunse real resource se juda hai, isliye use **remote backend (S3 + lock)** mein rakho aur Git mein commit **mat** karo. Console se manual change karoge to **drift** hoga. Reusable code ke liye **modules** banao.""",
mnemonics=[("Workflow", "I-P-A-D: Init, Plan, Apply, Destroy"), ("Files", "main.tf, variables.tf, outputs.tf, providers.tf, versions.tf"), ("State rule", "Remote, locked, versioned, encrypted, never in Git"), ("Golden rule", "Read the plan before every apply")],
client=dict(
s30="""Terraform lets us define your cloud infrastructure as code. That means environments can be created, reviewed, changed and rebuilt in a repeatable, auditable way instead of by manual clicking.""",
m2="""Instead of building servers and networks by hand, we write them as code and store it in Git. Every change goes through a pull request; a plan shows exactly what will change before anything is applied. This removes configuration drift between environments, gives a full audit trail, and lets us recreate the whole platform quickly for testing or disaster recovery. We keep the state securely in a shared, locked location and scan the code for security problems before deployment. You get faster, safer changes and consistent environments.""",
m5="""Consider four points. **Model:** Terraform is declarative: we describe the desired infrastructure (VPC, Kubernetes cluster, database), and Terraform computes the changes using providers for each cloud service. **Workflow:** code in Git, automated format/validate/security checks, `plan` in the pull request for review, then `apply` from the pipeline after approval, using short-lived credentials. **State and structure:** remote encrypted state with locking, separate stacks per environment, and versioned reusable modules so teams follow the same secure patterns. **Governance:** policy as code to block risky configurations, cost estimates in PRs, drift detection, and `prevent_destroy` on critical data stores. Together this reduces risk, speeds delivery and provides compliance evidence."""),
roadmap=[
("Beginner", ["IaC concept", "Providers and resources", "Variables/outputs", "init/plan/apply/destroy"]),
("Intermediate", ["State and remote backend", "Data sources", "count/for_each", "Modules", "Workspaces vs directories"]),
("Advanced", ["Import and refactor (moved)", "Provisioners vs config mgmt", "Policy as code, testing (terraform test/terratest)", "Multi-account/region patterns"]),
("Production", ["CI/CD for Terraform (Atlantis/Actions)", "Secrets handling", "Drift detection", "Cost control"]),
("Interview", ["Explain state and locking", "Modules design", "Terraform vs Ansible/CloudFormation", "Handle drift/imports"])],
miniproject=dict(title="VPC + EC2 with remote state and a reusable module",
arch="""Git repo
  envs/dev/main.tf --> module "network" (VPC, subnets) --> module "web" (EC2 + SG)
  backend: S3 bucket (versioned, encrypted) + DynamoDB lock table
CI: fmt, validate, tflint, checkov > plan (PR comment) > apply (approved)""",
steps=[
("Step 1: Provider and backend", """terraform {
  required_version = ">= 1.6"
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
  }
  backend "s3" {
    bucket         = "my-tf-state-123456"
    key            = "dev/network/terraform.tfstate"
    region         = "ap-south-1"
    dynamodb_table = "tf-locks"
    encrypt        = true
  }
}
provider "aws" {
  region = var.region
  default_tags { tags = { Env = "dev", ManagedBy = "terraform" } }
}""", "`required_version`/`version` pin tool versions. The S3 backend stores state remotely; `dynamodb_table` provides locking (newer Terraform releases also support S3-native locking: check the docs for your version). `default_tags` tags every resource for cost tracking. The bucket and table must exist before `init`."),
("Step 2: Variables and outputs", """variable "region"   { type = string  default = "ap-south-1" }
variable "vpc_cidr" { type = string  default = "10.0.0.0/16" }
variable "db_password" { type = string  sensitive = true }

output "vpc_id" { value = aws_vpc.main.id }""", "Typed variables document inputs; `sensitive` hides values in output; outputs feed other stacks or CI."),
("Step 3: Resources", """resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  tags = { Name = "dev-vpc" }
}

resource "aws_subnet" "public" {
  for_each          = { a = "10.0.0.0/24", b = "10.0.1.0/24" }
  vpc_id            = aws_vpc.main.id
  cidr_block        = each.value
  availability_zone = "${var.region}${each.key}"
  tags = { Name = "public-${each.key}" }
}""", "Referencing `aws_vpc.main.id` creates an implicit dependency, so Terraform creates the VPC first. `for_each` creates one subnet per map key with stable addresses (adding/removing a key does not shift others)."),
("Step 4: Run the workflow", """terraform fmt -check && terraform init
terraform validate
terraform plan -out tfplan
terraform apply tfplan
terraform output
terraform destroy   # when finished, to avoid cost""", "`plan -out` then `apply tfplan` guarantees you apply exactly what was reviewed. Always destroy lab resources.")]),
interview=[
("Beginner", "What is Terraform?", "An IaC tool using declarative HCL to provision and manage infrastructure across providers.", "Foundation.", "Create a VPC with code."),
("Beginner", "What is IaC?", "Managing infrastructure through versioned code rather than manual processes.", "Concept.", "Same code for dev and prod."),
("Beginner", "Explain init, plan, apply, destroy.", "init downloads providers/backends; plan previews; apply executes; destroy removes resources.", "Workflow.", "Plan before apply."),
("Beginner", "What is a provider?", "A plugin that translates Terraform resources into API calls for a platform.", "Architecture.", "aws, azurerm, kubernetes."),
("Beginner", "What is the state file?", "JSON mapping Terraform resources to real objects and metadata.", "Core concept.", "terraform.tfstate."),
("Beginner", "What is a resource vs data source?", "Resource creates/manages something; data source reads existing information.", "Syntax.", "`data aws_ami`."),
("Beginner", "What are variables and outputs?", "Inputs and exposed values of a configuration/module.", "Reusability.", "Output ALB DNS."),
("Beginner", "What is `terraform fmt` and `validate`?", "fmt formats code; validate checks syntax and consistency.", "Quality.", "Run in CI."),
("Beginner", "What does `terraform destroy` do?", "Destroys all managed resources in the configuration.", "Cleanup.", "Tear down lab."),
("Beginner", "What language does Terraform use?", "HCL (HashiCorp Configuration Language).", "Basics.", "`resource \"aws_instance\" \"web\" {}`."),
("Intermediate", "Why remote state and locking?", "Share state across a team safely and prevent concurrent applies that corrupt it.", "Team workflow.", "S3 + DynamoDB."),
("Intermediate", "What are modules?", "Reusable packages of Terraform config with inputs and outputs.", "DRY.", "vpc module reused for each env."),
("Intermediate", "count vs for_each?", "count uses numeric index (removal shifts indexes); for_each uses keys for stable addressing.", "Common pitfall.", "for_each for subnets."),
("Intermediate", "Explain implicit vs explicit dependencies.", "References create implicit dependencies; `depends_on` declares explicit ones.", "Ordering.", "SG before instance."),
("Intermediate", "What is `terraform import`?", "Bring an existing resource under Terraform management by adding it to state (code must exist).", "Adoption.", "Import a console-made bucket."),
("Intermediate", "What are lifecycle rules?", "`create_before_destroy`, `prevent_destroy`, `ignore_changes`, `replace_triggered_by`.", "Safety controls.", "prevent_destroy on RDS."),
("Intermediate", "Workspaces vs separate dirs?", "Workspaces share config with separate state; directories/stacks isolate environments more strongly.", "Env strategy.", "Prod in own state and account."),
("Intermediate", "How to handle secrets?", "Do not hardcode; use variables marked sensitive from a secret store/CI, reference Secrets Manager/Vault data sources; remember values may still land in state.", "Security.", "Encrypt state."),
("Intermediate", "What is a data source used for?", "Read info such as latest AMI, existing VPC, caller identity.", "Composition.", "`aws_caller_identity`."),
("Intermediate", "What are provisioners and why avoid them?", "local-exec/remote-exec run scripts at create time; last resort as they are not declarative; prefer cloud-init/Ansible/images.", "Best practice.", "user_data instead."),
("Intermediate", "How do you pin versions?", "`required_version`, `required_providers` with `~>`, lock file `.terraform.lock.hcl` committed.", "Reproducibility.", "Avoid surprise upgrades."),
("Intermediate", "What is `terraform taint`/`-replace`?", "Force recreation of a resource; use `terraform apply -replace=addr` (taint is deprecated).", "Modern syntax.", "Rebuild a bad instance."),
("Intermediate", "How to structure a Terraform repo?", "Modules directory, envs directories, per-component states, README, CI checks.", "Organisation.", "modules/, envs/dev/."),
("Advanced", "How does Terraform build the execution plan?", "Loads config and state, refreshes real state, builds a dependency graph, diffs desired vs current, outputs actions, executes in parallel where independent.", "Internals.", "Graph via `terraform graph`."),
("Advanced", "How do you refactor without recreating resources?", "`moved` blocks or `terraform state mv`; import blocks; careful plan review.", "Maintenance.", "Rename resource to module."),
("Advanced", "How to detect and handle drift?", "Scheduled `plan -detailed-exitcode`, refresh, alerts; reconcile by applying or updating code; restrict console access.", "Ops.", "Nightly drift job."),
("Advanced", "Design multi-account, multi-region Terraform.", "Separate state and provider aliases per account/region, assume-role/OIDC, modules, layered stacks (network, platform, apps).", "Enterprise design.", "Provider alias `aws.dr`."),
("Advanced", "Secure the CI pipeline for Terraform.", "OIDC federation, least-privilege role per environment, plan in PR with read-only role, apply with approval, policy checks, no secrets in logs.", "Security.", "GitHub Actions to AWS."),
("Advanced", "Policy as code options?", "Sentinel (Terraform Cloud), OPA/Conftest, Checkov/tfsec rules.", "Governance.", "Deny public S3."),
("Advanced", "How do you test Terraform?", "validate, tflint, `terraform test`, Terratest, ephemeral environments, plan assertions.", "Quality.", "Terratest for modules."),
("Advanced", "State locking internals with S3/DynamoDB?", "Terraform writes a lock item with ID/who/operation; concurrent runs fail until released; newer versions offer native S3 lock files.", "State handling.", "force-unlock caution."),
("Advanced", "Explain `sensitive` values and state.", "Sensitive hides values in CLI output but they are stored in state in plain text; protect the state.", "Security nuance.", "DB passwords."),
("Advanced", "Terraform vs Kubernetes operators for infrastructure?", "Crossplane/operators provide continuous reconciliation in cluster; Terraform is run-based with explicit plan/apply.", "Design choices.", "Crossplane for self-service infra."),
("Advanced", "How to manage large blast radius?", "Split state by lifecycle and ownership, use targeted plans carefully, approvals, `prevent_destroy`.", "Risk control.", "Separate network and app states."),
("Scenario-Based", "Two engineers ran apply at the same time.", "Locking should prevent this; without locking state may corrupt. Enforce remote backend with lock and apply through CI only.", "Team safety.", "Backend misconfigured."),
("Scenario-Based", "Plan shows database will be destroyed.", "Stop, inspect why (`forces replacement`), avoid apply, adjust code or use lifecycle, take a snapshot first.", "Risk handling.", "Changed identifier."),
("Scenario-Based", "Infrastructure was changed in the console.", "Run plan to see drift, decide to revert (apply) or codify, then lock down access.", "Governance.", "SG rule added manually."),
("Scenario-Based", "Onboard existing infrastructure to Terraform.", "Inventory, write code, `import` blocks, plan until no diff, gradually adopt with modules.", "Migration.", "Legacy VPC."),
("Scenario-Based", "State file leaked.", "Treat all secrets in state as compromised: rotate, restrict access, encrypt bucket, audit access.", "Incident response.", "Public bucket."),
("Scenario-Based", "Need dev/stage/prod with minimal duplication.", "Reusable modules + per-environment root modules/tfvars, separate state and accounts.", "Structure.", "envs/prod/main.tf calls module."),
("Scenario-Based", "Terraform is slow with 2000 resources.", "Split stacks, increase parallelism carefully, reduce refresh with targeted plans in emergencies, use data sources sparingly.", "Scale.", "Network vs app split."),
("Scenario-Based", "Upgrade a provider major version safely.", "Read upgrade guide, test in dev with plan, fix deprecated args, roll out gradually.", "Change management.", "AWS provider v4 to v5."),
("Scenario-Based", "How do you deploy to multiple regions?", "Provider aliases or per-region stacks, shared modules, region variable.", "Multi-region.", "DR region."),
("Scenario-Based", "Prevent public S3 buckets by policy.", "Block Public Access resource, checkov/OPA rule in CI, SCP.", "Preventive control.", "Fail PR on violation."),
("Troubleshooting-Based", "`Error: No valid credential sources found`.", "Provider cannot find credentials; set env/profile/OIDC role.", "Auth.", "CI missing role."),
("Troubleshooting-Based", "`Provider produced inconsistent result after apply`.", "Provider bug or eventual consistency; re-run apply, upgrade provider, check known issues.", "Provider issues.", "Tags propagation."),
("Troubleshooting-Based", "`Error: Cycle`.", "Circular dependency between resources; break with separate resources or data references.", "Graph.", "SG rules referencing each other: use aws_security_group_rule."),
("Troubleshooting-Based", "`Inconsistent lock file`.", "Provider versions changed; run `terraform init -upgrade` and commit the lock file.", "Version control.", "After bumping version."),
("Troubleshooting-Based", "Apply stuck creating a resource.", "Waiting on API/dependencies/quotas; check cloud console, timeouts, quotas.", "Ops.", "NAT gateway or EKS creation is slow."),
("Troubleshooting-Based", "`Error: Invalid for_each argument`.", "Keys must be known at plan time; use static keys or apply in stages.", "Language limit.", "Keys from resource attributes."),
("Troubleshooting-Based", "Plan differs every time (perpetual diff).", "Provider normalises values (case/order/JSON); use `jsonencode`, `ignore_changes` where justified.", "Idempotency.", "IAM policy JSON."),
("Troubleshooting-Based", "`AccessDenied` during apply.", "CI role lacks the action; use CloudTrail to find the denied API call and add least privilege.", "IAM.", "Missing iam:PassRole."),
("Troubleshooting-Based", "Backend init fails.", "Bucket/table missing, region or permissions wrong; create backend or fix credentials.", "Backend.", "State bucket in another region."),
("Troubleshooting-Based", "Destroy fails with dependency error.", "Non-managed dependents (ENIs, objects in bucket); remove them or use force_destroy where appropriate.", "Cleanup.", "S3 bucket not empty.")],
cheatsheet={
"Definitions": ["Provider, resource, data source, variable, local, output, module, state, backend, plan, apply, drift, import."],
"Commands": ["`terraform init [-upgrade]` `fmt` `validate` `plan -out tfplan` `apply tfplan` `destroy`", "`terraform state list|show|mv|rm` `terraform import addr id` `terraform output` `terraform graph`", "`terraform apply -replace=addr` `terraform workspace new|select` `terraform force-unlock ID`"],
"Files": ["main.tf variables.tf outputs.tf providers.tf versions.tf terraform.tfvars .terraform.lock.hcl (commit) terraform.tfstate (never commit) .terraform/ (ignore)"],
"Architecture": ["Code > init > plan > apply > provider API > cloud; state in remote backend with lock."],
"Ports": ["N/A (calls HTTPS 443 APIs); backend S3/DynamoDB over 443"],
"Differences": ["Terraform vs Ansible vs CloudFormation; count vs for_each; workspace vs directory; variable vs local vs output."],
"Troubleshooting commands": ["`terraform validate` > `plan` > `state list` > `TF_LOG=DEBUG terraform plan` > cloud CloudTrail"],
"Best practices": ["Remote locked state, pin versions, modules, plan in PR, apply via CI, policy scans, prevent_destroy, no secrets/state in Git."]}
),
subs={
"terraform-basics": dict(
define=dict(simple="Write what you want in a file; Terraform builds it.",
technical="Terraform parses HCL, builds a resource graph, compares to state, and calls provider APIs to converge infrastructure to the declared configuration.",
why="Repeatable, reviewable infrastructure.", without="Manual console work and drift.", use="Any cloud/infra provisioning.", avoid="Configuring software inside servers (use Ansible/images).", analogy="A blueprint; Terraform is the builder that also remembers what it built."),
internals="""`terraform plan` refreshes state from the provider, compares desired configuration and produces an ordered action list. `apply` executes it using the dependency graph, running independent resources in parallel (default 10) and writing results to state after each change.""",
config=[("Minimal EC2 example explained", """terraform {
  required_providers { aws = { source = "hashicorp/aws", version = "~> 5.0" } }
}
provider "aws" { region = "ap-south-1" }

data "aws_ami" "al2023" {
  most_recent = true
  owners      = ["amazon"]
  filter { name = "name", values = ["al2023-ami-*-x86_64"] }
}

resource "aws_instance" "web" {
  ami           = data.aws_ami.al2023.id
  instance_type = "t3.micro"
  tags          = { Name = "demo-web" }
}
output "public_ip" { value = aws_instance.web.public_ip }""", [("required_providers", "Pins the provider source and version."), ("data aws_ami", "Reads the latest Amazon Linux image instead of hard-coding an ID."), ("resource aws_instance.web", "Creates a VM; `web` is the local name."), ("ami = data...id", "Reference = automatic dependency."), ("output", "Prints the IP after apply.")])],
lab=dict(goal="Create and destroy an EC2 instance.", prereq=["AWS credentials", "Terraform installed", "Budget alert"],
steps=[("terraform init", "Downloads the AWS provider into `.terraform/`."), ("terraform plan", "Shows `Plan: 1 to add`."), ("terraform apply", "Type yes; instance is created; state written to terraform.tfstate."), ("terraform destroy", "Removes it. Always clean up.")]),
mnemonics=[("Flow", "Init > Plan > Apply > Destroy")], hinglish="**Plan hamesha padho, phir apply karo.** State file Git mein mat daalo.",
practices={"Development": ["fmt/validate, pinned versions."]}, mistakes={"Beginner mistakes": ["Apply without reading the plan."]},
qa_extra=[("Intermediate", "What does `terraform plan -out` give?", "A saved plan that `apply` executes exactly, ensuring reviewed changes are the applied changes.", "Safety.", "CI plan artifact.")]),

"terraform-state-modules": dict(
define=dict(simple="State remembers what Terraform created; modules let you reuse code.",
technical="State maps resource addresses to real IDs and attributes; backends store and lock it. Modules encapsulate resources behind input variables and outputs and can be versioned.",
why="Team collaboration and DRY code.", without="Conflicts and copy-paste.", use="Any team project.", avoid="Over-abstracted modules.", analogy="State = the builder's notebook; modules = prefab building parts."),
internals="""With an S3 backend, `init` configures the backend; each operation takes a DynamoDB lock item, reads state, works, writes new state and releases the lock. A module call creates a child scope: inputs become variables, outputs return values, and resources are addressed as `module.name.resource`.""",
config=[("Module usage explained", """module "network" {
  source   = "git::https://github.com/acme/tf-modules.git//vpc?ref=v1.4.0"
  cidr     = "10.0.0.0/16"
  azs      = ["ap-south-1a", "ap-south-1b"]
}
output "vpc_id" { value = module.network.vpc_id }""", [("source ...?ref=v1.4.0", "Pin module version by Git tag."), ("inputs", "Variables the module exposes."), ("module.network.vpc_id", "Read a module output.")])],
lab=dict(goal="Configure remote state.", prereq=["AWS credentials"],
steps=[("aws s3 mb s3://my-tf-state-<unique> && aws s3api put-bucket-versioning --bucket my-tf-state-<unique> --versioning-configuration Status=Enabled", "Versioned state bucket."), ("aws dynamodb create-table --table-name tf-locks --attribute-definitions AttributeName=LockID,AttributeType=S --key-schema AttributeName=LockID,KeyType=HASH --billing-mode PAY_PER_REQUEST", "Lock table."), ("Add the backend block and run terraform init -migrate-state", "Moves local state to S3.")]),
mnemonics=[("State", "Remote, Locked, Versioned, Encrypted")], hinglish="**State ko remote backend mein rakho** (S3 + lock). Modules ko **version pin** karo taaki achanak change na aaye.",
practices={"Security": ["Encrypt and restrict state bucket; no secrets in outputs."]}, mistakes={"DevOps mistakes": ["Local state for teams."]},
qa_extra=[("Scenario-Based", "State bucket deleted accidentally.", "Restore from bucket versioning/backup; protect with deletion policy and MFA delete; re-import if lost.", "DR for state.", "Enable versioning up front.")]),

"terraform-real-infra": dict(
define=dict(simple="Use Terraform to build a realistic stack: network, Kubernetes cluster and database.",
technical="Layered stacks (network > platform (EKS) > data (RDS)) exchange values through outputs/remote state or data sources; community modules (terraform-aws-modules) provide well-tested building blocks.",
why="Real environments are composed of several dependent parts.", without="One unmanageable file.", use="Production platforms.", avoid="Coupling everything in one state.", analogy="Building a house in stages: foundation, structure, interior."),
internals="""Stack 1 creates the VPC and outputs subnet IDs. Stack 2 (EKS) reads them via `terraform_remote_state` or SSM/data sources, creates the cluster with IAM/OIDC. Stack 3 creates RDS in database subnets, with a security group allowing only the node/app SG. Each has its own state and plan.""",
config=[("Composition example explained", """module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"
  name = "prod"
  cidr = "10.0.0.0/16"
  azs             = ["ap-south-1a", "ap-south-1b"]
  private_subnets = ["10.0.10.0/24", "10.0.11.0/24"]
  public_subnets  = ["10.0.0.0/24", "10.0.1.0/24"]
  enable_nat_gateway = true
}
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 20.0"
  cluster_name    = "prod"
  vpc_id          = module.vpc.vpc_id
  subnet_ids      = module.vpc.private_subnets
}""", [("terraform-aws-modules", "Widely used community modules: pin versions and read their upgrade notes."), ("module.vpc.private_subnets", "Passing outputs between modules."), ("subnet_ids", "Cluster nodes live in private subnets.")])],
lab=dict(goal="Plan (not apply) a VPC + EKS + RDS composition.", prereq=["Terraform", "AWS credentials"],
steps=[("Write the modules above plus an aws_db_instance in database subnets", "Complete stack."), ("terraform init && terraform plan", "Review the resources to be created and estimated complexity; EKS and NAT cost real money."), ("Only apply in a sandbox account, then terraform destroy", "Avoid surprise bills.")]),
mnemonics=[("Layers", "Network > Platform > Data > Apps")], hinglish="Bade project mein **network, cluster, database ko alag stacks** mein rakho, taaki galti ka **blast radius** chhota rahe.",
practices={"Production": ["Separate state per layer; prevent_destroy on data; pinned module versions."], "Cost Optimization": ["Sandbox destroy schedule; single NAT for dev."]}, mistakes={"Production mistakes": ["Everything in one state."]},
versions=["terraform-aws-modules major versions change inputs; always check the module's upgrade guide."],
qa_extra=[("Advanced", "How do stacks share values?", "Outputs via `terraform_remote_state`, SSM Parameter Store/Secrets Manager, or data sources; prefer data sources to avoid tight state coupling.", "Design.", "Read VPC by tag.")]),

"terraform-ci-policy": dict(
define=dict(simple="Run Terraform automatically in pipelines with safety checks.",
technical="CI runs fmt/validate/lint/scan on PRs, posts the plan for review, then applies on merge using short-lived OIDC credentials and policy checks (OPA/Sentinel/checkov).",
why="Consistent, reviewed, audited changes.", without="Laptop applies with broad credentials.", use="Team infrastructure.", avoid="Auto-apply to production without approval.", analogy="A quality-control line before shipping."),
internals="""PR opened > CI runs checks > `plan` with read-only role > plan posted as comment > reviewers approve > merge > pipeline runs `apply` with a write role for that environment (often requiring manual approval for prod) > state locked during apply.""",
config=[("GitHub Actions job explained", """jobs:
  plan:
    runs-on: ubuntu-latest
    permissions: { id-token: write, contents: read, pull-requests: write }
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
      - uses: aws-actions/configure-aws-credentials@v4
        with: { role-to-assume: arn:aws:iam::123456789012:role/tf-plan, aws-region: ap-south-1 }
      - run: terraform init -input=false
      - run: terraform fmt -check && terraform validate
      - run: terraform plan -input=false -out=tfplan""", [("id-token: write", "Allows OIDC to assume a role without stored keys."), ("tf-plan role", "Read-only role for planning; a separate role applies."), ("-input=false", "Never prompt in CI."), ("fmt -check/validate", "Fail early on style/syntax problems.")])],
lab=dict(goal="Add checks to a Terraform repo.", prereq=["Terraform repo", "pip or brew for checkov"],
steps=[("pip install checkov && checkov -d .", "Scans for insecure settings (open security groups, unencrypted storage)."), ("tflint --init && tflint", "Lints provider-specific errors."), ("Wire both into a CI job before plan", "Failures block the PR.")]),
mnemonics=[("CI order", "fmt > validate > lint > scan > plan > approve > apply")], hinglish="Terraform ko bhi **pipeline se chalao**: PR mein plan dikhao, approval ke baad apply karo. **OIDC** se keys ki zaroorat nahi.",
practices={"Security": ["OIDC, separate plan/apply roles, policy checks."]}, mistakes={"Security mistakes": ["Admin credentials in CI secrets."]},
versions=["Action versions and Terraform setup actions change: verify the latest in the marketplace/docs."],
qa_extra=[("Scenario-Based", "How to stop someone from applying to prod from a laptop?", "Restrict IAM: only the CI role can write; remote state permissions; SCP; audit with CloudTrail.", "Governance.", "Laptops get read-only.")])
})
