TOPIC = dict(slug="08-aws-cloud", title="Cloud (AWS)", intro="Ek cloud deeply seekho (AWS). Concepts Azure/GCP mein bhi same hain. Free tier par practice karo aur budget alert zaroor lagao.", subs=[

dict(slug="aws-iam-basics", title="AWS Basics, Account Setup & IAM", level="Basic",
intro="Region = geographic area, AZ = isolated data center in region. IAM decides WHO can do WHAT. Root account use mat karo, MFA lagao.",
diagram="""
AWS Account
 ├── Region (ap-south-1)
 │    ├── AZ a | AZ b | AZ c
 └── IAM: User/Group/Role + Policy (JSON) -> allow/deny actions on resources
Role = temporary credentials for services (EC2, Lambda) or cross-account
""",
install="""# AWS CLI v2
winget install Amazon.AWSCLI   # or: curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o a.zip && unzip a.zip && sudo ./aws/install
aws configure sso     # preferred over static keys
aws sts get-caller-identity""",
examples=[("Least-privilege policy for one S3 bucket","""{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": ["s3:GetObject","s3:PutObject"],
    "Resource": "arn:aws:s3:::my-app-bucket/*"
  }]
}"""),
("First-day security checklist","""1 Enable MFA on root; don't create root access keys
2 Create admin IAM Identity Center user; use SSO
3 Budget alert at $5/$10 (Billing -> Budgets)
4 Enable CloudTrail; set region restrictions via SCP later""")],
problems=[("Huge unexpected AWS bill","Forgotten EC2/NAT/EBS/ELB, or leaked keys mining crypto","Budgets + alerts, Cost Explorer, tag everything, delete unused; rotate/revoke leaked keys."),
("AccessDenied though policy looks right","Explicit deny, SCP, permission boundary, or resource policy","Use IAM Policy Simulator and CloudTrail event to see denying policy.")],
qa=[("IAM user vs role?","User has long-term credentials; role is assumed for temporary credentials (preferred for services)."),
("What is the shared responsibility model?","AWS secures the cloud; you secure what you put in it."),
("Policy evaluation logic?","Default deny; explicit deny always wins; else needs an allow."),
("What is STS?","Service issuing temporary credentials (AssumeRole)."),
("Region vs AZ?","Region = independent geography; AZ = isolated datacenters within it; deploy across AZs for HA.")]),

dict(slug="aws-vpc", title="VPC Networking", level="Intermediate",
intro="VPC tumhara private network hai AWS mein. Subnets, route tables, IGW, NAT, SG, NACL: har production design ka base.",
diagram="""
VPC 10.0.0.0/16
 ├─ Public subnet a/b   (route 0.0.0.0/0 -> IGW): ALB, NAT GW, bastion
 ├─ Private subnet a/b  (route 0.0.0.0/0 -> NAT): app / EKS nodes
 └─ DB subnet a/b       (no internet route): RDS
Internet <-> IGW <-> ALB -> app -> RDS ;  app -> NAT -> IGW (outbound only)
Endpoints: S3 gateway, ECR/STS interface (private access, saves NAT cost)
""",
install="aws ec2 describe-vpcs   # practice in console then automate with Terraform",
examples=[("Create with CLI (concept)","""aws ec2 create-vpc --cidr-block 10.0.0.0/16
aws ec2 create-subnet --vpc-id vpc-123 --cidr-block 10.0.1.0/24 --availability-zone ap-south-1a
aws ec2 create-internet-gateway; aws ec2 attach-internet-gateway --vpc-id vpc-123 --internet-gateway-id igw-123
aws ec2 create-route --route-table-id rtb-123 --destination-cidr-block 0.0.0.0/0 --gateway-id igw-123"""),
("Debug connectivity","""Use VPC Reachability Analyzer; check: route table -> SG -> NACL -> OS firewall -> app bind address""")],
problems=[("Private instance can't reach internet","Missing NAT route","Add NAT gateway in public subnet + route in private RT."),
("NAT gateway cost too high","All AWS traffic (S3/ECR) goes via NAT","Add VPC gateway/interface endpoints; one NAT per AZ only for prod.")],
qa=[("Public vs private subnet?","Public has route to IGW; private doesn't."),
("NAT gateway vs IGW?","IGW two-way for public IPs; NAT allows outbound-only for private."),
("VPC peering vs Transit Gateway?","Peering 1:1 non-transitive; TGW hub-and-spoke."),
("What is VPC endpoint?","Private connectivity to AWS services without internet."),
("Security Group stateful?","Yes; return traffic auto-allowed. NACLs are stateless.")]),

dict(slug="aws-compute-ec2", title="EC2, Auto Scaling & Load Balancing", level="Intermediate",
intro="EC2 virtual servers hain. ASG instances ko scale/replace karta hai, ALB traffic distribute karta hai. Classic 3-tier HA pattern.",
diagram="""
Route53 -> ALB (public subnets, 2 AZ) -> Target Group -> ASG (private subnets)
                                              |         EC2 (launch template: AMI, user-data, IAM role)
                                            health checks -> replace unhealthy
Scaling policy: target tracking CPU 50%
""",
install="aws ec2 describe-instance-types --filters Name=free-tier-eligible,Values=true --query 'InstanceTypes[].InstanceType'",
examples=[("Launch instance with user-data","""aws ec2 run-instances --image-id ami-xxxx --instance-type t3.micro \\
  --subnet-id subnet-123 --security-group-ids sg-123 --iam-instance-profile Name=app-role \\
  --user-data file://userdata.sh --tag-specifications 'ResourceType=instance,Tags=[{Key=Env,Value=dev}]'

# userdata.sh
#!/bin/bash
apt update && apt install -y nginx
systemctl enable --now nginx"""),
("Target tracking policy","""aws autoscaling put-scaling-policy --auto-scaling-group-name web-asg --policy-name cpu50 \\
  --policy-type TargetTrackingScaling \\
  --target-tracking-configuration '{"PredefinedMetricSpecification":{"PredefinedMetricType":"ASGAverageCPUUtilization"},"TargetValue":50}'""")],
problems=[("New instance passes health check but app fails","Health check on wrong path / too early","Use app-level /health, grace period, warm-up."),
("Can't SSH to instance","SG closed / wrong key / no public IP","Use SSM Session Manager (no SSH keys/ports needed).")],
qa=[("On-demand vs reserved vs spot?","On-demand pay as you go; Reserved/Savings Plans commit for discount; Spot cheap but can be reclaimed."),
("ALB vs NLB?","ALB L7 HTTP routing; NLB L4 ultra-low latency, static IP."),
("What is an AMI?","Machine image template used to launch instances."),
("Instance store vs EBS?","Instance store ephemeral, EBS persistent network disk."),
("How to make app highly available?","Multi-AZ ASG behind ALB, multi-AZ DB, stateless app.")]),

dict(slug="aws-storage-db", title="S3, EBS, RDS & DynamoDB", level="Intermediate",
intro="S3 object storage (static sites, backups, logs). RDS managed relational DB. DynamoDB serverless NoSQL.",
diagram="""
S3: bucket -> objects (versioning, lifecycle: Standard -> IA -> Glacier), SSE-KMS, block public access
RDS: Primary (AZ a) <-sync-> Standby (AZ b)  [Multi-AZ failover]; Read replicas for scale
""",
install="aws s3 ls; aws rds describe-db-instances",
examples=[("S3 essentials","""aws s3 mb s3://my-unique-bucket-123
aws s3 sync ./dist s3://my-unique-bucket-123 --delete
aws s3api put-bucket-versioning --bucket my-unique-bucket-123 --versioning-configuration Status=Enabled
aws s3 presign s3://my-unique-bucket-123/file.pdf --expires-in 600"""),
("Lifecycle rule","""{"Rules":[{"ID":"archive","Status":"Enabled","Filter":{"Prefix":"logs/"},
 "Transitions":[{"Days":30,"StorageClass":"STANDARD_IA"},{"Days":90,"StorageClass":"GLACIER"}],
 "Expiration":{"Days":365}}]}"""),
("RDS backup and restore","""aws rds create-db-snapshot --db-instance-identifier prod --db-snapshot-identifier prod-2025-01-01
aws rds restore-db-instance-to-point-in-time --source-db-instance-identifier prod --target-db-instance-identifier prod-restore --restore-time 2025-01-01T10:00:00Z""")],
problems=[("Company data exposed via public S3 bucket","Public ACL/policy","Enable account-level Block Public Access, use CloudFront OAC, Access Analyzer/Config rules."),
("RDS CPU 100%","Missing indexes / connection storm","Performance Insights, slow query log, RDS Proxy, read replicas.")],
qa=[("S3 storage classes?","Standard, IA, One Zone-IA, Glacier tiers, Intelligent-Tiering."),
("Multi-AZ vs read replica?","Multi-AZ for HA/failover (sync); read replica for read scaling (async)."),
("How to secure S3?","Block public access, bucket policy, encryption, versioning, MFA delete, logging."),
("DynamoDB partition key importance?","Even distribution avoids hot partitions."),
("EBS snapshots?","Incremental backups stored in S3; used for backup/AMI.")]),

dict(slug="aws-serverless-monitoring", title="Lambda, ECS/EKS, CloudWatch & Cost", level="Advanced",
intro="Serverless (Lambda), containers (ECS Fargate/EKS), monitoring (CloudWatch/CloudTrail), aur cost optimization (FinOps).",
diagram="""
API Gateway -> Lambda -> DynamoDB          (serverless)
S3 event -> Lambda -> process -> SNS/SQS
ECS Fargate: task definition -> service -> ALB (no servers to manage)
CloudWatch: metrics + logs + alarms -> SNS -> Slack/PagerDuty
""",
install="pip install aws-sam-cli   # local Lambda dev",
examples=[("Lambda with EventBridge schedule (SAM)","""Resources:
  Fn:
    Type: AWS::Serverless::Function
    Properties:
      Runtime: python3.12
      Handler: app.handler
      Timeout: 30
      Events:
        Nightly: { Type: Schedule, Properties: { Schedule: cron(0 20 * * ? *) } }"""),
("CloudWatch alarm","""aws cloudwatch put-metric-alarm --alarm-name high-cpu --namespace AWS/EC2 --metric-name CPUUtilization \\
 --statistic Average --period 300 --threshold 80 --comparison-operator GreaterThanThreshold --evaluation-periods 2 \\
 --alarm-actions arn:aws:sns:ap-south-1:123456789012:ops-alerts"""),
("Cost optimization checklist","""Right-size (Compute Optimizer) | Savings Plans | Spot for stateless/dev | delete unattached EBS/idle ELB
S3 lifecycle | scale non-prod to zero at night | tag + Cost allocation | VPC endpoints vs NAT""")],
problems=[("Lambda cold starts slow API","Large package / VPC / runtime","Provisioned concurrency, smaller package, SnapStart."),
("CloudWatch logs bill explosion","Verbose debug logs, infinite retention","Set retention, sample logs, filter before shipping.")],
qa=[("Lambda limits?","15 min max, memory up to 10GB, 250MB package (10GB container), concurrency limits."),
("ECS vs EKS?","ECS AWS-native simpler; EKS managed Kubernetes for portability/ecosystem."),
("CloudWatch vs CloudTrail?","CloudWatch = metrics/logs; CloudTrail = API audit logs."),
("Well-Architected pillars?","Operational excellence, security, reliability, performance efficiency, cost optimization, sustainability."),
("DR strategies?","Backup&restore, pilot light, warm standby, multi-site active-active (increasing cost, decreasing RTO).")]),
])
