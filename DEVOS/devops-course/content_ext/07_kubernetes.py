EXT = dict(
guide=dict(
bigpicture=dict(
problem="""**Problem it solves:** Docker runs containers on one machine. In production you need dozens or hundreds of containers across many servers. Who restarts a crashed container? Who spreads load? Who does rolling updates without downtime? **Kubernetes (K8s)** is the container orchestrator that does this automatically: you declare the **desired state** ("run 3 copies of this image") and Kubernetes keeps reality equal to it.""",
chain=["PROBLEM: many containers on many servers must stay up, scale and update safely",
       "TRADITIONAL APPROACH: shell scripts, manual `docker run` on each host, hand-made load balancers",
       "PAIN: a node dies and apps stay down, manual scaling, downtime during deploys, no service discovery",
       "TECHNOLOGY: Kubernetes (control plane + worker nodes + controllers)",
       "SOLUTION: declarative YAML; controllers reconcile desired vs actual state continuously",
       "REAL-WORLD BENEFIT: self-healing, autoscaling, rolling updates/rollback, portable across clouds"],
text="""Container vs Kubernetes: a container is one packaged process; Kubernetes is the system that schedules, connects, scales and heals many containers. Kubernetes does not build images; it runs them."""),
e2e=dict(diagram="""kubectl apply -f deploy.yaml
      |
      v
API Server (authenticate, authorize, validate)
      |
      v
etcd (stores desired state)
      |
      v
Controller Manager (Deployment > ReplicaSet > Pods needed)
      |
      v
Scheduler (picks a node for each Pod)
      |
      v
kubelet on node (talks to container runtime, starts containers)
      |
      v
Container runtime (containerd) pulls image, runs container
      |
      v
kube-proxy / CNI (Service networking) -> Application reachable
      |
      v
Controllers keep comparing DESIRED vs ACTUAL and fix any difference""",
text="""`kubectl` sends your YAML to the **API Server**, the only component that talks to **etcd** (the cluster database). The API server authenticates you (who are you), authorizes (RBAC: are you allowed) and validates the object. The **Deployment controller** inside the **controller manager** notices "desired 3 replicas, actual 0" and creates a ReplicaSet, which creates 3 Pod objects. The **scheduler** assigns each unscheduled Pod to a node based on resources, taints and affinity. The **kubelet** on that node sees a Pod assigned to it, asks the container runtime (containerd) to pull the image and start containers, and reports status back. **kube-proxy** (or the CNI plugin) programs rules so a **Service** IP load-balances to the Pods. This loop never stops: if a Pod dies, the ReplicaSet controller creates a new one. That is **self-healing**."""),
tools=dict(rows=[
["kubectl", "CLI for the API", "YAML / commands", "Cluster changes", "Admin and CI"],
["kubeadm / EKS / GKE / AKS / kind / minikube", "Create clusters", "Nodes/cloud account", "Running cluster", "Lab or production"],
["Helm", "Package manager for K8s (templated YAML)", "Chart + values.yaml", "Rendered manifests / release", "Deploy apps and versions"],
["Kustomize", "Overlay-based config", "Base + overlays", "Patched manifests", "Env differences"],
["ArgoCD / Flux", "GitOps controller", "Git repo", "Cluster in sync with Git", "CD for Kubernetes"],
["Ingress controller (NGINX/ALB)", "L7 routing into cluster", "Ingress objects", "HTTP(S) routing", "Edge traffic"],
["Prometheus + Grafana", "Metrics and dashboards", "kube-state-metrics, node exporter", "Graphs, alerts", "Monitoring"],
["Kyverno / OPA Gatekeeper", "Policy engine", "Admission requests", "Allow/deny/mutate", "Security guardrails"]],
why="**Compose vs Kubernetes:** Compose is single-host; Kubernetes is multi-node with self-healing and scaling. **Helm vs Kustomize:** Helm templates and versions releases; Kustomize patches plain YAML without templates. **Managed (EKS) vs self-managed (kubeadm):** managed clouds run the control plane for you (less ops); self-managed gives full control but you own upgrades and etcd backups."),
compare=[
("Pod vs Container", ["Topic", "Pod", "Container"], [["What", "Smallest deployable unit; 1+ containers", "A single packaged process"], ["Shared", "Network namespace (one IP), volumes", "Own filesystem/process"], ["Lifecycle", "Ephemeral; replaced not repaired", "Lives inside a Pod"]]),
("Deployment vs StatefulSet vs DaemonSet", ["Topic", "Deployment", "StatefulSet", "DaemonSet"], [["Use for", "Stateless apps", "Databases, Kafka (stable identity)", "One Pod per node (log/monitor agents)"], ["Pod names", "Random suffix", "Ordered: name-0, name-1", "One per node"], ["Storage", "Shared/none", "Per-Pod PVC", "Usually hostPath"], ["Scaling", "Any order", "Ordered", "Follows nodes"]]),
("Service types", ["Type", "Reachable from", "Use"], [["ClusterIP", "Inside cluster only", "Internal service-to-service"], ["NodePort", "NodeIP:30000-32767", "Simple external access / labs"], ["LoadBalancer", "Cloud load balancer IP", "Public service on cloud"], ["ExternalName", "DNS CNAME", "Map to external service"]]),
("Service vs Ingress", ["Topic", "Service", "Ingress"], [["Layer", "L4 (TCP/UDP)", "L7 (HTTP/HTTPS host/path)"], ["Purpose", "Stable virtual IP for Pods", "Route many hosts/paths through one entry point, TLS"], ["Needs", "kube-proxy/CNI", "An Ingress controller"]]),
("ConfigMap vs Secret", ["Topic", "ConfigMap", "Secret"], [["Data", "Non-sensitive config", "Sensitive data"], ["Encoding", "Plain text", "Base64 (NOT encryption)"], ["Hardening", "-", "Enable encryption at rest, RBAC, external secret store"]]),
("Rolling vs Blue/Green vs Canary", ["Topic", "Rolling", "Blue/Green", "Canary"], [["How", "Replace Pods gradually", "Two full environments, switch traffic", "Send small % to new version"], ["Rollback", "`kubectl rollout undo`", "Switch back instantly", "Set weight to 0"], ["Cost", "Low", "2x resources", "Low-medium"], ["Native support", "Deployment default", "Via Service selector/Argo Rollouts", "Via ingress/mesh/Argo Rollouts"]])],
troubleshooting=[
("Pod stuck in Pending", "Not enough CPU/memory, node taints, unbound PVC, nodeSelector mismatch", "`kubectl describe pod X` (Events), `kubectl get nodes`, `kubectl get pvc`", "Add nodes/resources, fix requests, add tolerations, bind PVC.", "Right-size requests; use cluster autoscaler."),
("ImagePullBackOff / ErrImagePull", "Wrong image/tag, private registry without imagePullSecret, rate limit", "`kubectl describe pod X`; `kubectl get events`", "Fix image name/tag, create `docker-registry` secret and reference it.", "Pin tags, use private registry with credentials."),
("CrashLoopBackOff", "App exits at start: bad config, missing env/secret, failing probe, OOM", "`kubectl logs X --previous`, `kubectl describe pod X` (Last State, Exit Code)", "Fix config/command; raise memory limit if OOMKilled (137); fix liveness probe.", "Test image locally; use startupProbe for slow apps."),
("Service not reachable", "Selector does not match Pod labels, wrong targetPort, no ready endpoints, NetworkPolicy", "`kubectl get endpoints svc`, `kubectl get pods --show-labels`, `kubectl exec -it pod -- curl svc:port`", "Match labels/ports; fix readiness probe; adjust NetworkPolicy.", "Use consistent labels and templates (Helm)."),
("Ingress returns 404/502", "Wrong host/path, backend service/port wrong, controller not installed, unhealthy backend", "`kubectl describe ingress`, controller logs, `kubectl get endpoints`", "Fix rules and service port; ensure controller and IngressClass exist.", "Smoke test after deploy."),
("Node NotReady", "kubelet down, disk/memory pressure, network problem", "`kubectl describe node`, `journalctl -u kubelet` on node", "Restart kubelet, free disk, replace node.", "Node monitoring, autoscaling group health checks.")],
practices={
"Development": ["Use kind/minikube locally; `kubectl diff` and `--dry-run=client -o yaml` before applying."],
"Production": ["Always set resource requests and limits.", "Liveness, readiness and startup probes.", "At least 2-3 replicas with PodDisruptionBudget and anti-affinity across zones.", "Namespaces per team/env; labels everywhere; pin image tags."],
"Security": ["RBAC least privilege, dedicated ServiceAccounts.", "NetworkPolicy default-deny.", "Pod Security Standards (restricted), non-root, read-only root FS.", "Secrets from an external store (External Secrets/Vault); encrypt etcd.", "Scan images; admission policies (Kyverno/OPA)."],
"Performance": ["HPA for scaling, right-sized requests, topology spread, node autoscaling."],
"Reliability": ["Rolling update with maxUnavailable=0 for critical services; PDBs; multi-AZ; backup etcd/Velero."],
"Cost Optimization": ["Right-size requests, Spot nodes for stateless workloads, cluster autoscaler/Karpenter, delete idle namespaces."],
"Monitoring & Logging": ["Prometheus + kube-state-metrics + Grafana; Loki/ELK for logs; alert on Pod restarts, Pending Pods, node pressure."],
"Backup & Disaster Recovery": ["etcd snapshots (self-managed), Velero for resources and volumes, GitOps repo as source of truth."]},
mistakes={
"Beginner mistakes": ["Using bare Pods instead of Deployments.", "Editing objects by hand instead of YAML in Git.", "Using `latest` tag."],
"Developer mistakes": ["No readiness probe so traffic hits a starting Pod.", "Hard-coding config instead of ConfigMap/Secret."],
"DevOps mistakes": ["No requests/limits (noisy neighbours, evictions).", "Giving cluster-admin to everyone."],
"Production mistakes": ["Single replica for critical services.", "No backups of persistent volumes.", "Skipping version upgrades until unsupported."],
"Security mistakes": ["Treating base64 Secrets as encrypted.", "Running privileged/root Pods.", "No NetworkPolicy so any Pod can talk to any Pod."]},
versions=[
"Kubernetes releases about 3 times a year and supports roughly the latest three minor versions; check kubernetes.io for the current list.",
"Dockershim was removed in v1.24: nodes use containerd or CRI-O; `docker` commands on nodes do not show K8s containers (use `crictl`).",
"PodSecurityPolicy was removed in v1.25; use Pod Security Admission or Kyverno/OPA.",
"`apiVersion` values change (for example `extensions/v1beta1` Ingress was removed): use `networking.k8s.io/v1` and run `kubectl explain` / `kubectl api-resources` for your cluster.",
"Managed clusters (EKS/GKE/AKS) differ in load balancer annotations, storage classes and IAM integration."],
hinglish="""Kubernetes **containers ka manager** hai. Tum bas batate ho **desired state** (jaise "3 replicas chalao"), aur Kubernetes ke **controllers** continuously check karte hain ki **actual state** wahi hai ya nahi. Pod mar jaye to naya bana deta hai (**self-healing**). **API Server** cluster ka darwaza hai, **etcd** uska database, **scheduler** decide karta hai Pod kis node par chalega, aur **kubelet** node par container chalata hai. Service Pods ko ek stable IP deti hai, Ingress bahar se HTTP traffic route karta hai.""",
mnemonics=[
("Control plane", "A-E-S-C: API server, etcd, Scheduler, Controller manager"),
("Worker node", "K-K-R: kubelet, kube-proxy, Runtime"),
("Reconciliation", "Desired (YAML) == Actual (cluster)? If not, controller acts."),
("Service types", "C-N-L: ClusterIP < NodePort < LoadBalancer (each builds on the previous)"),
("Probes", "Liveness = restart me; Readiness = send me traffic; Startup = wait for me")],
client=dict(
s30="""Kubernetes is the platform that runs our containerised applications reliably in production. You tell it what you want, for example three copies of the app, and it keeps that true: it restarts failures, scales with traffic and updates without downtime.""",
m2="""Docker packages applications, but in production you need something to run them across many servers. Kubernetes schedules containers onto machines, restarts them if they fail, spreads traffic between copies and performs rolling updates so users see no downtime. Everything is described in version-controlled YAML, so environments are repeatable and auditable. For the business this means higher availability, faster releases, easy scaling during peak load and less vendor lock-in because it runs on any cloud. The trade-off is operational complexity, which is why we often use a managed service such as EKS.""",
m5="""I will cover four points. **One, architecture:** a control plane (API server, etcd, scheduler, controllers) decides what should run; worker nodes with kubelet run it. **Two, how we deploy:** the application is a Deployment with resource requests/limits and health probes, exposed through a Service and Ingress with TLS, with configuration in ConfigMaps and secrets from a secret manager. **Three, delivery:** the CI pipeline builds, tests, scans and pushes an image; ArgoCD or Helm updates the cluster from Git, using rolling updates with automatic rollback. **Four, operations and security:** autoscaling (HPA and node autoscaling), monitoring with Prometheus and Grafana, RBAC and network policies, backups, and regular version upgrades. The result is a platform that self-heals, scales and can be audited, and the team ships changes many times a day with lower risk."""),
roadmap=[
("Beginner", ["Containers/Docker first", "Cluster architecture", "kubectl basics", "Pods, Deployments, Services"]),
("Intermediate", ["ConfigMaps, Secrets", "Ingress", "PV/PVC/StorageClass", "Probes, requests/limits", "Namespaces, labels"]),
("Advanced", ["HPA/VPA/Cluster Autoscaler", "Scheduling: taints, affinity, topology", "RBAC, NetworkPolicy, Pod Security", "StatefulSets, Jobs, DaemonSets", "Helm, Kustomize, GitOps"]),
("Production", ["Multi-AZ HA, PDB", "Monitoring/logging/alerting", "Backup with Velero, upgrades", "Cost control"]),
("Interview", ["Explain kubectl apply flow", "Debug CrashLoopBackOff / Pending / 502", "Design HA app on EKS", "Compare deployment strategies"])],
miniproject=dict(title="Deploy a 3-tier app to Kubernetes with Ingress, HPA and Prometheus",
arch="""Internet -> Ingress (TLS) -> Service web -> Deployment web (3 pods)
                                   -> Service api -> Deployment api (HPA 2-10)
                                                       -> Service db  -> StatefulSet postgres (PVC)
                                                       -> Service redis
Pipeline: Git > CI (build, test, scan) > Harbor/ECR > ArgoCD > Cluster > Prometheus/Grafana""",
steps=[
("Step 1: Local cluster", """kind create cluster --name demo
kubectl cluster-info
kubectl create namespace shop""", "Creates a local cluster in Docker and a namespace. On EKS/GKE the cluster already exists."),
("Step 2: API Deployment + Service", """apiVersion: apps/v1
kind: Deployment
metadata: { name: api, namespace: shop }
spec:
  replicas: 3
  selector: { matchLabels: { app: api } }
  strategy: { type: RollingUpdate, rollingUpdate: { maxUnavailable: 0, maxSurge: 1 } }
  template:
    metadata: { labels: { app: api } }
    spec:
      containers:
      - name: api
        image: myrepo/api:1.0.0
        ports: [{ containerPort: 3000 }]
        envFrom: [{ configMapRef: { name: api-config } }, { secretRef: { name: api-secret } }]
        resources: { requests: { cpu: 100m, memory: 128Mi }, limits: { cpu: 500m, memory: 256Mi } }
        readinessProbe: { httpGet: { path: /health, port: 3000 }, periodSeconds: 5 }
        livenessProbe: { httpGet: { path: /health, port: 3000 }, initialDelaySeconds: 15 }
---
apiVersion: v1
kind: Service
metadata: { name: api, namespace: shop }
spec:
  selector: { app: api }
  ports: [{ port: 80, targetPort: 3000 }]""", "The Deployment keeps 3 Pods, rolls out with zero unavailable Pods, and only sends traffic to Pods passing `readinessProbe`. `selector` must match the Pod `labels`, otherwise the Service has no endpoints. `port` is the Service port, `targetPort` the container port."),
("Step 3: Ingress + HPA", """apiVersion: networking.k8s.io/v1
kind: Ingress
metadata: { name: shop, namespace: shop }
spec:
  ingressClassName: nginx
  rules:
  - host: shop.example.com
    http:
      paths:
      - { path: /api, pathType: Prefix, backend: { service: { name: api, port: { number: 80 } } } }
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata: { name: api, namespace: shop }
spec:
  scaleTargetRef: { apiVersion: apps/v1, kind: Deployment, name: api }
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource: { name: cpu, target: { type: Utilization, averageUtilization: 70 } }""", "Ingress routes `shop.example.com/api` to the api Service (needs an ingress controller installed). HPA scales between 2 and 10 Pods to keep average CPU near 70% of requests (needs metrics-server)."),
("Step 4: Apply, verify, roll back", """kubectl apply -f k8s/
kubectl -n shop get pods,svc,ingress,hpa
kubectl -n shop rollout status deploy/api
kubectl -n shop set image deploy/api api=myrepo/api:1.1.0
kubectl -n shop rollout undo deploy/api""", "Apply manifests, check status, perform a rolling update by changing the image and roll back if the new version misbehaves. In production ArgoCD does the apply from Git.")]),
interview=[
("Beginner", "What is Kubernetes?", "An open-source container orchestration platform that schedules, scales, heals and updates containerised apps across a cluster.", "Foundation question.", "Running 50 microservices across 10 nodes."),
("Beginner", "What is a Pod?", "The smallest deployable unit: one or more containers sharing network and storage.", "Core object.", "App container + sidecar log shipper in one Pod."),
("Beginner", "What is a Deployment?", "A controller that manages ReplicaSets/Pods, providing scaling, rolling updates and rollback.", "How stateless apps are run.", "`kubectl create deployment web --image=nginx --replicas=3`."),
("Beginner", "What is a Service?", "A stable virtual IP/DNS name that load-balances to a set of Pods chosen by label selector.", "Pods are ephemeral with changing IPs.", "`api.shop.svc.cluster.local`."),
("Beginner", "What is a Namespace?", "A virtual partition of a cluster for isolation, quotas and RBAC.", "Multi-team/env usage.", "dev, staging, prod namespaces."),
("Beginner", "What are labels and selectors?", "Key-value tags on objects; selectors query them. Services and Deployments use them to find Pods.", "Glue of Kubernetes.", "`app=api` label matches Service selector."),
("Beginner", "What is kubectl?", "The CLI client for the Kubernetes API.", "Daily tool.", "`kubectl get pods -A`."),
("Beginner", "ConfigMap vs Secret?", "ConfigMap holds non-sensitive config; Secret holds sensitive data (base64-encoded, not encrypted by default).", "Config and security.", "DB host in ConfigMap, DB password in Secret."),
("Beginner", "What is self-healing?", "Controllers replace failed Pods, restart failing containers and reschedule from dead nodes.", "Main K8s benefit.", "Delete a Pod and watch the ReplicaSet create a new one."),
("Beginner", "What is the difference between kubectl apply and create?", "`create` fails if the object exists; `apply` is declarative and updates to match the file.", "GitOps friendliness.", "Re-running `apply -f` in CI."),
("Intermediate", "Explain Kubernetes architecture.", "Control plane: API server, etcd, scheduler, controller manager (and cloud controller). Nodes: kubelet, kube-proxy, container runtime.", "Tests component knowledge.", "On EKS the control plane is managed by AWS."),
("Intermediate", "What happens when you run kubectl apply?", "Request to API server > authN/authZ/admission > stored in etcd > controllers create ReplicaSet/Pods > scheduler assigns node > kubelet starts containers > status reported.", "End-to-end flow.", "See e2e diagram."),
("Intermediate", "Service types?", "ClusterIP, NodePort, LoadBalancer, ExternalName (and headless with clusterIP: None).", "Networking basics.", "LoadBalancer creates an AWS ELB on EKS."),
("Intermediate", "Ingress vs LoadBalancer Service?", "Each LoadBalancer Service creates one cloud LB (L4); Ingress shares one entry point with host/path routing and TLS (L7) via a controller.", "Cost and design.", "One ALB for 20 services."),
("Intermediate", "Liveness vs readiness vs startup probe?", "Liveness restarts a hung container; readiness removes the Pod from Service endpoints; startup delays the other probes for slow starters.", "Reliability.", "Java app needs a startup probe."),
("Intermediate", "Requests vs limits?", "Requests are used by the scheduler and guarantee minimum resources; limits cap usage (CPU throttled, memory OOMKilled).", "Resource management.", "Request 100m, limit 500m CPU."),
("Intermediate", "How does a rolling update work?", "Deployment creates a new ReplicaSet, scaling it up while scaling the old one down within maxSurge/maxUnavailable, gated by readiness.", "Zero-downtime deploys.", "`kubectl rollout status`."),
("Intermediate", "How to roll back?", "`kubectl rollout undo deployment/api` (or `--to-revision`); GitOps: revert the commit.", "Release safety.", "Bad image tag rolled back in seconds."),
("Intermediate", "PV, PVC and StorageClass?", "PV is storage; PVC is a request for storage; StorageClass enables dynamic provisioning.", "Stateful workloads.", "EBS volume for Postgres via gp3 StorageClass."),
("Intermediate", "StatefulSet vs Deployment?", "StatefulSet gives stable network identity, ordered rollout and per-Pod persistent volumes.", "Databases.", "kafka-0, kafka-1, kafka-2."),
("Intermediate", "What is HPA?", "HorizontalPodAutoscaler scales replicas from metrics such as CPU (needs metrics-server).", "Elasticity.", "Scale 2 to 10 Pods at 70% CPU."),
("Intermediate", "What is a DaemonSet?", "Ensures one Pod runs on every (or selected) node.", "Node agents.", "Fluent Bit, node-exporter."),
("Intermediate", "Jobs and CronJobs?", "Job runs to completion; CronJob runs Jobs on a schedule.", "Batch tasks.", "Nightly DB backup."),
("Intermediate", "How do Pods discover services?", "CoreDNS provides `svc.namespace.svc.cluster.local`; env vars are also injected.", "Service discovery.", "API calls `http://db:5432`."),
("Intermediate", "What is Helm?", "Package manager using charts with templates and values.yaml; supports releases, upgrades and rollbacks.", "Reusable deployments.", "`helm upgrade --install api ./chart -f prod.yaml`."),
("Advanced", "What does etcd do and how do you protect it?", "Consistent key-value store holding all cluster state. Protect with TLS, restricted access, regular snapshots, encryption at rest and 3/5 member HA.", "Cluster recovery.", "`etcdctl snapshot save`."),
("Advanced", "Explain the scheduler's decision process.", "Filter nodes (resources, taints, affinity, selectors) then score and choose the best; bind Pod to node.", "Placement control.", "Use nodeAffinity for GPU nodes."),
("Advanced", "Taints and tolerations vs affinity?", "Taints repel Pods unless tolerated; affinity attracts Pods to nodes/Pods. Use taints to reserve nodes, affinity to prefer placement.", "Scheduling design.", "Taint spot nodes; only batch Pods tolerate."),
("Advanced", "How does kube-proxy implement Services?", "Programs iptables or IPVS rules on each node to DNAT Service IPs to Pod endpoints (some CNIs like Cilium replace it with eBPF).", "Networking internals.", "`iptables -t nat -L KUBE-SERVICES`."),
("Advanced", "CNI and Pod networking model?", "Every Pod gets its own IP and can reach every other Pod without NAT; a CNI plugin (Calico, Cilium, AWS VPC CNI) implements it.", "Networking depth.", "AWS VPC CNI assigns VPC IPs to Pods."),
("Advanced", "RBAC components?", "Role/ClusterRole define permissions; RoleBinding/ClusterRoleBinding bind them to users, groups or ServiceAccounts.", "Security.", "CI ServiceAccount allowed only to patch Deployments in one namespace."),
("Advanced", "How to secure a cluster?", "RBAC least privilege, NetworkPolicy, Pod Security Standards, secrets encryption/external secrets, image scanning and signing, admission policies, audit logs, regular upgrades.", "Defence in depth.", "Kyverno blocks privileged Pods."),
("Advanced", "PodDisruptionBudget?", "Limits voluntary disruptions (drains, upgrades) so a minimum number of Pods stay available.", "Safe node maintenance.", "minAvailable: 2 for api."),
("Advanced", "What is a Custom Resource / Operator?", "CRDs extend the API; an operator is a controller that manages an app's lifecycle using CRDs.", "Extensibility.", "Postgres operator creates HA clusters."),
("Advanced", "Cluster autoscaler vs Karpenter vs HPA?", "HPA scales Pods; Cluster Autoscaler/Karpenter add/remove nodes for pending Pods.", "Full autoscaling story.", "HPA adds Pods, then nodes are added."),
("Advanced", "How do you upgrade a cluster with zero downtime?", "Upgrade control plane first, then nodes one by one (cordon, drain respecting PDBs), check API deprecations beforehand, test in staging.", "Operational maturity.", "EKS managed node group rolling upgrade."),
("Advanced", "What is a sidecar and service mesh?", "Sidecar is a helper container in the Pod; a service mesh (Istio/Linkerd) uses sidecars/eBPF for mTLS, retries and traffic shifting.", "Advanced networking.", "Canary via Istio VirtualService."),
("Advanced", "Explain the Kubernetes API request lifecycle.", "AuthN > AuthZ (RBAC) > Mutating admission > Schema validation > Validating admission > persist to etcd > watchers notified.", "Security/policy hooks.", "Kyverno is an admission webhook."),
("Advanced", "Difference between Deployment `Recreate` and `RollingUpdate`?", "Recreate kills all old Pods first (downtime); RollingUpdate replaces gradually.", "Strategy choice.", "Recreate for apps that cannot run two versions."),
("Scenario-Based", "Design HA deployment for a critical API.", "3+ replicas across AZs (topologySpreadConstraints), PDB, readiness/liveness probes, HPA, resource requests, rolling update maxUnavailable 0, multi-AZ nodes, monitoring and alerts.", "Design thinking.", "Zone failure leaves 2/3 Pods running."),
("Scenario-Based", "Zero-downtime deployment requirements?", "Readiness probes, rolling update, preStop hook/graceful shutdown, enough replicas, PDB, connection draining at LB.", "Detail matters.", "Users saw 502s until preStop sleep added."),
("Scenario-Based", "Traffic spikes on Black Friday.", "HPA with sane limits, cluster autoscaler/Karpenter, pre-scale, cache, load test, PDBs.", "Scaling plan.", "Pre-scale replicas at 8am."),
("Scenario-Based", "A namespace consumes all cluster resources.", "ResourceQuota and LimitRange per namespace, requests/limits mandatory via policy.", "Multi-tenant fairness.", "Dev team's job consumed 90% CPU."),
("Scenario-Based", "Secrets committed to Git.", "Rotate immediately, purge history, use Sealed Secrets/External Secrets/SOPS, add secret scanning.", "Security response.", "Gitleaks in CI."),
("Scenario-Based", "Move from Compose to Kubernetes.", "Translate services to Deployments/Services, config to ConfigMaps/Secrets, volumes to PVCs, add probes/limits, Ingress, CI/CD, migrate step by step (Kompose helps as a start).", "Migration path.", "Start with stateless services."),
("Scenario-Based", "Database on Kubernetes or managed?", "Prefer managed (RDS) for reliability and backups; run in-cluster only with an operator, PVs, backups and expertise.", "Judgement.", "Postgres via CloudNativePG operator vs RDS."),
("Scenario-Based", "Multi-environment configuration.", "Same image, per-env values (Helm values/Kustomize overlays), namespaces, GitOps promotion.", "Environment parity.", "values-dev.yaml, values-prod.yaml."),
("Scenario-Based", "Restrict who can deploy to prod.", "RBAC + GitOps: only ArgoCD ServiceAccount writes to prod, humans via PR approval, branch protection.", "Governance.", "Prod repo requires 2 approvals."),
("Scenario-Based", "Reduce cluster cost by 30%.", "Right-size requests using metrics, Spot nodes, autoscaler, delete unused resources, schedule dev clusters off-hours.", "FinOps.", "Karpenter consolidation."),
("Scenario-Based", "Need to run a batch job every night.", "CronJob with concurrencyPolicy Forbid, backoffLimit, resource limits, history limits, alert on failure.", "Batch workloads.", "Report generator."),
("Scenario-Based", "Application needs to talk to AWS S3 securely.", "Use IRSA/Pod Identity (IAM role for ServiceAccount) instead of static keys.", "Cloud integration.", "S3 read-only role on the api ServiceAccount."),
("Scenario-Based", "Isolate database from other Pods.", "NetworkPolicy default deny and allow only api Pods to port 5432.", "Zero-trust networking.", "Requires a CNI that enforces policy (Calico/Cilium)."),
("Scenario-Based", "Blue/green on Kubernetes.", "Two Deployments (blue/green) and switch the Service selector or use Argo Rollouts/ingress weights; keep old version for quick rollback.", "Release strategy.", "Change selector version: green."),
("Scenario-Based", "Observe a microservice slow response.", "Check Pod CPU throttling, HPA, DB latency, use traces/metrics/logs, compare RED metrics.", "Observability.", "CPU limit too low causing throttling."),
("Troubleshooting-Based", "Pod is Pending.", "`kubectl describe pod` Events: insufficient resources, taints, PVC unbound, nodeSelector. Fix accordingly.", "Scheduling issues.", "0/3 nodes are available: Insufficient memory."),
("Troubleshooting-Based", "CrashLoopBackOff.", "`kubectl logs --previous`, describe for exit code, check env/Secrets/probes/OOM.", "Most common failure.", "Missing DB_URL env variable."),
("Troubleshooting-Based", "ImagePullBackOff.", "Check image name/tag, imagePullSecret, registry reachability and rate limits.", "Registry issues.", "Typo in tag."),
("Troubleshooting-Based", "Service has no endpoints.", "Selector/label mismatch or Pods not ready. `kubectl get endpoints`, `--show-labels`.", "Networking basics.", "Label `app: api` vs `app: apis`."),
("Troubleshooting-Based", "OOMKilled Pod.", "Exit code 137/`OOMKilled` in describe. Increase memory limit or fix leak; check requests.", "Resource limits.", "Node app heap exceeded 256Mi."),
("Troubleshooting-Based", "Ingress 502/503.", "Backend Pods not ready or wrong port; check controller logs, endpoints, service targetPort.", "L7 debugging.", "targetPort 8080 vs app 3000."),
("Troubleshooting-Based", "Node NotReady.", "`kubectl describe node`, kubelet logs, disk/memory pressure, CNI issues; cordon/drain and replace.", "Node health.", "Disk full from logs."),
("Troubleshooting-Based", "kubectl: Unauthorized/Forbidden.", "Check kubeconfig context/credentials (Unauthorized) and RBAC with `kubectl auth can-i` (Forbidden).", "AuthN vs AuthZ.", "Expired EKS token."),
("Troubleshooting-Based", "Rollout stuck.", "`kubectl rollout status`, new Pods not ready (probe, image, quota); `rollout undo`.", "Deployment debugging.", "Readiness probe path wrong."),
("Troubleshooting-Based", "DNS not resolving inside Pods.", "Check CoreDNS Pods/logs, `kubectl exec -- nslookup svc`, NetworkPolicy blocking UDP 53.", "Cluster DNS.", "CoreDNS OOM.")],
cheatsheet={
"Definitions": ["Pod: smallest unit. Deployment: manages stateless Pods. Service: stable virtual IP. Ingress: HTTP routing. ConfigMap/Secret: config.", "Desired state vs actual state: controllers reconcile.", "PV/PVC/StorageClass: persistent storage."],
"Commands": ["`kubectl get pods|svc|deploy|nodes -A -o wide`", "`kubectl describe pod X` | `kubectl logs X [-f --previous]` | `kubectl exec -it X -- sh`", "`kubectl apply -f file.yaml` | `kubectl delete -f file.yaml` | `kubectl diff -f`", "`kubectl scale deploy X --replicas=5` | `kubectl set image deploy/X c=img:tag`", "`kubectl rollout status|history|undo deploy/X`", "`kubectl port-forward svc/X 8080:80` | `kubectl top pods|nodes`", "`kubectl config get-contexts` | `kubectl config use-context X` | `kubectl auth can-i verb resource`", "`kubectl explain pod.spec` | `kubectl api-resources`"],
"Files": ["Deployment/Service/Ingress/ConfigMap/Secret/HPA YAML", "~/.kube/config", "Helm: Chart.yaml, values.yaml, templates/"],
"Architecture": ["kubectl > API server > etcd; scheduler; controller manager > kubelet > runtime; kube-proxy/CNI."],
"Ports": ["API server 6443, etcd 2379-2380, kubelet 10250, NodePort 30000-32767, Ingress 80/443"],
"Differences": ["Pod vs container; Deployment vs StatefulSet vs DaemonSet; ClusterIP vs NodePort vs LoadBalancer; Service vs Ingress; requests vs limits; liveness vs readiness."],
"Troubleshooting commands": ["`kubectl get events --sort-by=.lastTimestamp` > `describe` > `logs --previous` > `get endpoints` > `exec curl` > `top` > `describe node`"],
"Best practices": ["Requests/limits, probes, 3 replicas across AZs, PDB, RBAC, NetworkPolicy, secrets in external store, GitOps, monitoring, backups, regular upgrades."]}
),
subs={
"k8s-architecture": dict(
define=dict(simple="A Kubernetes cluster is a group of machines (nodes) managed by a brain (control plane).",
technical="Kubernetes is a declarative, API-driven container orchestrator: a control plane (kube-apiserver, etcd, kube-scheduler, kube-controller-manager) maintains desired state while nodes run kubelet, kube-proxy and a CRI runtime.",
why="To automate deployment, scaling and healing of containers across machines.", without="Manual scripts per host, no automatic recovery.", use="Multiple services, need for scale/HA, many teams.", avoid="One small app on one server: Docker Compose or a PaaS is simpler.", analogy="A city administration: the control plane is City Hall making decisions; nodes are districts doing the work."),
internals="""Every action goes through the **API server**. It validates and stores objects in **etcd**. Controllers **watch** the API for changes and act to make actual state match desired state. The **scheduler** binds unscheduled Pods to nodes. The **kubelet** watches for Pods assigned to its node and uses the CRI runtime (containerd) to run them, then reports status. **kube-proxy** maintains Service networking rules.""",
commands=[("kubectl get nodes -o wide", "Lists nodes with status, version, IPs and OS.", "`-o wide|yaml|json`, `--show-labels`, `-w` watch.", "NAME STATUS ROLES AGE VERSION ...", "Wrong context: you are looking at another cluster.", "NotReady: `kubectl describe node`, kubelet logs on the node."),
("kubectl get pods -A", "Lists Pods in all namespaces (control plane Pods are in kube-system).", "`-n ns`, `-A`, `-l app=x`, `--field-selector`.", "Pods with READY, STATUS, RESTARTS.", "Forgetting `-n` and seeing nothing.", "Use `kubectl config view --minify` to see your default namespace.")],
lab=dict(goal="Create a local cluster with kind and explore its components.", prereq=["Docker running", "kubectl installed", "kind installed"],
steps=[("kind create cluster --name lab", "Creates a control-plane node as a Docker container and configures kubeconfig."),
("kubectl cluster-info && kubectl get nodes", "Shows API server URL and one Ready node."),
("kubectl -n kube-system get pods", "You will see etcd, kube-apiserver, kube-scheduler, kube-controller-manager, coredns and kube-proxy Pods: the architecture is running as Pods."),
("kubectl create deployment web --image=nginx:1.27 --replicas=2 && kubectl get pods -w", "Watch controllers create Pods. Delete one with `kubectl delete pod <name>` and see it recreated: self-healing.")]),
mnemonics=[("Control plane", "A-E-S-C"), ("Node", "K-K-R")],
hinglish="Control plane **decide** karta hai kya chalna chahiye; worker node **chalata** hai. **etcd** poore cluster ki memory hai, isko backup karna zaroori hai.",
practices={"Production": ["3 control-plane nodes or managed service; back up etcd.", "Keep versions within support window."], "Security": ["Restrict API server access; enable audit logs."]},
mistakes={"DevOps mistakes": ["Running workloads on control-plane nodes.", "No etcd backup."]},
versions=["Since v1.24 dockershim is removed: use containerd/CRI-O; use `crictl` on nodes.", "kind/minikube/Docker Desktop differ in ingress and LoadBalancer support."],
qa_extra=[("Advanced", "Why is only the API server allowed to talk to etcd?", "Central validation, authentication, authorization and admission; consistent schema and audit trail. Components watch the API rather than the database.", "Design reasoning.", "Direct etcd writes would bypass RBAC.")]),

"pods-deployments": dict(
define=dict(simple="A Pod runs your containers; a Deployment makes sure the right number of Pods are always running.",
technical="A Pod is the atomic scheduling unit sharing a network namespace and volumes. A Deployment manages ReplicaSets declaratively to provide rolling updates and rollbacks.",
why="Pods are ephemeral; Deployments provide desired count and controlled updates.", without="A bare Pod that dies stays dead.", use="Stateless applications.", avoid="Databases needing stable identity (use StatefulSet).", analogy="Pod = a worker; Deployment = manager who ensures N workers are always on shift."),
internals="""Deployment > ReplicaSet (one per version) > Pods. On image change the Deployment creates a new ReplicaSet and scales it up while scaling the old one down, respecting `maxSurge` and `maxUnavailable` and waiting for readiness. Old ReplicaSets are kept (revisionHistoryLimit) for rollback.""",
config=[("Deployment explained", """apiVersion: apps/v1
kind: Deployment
metadata: { name: web }
spec:
  replicas: 3
  selector: { matchLabels: { app: web } }
  template:
    metadata: { labels: { app: web } }
    spec:
      containers:
      - name: web
        image: nginx:1.27
        resources: { requests: { cpu: 100m, memory: 64Mi }, limits: { memory: 128Mi } }
        readinessProbe: { httpGet: { path: /, port: 80 } }""", [
("apiVersion: apps/v1", "API group and version for Deployments (check with `kubectl api-resources`)."),
("replicas: 3", "Desired number of Pods; the controller keeps this true."),
("selector.matchLabels", "How the Deployment finds its Pods; must equal template labels."),
("template.metadata.labels", "Labels put on each Pod so Services can select them."),
("image: nginx:1.27", "Pinned version for reproducible deploys."),
("resources.requests", "What the scheduler reserves; also basis for HPA percentages."),
("resources.limits.memory", "Hard cap; exceeding it gives OOMKilled."),
("readinessProbe", "Pod receives Service traffic only after it passes.")])],
lab=dict(goal="Deploy, scale, update and roll back an app.", prereq=["Running cluster (kind/minikube)"],
steps=[("kubectl create deployment web --image=nginx:1.26 --replicas=3 && kubectl get pods", "Creates a Deployment with 3 Pods."),
("kubectl set image deploy/web nginx=nginx:1.27 && kubectl rollout status deploy/web", "Rolling update. `kubectl get rs` shows old and new ReplicaSets."),
("kubectl set image deploy/web nginx=nginx:does-not-exist && kubectl get pods", "Simulates a bad release: new Pods show ImagePullBackOff while old Pods keep serving because rolling update protects availability."),
("kubectl rollout undo deploy/web && kubectl rollout history deploy/web", "Rolls back to the working revision.")]),
compare=[("ReplicaSet vs Deployment", ["Topic", "ReplicaSet", "Deployment"], [["Purpose", "Keep N Pods running", "Manages ReplicaSets, updates, rollback"], ["Use directly?", "Rarely", "Yes"]])],
mnemonics=[("Update knobs", "maxSurge = extra Pods allowed; maxUnavailable = Pods allowed to be down")],
hinglish="Bare Pod kabhi mat chalao. **Deployment** use karo: wo Pod mar jaye to naya bana deta hai aur **rolling update/rollback** deta hai.",
practices={"Production": ["3+ replicas, probes, requests/limits, PDB.", "Use `maxUnavailable: 0` for critical services."]},
mistakes={"Beginner mistakes": ["Running bare Pods.", "Selector not matching template labels."]},
qa_extra=[("Scenario-Based", "A new version fails only in prod. How does Kubernetes limit the damage?", "Readiness probes stop traffic to bad Pods and rolling update keeps old Pods until new ones are Ready; then `rollout undo`.", "Release safety.", "Bad config caused new Pods to fail readiness; users unaffected.")]),

"services-ingress": dict(
define=dict(simple="A Service gives Pods a fixed address; Ingress lets outside HTTP traffic in and routes it by host and path.",
technical="A Service is a stable virtual IP + DNS name with endpoints selected by labels, implemented by kube-proxy/CNI. Ingress is an L7 routing API implemented by an Ingress controller.",
why="Pod IPs change constantly.", without="Clients would need to track Pod IPs.", use="Any Pod that others must reach.", avoid="NodePort for production public exposure.", analogy="Service = a company phone number that forwards to whichever employee is available; Ingress = the receptionist who routes visitors by request."),
internals="""Client > (DNS) Service ClusterIP > iptables/IPVS DNAT on the node > one of the ready Pod IPs from the **Endpoints/EndpointSlice**. Only Pods passing readiness are included. For external traffic: Cloud LB > Ingress controller Pods (nginx/ALB) > Service > Pods.""",
config=[("Service + Ingress explained", """apiVersion: v1
kind: Service
metadata: { name: api }
spec:
  type: ClusterIP
  selector: { app: api }
  ports: [{ port: 80, targetPort: 3000 }]
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: api
  annotations: { cert-manager.io/cluster-issuer: letsencrypt }
spec:
  ingressClassName: nginx
  tls: [{ hosts: [api.example.com], secretName: api-tls }]
  rules:
  - host: api.example.com
    http:
      paths: [{ path: /, pathType: Prefix, backend: { service: { name: api, port: { number: 80 } } } }]""", [
("type: ClusterIP", "Internal-only virtual IP (default)."),
("selector: app: api", "Chooses backend Pods by label; mismatch means zero endpoints."),
("port: 80 / targetPort: 3000", "Port clients use vs port the container listens on."),
("ingressClassName: nginx", "Which Ingress controller handles this object."),
("tls.secretName", "Secret with the TLS certificate (cert-manager can create it)."),
("host/path", "L7 routing rules.")])],
lab=dict(goal="Expose an app internally and via port-forward/Ingress.", prereq=["Cluster with an ingress controller (kind: install ingress-nginx)"],
steps=[("kubectl create deployment api --image=nginx:1.27 --replicas=2 && kubectl expose deploy api --port=80", "Creates a ClusterIP Service."),
("kubectl get svc,endpoints api", "Endpoints list the Pod IPs; empty means selector/readiness problem."),
("kubectl run tmp --rm -it --image=busybox -- wget -qO- http://api", "Tests in-cluster DNS and load balancing."),
("kubectl port-forward svc/api 8080:80", "Reach it at http://localhost:8080 for debugging.")]),
mnemonics=[("Service ladder", "ClusterIP inside; NodePort adds a node port; LoadBalancer adds a cloud LB")],
hinglish="Pod ka IP badalta rehta hai, isliye **Service** use hoti hai. Bahar se HTTP traffic ke liye **Ingress** (ek hi LB par host/path routing + TLS).",
practices={"Production": ["Use Ingress or Gateway API, not NodePort.", "TLS via cert-manager."], "Security": ["NetworkPolicy; restrict who can create LoadBalancer Services."]},
mistakes={"Developer mistakes": ["targetPort wrong.", "Labels mismatch."]},
versions=["Ingress-nginx annotations differ from ALB controller annotations; the Gateway API is the newer successor to Ingress.", "LoadBalancer on bare metal/kind needs MetalLB."],
qa_extra=[("Troubleshooting-Based", "Service exists but curl times out. Steps?", "1) `kubectl get endpoints` non-empty? 2) labels/selector 3) Pods Ready 4) targetPort matches 5) exec into a Pod and curl the Service 6) check NetworkPolicy.", "Systematic debugging.", "Endpoints empty due to failing readiness.")]),

"config-storage": dict(
define=dict(simple="ConfigMaps and Secrets hold settings; PersistentVolumes hold data that must survive Pod restarts.",
technical="ConfigMap/Secret objects inject configuration as env vars or files. PV/PVC/StorageClass abstract storage: a PVC requests capacity and a StorageClass dynamically provisions a PV via a CSI driver.",
why="Separate config from image and keep state outside ephemeral Pods.", without="Rebuild images for every config change; lose data when Pods restart.", use="Any app with configuration or state.", avoid="Storing secrets in ConfigMaps or Git.", analogy="ConfigMap = settings sheet; PVC = rented storage locker."),
internals="""Kubelet mounts ConfigMap/Secret data into the Pod as env vars or tmpfs-backed files (files update automatically, env vars do not). For storage: Pod references a PVC > PVC binds to a PV > PV points to a cloud disk (EBS) provisioned by the CSI driver via the StorageClass > kubelet attaches and mounts it into the container.""",
config=[("Config + PVC explained", """apiVersion: v1
kind: ConfigMap
metadata: { name: api-config }
data: { LOG_LEVEL: info }
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata: { name: pgdata }
spec:
  accessModes: [ReadWriteOnce]
  storageClassName: gp3
  resources: { requests: { storage: 20Gi } }""", [
("data.LOG_LEVEL", "Key/value config; use `envFrom` to inject."),
("accessModes: ReadWriteOnce", "Volume mounted read-write by one node at a time (typical for EBS)."),
("storageClassName: gp3", "Selects the provisioner and volume type."),
("requests.storage", "Requested size; expansion depends on StorageClass `allowVolumeExpansion`.")])],
lab=dict(goal="Inject config and prove data persistence.", prereq=["Cluster with a default StorageClass (kind has one)"],
steps=[("kubectl create configmap app --from-literal=MODE=prod && kubectl create secret generic db --from-literal=PASSWORD=s3cret", "Creates config and a secret."),
("kubectl run t --image=busybox --restart=Never --env=X=1 --dry-run=client -o yaml > /dev/null; kubectl get cm,secret", "Objects exist. Secret values are base64: `kubectl get secret db -o jsonpath='{.data.PASSWORD}' | base64 -d`."),
("kubectl apply -f pvc.yaml && kubectl get pvc", "STATUS Bound means a PV was provisioned (some classes wait until a Pod uses it: WaitForFirstConsumer)."),
("Delete the Pod using the PVC and recreate it", "Data written to the mounted path is still there.")]),
mnemonics=[("Secret", "Base64 is encoding, NOT encryption"), ("Storage chain", "Pod > PVC > PV > Disk")],
hinglish="**Secret base64 hota hai, encrypted nahi.** Isliye RBAC, etcd encryption ya External Secrets/Vault use karo. Data ke liye **PVC** lagao, warna Pod restart par data jayega.",
practices={"Security": ["Enable etcd encryption; use External Secrets/Vault/Sealed Secrets.", "Never commit Secret YAML."], "Reliability": ["Back up volumes (Velero/snapshots)."]},
mistakes={"Security mistakes": ["Thinking base64 is secure.", "Secret YAML in Git."], "Production mistakes": ["No PV backup.", "`Retain`/`Delete` reclaim policy misunderstood."]},
versions=["Storage classes and provisioners differ per cloud (EBS CSI, GCE PD, Azure Disk).", "Env vars from ConfigMap need Pod restart to update; mounted files update automatically."],
qa_extra=[("Advanced", "What is WaitForFirstConsumer?", "A volume binding mode that delays provisioning until a Pod is scheduled, so the volume is created in the same zone as the node.", "Zone-aware storage.", "EBS volumes cannot attach across AZs.")]),

"scaling-scheduling": dict(
define=dict(simple="Scaling = more or fewer Pods/nodes as load changes; scheduling = deciding which node runs each Pod.",
technical="HPA/VPA/Cluster Autoscaler/Karpenter adjust capacity; the scheduler filters and scores nodes using requests, taints/tolerations, affinity, topology spread and priorities.",
why="Handle traffic changes and control placement and cost.", without="Over-provisioning or outages in spikes.", use="Any production workload.", avoid="HPA on memory for apps that do not release memory.", analogy="Scheduler = seating manager placing guests by preference; HPA = adding tables when the restaurant fills."),
internals="""metrics-server collects CPU/memory. HPA compares average usage with the target percentage of **requests** and changes replicas. If new Pods are Pending, the Cluster Autoscaler/Karpenter adds nodes. The scheduler filters nodes (enough resources? taints tolerated? selectors?) then scores them and binds the Pod.""",
lab=dict(goal="Autoscale a CPU-bound deployment.", prereq=["metrics-server installed", "Deployment with CPU requests"],
steps=[("kubectl autoscale deploy web --cpu-percent=50 --min=2 --max=8", "Creates an HPA."),
("kubectl run load --rm -it --image=busybox -- sh -c 'while true; do wget -q -O- http://web; done'", "Generates load."),
("kubectl get hpa -w", "Watch TARGETS rise and REPLICAS increase. Stop the load and see it scale down after the stabilisation window.")]),
compare=[("Autoscalers", ["Tool", "Scales", "Signal"], [["HPA", "Pod replicas", "CPU/memory/custom metrics"], ["VPA", "Pod requests/limits", "Historical usage"], ["Cluster Autoscaler / Karpenter", "Nodes", "Pending Pods"]])],
mnemonics=[("Scheduling knobs", "Taint = repel; Toleration = allowed; Affinity = attract; Spread = distribute")],
hinglish="HPA Pods badhata hai, **Cluster Autoscaler/Karpenter nodes** badhata hai. HPA ka percentage **requests** par based hota hai, isliye requests sahi set karo.",
practices={"Production": ["Set requests; HPA min >= 2; topologySpreadConstraints across zones."], "Cost Optimization": ["Spot nodes for stateless, Karpenter consolidation."]},
mistakes={"DevOps mistakes": ["HPA without requests.", "Scaling Pods but not nodes."]},
qa_extra=[("Scenario-Based", "HPA shows <unknown> for targets.", "metrics-server missing/unhealthy or no CPU requests set on the Pods.", "Common lab issue.", "Install metrics-server, add requests.")]),

"helm-rbac-security": dict(
define=dict(simple="Helm packages Kubernetes YAML; RBAC controls who can do what; other controls harden the cluster.",
technical="Helm renders Go-templated charts with values into manifests and tracks releases. RBAC binds verbs on resources to subjects. Pod Security, NetworkPolicy and admission policies enforce runtime safety.",
why="Reuse and version deployments; enforce least privilege.", without="Copy-paste YAML per environment; everyone is admin.", use="Every real cluster.", avoid="Overly complex templates.", analogy="Helm = installer with settings; RBAC = access badges."),
internals="""`helm upgrade --install` renders templates + values into YAML, sends them to the API server and stores release history as Secrets in the namespace (enabling `helm rollback`). RBAC: the API server checks each request: subject (user/ServiceAccount) > Role/ClusterRole rules (verbs, resources) via RoleBinding.""",
config=[("Role and RoleBinding explained", """apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata: { namespace: shop, name: deployer }
rules:
- apiGroups: ["apps"]
  resources: ["deployments"]
  verbs: ["get","list","patch"]
---
kind: RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata: { namespace: shop, name: ci-deployer }
subjects: [{ kind: ServiceAccount, name: ci, namespace: shop }]
roleRef: { kind: Role, name: deployer, apiGroup: rbac.authorization.k8s.io }""", [
("Role", "Namespaced set of permissions (ClusterRole is cluster-wide)."),
("verbs", "Only get/list/patch: least privilege."),
("RoleBinding.subjects", "Who gets the permissions (a ServiceAccount used by CI)."),
("roleRef", "Which Role is granted.")])],
lab=dict(goal="Install a chart and test RBAC.", prereq=["Helm 3", "Cluster"],
steps=[("helm repo add bitnami https://charts.bitnami.com/bitnami && helm install web bitnami/nginx --set replicaCount=2", "Installs a release."),
("helm list && helm upgrade web bitnami/nginx --set replicaCount=3 && helm rollback web 1", "Upgrade and rollback a release."),
("kubectl create sa ci && kubectl auth can-i delete pods --as=system:serviceaccount:default:ci", "Answers `no`: new ServiceAccounts have no permissions.")]),
compare=[("Helm vs Kustomize", ["Topic", "Helm", "Kustomize"], [["Approach", "Templates + values", "Patches/overlays on plain YAML"], ["Release tracking", "Yes", "No"], ["Learning curve", "Higher", "Lower"]])],
mnemonics=[("RBAC", "Who (subject) can do what (verb) on which (resource)")],
hinglish="Helm = **Kubernetes ka package manager**. RBAC = **kaun kya kar sakta hai**. CI ko sirf utni hi permission do jitni chahiye.",
practices={"Security": ["Least privilege RBAC; separate ServiceAccounts; Pod Security restricted; default-deny NetworkPolicy; admission policies; scan images.", "Pin chart versions; `helm diff` before upgrade."]},
mistakes={"Security mistakes": ["cluster-admin for CI.", "Privileged Pods."]},
versions=["Helm 3 has no Tiller. Helm 2 is obsolete.", "PodSecurityPolicy removed in v1.25; use Pod Security Admission."],
qa_extra=[("Scenario-Based", "How do you give a CI pipeline deploy access safely?", "Dedicated ServiceAccount + namespaced Role limited to needed verbs, short-lived credentials (OIDC/IRSA), or GitOps so CI never touches the cluster.", "Least privilege.", "ArgoCD applies; CI only pushes to Git.")]),

"k8s-troubleshooting": dict(
define=dict(simple="A repeatable method to find why an app on Kubernetes is broken.",
technical="Troubleshooting follows the request path and object hierarchy: events, Pod status/logs, Service endpoints, Ingress, node health and control plane.",
why="Production incidents need fast, systematic diagnosis.", without="Random guessing and long outages.", use="Every incident.", avoid="N/A", analogy="A doctor checking symptoms in order rather than guessing."),
internals="""Work from the top of the symptom down: is the object created? is the Pod scheduled? is the container running? is the app healthy? is the Service selecting it? is traffic allowed? is the node healthy? At each step there is one command that answers the question.""",
lab=dict(goal="Practise diagnosing three broken Pods.", prereq=["Cluster"],
steps=[("kubectl run bad1 --image=nginx:doesnotexist && kubectl describe pod bad1", "Events show ErrImagePull/ImagePullBackOff."),
("kubectl run bad2 --image=busybox -- sh -c 'exit 1' && kubectl logs bad2 --previous; kubectl get pod bad2", "CrashLoopBackOff; check exit code with describe."),
("kubectl run big --image=nginx --overrides='{\"spec\":{\"containers\":[{\"name\":\"big\",\"image\":\"nginx\",\"resources\":{\"requests\":{\"memory\":\"1000Gi\"}}}]}}' && kubectl describe pod big", "The Pod stays Pending; Events show `Insufficient memory` because no node can satisfy the request.")]),
mnemonics=[("Debug order", "Events > Status > Logs > Endpoints > Network > Node")],
hinglish="Hamesha pehle `kubectl describe` ke **Events** dekho, phir `logs --previous`, phir Service ke **endpoints**. Andaaza mat lagao.",
practices={"Monitoring & Logging": ["Alert on restarts, Pending, NotReady; keep central logs so crashed Pod logs are not lost."]},
mistakes={"DevOps mistakes": ["Deleting Pods before capturing logs and events."]},
qa_extra=[("Troubleshooting-Based", "Give the step-by-step flow when users report 503 from the app.", "Ingress controller logs > Ingress rule/host > Service endpoints > Pod readiness > Pod logs > resource/limit issues > node health > recent deploy (rollout history) > rollback if needed.", "Structured thinking.", "Recent deployment changed the readiness path.")])
})
