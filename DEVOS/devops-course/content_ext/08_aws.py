EXT = dict(
guide=dict(
bigpicture=dict(
problem="""**Problem it solves:** Buying, racking and maintaining servers takes weeks and large upfront cost, and you must provision for peak load. **Cloud (AWS = Amazon Web Services)** gives you computing, storage, databases and networking on demand, paid per use, in minutes, across many data centres.""",
chain=["PROBLEM: need infrastructure quickly, at variable scale, with high availability",
       "TRADITIONAL APPROACH: buy hardware, own data centre, plan capacity for years",
       "PAIN: slow, expensive, over/under-provisioned, single site failure",
       "TECHNOLOGY: AWS (regions, availability zones, managed services)",
       "SOLUTION: on-demand resources, pay-as-you-go, managed HA services, APIs for automation",
       "REAL-WORLD BENEFIT: faster delivery, elasticity, resilience, lower ops burden"],
text="""Key building blocks: **Region** (geographic area) > **Availability Zone (AZ)** (isolated data centre group) > services. Security follows the **shared responsibility model**: AWS secures the cloud itself; you secure what you put in it (IAM, data, OS patches on EC2, security groups)."""),
e2e=dict(diagram="""User
  v
Route 53 (DNS)
  v
CloudFront (CDN) + WAF
  v
Application Load Balancer (public subnets, 2+ AZs)
  v
EC2 Auto Scaling group / ECS / EKS (private app subnets)
  v
RDS Multi-AZ + ElastiCache (private DB subnets)   S3 (static/files)
  v
CloudWatch (metrics/logs/alarms) + CloudTrail (audit) + IAM (access)
  v
Cost: Budgets / Cost Explorer / tags""",
text="""DNS in **Route 53** points users to **CloudFront**, which caches content and passes requests through **WAF**. The **ALB** sits in public subnets across at least two AZs and forwards requests to application servers (EC2 Auto Scaling, ECS or EKS) in **private subnets**. The app uses **RDS** (managed database with Multi-AZ failover) in isolated subnets, **ElastiCache** for caching and **S3** for objects. Every access is governed by **IAM** roles. **CloudWatch** collects metrics and logs and triggers alarms; **CloudTrail** records API activity for audit; **Budgets** and tags control cost."""),
tools=dict(rows=[
["IAM", "Identity and permissions", "Users/roles/policies", "Allow/deny decisions", "Every request"],
["VPC (subnets, route tables, IGW, NAT, SG)", "Private network", "CIDR + rules", "Isolated network", "Foundation"],
["EC2 / Auto Scaling / ELB", "Virtual servers + scaling + balancing", "AMI, instance type, policy", "Running scalable fleet", "Compute tier"],
["S3 / EBS / EFS", "Object / block / file storage", "Data", "Durable storage", "Files, disks, shared FS"],
["RDS / DynamoDB / ElastiCache", "Relational / NoSQL / cache", "Queries", "Data", "Data tier"],
["Lambda / ECS / EKS", "Serverless / containers / Kubernetes", "Code or images", "Running workloads", "App tier"],
["CloudWatch / CloudTrail / Config", "Metrics-logs / audit / compliance", "Events", "Alarms, records", "Operations"],
["Terraform / CloudFormation", "Infrastructure as Code", "Code", "Provisioned resources", "Provisioning"]],
why="**EC2 vs Lambda vs ECS/EKS:** EC2 for full control/long-running; Lambda for event-driven short tasks with no servers; ECS is simpler container orchestration, EKS if you need Kubernetes. **RDS vs DynamoDB:** RDS for relational/SQL/transactions; DynamoDB for key-value scale and predictable low latency."),
compare=[
("IAM User vs Role vs Group vs Policy", ["Topic", "Meaning"], [["User", "Identity for a person/app with long-term credentials (avoid for apps)"], ["Group", "Collection of users to attach policies"], ["Role", "Identity assumed temporarily (EC2, Lambda, cross-account, SSO)"], ["Policy", "JSON document defining allowed/denied actions"]]),
("Security Group vs NACL", ["Topic", "SG", "NACL"], [["State", "Stateful", "Stateless"], ["Applies to", "ENI/instance", "Subnet"], ["Rules", "Allow only", "Allow + deny, ordered"]]),
("S3 vs EBS vs EFS", ["Topic", "S3", "EBS", "EFS"], [["Type", "Object", "Block (one instance, one AZ)", "Shared file system (NFS)"], ["Use", "Files, backups, static site", "Boot/data disks, databases", "Shared content across instances"]]),
("EC2 purchasing", ["Option", "Best for", "Note"], [["On-Demand", "Unpredictable", "Highest price, flexible"], ["Reserved/Savings Plans", "Steady baseline", "Up to large discounts for commitment"], ["Spot", "Fault-tolerant/batch", "Can be interrupted"]]),
("ALB vs NLB", ["Topic", "ALB", "NLB"], [["Layer", "7 HTTP/HTTPS", "4 TCP/UDP"], ["Use", "Path/host routing", "Static IP, extreme performance"]]),
("RDS Multi-AZ vs Read Replica", ["Topic", "Multi-AZ", "Read replica"], [["Purpose", "High availability/failover", "Read scaling"], ["Replication", "Synchronous standby", "Asynchronous"]])],
troubleshooting=[
("EC2 instance not reachable via SSH", "Security group, NACL, route/IGW, key pair, public IP, instance state/status checks", "EC2 console status checks, SG inbound rule 22, route table has IGW, `ssh -vvv`", "Fix SG/route/key; use SSM Session Manager as alternative.", "Use SSM; avoid public SSH."),
("AccessDenied / UnauthorizedOperation", "IAM policy, SCP, permission boundary or resource policy", "Error message names action; CloudTrail; IAM policy simulator", "Add least-privilege action; check explicit denies/SCP.", "Use least privilege with tests."),
("Private instance has no internet", "Missing route to NAT gateway, NAT in wrong subnet, SG/NACL egress", "Route table of the private subnet, NAT status", "Add `0.0.0.0/0` to NAT; ensure NAT is in a public subnet with EIP.", "IaC modules for standard VPC."),
("Unexpected AWS bill", "Idle resources, NAT/data transfer, unattached EBS, forgotten instances", "Cost Explorer by service/tag, Budgets", "Delete/stop unused resources, VPC endpoints, rightsizing.", "Budgets, alerts, tagging, automation."),
("ALB targets unhealthy", "Health check path/port mismatch, SG blocks ALB, app down", "Target group health reason, SG rules, curl app locally", "Fix path/port; allow ALB SG to app SG.", "Match health check to a lightweight endpoint."),
("RDS connection timeout", "SG missing, not in same VPC/subnet route, public accessibility, max connections", "SG inbound 5432/3306, `nc -zv endpoint port`, RDS events", "Allow app SG to DB SG; check subnet group.", "Chain SGs (app SG to DB SG).")],
practices={
"Development": ["Use separate accounts/environments; IaC (Terraform) instead of console; use free tier carefully with budget alerts."],
"Production": ["Multi-AZ everywhere; Auto Scaling; managed services; backups; tagging standards; separate AWS accounts (AWS Organizations)."],
"Security": ["Enable MFA; never use root; least-privilege IAM roles; no long-lived keys; encrypt at rest (KMS) and in transit; private subnets for data; CloudTrail, GuardDuty, Security Hub; S3 Block Public Access."],
"Performance": ["Right-size instances; CloudFront; caching (ElastiCache); read replicas; gp3 volumes."],
"Reliability": ["Multi-AZ, health checks, automated failover, backups tested, defined RPO/RTO."],
"Cost Optimization": ["Budgets and alarms; Savings Plans/Reserved for baseline; Spot for batch; delete unused EBS/EIPs/snapshots; S3 lifecycle; VPC endpoints to cut NAT costs; schedule dev environments."],
"Monitoring & Logging": ["CloudWatch metrics/alarms/log groups; ALB and VPC flow logs; CloudTrail to S3."],
"Backup & Disaster Recovery": ["RDS automated backups + snapshots, S3 versioning and cross-region replication, AWS Backup; pilot light/warm standby/multi-site DR by RPO/RTO."]},
mistakes={
"Beginner mistakes": ["Using the root account daily.", "Leaving resources running.", "Public S3 buckets."],
"Developer mistakes": ["Access keys in code/Git.", "Hard-coded region/account IDs."],
"DevOps mistakes": ["Manual console changes (drift).", "Overly broad `*:*` IAM policies.", "Single AZ deployments."],
"Production mistakes": ["No backup restore test.", "No cost alerts.", "Database publicly accessible."],
"Security mistakes": ["Security group 0.0.0.0/0 on SSH/DB.", "No MFA.", "Unencrypted data."]},
versions=[
"AWS services and console UI change often; confirm limits, prices and regions in the official documentation and pricing pages.",
"AWS CLI v2 is current (v1 is legacy). Use SSO (`aws configure sso`) over static keys.",
"Amazon Linux 2 is being replaced by Amazon Linux 2023 (dnf-based); check end-of-support dates.",
"IMDSv2 should be required on EC2 (`HttpTokens=required`) to reduce SSRF risk.",
"Azure/GCP have equivalent concepts with different names (VPC=VNet, IAM roles=Managed identities/Service accounts)."],
hinglish="""AWS mein sab kuch **API se on-demand** milta hai aur **use ke hisaab se paisa** lagta hai. **Region** bada area, **AZ** us ke andar alag data centre. Security **shared responsibility** hai: AWS cloud ka hardware secure karta hai, tum apna data, IAM, security groups aur OS patch secure karte ho. **Root account use mat karo**, **MFA lagao**, aur apps ko **IAM role** do (access keys nahi). Database aur app **private subnet** mein rakho, sirf load balancer public rakho. Budget alert zaroor lagao.""",
mnemonics=[
("Well-Architected pillars", "O-S-R-P-C-S: Operational excellence, Security, Reliability, Performance efficiency, Cost optimization, Sustainability"),
("VPC tiers", "Public: ALB/NAT; Private: app; Isolated: DB"),
("IAM", "Who (principal) can do What (action) on Which (resource) When (condition)"),
("Storage", "S3 = objects, EBS = one server disk, EFS = shared folder"),
("DR strategies", "Backup & Restore < Pilot Light < Warm Standby < Multi-site (cost and speed increase)")],
client=dict(
s30="""AWS lets us run your applications on demand in secure, highly available data centres and pay only for what we use. We can scale quickly, recover from failures automatically and avoid buying hardware.""",
m2="""Instead of buying servers, we use AWS to build your environment as code in minutes. Your application runs in a private network across multiple availability zones, so a data centre failure does not stop the service. Access is controlled with IAM roles and MFA, data is encrypted, and all activity is logged. We use managed services like RDS for databases and S3 for storage to reduce maintenance, Auto Scaling to handle traffic peaks, and budgets, tagging and rightsizing to keep costs under control. You get faster delivery, better resilience and a clear view of cost.""",
m5="""I will explain in five layers. **Foundation:** an AWS Organization with separate accounts for production and non-production, SSO with MFA and centralised logging. **Network:** a VPC across at least two availability zones with public subnets for load balancers, private subnets for applications and isolated subnets for databases, controlled with security groups. **Compute and data:** Auto Scaling EC2 or containers on ECS/EKS, RDS with Multi-AZ, S3 for objects, ElastiCache for performance. **Security and compliance:** least-privilege IAM roles, KMS encryption, CloudTrail, GuardDuty, WAF and patching. **Operations and cost:** everything defined in Terraform, CloudWatch dashboards and alarms, backups with tested restores, and Savings Plans, Spot and lifecycle policies to lower cost. This design targets high availability, security and predictable spend."""),
roadmap=[
("Beginner", ["Cloud concepts, regions/AZs", "IAM basics and MFA", "EC2, S3 basics", "Billing and free tier alerts"]),
("Intermediate", ["VPC design", "ALB + Auto Scaling", "RDS and backups", "CloudWatch, CloudTrail", "AWS CLI"]),
("Advanced", ["ECS/EKS, Lambda/serverless", "IAM advanced (SCP, boundaries, cross-account)", "Multi-account (Organizations, Control Tower)", "DR strategies, Well-Architected"]),
("Production", ["Terraform for everything", "Security services (GuardDuty, Config)", "Cost optimization/FinOps", "Observability"]),
("Interview", ["Design a 3-tier HA app", "IAM policy evaluation", "S3 vs EBS vs EFS", "Reduce AWS bill"])],
miniproject=dict(title="Highly available web app on EC2 with ALB, Auto Scaling and RDS",
arch="""Internet --> ALB (public subnets, AZ-a/AZ-b) --> Auto Scaling group (private app subnets)
                                                      --> RDS Multi-AZ (private DB subnets)
S3 for static files ; CloudWatch alarms ; NAT for outbound ; SSM for admin access""",
steps=[
("Step 1: Network plan", """VPC 10.0.0.0/16
public-a 10.0.0.0/24   public-b 10.0.1.0/24     (ALB, NAT)
app-a    10.0.10.0/24  app-b    10.0.11.0/24    (EC2)
db-a     10.0.20.0/24  db-b     10.0.21.0/24    (RDS)""", "Two AZs and three tiers. Only the ALB is internet facing."),
("Step 2: Security groups (chain)", """alb-sg : inbound 80/443 from 0.0.0.0/0
app-sg : inbound 8080 from alb-sg
db-sg  : inbound 5432 from app-sg""", "Referencing security groups instead of IPs means each tier only accepts traffic from the tier in front of it."),
("Step 3: Launch template + ASG via CLI (illustrative)", """aws ec2 create-launch-template --launch-template-name web-lt \\
  --launch-template-data '{"ImageId":"ami-xxxx","InstanceType":"t3.micro","SecurityGroupIds":["sg-app"],"IamInstanceProfile":{"Name":"web-profile"},"MetadataOptions":{"HttpTokens":"required"}}'
aws autoscaling create-auto-scaling-group --auto-scaling-group-name web-asg \\
  --launch-template LaunchTemplateName=web-lt,Version='$Latest' \\
  --min-size 2 --max-size 6 --desired-capacity 2 \\
  --vpc-zone-identifier "subnet-app-a,subnet-app-b" --target-group-arns arn:aws:elasticloadbalancing:...""", "AMI IDs, subnets and ARNs are placeholders you must replace. `HttpTokens=required` enforces IMDSv2. In real projects define all of this in Terraform."),
("Step 4: Verify and monitor", """aws elbv2 describe-target-health --target-group-arn <arn>
curl -I http://<alb-dns-name>
aws cloudwatch put-metric-alarm --alarm-name web-cpu-high --metric-name CPUUtilization --namespace AWS/EC2 \\
  --statistic Average --period 300 --threshold 70 --comparison-operator GreaterThanThreshold --evaluation-periods 2 \\
  --dimensions Name=AutoScalingGroupName,Value=web-asg --alarm-actions <sns-topic-arn>""", "Check targets are healthy, call the ALB, and create a CPU alarm that notifies an SNS topic. Remember to delete resources afterward to avoid charges.")]),
interview=[
("Beginner", "What is cloud computing?", "On-demand delivery of IT resources over the internet with pay-as-you-go pricing.", "Foundation.", "Launch a server in minutes."),
("Beginner", "Region vs Availability Zone?", "Region is a geographic area; AZ is an isolated data centre location within it.", "HA basics.", "ap-south-1a and 1b."),
("Beginner", "What is EC2?", "Virtual servers in the cloud.", "Core compute.", "t3.micro web server."),
("Beginner", "What is S3?", "Object storage with high durability, used for files, backups and static sites.", "Core storage.", "Store images and logs."),
("Beginner", "What is IAM?", "Service to manage identities and permissions.", "Security base.", "Roles for EC2."),
("Beginner", "What is a VPC?", "Your isolated virtual network in AWS.", "Networking.", "10.0.0.0/16."),
("Beginner", "What is the shared responsibility model?", "AWS secures the infrastructure; customer secures configuration, data, identities and guest OS.", "Security basics.", "You patch EC2; AWS patches RDS engine hardware."),
("Beginner", "What is an AMI?", "Machine image template used to launch EC2 instances.", "Provisioning.", "Golden AMI."),
("Beginner", "What is a security group?", "Stateful virtual firewall for instances.", "Access control.", "Allow 443 only."),
("Beginner", "What is CloudWatch?", "Monitoring service for metrics, logs and alarms.", "Operations.", "CPU alarm."),
("Intermediate", "Explain public vs private subnet.", "Public subnet route table has a route to an Internet Gateway; private subnets do not and use NAT for outbound.", "VPC design.", "DB in private."),
("Intermediate", "What is NAT Gateway?", "Managed service allowing private subnets outbound internet without inbound exposure; in a public subnet with an Elastic IP.", "Connectivity and cost.", "OS updates from private EC2."),
("Intermediate", "IAM role vs user?", "Users have long-term credentials; roles provide temporary credentials assumed by services/people.", "Best practice: roles.", "Lambda execution role."),
("Intermediate", "Explain S3 storage classes and lifecycle.", "Standard, Standard-IA, One Zone-IA, Glacier tiers; lifecycle rules transition/expire objects to reduce cost.", "Cost.", "Move logs to Glacier after 90 days."),
("Intermediate", "EBS volume types?", "gp3/gp2 general SSD, io1/io2 provisioned IOPS, st1/sc1 HDD throughput/cold.", "Storage design.", "gp3 for most workloads."),
("Intermediate", "How does Auto Scaling work?", "Launch template + ASG with min/max/desired and scaling policies on metrics; replaces unhealthy instances across AZs.", "Elasticity.", "Target tracking 50% CPU."),
("Intermediate", "ALB vs NLB vs CLB?", "ALB L7, NLB L4, CLB legacy.", "Load balancing.", "ALB for web apps."),
("Intermediate", "RDS Multi-AZ vs read replicas?", "Multi-AZ = availability/failover; read replica = read scaling.", "Database design.", "Read replica for reporting."),
("Intermediate", "What is Route 53 routing policies?", "Simple, weighted, latency, failover, geolocation, multi-value.", "DNS.", "Failover to DR region."),
("Intermediate", "What is CloudTrail?", "Records AWS API calls for audit and security analysis.", "Governance.", "Who deleted the bucket?"),
("Intermediate", "Explain SNS vs SQS.", "SNS is pub/sub push; SQS is a queue (pull) for decoupling; combine for fan-out.", "Messaging.", "S3 event to SNS to multiple SQS."),
("Intermediate", "What is an Elastic IP?", "Static public IPv4 address you can remap between instances; chargeable when idle.", "Networking/cost.", "NAT gateway EIP."),
("Intermediate", "What is Infrastructure as Code on AWS?", "Define resources in CloudFormation/Terraform for repeatable, versioned deployments.", "Automation.", "terraform apply."),
("Intermediate", "How do you connect on-premises to AWS?", "Site-to-Site VPN or Direct Connect (plus Transit Gateway).", "Hybrid.", "VPN as quick start."),
("Intermediate", "What is AWS Organizations and SCP?", "Multi-account management; SCPs set maximum permission guardrails.", "Governance.", "Deny leaving regions."),
("Advanced", "Explain IAM policy evaluation logic.", "Default deny; explicit deny always wins; an allow is needed from identity policy (and resource policy where applicable) and must not be blocked by SCP/boundary/session policy.", "Security depth.", "SCP denies overrides admin allow."),
("Advanced", "Design a highly available 3-tier app.", "ALB across 2-3 AZs, ASG in private subnets, RDS Multi-AZ, ElastiCache, S3/CloudFront, SG chaining, NAT per AZ, Route 53, monitoring and backups.", "Architecture.", "See mini project."),
("Advanced", "DR strategies and RPO/RTO?", "Backup & restore (hours), pilot light, warm standby, multi-site active-active; choose by RPO/RTO and cost.", "Resilience.", "Cross-region RDS replica."),
("Advanced", "VPC peering vs Transit Gateway vs PrivateLink?", "Peering is 1:1 non-transitive; TGW is a hub for many VPCs/VPNs; PrivateLink exposes a service privately without full network connectivity.", "Networking design.", "Shared services VPC via TGW."),
("Advanced", "S3 security best practices.", "Block Public Access, bucket policies with least privilege, encryption (SSE-KMS), versioning, MFA delete, access logs, VPC endpoints.", "Data protection.", "Prevent public bucket leaks."),
("Advanced", "How would you reduce NAT gateway costs?", "Gateway VPC endpoints for S3/DynamoDB, interface endpoints for other services, consolidate egress carefully, cache/proxy.", "FinOps.", "S3 traffic via endpoint."),
("Advanced", "ECS vs EKS vs Lambda selection?", "Lambda for event-driven short tasks; ECS/Fargate for simple containers; EKS for Kubernetes portability/ecosystem.", "Compute choice.", "Team already runs Kubernetes: EKS."),
("Advanced", "How do IAM roles for service accounts (IRSA) work?", "EKS OIDC provider lets a Kubernetes ServiceAccount assume an IAM role via web identity tokens, giving pods least-privilege AWS access.", "EKS security.", "Pod reads only one S3 bucket."),
("Advanced", "Explain DynamoDB partition key design.", "Choose high-cardinality keys to spread load; avoid hot partitions; use GSIs for alternate access patterns.", "NoSQL design.", "userId as partition key."),
("Advanced", "How does KMS envelope encryption work?", "A data key encrypts data; KMS master key encrypts the data key; only the encrypted data key is stored.", "Encryption.", "S3 SSE-KMS."),
("Advanced", "Well-Architected Framework?", "Six pillars: operational excellence, security, reliability, performance efficiency, cost optimization, sustainability.", "Design review.", "Review before go-live."),
("Advanced", "What is eventual consistency in DynamoDB/S3 context?", "Reads may briefly see stale data; S3 now provides strong read-after-write consistency, DynamoDB offers strongly consistent read option.", "Data semantics.", "ConsistentRead=true."),
("Advanced", "Multi-account strategy?", "Separate accounts for prod, non-prod, security, logging, shared services; Organizations, SCPs, centralised identity.", "Enterprise setup.", "Control Tower landing zone."),
("Advanced", "How to secure EC2 metadata?", "Require IMDSv2, least-privilege instance roles, restrict SSRF vectors.", "Cloud security.", "Prevent credential theft."),
("Scenario-Based", "Website went down in one AZ.", "Multi-AZ design keeps serving; check ALB target health, ASG replaces, RDS fails over; investigate AZ event.", "HA in practice.", "RDS failover in ~1-2 minutes."),
("Scenario-Based", "AWS bill doubled this month.", "Cost Explorer by service/account/tag, find NAT/data transfer/EC2/Snapshots, remove idle, set budgets and anomaly detection.", "FinOps.", "Forgotten GPU instance."),
("Scenario-Based", "Developers need temporary production access.", "IAM Identity Center with time-limited permission sets, approval, session logging, no shared keys.", "Access governance.", "Break-glass role."),
("Scenario-Based", "S3 bucket was made public accidentally.", "Enable Block Public Access at account level, review policies/ACLs, check access logs, rotate exposed data, add AWS Config rule.", "Incident response.", "Config rule s3-bucket-public-read-prohibited."),
("Scenario-Based", "Need to migrate a database with minimal downtime.", "AWS DMS with continuous replication, cut over, validate, rollback plan.", "Migration.", "On-prem MySQL to RDS."),
("Scenario-Based", "Traffic spike at a marketing event.", "Pre-warm ALB, scale ASG with scheduled scaling, CDN caching, DB read replicas, load test.", "Capacity.", "Scheduled scale-out."),
("Scenario-Based", "Restrict an app to read one S3 prefix.", "IAM role with policy allowing s3:GetObject on `arn:aws:s3:::bucket/prefix/*` and ListBucket with prefix condition.", "Least privilege.", "Reports service."),
("Scenario-Based", "Secure database credentials for an app.", "Secrets Manager with rotation, IAM role for retrieval, no credentials in code/AMI.", "Secrets.", "RDS automatic rotation."),
("Scenario-Based", "Choose storage for shared uploads across multiple app servers.", "S3 for objects (preferred) or EFS for POSIX shared file system.", "Design choice.", "Uploads to S3 with presigned URLs."),
("Scenario-Based", "Compliance requires audit of all changes.", "CloudTrail organisation trail to locked S3, AWS Config, log integrity validation, alerts.", "Audit.", "Central log archive account."),
("Scenario-Based", "Reduce EC2 cost by 40%.", "Right-size, Savings Plans for baseline, Spot for stateless, Graviton instances, schedule non-prod.", "Optimization.", "Move to t4g/m7g."),
("Scenario-Based", "Run scheduled jobs without servers.", "EventBridge Scheduler + Lambda/ECS task.", "Serverless ops.", "Nightly cleanup."),
("Scenario-Based", "Cross-region disaster recovery for a web app.", "Replicate data (S3 CRR, Aurora global/RDS cross-region replica), IaC for infrastructure, Route 53 failover, regular game days.", "DR planning.", "Warm standby."),
("Scenario-Based", "Private EC2 needs to reach S3 without internet.", "Gateway VPC endpoint for S3 and route table association.", "Networking.", "No NAT costs."),
("Scenario-Based", "Allow another AWS account to access a bucket.", "Bucket policy with principal of the other account/role plus IAM permission in that account (cross-account).", "Cross-account.", "Data sharing."),
("Troubleshooting-Based", "EC2 status check failed.", "System check: AWS hardware issue (stop/start migrates); instance check: OS problem (console output, EBS snapshot, recovery).", "EC2 debugging.", "Kernel panic."),
("Troubleshooting-Based", "`Unable to locate credentials` in CLI.", "No profile/env/role; `aws configure`, set AWS_PROFILE, or use instance role.", "CLI auth.", "Cron without env."),
("Troubleshooting-Based", "ALB returns 502/503.", "No healthy targets or app crash; check target group health, SG, listener rules, logs.", "LB debugging.", "Wrong port."),
("Troubleshooting-Based", "Lambda times out.", "Timeout too low, cold start, VPC/NAT connectivity, slow downstream, memory; check CloudWatch logs and X-Ray.", "Serverless.", "Lambda in VPC without NAT."),
("Troubleshooting-Based", "RDS storage full/CPU high.", "Enable autoscaling storage, inspect slow queries via Performance Insights, add indexes/replicas, resize.", "DB ops.", "Long-running query."),
("Troubleshooting-Based", "Cannot delete a resource (dependency violation).", "Dependencies exist (ENIs, SG references, route tables); remove dependents first or use IaC destroy order.", "Cleanup.", "Deleting VPC."),
("Troubleshooting-Based", "S3 403 Access Denied.", "Bucket policy/IAM/KMS key policy/Block Public Access/Object ownership; check exact principal and ARN.", "S3 security.", "KMS key denies role."),
("Troubleshooting-Based", "Auto Scaling not scaling.", "Max size reached, cooldown, wrong metric/alarm, capacity limits or launch failures; check activity history.", "ASG debugging.", "vCPU quota exceeded."),
("Troubleshooting-Based", "Instance can't reach internet from public subnet.", "Missing public IP, IGW route, SG/NACL egress.", "VPC.", "No route 0.0.0.0/0 to IGW."),
("Troubleshooting-Based", "CloudFormation/Terraform stuck or failing.", "Read the first failing event, IAM permissions, quotas, dependency ordering; fix and retry.", "IaC ops.", "Limit exceeded.")],
cheatsheet={
"Definitions": ["Region/AZ; VPC; subnet; IGW; NAT; SG (stateful) vs NACL (stateless); IAM user/role/policy; S3 object, EBS block, EFS file; RDS managed SQL; DynamoDB NoSQL."],
"Commands": ["`aws sts get-caller-identity` `aws configure sso` `aws ec2 describe-instances --query ...`", "`aws s3 ls|cp|sync s3://bucket` `aws iam list-roles` `aws logs tail /aws/lambda/fn --follow`", "`aws ec2 describe-security-groups` `aws elbv2 describe-target-health` `aws rds describe-db-instances`"],
"Files": ["~/.aws/config ~/.aws/credentials IAM policy JSON, CloudFormation/Terraform files"],
"Architecture": ["Route53 > CloudFront/WAF > ALB > ASG/ECS/EKS > RDS/ElastiCache/S3, across 2+ AZs in private subnets."],
"Ports": ["SSH 22, RDP 3389, HTTP 80, HTTPS 443, MySQL 3306, PostgreSQL 5432, Redis 6379"],
"Differences": ["SG vs NACL; user vs role; S3 vs EBS vs EFS; Multi-AZ vs replica; ALB vs NLB; Lambda vs ECS vs EKS."],
"Troubleshooting commands": ["`aws sts get-caller-identity` > CloudTrail event > SG/NACL/route table > target health > CloudWatch logs > Cost Explorer"],
"Best practices": ["MFA, no root, roles not keys, private subnets, Multi-AZ, encryption, IaC, tagging, budgets, tested backups."]}
),
subs={
"aws-iam-basics": dict(
define=dict(simple="IAM decides who can do what in your AWS account.",
technical="IAM evaluates requests against identity-based policies, resource-based policies, permission boundaries, session policies and Organizations SCPs; explicit deny overrides allow; default is deny.",
why="Control access and provide temporary credentials.", without="Everyone shares root-level access.", use="Always.", avoid="Using the root user or long-lived access keys.", analogy="Building security badges with access levels."),
internals="""A request (principal + action + resource + context) reaches IAM. IAM gathers applicable policies and evaluates: explicit deny? SCP/boundary allow? identity or resource policy allow? If allowed, the action proceeds and CloudTrail logs it. Roles issue temporary credentials through STS `AssumeRole`.""",
config=[("Least-privilege policy explained", """{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": ["s3:GetObject"],
    "Resource": "arn:aws:s3:::my-app-bucket/reports/*",
    "Condition": {"IpAddress": {"aws:SourceIp": "203.0.113.0/24"}}
  }]
}""", [("Effect: Allow", "Grants; without an allow the request is denied."), ("Action", "Only read objects: no put/delete."), ("Resource ARN", "Limited to the reports/ prefix."), ("Condition", "Additional guard by source IP; can also require MFA or tags.")])],
lab=dict(goal="Secure a new account and use a role.", prereq=["AWS account", "AWS CLI v2"],
steps=[("Enable MFA on the root user and create an admin via IAM Identity Center (or an IAM user with MFA) for daily use", "Root is used only for account-level tasks."),
("aws configure sso && aws sts get-caller-identity", "Uses short-lived SSO credentials; the output shows the assumed role ARN."),
("Create a budget with alerts (Billing > Budgets)", "Protects against surprise costs.")]),
compare=[("Identity types", ["Type", "Credential", "Use"], [["Root", "Email + password + MFA", "Account tasks only"], ["IAM user", "Long-term keys", "Legacy/humans (prefer SSO)"], ["IAM role", "Temporary via STS", "Services, cross-account, SSO"]])],
mnemonics=[("Evaluation", "Deny beats Allow; default is Deny")], hinglish="**Root account use mat karo**, MFA lagao. Apps ko **role** do, access keys nahi. Policy mein **sirf jitna zaroori ho utni permission** likho.",
practices={"Security": ["MFA, SSO, least privilege, no wildcards, rotate/eliminate keys, review with Access Analyzer."]}, mistakes={"Security mistakes": ["`Action: *` on `Resource: *`.", "Keys in Git."]},
qa_extra=[("Advanced", "How does cross-account access work?", "Account B role trusts Account A principal; A's identity policy allows `sts:AssumeRole`; A assumes the role and gets temporary credentials.", "IAM depth.", "Central security account auditing others.")]),

"aws-vpc": dict(
define=dict(simple="A VPC is your own private network inside AWS.",
technical="A VPC is a logically isolated CIDR block with subnets per AZ, route tables, an Internet Gateway, NAT gateways, security groups and NACLs.",
why="Network isolation and control.", without="Everything exposed on shared networking.", use="All AWS workloads.", avoid="Overlapping CIDRs across VPCs you may connect.", analogy="Your own fenced compound in a big city."),
internals="""Traffic decisions: route table for the subnet chooses next hop (local, IGW, NAT, peering/TGW). NACL filters at subnet edge (stateless). Security group filters at the instance ENI (stateful). Outbound from private subnet: 0.0.0.0/0 to NAT in a public subnet, which uses an Elastic IP through the IGW.""",
config=[("Route tables explained", """Public route table:  10.0.0.0/16 -> local ; 0.0.0.0/0 -> igw-xxxx
Private route table: 10.0.0.0/16 -> local ; 0.0.0.0/0 -> nat-xxxx
DB route table:      10.0.0.0/16 -> local   (no internet route)""", [("local", "Automatic route for intra-VPC traffic."), ("0.0.0.0/0 -> igw", "Makes a subnet public."), ("0.0.0.0/0 -> nat", "Outbound-only internet for private subnets."), ("No default route", "Fully isolated DB subnet.")])],
lab=dict(goal="Build a VPC with public/private subnets (VPC wizard or Terraform).", prereq=["AWS account", "Budget alert set"],
steps=[("VPC > Create VPC > 'VPC and more' with 2 AZs, 2 public, 2 private, 1 NAT", "Creates subnets, route tables, IGW and NAT (NAT gateway is chargeable: delete afterward)."),
("Launch EC2 in a private subnet using an SSM role and no public IP", "Access via Session Manager: no SSH port open."),
("From the instance: curl -I https://example.com", "Works via NAT. Remove the NAT route and it fails: demonstrates the route table role.")]),
mnemonics=[("Public means", "Route to IGW (not just a public IP)")], hinglish="Subnet **public tab banta hai jab uske route table mein IGW ka route ho**. Private instance ko internet chahiye to **NAT gateway**. DB ko internet route mat do.",
practices={"Security": ["Private subnets for app/DB, SG chaining, VPC endpoints, flow logs."], "Cost Optimization": ["NAT per AZ for HA but consider endpoints to cut cost."]}, mistakes={"DevOps mistakes": ["Too small CIDR.", "Single NAT for a multi-AZ prod."]},
qa_extra=[("Scenario-Based", "How to give private instances access to S3 without NAT?", "Gateway VPC endpoint for S3 with route table entry.", "Cost/security.", "Logs to S3.")]),

"aws-compute-ec2": dict(
define=dict(simple="EC2 gives you virtual servers; Auto Scaling adds/removes them; a load balancer spreads traffic.",
technical="EC2 instances launch from AMIs using launch templates; ASGs maintain capacity across AZs using scaling policies; ELB distributes traffic and performs health checks.",
why="Elastic, resilient compute.", without="Fixed servers that fail or over-provision.", use="Long-running or custom OS workloads.", avoid="Simple event tasks better on Lambda.", analogy="A taxi fleet that grows during rush hour."),
internals="""ASG desired capacity > launches instances from the launch template in chosen subnets > registers them with the target group > ALB health checks mark them healthy > traffic flows. If an instance fails checks, ASG terminates and replaces it. Scaling policies (target tracking) adjust desired capacity based on CloudWatch metrics.""",
config=[("User data bootstrap explained", """#!/bin/bash
dnf install -y nginx
echo "hello from $(hostname)" > /usr/share/nginx/html/index.html
systemctl enable --now nginx""", [("#!/bin/bash", "User data runs once at first boot as root."), ("dnf install", "Amazon Linux 2023 uses dnf (AL2 uses yum)."), ("systemctl enable --now", "Start and persist across reboots.")])],
lab=dict(goal="Launch a web server with an ALB.", prereq=["VPC with 2 public subnets", "Budget alert"],
steps=[("Create launch template with the user data above (t3.micro, AL2023, SG allowing 80 from ALB SG)", "Repeatable instance definition."),
("Create target group (HTTP 80, health check /) and ALB in public subnets", "ALB DNS becomes the entry point."),
("Create ASG min 2/max 4 across two AZs attached to the target group; then terminate one instance", "ASG replaces it automatically: self-healing.")]),
mnemonics=[("ASG trio", "Launch template + ASG + scaling policy")], hinglish="**Instance ko manually mat banao;** Launch template + Auto Scaling group use karo, taaki fail hone par khud replace ho jaye.",
practices={"Security": ["IMDSv2, SSM instead of SSH, instance roles."], "Cost Optimization": ["Savings Plans, Spot, Graviton, right-sizing."]}, mistakes={"Production mistakes": ["Single instance without ASG.", "Manual config drift."]},
versions=["Amazon Linux 2 uses yum; Amazon Linux 2023 uses dnf. Instance families change (t3/t4g/m7g); check availability by region."],
qa_extra=[("Scenario-Based", "Zero-downtime deployment on ASG?", "Use instance refresh or blue/green with new launch template versions, ALB health checks and minimum healthy percentage.", "Release strategy.", "Rolling instance refresh 90%.")]),

"aws-storage-db": dict(
define=dict(simple="S3 stores files, EBS is a server disk, RDS is a managed relational database, DynamoDB is a managed NoSQL database.",
technical="S3 is regional object storage (11 nines durability design); EBS is AZ-bound block storage; RDS runs managed engines with backups, patching and Multi-AZ; DynamoDB is a serverless key-value/document store.",
why="Use the right storage for each data type with managed reliability.", without="Self-managed backups and failover.", use="All data workloads.", avoid="Using EBS as shared storage across AZs.", analogy="S3 = warehouse, EBS = your laptop's SSD, RDS = a database run by a DBA service."),
internals="""RDS Multi-AZ writes synchronously to a standby in another AZ; on failure DNS flips to the standby. Read replicas replicate asynchronously. EBS snapshots are incremental and stored in S3. S3 stores objects redundantly across AZs and offers versioning and lifecycle rules.""",
config=[("S3 lifecycle rule explained", """{
  "Rules": [{
    "ID": "logs",
    "Status": "Enabled",
    "Filter": {"Prefix": "logs/"},
    "Transitions": [{"Days": 30, "StorageClass": "STANDARD_IA"}, {"Days": 90, "StorageClass": "GLACIER"}],
    "Expiration": {"Days": 365}
  }]
}""", [("Filter Prefix", "Applies only to logs/."), ("Transitions", "Cheaper storage classes over time."), ("Expiration", "Delete after a year to control cost.")])],
lab=dict(goal="Use S3 and create a snapshot.", prereq=["AWS CLI configured"],
steps=[("aws s3 mb s3://my-unique-bucket-12345 && echo hi > a.txt && aws s3 cp a.txt s3://my-unique-bucket-12345/", "Creates a bucket (Block Public Access is on by default) and uploads."),
("aws s3api put-bucket-versioning --bucket my-unique-bucket-12345 --versioning-configuration Status=Enabled", "Protects against accidental deletes."),
("aws s3 rb s3://my-unique-bucket-12345 --force", "Cleanup to avoid charges.")]),
mnemonics=[("Choose storage", "Object=S3, Block=EBS, File=EFS, SQL=RDS, Key-value=DynamoDB")], hinglish="**Database ko RDS Multi-AZ** mein chalao, backups on rakho aur **restore test** karo. S3 bucket kabhi public mat rakho.",
practices={"Security": ["Encryption at rest/in transit, private access, Block Public Access."], "Backup & Disaster Recovery": ["Automated backups, snapshots, versioning, cross-region copy."]}, mistakes={"Production mistakes": ["No restore test.", "Public bucket or DB."]},
qa_extra=[("Scenario-Based", "How to restore an accidentally deleted S3 object?", "If versioning was on, remove the delete marker or restore a previous version; otherwise restore from backup/replication.", "Data protection.", "Enable versioning up front.")]),

"aws-serverless-monitoring": dict(
define=dict(simple="Lambda runs code without servers; ECS/EKS run containers; CloudWatch watches everything; cost tools control spending.",
technical="Lambda executes functions per event with managed scaling; ECS/EKS orchestrate containers (EC2 or Fargate); CloudWatch provides metrics, logs, alarms and dashboards; Cost Explorer/Budgets track spend.",
why="Reduce operations and control cost.", without="Idle servers and blind operations.", use="Event-driven tasks (Lambda), container workloads (ECS/EKS).", avoid="Lambda for long-running (>15 min) or steady heavy compute.", analogy="Lambda is a taxi you pay per ride; EC2 is a car you own."),
internals="""An event (S3 upload, API Gateway request, schedule) invokes Lambda; AWS starts an execution environment (cold start) if none is warm, runs your handler with the function's IAM role, and logs to CloudWatch Logs. CloudWatch alarms evaluate metrics and trigger SNS/Auto Scaling actions.""",
config=[("Lambda handler explained", """import json, os

def handler(event, context):
    name = event.get("name", "world")
    print(json.dumps({"msg": "invoked", "name": name}))
    return {"statusCode": 200, "body": f"hello {name}"}""", [("handler(event, context)", "Entry point; `event` holds trigger data."), ("print(json...)", "Goes to CloudWatch Logs (structured logging)."), ("Return dict", "API Gateway proxy response format.")])],
lab=dict(goal="Create a Lambda and a CloudWatch alarm.", prereq=["AWS account", "CLI"],
steps=[("Create a function in the console (Python), paste the handler, Test with {\"name\":\"devops\"}", "See the response and logs."),
("aws logs tail /aws/lambda/<function> --follow", "Live logs."),
("Set a budget alert and a Lambda Errors alarm to SNS email", "Operational safety net.")]),
compare=[("Lambda vs ECS Fargate vs EKS", ["Topic", "Lambda", "ECS Fargate", "EKS"], [["Unit", "Function", "Container task", "Pod"], ["Ops effort", "Lowest", "Low", "Higher"], ["Best for", "Event-driven", "Simple containers", "Kubernetes ecosystem"]])],
mnemonics=[("Monitoring", "Metrics, Logs, Alarms, Dashboards")], hinglish="**Lambda** chhote event-driven kaam ke liye. **CloudWatch alarms** aur **Budgets** lagana mat bhoolo.",
practices={"Cost Optimization": ["Right-size memory, use Savings Plans, Fargate Spot, budgets and anomaly detection."], "Monitoring & Logging": ["Structured logs, alarms on errors/latency, X-Ray tracing."]}, mistakes={"Production mistakes": ["No alarms.", "Unbounded Lambda concurrency hitting the database."]},
versions=["Lambda runtimes are deprecated on a schedule: check supported Python/Node versions. Limits (timeout, memory, package size) change: see AWS docs."],
qa_extra=[("Troubleshooting-Based", "Lambda has high latency on the first request.", "Cold start: reduce package size, use provisioned concurrency, avoid heavy init, avoid VPC where unnecessary.", "Serverless performance.", "Provisioned concurrency for APIs.")])
})
