TOPIC = dict(slug="07-kubernetes", title="Kubernetes", intro="Container orchestrator: scaling, self-healing, rolling updates, service discovery. Job market mein sabse zyada demand.", subs=[

dict(slug="k8s-architecture", title="Architecture & Local Setup", level="Basic",
intro="Cluster = Control Plane (brain) + Worker Nodes (muscle). Aap desired state YAML dete ho; Kubernetes actual state ko wahi banata hai.",
diagram="""
Control Plane                              Worker Node
┌───────────────────────────┐     ┌──────────────────────────┐
│ kube-apiserver  <-- kubectl│     │ kubelet   (runs pods)    │
│ etcd (state DB)            │     │ kube-proxy (svc network) │
│ scheduler (pod -> node)    │     │ container runtime        │
│ controller-manager (loops) │     │ [Pod][Pod][Pod]          │
└───────────────────────────┘     └──────────────────────────┘
""",
install="""# kubectl + kind (Kubernetes in Docker)
winget install Kubernetes.kubectl Kubernetes.kind    # or brew/apt
kind create cluster --name dev
kubectl cluster-info; kubectl get nodes
# alternatives: minikube start | k3s (curl -sfL https://get.k3s.io | sh -)""",
examples=[("First commands","""kubectl get ns; kubectl get pods -A
kubectl run nginx --image=nginx:1.27
kubectl get pods -o wide
kubectl describe pod nginx        # events = first place to debug
kubectl logs nginx; kubectl exec -it nginx -- sh
kubectl delete pod nginx
kubectl api-resources; kubectl explain deployment.spec""")],
problems=[("kubectl says connection refused","Wrong context / cluster down","`kubectl config get-contexts`, `kubectl config use-context kind-dev`."),
("Don't know YAML fields","-","`kubectl explain pod.spec.containers --recursive`, or `kubectl run ... --dry-run=client -o yaml`.")],
qa=[("What does etcd store?","All cluster state (key-value store); back it up."),
("What does the scheduler do?","Assigns unscheduled pods to nodes based on resources, affinity, taints."),
("What is kubelet?","Node agent ensuring containers in pod specs are running."),
("Declarative vs imperative?","Declarative `kubectl apply -f` describes desired state; imperative runs one-off commands."),
("What is a namespace?","Virtual cluster partition for isolation/quota/RBAC.")]),

dict(slug="pods-deployments", title="Pods, ReplicaSets & Deployments", level="Basic",
intro="Pod = smallest unit (1+ containers sharing network/storage). Deployment pods ko manage karta hai: replicas, rolling update, rollback.",
diagram="""
Deployment -> ReplicaSet (v2) -> Pod, Pod, Pod
           \\-> ReplicaSet (v1)  (kept for rollback; scaled to 0)
Pod: [app container][sidecar]  shared IP, localhost, volumes
""",
install="# kind cluster from previous topic",
examples=[("Deployment YAML","""apiVersion: apps/v1
kind: Deployment
metadata: { name: web }
spec:
  replicas: 3
  selector: { matchLabels: { app: web } }
  strategy: { type: RollingUpdate, rollingUpdate: { maxSurge: 1, maxUnavailable: 0 } }
  template:
    metadata: { labels: { app: web } }
    spec:
      containers:
      - name: web
        image: nginx:1.27
        ports: [{ containerPort: 80 }]
        resources:
          requests: { cpu: 100m, memory: 128Mi }
          limits:   { cpu: 500m, memory: 256Mi }
        readinessProbe: { httpGet: { path: /, port: 80 }, initialDelaySeconds: 3 }
        livenessProbe:  { httpGet: { path: /, port: 80 }, initialDelaySeconds: 10 }"""),
("Operate it","""kubectl apply -f web.yaml
kubectl scale deploy web --replicas=5
kubectl set image deploy/web web=nginx:1.28
kubectl rollout status deploy/web
kubectl rollout history deploy/web
kubectl rollout undo deploy/web""")],
problems=[("CrashLoopBackOff","App crashes on start (bad config/missing env/OOM)","`kubectl logs pod --previous`, `describe pod` (Last State, exit code 137 = OOM), fix config."),
("ImagePullBackOff","Wrong image name/tag or private registry without pull secret","Verify image; create `imagePullSecrets`."),
("Pod Pending","Insufficient CPU/mem or unbound PVC or taints","`describe pod` Events show reason; add nodes/adjust requests.")],
qa=[("Pod vs container?","Pod wraps one or more containers sharing network and storage."),
("Liveness vs readiness vs startup probe?","Liveness restarts unhealthy container; readiness removes from Service endpoints; startup protects slow-start apps."),
("Requests vs limits?","Requests used for scheduling and guarantees; limits are caps (CPU throttled, memory OOM-killed)."),
("How does rolling update work?","New ReplicaSet scales up while old scales down respecting maxSurge/maxUnavailable."),
("Deployment vs StatefulSet?","Deployment for stateless; StatefulSet gives stable identity/storage/order.")]),

dict(slug="services-ingress", title="Services, Ingress & Networking", level="Intermediate",
intro="Pod IPs change hote hain. Service stable virtual IP + DNS deta hai. Ingress HTTP routing (host/path) aur TLS handle karta hai.",
diagram="""
Internet -> LoadBalancer -> Ingress Controller (nginx)
                               |  host/path rules
              /api -> Service api (ClusterIP) -> Pods
              /    -> Service web (ClusterIP) -> Pods

DNS inside cluster:  api.prod.svc.cluster.local
Types: ClusterIP (internal) | NodePort | LoadBalancer | ExternalName | Headless
""",
install="""# ingress-nginx on kind
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
# cert-manager for TLS
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/latest/download/cert-manager.yaml""",
examples=[("Service + Ingress with TLS","""apiVersion: v1
kind: Service
metadata: { name: web }
spec:
  selector: { app: web }
  ports: [{ port: 80, targetPort: 80 }]
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: web
  annotations: { cert-manager.io/cluster-issuer: letsencrypt }
spec:
  ingressClassName: nginx
  tls: [{ hosts: [app.example.com], secretName: app-tls }]
  rules:
  - host: app.example.com
    http:
      paths:
      - { path: /, pathType: Prefix, backend: { service: { name: web, port: { number: 80 } } } }"""),
("NetworkPolicy default deny","""apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: { name: default-deny, namespace: prod }
spec: { podSelector: {}, policyTypes: [Ingress] }""")],
problems=[("Service has no endpoints","Selector labels don't match pod labels","`kubectl get endpoints web`; compare `selector` with pod labels."),
("Ingress returns 404/502","Wrong path/backend port, pods not ready","`kubectl describe ingress`, check controller logs and readiness.")],
qa=[("ClusterIP vs NodePort vs LoadBalancer?","ClusterIP internal only; NodePort exposes on each node port; LoadBalancer provisions cloud LB."),
("Ingress vs Service?","Service L4 exposure; Ingress L7 HTTP routing on top of Services."),
("How does DNS work in K8s?","CoreDNS resolves `svc.namespace.svc.cluster.local`."),
("What is a headless service?","`clusterIP: None` returns pod IPs directly; used by StatefulSets."),
("What is Gateway API?","Successor to Ingress with richer, role-oriented routing resources.")]),

dict(slug="config-storage", title="ConfigMaps, Secrets & Persistent Storage", level="Intermediate",
intro="Config ko image se alag rakho (ConfigMap), sensitive data Secret mein, aur database ke liye PV/PVC + StatefulSet.",
diagram="""
ConfigMap/Secret --env or volume--> Pod
Pod -> PVC (claim) -> PV (actual disk: EBS) via StorageClass (dynamic provisioning)
StatefulSet: db-0, db-1, db-2 each with own PVC (stable names)
""",
install="# built-in; cloud needs CSI driver (EBS CSI on EKS)",
examples=[("Config and secret","""kubectl create configmap app-config --from-literal=LOG_LEVEL=info
kubectl create secret generic db-secret --from-literal=password='S3cret!'
# use in pod
envFrom:
- configMapRef: { name: app-config }
env:
- name: DB_PASSWORD
  valueFrom: { secretKeyRef: { name: db-secret, key: password } }"""),
("StatefulSet with storage","""apiVersion: apps/v1
kind: StatefulSet
metadata: { name: pg }
spec:
  serviceName: pg
  replicas: 1
  selector: { matchLabels: { app: pg } }
  template:
    metadata: { labels: { app: pg } }
    spec:
      containers:
      - name: pg
        image: postgres:16
        env: [{ name: POSTGRES_PASSWORD, valueFrom: { secretKeyRef: { name: db-secret, key: password } } }]
        volumeMounts: [{ name: data, mountPath: /var/lib/postgresql/data }]
  volumeClaimTemplates:
  - metadata: { name: data }
    spec: { accessModes: [ReadWriteOnce], resources: { requests: { storage: 10Gi } } }""")],
problems=[("Config change not picked up","Env vars read at start only","Restart pods (`rollout restart`) or use checksum annotation via Helm."),
("PVC Pending","No matching StorageClass / CSI driver","`kubectl get sc`; install CSI driver; check zone."),
("Secrets are just base64","Not encrypted by default","Enable etcd encryption; use External Secrets/Vault; RBAC least privilege.")],
qa=[("Is a Secret encrypted?","Only base64-encoded by default; enable encryption at rest and restrict RBAC."),
("PV vs PVC vs StorageClass?","PV is storage; PVC is a request for it; StorageClass defines provisioner for dynamic PVs."),
("Access modes?","RWO one node, ROX many read-only, RWX many read-write, RWOP single pod."),
("How to inject config as a file?","Mount ConfigMap as a volume."),
("How to safely handle secrets in GitOps?","Sealed Secrets, SOPS, or External Secrets Operator.")]),

dict(slug="scaling-scheduling", title="Scaling, Scheduling & Resource Management", level="Advanced",
intro="HPA pods scale karta hai, cluster autoscaler/Karpenter nodes. Scheduling controls: affinity, taints, topology spread, PDB.",
diagram="""
Load up -> HPA adds pods -> pods Pending -> Cluster Autoscaler/Karpenter adds node
Scheduling controls: nodeSelector | affinity/anti-affinity | taints+tolerations | topologySpread | priorityClass
""",
install="kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml",
examples=[("HPA","""kubectl autoscale deploy web --cpu-percent=70 --min=2 --max=10
kubectl get hpa -w"""),
("Spread across zones + PDB","""topologySpreadConstraints:
- maxSkew: 1
  topologyKey: topology.kubernetes.io/zone
  whenUnsatisfiable: DoNotSchedule
  labelSelector: { matchLabels: { app: web } }
---
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata: { name: web }
spec: { minAvailable: 2, selector: { matchLabels: { app: web } } }"""),
("Taint dedicated GPU nodes","""kubectl taint nodes gpu1 dedicated=gpu:NoSchedule
# pod toleration: key dedicated, value gpu, effect NoSchedule""")],
problems=[("HPA shows <unknown> targets","metrics-server missing or no resource requests","Install metrics-server; set CPU requests."),
("Node drain blocked","PDB too strict","Adjust PDB or scale up replicas before draining."),
("Pods evicted under memory pressure","No/low requests; BestEffort QoS","Set requests=limits for critical pods (Guaranteed QoS).")],
qa=[("HPA vs VPA vs Cluster Autoscaler?","HPA changes pod count, VPA changes pod resources, CA changes node count."),
("Taints vs affinity?","Taints repel pods from nodes (need toleration); affinity attracts pods to nodes/pods."),
("QoS classes?","Guaranteed, Burstable, BestEffort; eviction order reversed."),
("What is a PDB?","Limits voluntary disruptions to keep min availability."),
("Karpenter vs Cluster Autoscaler?","Karpenter provisions right-sized nodes directly from pending pods, faster and more flexible.")]),

dict(slug="helm-rbac-security", title="Helm, RBAC & Cluster Security", level="Advanced",
intro="Helm K8s package manager (templates + values). RBAC access control. Policies (Kyverno/OPA) aur Pod Security se hardening.",
diagram="""
Helm chart = templates/ + values.yaml -> helm install -> release (versioned, rollback)
RBAC: Subject (user/SA) --RoleBinding--> Role (verbs on resources) in namespace
""",
install="""winget install Helm.Helm     # or: curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
helm repo add bitnami https://charts.bitnami.com/bitnami""",
examples=[("Helm usage","""helm create myapp
helm install web ./myapp -f values-prod.yaml -n prod --create-namespace
helm upgrade web ./myapp --set image.tag=v2 --atomic
helm rollback web 1; helm list -A; helm template ./myapp   # render only"""),
("RBAC read-only user","""apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata: { name: pod-reader, namespace: dev }
rules: [{ apiGroups: [""], resources: [pods, pods/log], verbs: [get, list, watch] }]
---
kind: RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata: { name: read-pods, namespace: dev }
subjects: [{ kind: User, name: anup }]
roleRef: { kind: Role, name: pod-reader, apiGroup: rbac.authorization.k8s.io }
# check: kubectl auth can-i delete pods --as anup -n dev"""),
("Kyverno policy: disallow latest tag","""apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata: { name: no-latest }
spec:
  validationFailureAction: Enforce
  rules:
  - name: no-latest
    match: { any: [{ resources: { kinds: [Pod] } }] }
    validate:
      message: "Use a pinned image tag"
      pattern: { spec: { containers: [{ image: "!*:latest" }] } }""")],
problems=[("Helm upgrade half-applied and stuck","Failed hook/timeouts","Use `--atomic --timeout`; `helm rollback`."),
("'forbidden' errors for a service account","Missing RBAC","`kubectl auth can-i --as=system:serviceaccount:ns:sa ...`; add minimal Role.")],
qa=[("Role vs ClusterRole?","Role namespaced; ClusterRole cluster-wide (or reusable definition)."),
("Helm vs Kustomize?","Helm templating with values and releases; Kustomize overlays/patches on plain YAML."),
("How to secure a cluster?","RBAC least privilege, network policies, PSS, image scanning, secrets encryption, audit logs, private API endpoint."),
("What is a service account?","Identity for pods to call the API; use IRSA for AWS."),
("What is Pod Security Standards?","privileged, baseline, restricted profiles enforced per namespace.")]),

dict(slug="k8s-troubleshooting", title="Kubernetes Troubleshooting Playbook", level="Advanced",
intro="Interview aur production dono mein: pod kyun fail hua? Systematic flow follow karo.",
diagram="""
Pod problem?
 Pending           -> describe (events): resources? taints? PVC? nodeSelector?
 ImagePullBackOff  -> image name/tag, registry auth
 CrashLoopBackOff  -> logs --previous, exit code, config/env, probes too strict
 Running but no traffic -> readiness, service selector, endpoints, NetworkPolicy, ingress
 Node NotReady     -> kubelet logs, disk/mem pressure, network
""",
install="# helpful: k9s, stern (multi-pod logs), kubectx/kubens, kubectl-debug",
examples=[("Command toolkit","""kubectl get events --sort-by=.lastTimestamp -n prod
kubectl describe pod <p>; kubectl logs <p> -c <container> --previous
kubectl top pod; kubectl top node
kubectl debug -it <pod> --image=busybox --target=<container>
kubectl run tmp --rm -it --image=nicolaka/netshoot -- bash    # nslookup, curl, dig
kubectl get endpoints svc; kubectl port-forward svc/web 8080:80
journalctl -u kubelet -f     # on node"""),
("Exit codes","""137 = SIGKILL (OOMKilled), 143 = SIGTERM, 1 = app error, 126/127 = command not executable/not found""")],
problems=[("Random 502s during deploy","Pod receives traffic before ready / killed before drain","Proper readinessProbe, `preStop: sleep 10`, `terminationGracePeriodSeconds`."),
("DNS resolution slow (5s)","ndots:5 + conntrack race","NodeLocal DNSCache, use FQDNs with trailing dot, tune ndots.")],
qa=[("Pod stuck in Terminating?","Finalizers or node down; `kubectl delete pod --force --grace-period=0` as last resort, check finalizers."),
("How do you debug a distroless container?","Ephemeral debug container: `kubectl debug`."),
("What does OOMKilled mean?","Container exceeded memory limit; increase limit or fix leak."),
("Node NotReady steps?","Check `describe node` conditions, kubelet logs, disk/PID/memory pressure, CNI."),
("How to find which pods use most CPU?","`kubectl top pod -A --sort-by=cpu`.")]),
])
