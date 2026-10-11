TOPIC = dict(slug="09-terraform", title="Infrastructure as Code: Terraform", intro="Infra ko code ki tarah likho: repeatable, reviewable, version-controlled. Click-ops (console) se chhutkara.", subs=[

dict(slug="terraform-basics", title="Terraform Basics & Workflow", level="Basic",
intro="Declarative HCL likhte ho; Terraform current state (tfstate) se compare karke plan banata hai aur apply karta hai. Workflow: init -> plan -> apply -> destroy.",
diagram="""
*.tf files --terraform init--> providers downloaded
        --terraform plan--> diff (desired vs state vs real)
        --terraform apply--> API calls -> resources created -> terraform.tfstate updated
""",
install="""winget install Hashicorp.Terraform    # or: sudo apt install terraform
terraform -version
# use an IAM role / SSO profile for AWS credentials""",
examples=[("First config: S3 bucket + EC2","""terraform {
  required_providers { aws = { source = "hashicorp/aws", version = "~> 5.0" } }
}
provider "aws" { region = "ap-south-1" }

variable "env" { default = "dev" }

resource "aws_s3_bucket" "logs" {
  bucket = "acme-logs-${var.env}-12345"
  tags   = { Env = var.env }
}

data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]
  filter { name = "name", values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"] }
}

resource "aws_instance" "web" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.micro"
  tags          = { Name = "web-${var.env}" }
}

output "web_ip" { value = aws_instance.web.public_ip }"""),
("Commands","""terraform init
terraform fmt -recursive; terraform validate
terraform plan -out tfplan
terraform apply tfplan
terraform output; terraform state list
terraform destroy""")],
problems=[("Plan wants to destroy and recreate a resource","Changed an immutable attribute or renamed resource","Read plan carefully (`-/+`); use `moved` block / `terraform state mv` for renames; `lifecycle { prevent_destroy = true }` for critical."),
("Accidentally committed tfstate with secrets","Local state in Git","Use remote encrypted state; .gitignore state files.")],
qa=[("What is terraform state?","Mapping between config and real resources; needed to plan changes."),
("terraform plan vs apply?","plan shows changes without doing; apply executes."),
("What are providers?","Plugins that talk to APIs (AWS, Azure, K8s)."),
("data source vs resource?","Data reads existing info; resource creates/manages."),
("Declarative vs imperative?","Terraform declares end state; scripts declare steps.")]),

dict(slug="terraform-state-modules", title="Remote State, Modules & Variables", level="Intermediate",
intro="Team mein kaam karne ke liye remote state + locking. Modules reuse ke liye. Variables, locals, for_each, dynamic blocks.",
diagram="""
envs/dev  --\\
envs/prod --+--> module "vpc" (modules/vpc)  ==> same code, different inputs
Remote state: S3 bucket (versioned, encrypted) + DynamoDB lock table (or use_lockfile)
""",
install="# create state bucket once (bootstrap) then configure backend",
examples=[("Backend","""terraform {
  backend "s3" {
    bucket         = "acme-tfstate"
    key            = "prod/network.tfstate"
    region         = "ap-south-1"
    dynamodb_table = "tf-locks"
    encrypt        = true
  }
}"""),
("Module structure and usage","""modules/vpc/{main.tf,variables.tf,outputs.tf}

module "vpc" {
  source = "../../modules/vpc"
  name   = "prod"
  cidr   = "10.0.0.0/16"
  azs    = ["ap-south-1a", "ap-south-1b"]
}
# use output: module.vpc.private_subnet_ids"""),
("for_each and dynamic","""variable "buckets" { default = ["logs", "backups"] }
resource "aws_s3_bucket" "b" {
  for_each = toset(var.buckets)
  bucket   = "acme-${each.key}"
}
resource "aws_security_group" "sg" {
  dynamic "ingress" {
    for_each = [80, 443]
    content { from_port = ingress.value, to_port = ingress.value, protocol = "tcp", cidr_blocks = ["0.0.0.0/0"] }
  }
}""")],
problems=[("Error acquiring state lock","Another run or crashed run holds lock","Verify nobody is running; `terraform force-unlock <ID>`."),
("Changing list order recreates resources","Using `count` with lists","Use `for_each` with stable keys.")],
qa=[("count vs for_each?","count index-based (fragile on removal); for_each key-based (stable)."),
("Why state locking?","Prevents concurrent applies corrupting state."),
("Workspaces vs directories per env?","Workspaces share config; directories give clearer isolation and separate backends (preferred for prod)."),
("How to import existing resource?","`terraform import` or `import` block, then write matching config."),
("Module versioning?","Pin `version`/git tag to avoid surprise changes.")]),

dict(slug="terraform-real-infra", title="Real Project: VPC + EKS + RDS", level="Intermediate",
intro="Full production-style stack Terraform mein: network, cluster, database, IAM. Community modules reuse karo.",
diagram="""
terraform/
 ├─ modules/ (vpc, rds)
 └─ envs/prod: vpc -> eks -> rds -> outputs
Dependencies flow via outputs (module.vpc.private_subnets -> eks.subnet_ids)
""",
install="terraform init && terraform plan   # in envs/prod",
examples=[("VPC + EKS using registry modules","""module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"
  name = "prod"
  cidr = "10.0.0.0/16"
  azs  = ["ap-south-1a", "ap-south-1b", "ap-south-1c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]
  enable_nat_gateway = true
  single_nat_gateway = false
}

module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 20.0"
  cluster_name    = "prod"
  cluster_version = "1.30"
  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets
  eks_managed_node_groups = {
    default = { instance_types = ["t3.large"], min_size = 2, max_size = 6, desired_size = 3 }
  }
}

resource "aws_db_instance" "pg" {
  identifier              = "prod-pg"
  engine                  = "postgres"
  instance_class          = "db.t3.medium"
  allocated_storage       = 50
  multi_az                = true
  storage_encrypted       = true
  backup_retention_period = 7
  db_subnet_group_name    = aws_db_subnet_group.db.name
  vpc_security_group_ids  = [aws_security_group.db.id]
  username                = "app"
  manage_master_user_password = true   # stored in Secrets Manager, not in state
}""")],
problems=[("Destroying VPC fails","Dependencies (ENIs from LBs/EKS) still exist","Delete K8s LoadBalancer Services / Ingress first, then terraform destroy."),
("DB password ends up in state","Hard-coded/plain variable","Use `manage_master_user_password` or Secrets Manager data source; encrypt state.")],
qa=[("How do modules pass data?","Outputs of one module become inputs of another."),
("How to avoid secrets in state?","Managed passwords, external secret stores, mark sensitive, restrict state access."),
("How to handle multiple environments?","Separate dirs/backends + shared modules + tfvars."),
("What is terraform drift?","Real infra changed outside Terraform; detect via plan/refresh."),
("`prevent_destroy` purpose?","Blocks accidental destroy of critical resources.")]),

dict(slug="terraform-ci-policy", title="Terraform in CI, Policy & Testing", level="Advanced",
intro="PR par plan comment, merge par apply. Checkov/tfsec/OPA se policy checks. Terratest/terraform test se testing.",
diagram="""
PR -> fmt/validate/tflint -> Checkov (policy) -> terraform plan -> comment on PR -> review
merge -> apply (with approval) -> state updated
""",
install="pip install checkov\ngo install github.com/terraform-linters/tflint@latest",
examples=[("GitHub Actions for Terraform","""name: terraform
on: { pull_request: { paths: ['infra/**'] } }
permissions: { id-token: write, contents: read, pull-requests: write }
jobs:
  plan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
      - uses: aws-actions/configure-aws-credentials@v4
        with: { role-to-assume: arn:aws:iam::123456789012:role/tf-plan, aws-region: ap-south-1 }
      - run: terraform -chdir=infra/envs/prod init
      - run: terraform -chdir=infra/envs/prod fmt -check
      - run: checkov -d infra --quiet
      - run: terraform -chdir=infra/envs/prod plan -no-color"""),
("Native test","""# tests/vpc.tftest.hcl
run "vpc_cidr" {
  command = plan
  assert { condition = module.vpc.cidr == "10.0.0.0/16", error_message = "wrong cidr" }
}""")],
problems=[("Two people applied at once","No CI-enforced single pipeline","Only pipeline applies; state locking; Atlantis/Terraform Cloud."),
("Config drift from console changes","Click-ops","Scheduled `plan` drift check, restrict console write via IAM/SCP.")],
qa=[("How to prevent insecure infra?","Policy-as-code (Checkov/OPA/Sentinel) in CI."),
("Terraform vs CloudFormation?","Terraform multi-cloud, HCL, larger ecosystem; CFN AWS-native, no state file to manage."),
("Terraform vs Pulumi/CDK?","Pulumi/CDK use real programming languages; Terraform declarative DSL."),
("What is Terragrunt?","Wrapper to keep configs DRY and orchestrate many stacks."),
("What is OpenTofu?","Open-source fork of Terraform after license change.")]),
])
