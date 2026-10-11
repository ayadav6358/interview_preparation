EXT = dict(
guide=dict(
bigpicture=dict(
problem="""**Problem it solves:** "Mere laptop pe chal raha hai, server pe nahi chal raha." Without Docker, every machine has a different OS, Node/Python version and library set, so the same app behaves differently. With Docker, the application **and** its dependencies are packaged into one image that runs the same way on a laptop, a CI server and production.""",
chain=["PROBLEM: app works on developer machine, fails on server",
       "TRADITIONAL APPROACH: install runtime + libraries by hand or with scripts on each server (or one VM per app)",
       "PAIN: version drift, 'works on my machine', slow VM boot, wasted RAM/CPU, hard rollbacks",
       "TECHNOLOGY: Docker (image + container, sharing the host Linux kernel)",
       "SOLUTION: build once (image), run anywhere (container), start in seconds",
       "REAL-WORLD BENEFIT: identical dev/test/prod, fast CI/CD, easy rollback, higher server density"],
text="""Docker did not invent containers. Linux already had **namespaces** (isolation) and **cgroups** (resource limits). Docker made them easy to use: a simple CLI, the Dockerfile format and image registries."""),
e2e=dict(diagram="""Developer
   |
   v
Dockerfile (recipe)
   |  docker build
   v
Docker Image (read-only layers)
   |  docker push
   v
Registry (Docker Hub / ECR / Harbor)
   |  docker pull
   v
Docker Host
   |  docker run
   v
Container (image + writable layer + namespaces + cgroups)
   |
   v
Application (listening on a port)
   |
   v
Logs (docker logs) / Metrics (docker stats, Prometheus) / Monitoring (Grafana)""",
text="""**Developer** writes source code and a **Dockerfile**. `docker build` executes each instruction and produces an **image** made of read-only layers (cached, so rebuilds are fast). `docker push` uploads the image to a **registry** so other machines can get it. On the server, `docker pull` downloads the layers and `docker run` creates a **container**: a new writable layer on top of the image, its own namespaces (PID, network, mount...) and cgroup limits. The application starts as PID 1 inside it. Then you observe it with `docker logs`, `docker stats` or a monitoring stack. If something is wrong you fix the code, rebuild with a new tag and redeploy; rollback means running the previous tag."""),
tools=dict(rows=[
["Git", "Source control", "Code + Dockerfile", "Commits / tags", "Start of every pipeline"],
["Dockerfile", "Recipe for an image", "Base image + instructions", "Image (via build)", "Repo root of each service"],
["Docker Engine (dockerd + containerd + runc)", "Build and run containers", "Image", "Running container", "Dev machine, CI agent, server"],
["Docker Compose", "Run multi-container apps on one host", "compose.yml", "Running stack", "Local dev, small deployments"],
["Registry (Docker Hub, ECR, Harbor)", "Store and distribute images", "Image push", "Image pull", "Between CI and servers"],
["Trivy / Grype", "Vulnerability scan", "Image", "CVE report", "CI pipeline before push"],
["Cosign / Syft", "Sign image / create SBOM", "Image", "Signature / SBOM file", "CI pipeline after build"],
["Kubernetes", "Orchestrate containers across nodes", "Image + YAML", "Scaled, self-healing app", "Production clusters"],
["Prometheus + Grafana", "Metrics and dashboards", "cAdvisor / app metrics", "Graphs and alerts", "Monitoring layer"]],
why="**Docker vs a VM tool such as Vagrant:** containers share the host kernel, so they start in seconds and use far less memory. **Compose vs Kubernetes:** Compose is enough for one host; use Kubernetes when you need multiple nodes, auto-scaling and self-healing. **Docker Hub vs Harbor:** Docker Hub is public and simple; Harbor is self-hosted with RBAC, scanning and replication for company use."),
compare=[
("Container vs Virtual Machine", ["Topic", "Container", "Virtual Machine"], [
["Isolation unit", "Process with namespaces + cgroups", "Full guest operating system"],
["Kernel", "Shares host kernel", "Own kernel per VM"],
["Startup", "Seconds or less", "Minutes"],
["Size", "MBs (image)", "GBs"],
["Isolation strength", "Weaker (shared kernel)", "Stronger (hypervisor)"],
["Best for", "Microservices, CI, dense packing", "Different OS, strong tenant isolation"]]),
("Image vs Container", ["Topic", "Image", "Container"], [
["What is it", "Read-only template (layers)", "Running (or stopped) instance of an image"],
["State", "Immutable", "Has a writable layer, changes are lost on `docker rm`"],
["Analogy", "Class / recipe", "Object / cooked dish"],
["Command", "`docker build`, `docker images`", "`docker run`, `docker ps`"]]),
("Volume vs Bind mount vs tmpfs", ["Topic", "Volume", "Bind mount", "tmpfs"], [
["Managed by", "Docker", "You (host path)", "Memory"],
["Persists after container removal", "Yes", "Yes (it is a host folder)", "No"],
["Best for", "Databases, production data", "Source code in development", "Secrets/scratch data"],
["Portability", "High", "Depends on host path", "N/A"]]),
("CMD vs ENTRYPOINT", ["Topic", "CMD", "ENTRYPOINT"], [
["Purpose", "Default command/arguments", "The fixed executable"],
["Overridden by `docker run image x`", "Yes, fully replaced", "No (arguments are appended); needs `--entrypoint`"],
["Typical use", "`CMD [\"node\",\"server.js\"]`", "`ENTRYPOINT [\"nginx\"]` + `CMD [\"-g\",\"daemon off;\"]`"]]),
("COPY vs ADD", ["Topic", "COPY", "ADD"], [
["Copy local files", "Yes", "Yes"],
["Auto-extract tar", "No", "Yes"],
["Download URL", "No", "Yes (not recommended)"],
["Recommendation", "Default choice", "Only when you need tar extraction"]]),
("EXPOSE vs -p", ["Topic", "EXPOSE", "-p host:container"], [
["Effect", "Documentation only (metadata)", "Actually publishes the port on the host"],
["Needed to reach app from host", "No", "Yes"]]),
("Docker Compose vs Kubernetes", ["Topic", "Compose", "Kubernetes"], [
["Scope", "Single host", "Cluster of nodes"],
["Self-healing / autoscale", "Restart policy only", "Yes (controllers, HPA)"],
["Learning curve", "Low", "High"],
["Use case", "Local dev, small apps", "Production at scale"]]),
("Docker Hub vs Harbor", ["Topic", "Docker Hub", "Harbor"], [
["Hosting", "SaaS by Docker", "Self-hosted (CNCF project)"],
["Access control", "Basic, paid teams", "Projects, RBAC, LDAP/OIDC"],
["Scanning / signing", "Limited on free tier", "Built-in Trivy, cosign support"],
["Rate limits", "Yes for pulls", "Your own limits"]])],
troubleshooting=[
("Container is running but application is not accessible", "Port not published, app listens on 127.0.0.1 only, wrong port, firewall/security group",
 "`docker ps` (check PORTS column), `docker logs web`, `docker inspect web`, `docker exec -it web sh`, then `curl localhost:PORT` inside and outside the container",
 "Publish with `-p 8080:80`; make the app bind to `0.0.0.0`; open the cloud security group.",
 "Add a HEALTHCHECK, document ports in compose, test with `curl` in CI smoke test."),
("Container exits immediately (Exited (0) or (1))", "PID 1 finished or crashed; missing env variable; wrong CMD",
 "`docker ps -a`, `docker logs <id>`, `docker inspect --format '{{.State.ExitCode}}' <id>`",
 "Fix the command or env; for a long-running process use foreground mode (`nginx -g 'daemon off;'`).",
 "Run the image locally in CI before deploy."),
("exec format error", "Image built for another CPU architecture (arm64 vs amd64)",
 "`docker image inspect img --format '{{.Architecture}}'`, `uname -m`",
 "Build multi-arch: `docker buildx build --platform linux/amd64,linux/arm64`.",
 "Always build multi-arch or pin the platform in CI."),
("Cannot connect to the Docker daemon", "Daemon not running or user not in docker group",
 "`systemctl status docker`, `groups`", "`sudo systemctl start docker`; `sudo usermod -aG docker $USER` then re-login.",
 "Enable at boot with `systemctl enable docker`."),
("Build is slow on every code change", "Layer cache invalidated because source is copied before dependency install",
 "`docker build` output shows no `CACHED` for the install step", "Copy `package.json` first, install, then copy the rest.", "Review Dockerfile order in code review; add `.dockerignore`."),
("OOMKilled (exit code 137)", "Container exceeded memory limit",
 "`docker inspect c --format '{{.State.OOMKilled}}'`, `docker stats`", "Increase `--memory` or fix the memory leak.", "Load-test and set realistic limits.")],
practices={
"Development": ["Use `docker compose` for the full stack locally.", "Mount source with bind mounts for hot reload; use named volumes for DB data.", "Keep a `.dockerignore`."],
"Production": ["Pin image tags (never `latest`) or use digests.", "Set restart policy and healthchecks.", "Set CPU/memory limits.", "One process per container; log to stdout/stderr."],
"Security": ["Run as non-root (`USER`).", "Use minimal/distroless base images.", "Scan with Trivy in CI, sign with cosign, generate SBOM with Syft.", "Never mount `/var/run/docker.sock` or use `--privileged` without a strong reason.", "Use `--read-only`, `--cap-drop ALL`, `no-new-privileges`."],
"Performance": ["Multi-stage builds for small images.", "Order layers from least to most frequently changing.", "Use BuildKit cache mounts."],
"Reliability": ["`restart: unless-stopped`.", "Healthchecks + `depends_on: condition: service_healthy`.", "Store data in volumes and back them up."],
"Cost Optimization": ["Small images reduce registry storage and pull time.", "Prune unused images/volumes regularly (`docker system prune`)."],
"Monitoring & Logging": ["`docker stats`, cAdvisor + Prometheus + Grafana.", "Use a logging driver or ship stdout to Loki/ELK; configure log rotation (`max-size`, `max-file`)."],
"Backup & Disaster Recovery": ["Back up named volumes with a tar container.", "Keep Dockerfiles and compose files in Git; images are reproducible from source + registry."]},
mistakes={
"Beginner mistakes": ["Using `latest` tag: pin versions.", "Storing data inside the container: use volumes.", "Thinking EXPOSE opens the port: use `-p`."],
"Developer mistakes": ["Copying the whole project before installing dependencies (cache miss).", "Forgetting `.dockerignore` so `node_modules`/`.git` bloat the image.", "Listening on `localhost` inside the container."],
"DevOps mistakes": ["No healthchecks or resource limits.", "Not cleaning old images so the disk fills up.", "Building different images per environment instead of one image + config."],
"Production mistakes": ["Running as root.", "Logs without rotation filling the disk.", "No rollback tag kept."],
"Security mistakes": ["Baking secrets into image layers (`ENV PASSWORD=...`, `COPY .env`).", "Mounting docker.sock into containers.", "Never scanning or updating base images."]},
versions=[
"Compose: use `docker compose` (v2 plugin). The old `docker-compose` (v1, Python) is deprecated and the `version:` key in compose files is obsolete.",
"BuildKit is the default builder in current Docker Engine; `docker buildx` provides multi-platform builds.",
"Docker Desktop (Windows/macOS) runs Docker inside a VM/WSL2; Linux runs the engine natively. Networking `host` mode behaves differently on Docker Desktop.",
"`docker scan` (Snyk) was removed; use `docker scout` or Trivy.",
"Commands and defaults change between releases: check `docker version` and the official docs at docs.docker.com for your version."],
hinglish="""Docker basically **app ko uski saari dependencies ke saath ek box (image)** mein pack kar deta hai. Jab wo box chalta hai to use **container** kehte hain. Container ek **isolated process** hai jo host ka **kernel share** karta hai, isliye VM ke comparison mein bahut halka aur fast hota hai. Image **read-only** hoti hai, container ke andar ka data container delete hote hi chala jata hai, isliye important data ke liye **volume** use karte hain. `EXPOSE` sirf batata hai ki app kaunsa port use karta hai; asli port khulta hai `-p` se.""",
mnemonics=[
("Namespace vs cgroups", "Namespace = what a process can SEE; cgroups = what a process can USE."),
("Image vs Container", "Image = recipe/class; Container = cooked dish/object."),
("Dockerfile layer order", "'Least changing first': base > deps > source."),
("Storage types", "V-B-T: Volume (Docker-managed), Bind (host path), Tmpfs (memory)."),
("Container lifecycle", "Created > Running > Paused > Stopped > Removed (`create, start, pause, stop, rm`)."),
("Ports", "-p HOST:CONTAINER, 'outside:inside'.")],
client=dict(
s30="""Docker packages an application together with everything it needs into a single unit called an image. That image runs exactly the same on a developer laptop, a test server and production. It removes 'it works on my machine' problems, speeds up releases and lets us run more applications on the same servers.""",
m2="""Traditionally we installed the runtime and libraries on every server, and small differences caused failures. With Docker, we describe the environment once in a Dockerfile and build an image. The image is stored in a registry, and any server can pull it and start a container in seconds. Containers share the operating system kernel, so they are much lighter than virtual machines. For your team this means faster onboarding (one command to run the full stack), consistent deployments, easy rollback (run the previous image version) and better server utilisation. We also add security scanning to the pipeline so vulnerable images never reach production.""",
m5="""Let me explain in four parts. **First, the problem:** applications depend on the operating system, language version and libraries. Different environments cause failures that are hard to reproduce. **Second, the solution:** a Docker image is a read-only, layered package of the app plus dependencies. A container is a running instance of it, isolated using Linux namespaces and limited using cgroups. **Third, how we use it in your project:** developers build the image through a Dockerfile in CI, the image is scanned, signed and pushed to a private registry such as Harbor, and the deployment platform, Docker Compose for small setups or Kubernetes for scale, pulls that exact version. Configuration and secrets are injected at runtime, and data lives in volumes. **Fourth, operations and risk:** we set health checks, CPU and memory limits, log rotation and monitoring, we run containers as non-root and keep base images updated. The business outcome is faster and safer releases, lower infrastructure cost and simple rollbacks."""),
roadmap=[
("Beginner", ["Container vs VM", "Images, containers, registry", "docker run/ps/logs/exec/stop/rm", "Ports and env variables"]),
("Intermediate", ["Dockerfile and layer cache", "Volumes and bind mounts", "Networks and DNS", "Docker Compose", "Healthchecks"]),
("Advanced", ["Multi-stage and multi-arch builds", "BuildKit cache", "Security: non-root, capabilities, seccomp, rootless", "Image scanning, SBOM, signing", "Namespaces, cgroups, containerd, runc"]),
("Production", ["Private registry (Harbor/ECR)", "Resource limits, restart policy, logging", "CI/CD integration", "Move to Kubernetes"]),
("Interview", ["Explain the architecture end-to-end", "Debug a crashing container", "Optimize a Dockerfile", "Compare Compose vs Kubernetes"])],
miniproject=dict(title="React + Node.js + PostgreSQL + Redis with Docker Compose",
arch="""Browser --> Nginx (:80, serves React build, proxies /api)
                 |
                 v
            Node.js API (:3000, internal only)
              |            |
              v            v
      PostgreSQL (:5432)  Redis (:6379)
        volume pgdata      (cache)
All on custom network 'appnet'; only Nginx publishes a host port.
Pipeline: Git > CI build > Trivy scan > push to registry > compose pull/up""",
steps=[
("Step 1: Project layout", """myapp/
  frontend/  (React, Dockerfile)
  api/       (Node.js, Dockerfile)
  nginx/default.conf
  compose.yml
  .env        (gitignored)""", "One folder per service. Each service has its own Dockerfile so it can be built and scanned separately."),
("Step 2: API Dockerfile", """FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --omit=dev
COPY . .
USER node
EXPOSE 3000
HEALTHCHECK CMD wget -qO- http://localhost:3000/health || exit 1
CMD ["node","server.js"]""", "Dependencies are copied first for cache, the app runs as the non-root `node` user, and the healthcheck lets Compose know when the API is ready."),
("Step 3: compose.yml", """services:
  web:
    build: ./frontend
    ports: ["80:80"]
    depends_on: [api]
    networks: [appnet]
  api:
    build: ./api
    environment:
      DB_URL: postgres://app:${DB_PASSWORD}@db:5432/app
      REDIS_URL: redis://cache:6379
    depends_on:
      db: { condition: service_healthy }
    networks: [appnet]
  db:
    image: postgres:16
    environment: { POSTGRES_USER: app, POSTGRES_PASSWORD: "${DB_PASSWORD}", POSTGRES_DB: app }
    volumes: [pgdata:/var/lib/postgresql/data]
    healthcheck: { test: ["CMD-SHELL","pg_isready -U app"], interval: 5s, retries: 10 }
    networks: [appnet]
  cache:
    image: redis:7-alpine
    networks: [appnet]
networks: { appnet: {} }
volumes: { pgdata: {} }""", "Only `web` publishes a port. `api`, `db`, `cache` are reachable only inside `appnet` by service name (DNS). The DB password comes from `.env`, not from the file. Data survives in the `pgdata` volume."),
("Step 4: Run, verify, scan", """docker compose up -d --build
docker compose ps
curl -i http://localhost/api/health
trivy image myapp-api:latest --severity HIGH,CRITICAL
docker compose logs -f api""", "Start the stack, confirm all services are healthy, hit the API through Nginx, scan the image, and read logs. In CI, the same build + scan runs and the pipeline pushes to Harbor; the server then pulls the tagged image and runs `docker compose up -d`.")]),
interview=[
("Beginner", "What is Docker?", "A platform to build, ship and run applications in containers. A container packages the app and its dependencies and shares the host kernel.", "Interviewers check that you know the core problem: environment consistency.", "A Node app runs the same in dev, CI and production because the same image is used."),
("Beginner", "Image vs container?", "Image is a read-only template made of layers; a container is a running instance with a writable layer.", "Most common confusion.", "One `nginx` image can start many containers."),
("Beginner", "What is a Dockerfile?", "A text file with instructions (FROM, COPY, RUN, CMD...) that `docker build` runs to create an image.", "Shows you understand reproducible builds.", "Node Dockerfile: FROM node, COPY, RUN npm ci, CMD node server.js."),
("Beginner", "What is Docker Hub?", "The default public registry for images.", "Registries are how images move between machines.", "`docker pull nginx` downloads from Docker Hub."),
("Beginner", "How do you list running and all containers?", "`docker ps` shows running; `docker ps -a` shows all including stopped.", "Basic debugging skill.", "A crashed container appears only with `-a` and status Exited."),
("Beginner", "What does `docker run -d -p 8080:80 nginx` do?", "Starts nginx in the background and maps host port 8080 to container port 80.", "Tests port mapping understanding.", "Then open http://localhost:8080."),
("Beginner", "How to see logs of a container?", "`docker logs -f <name>`.", "First step of every troubleshooting.", "See a stack trace when the app crashes."),
("Beginner", "How to enter a running container?", "`docker exec -it <name> sh` (or bash).", "Used to inspect files and test connectivity.", "`curl localhost:3000` from inside the container."),
("Beginner", "Why do we use volumes?", "Container filesystem is ephemeral; volumes persist data outside the container lifecycle.", "Data loss is a classic production incident.", "PostgreSQL data dir mounted to a named volume."),
("Beginner", "docker stop vs docker kill?", "`stop` sends SIGTERM then SIGKILL after a timeout (default 10s); `kill` sends SIGKILL immediately.", "Graceful shutdown matters for databases and in-flight requests.", "App needs SIGTERM to flush data."),
("Intermediate", "Explain image layers and caching.", "Each Dockerfile instruction creates a read-only layer, identified by content hash. If an instruction and its inputs are unchanged, the cached layer is reused; a changed layer invalidates all layers after it.", "Directly affects build speed and image size.", "Copy package.json and run `npm ci` before copying source so code changes do not reinstall dependencies."),
("Intermediate", "CMD vs ENTRYPOINT?", "ENTRYPOINT defines the executable; CMD gives default arguments and is overridable at `docker run`. Together they make a flexible CLI-like image.", "Tests Dockerfile depth.", "`ENTRYPOINT [\"curl\"]`, `CMD [\"--help\"]`."),
("Intermediate", "EXPOSE vs -p?", "EXPOSE is metadata; `-p` publishes the port to the host.", "Common wrong assumption.", "Without `-p`, the port is reachable only from other containers on the same network."),
("Intermediate", "Bridge vs host vs overlay network?", "Bridge: private network on one host with NAT. Host: shares host network stack (no isolation, no port mapping). Overlay: spans multiple hosts (Swarm/K8s-like).", "Shows networking knowledge.", "Custom bridge for a Compose stack."),
("Intermediate", "Why can't containers on the default bridge use names?", "The default bridge has no automatic DNS; user-defined networks provide embedded DNS.", "Frequent real issue.", "API cannot resolve `db` until both are on `appnet`."),
("Intermediate", "Volume vs bind mount?", "Volumes are managed by Docker and portable; bind mounts map a host path and depend on host layout.", "Choosing storage correctly.", "Bind mount for dev hot reload, volume for DB."),
("Intermediate", "What is a multi-stage build?", "Multiple FROM stages; you build in one stage and copy only artifacts to a small final stage.", "Size and security.", "Go/Java/Node builds shrink from ~1GB to ~100MB."),
("Intermediate", "What does depends_on guarantee?", "Only start order, not readiness, unless you use `condition: service_healthy` with a healthcheck.", "Classic race condition.", "API crashes because Postgres is still initialising."),
("Intermediate", "How to limit CPU and memory?", "`--memory=256m --cpus=0.5` or `deploy.resources`/`mem_limit` in Compose.", "Prevents noisy neighbours.", "One leaking container should not kill the host."),
("Intermediate", "What is a tag vs digest?", "A tag is a mutable label; a digest (sha256) is an immutable content hash.", "Supply-chain safety.", "Pin `nginx@sha256:...` in production."),
("Intermediate", "How do you pass secrets?", "Runtime env/secret files, Docker secrets or a secret manager; never bake into image layers.", "Security basics.", "Use `.env` (gitignored) locally and Vault/AWS Secrets Manager in production."),
("Intermediate", "How do you reduce image size?", "Slim/alpine/distroless base, multi-stage, combine RUN commands, clean caches, `.dockerignore`.", "Speed and attack surface.", "python:3.12-slim instead of python:3.12."),
("Intermediate", "What is a healthcheck?", "A command Docker runs periodically to decide if the container is healthy.", "Readiness and self-healing.", "`HEALTHCHECK CMD curl -f http://localhost/health`."),
("Intermediate", "How do containers log?", "Apps write to stdout/stderr; Docker's logging driver captures it (json-file by default).", "Twelve-factor logging.", "`docker logs`, then Fluent Bit ships to Loki."),
("Intermediate", "docker compose down vs down -v?", "`down` removes containers and networks; `-v` also removes named volumes (data loss).", "Avoid deleting DB data.", "Run `down -v` only in dev."),
("Advanced", "Explain Docker architecture.", "CLI talks via REST API to dockerd, which manages images/networks/volumes and delegates container lifecycle to containerd, which uses runc (OCI runtime) to create the container through the Linux kernel.", "Shows internals.", "Kubernetes can use containerd directly without dockerd."),
("Advanced", "How are containers isolated?", "Namespaces (pid, net, mnt, uts, ipc, user) give isolated views; cgroups limit CPU/memory/IO; capabilities and seccomp reduce privileges.", "Core internals.", "`unshare --pid --fork` demonstrates a PID namespace."),
("Advanced", "Explain overlay filesystem.", "OverlayFS stacks read-only image layers (lowerdir) with a writable upperdir; copy-on-write on modification.", "Explains layer sharing and write performance.", "Many containers share the same image layers on disk."),
("Advanced", "What is PID 1 problem in containers?", "The main process is PID 1, which does not get default signal handlers and must reap zombies. Shell form CMD makes `sh` PID 1 and swallows SIGTERM.", "Graceful shutdown bugs.", "Use exec form or `tini`/`--init`."),
("Advanced", "Rootless Docker vs root?", "Rootless runs the daemon and containers without root using user namespaces, reducing host risk but with networking/storage limitations.", "Security hardening.", "Shared CI hosts."),
("Advanced", "How does BuildKit improve builds?", "Parallel stage execution, better caching, cache mounts, secret mounts, and multi-platform builds.", "Modern build knowledge.", "`RUN --mount=type=cache` speeds npm/pip installs."),
("Advanced", "How to build multi-architecture images?", "`docker buildx build --platform linux/amd64,linux/arm64 --push`, producing a manifest list.", "ARM (Graviton, Apple Silicon) is common.", "Same tag works on M-series Mac and x86 server."),
("Advanced", "Secure a container image supply chain.", "Minimal base, pinned digests, scan (Trivy), SBOM (Syft), sign (cosign), verify in admission control, private registry.", "Security maturity.", "Kubernetes admission policy only allows signed images."),
("Advanced", "Why is mounting docker.sock dangerous?", "Access to the socket equals root on the host because the container can start privileged containers.", "Frequent security finding.", "CI job that builds images should use Kaniko/BuildKit rootless."),
("Advanced", "Docker networking internals for bridge?", "A virtual `docker0`/custom bridge, veth pairs per container, iptables NAT for published ports, embedded DNS at 127.0.0.11.", "Debugging connectivity.", "`iptables -t nat -L` shows the DNAT rule for `-p`."),
("Advanced", "What happens on `docker run`?", "CLI calls API; daemon checks local image, pulls if absent, creates container config, sets up namespaces/cgroups/network/mounts via containerd+runc, starts the process.", "End-to-end understanding.", "First run is slow because of the pull."),
("Advanced", "Capabilities and seccomp?", "Capabilities split root power into units; Docker drops many by default. Seccomp filters syscalls. Use `--cap-drop ALL` then add only what is needed.", "Least privilege.", "Web server only needs NET_BIND_SERVICE for port 80."),
("Advanced", "How to handle log growth?", "Set `--log-opt max-size=10m --log-opt max-file=3` or configure daemon.json; or use a remote logging driver.", "Disk-full incidents.", "Unbounded json-file logs filled a production disk."),
("Advanced", "Docker Swarm vs Kubernetes?", "Swarm is simpler and built in; Kubernetes has a richer ecosystem, extensibility and industry adoption.", "Tool selection reasoning.", "Most companies choose Kubernetes for new platforms."),
("Advanced", "Immutable infrastructure with containers?", "Never patch a running container; build a new image and replace. Config comes from environment.", "Reliability and reproducibility.", "Rollback = redeploy previous tag."),
("Scenario-Based", "API cannot reach Postgres in Compose.", "Check both are in the same network, use the service name as host, check DB health, credentials and port 5432 inside the network (not host port).", "Tests systematic debugging.", "`docker compose exec api nc -zv db 5432`."),
("Scenario-Based", "Image is 1.5 GB, make it small.", "Multi-stage, slim/distroless base, `.dockerignore`, remove build tools, `--omit=dev`, check layers with `dive`.", "Practical optimisation.", "Java app with JRE-only final image."),
("Scenario-Based", "Disk on the Docker host is full.", "`docker system df`, prune unused images/containers/build cache, check large logs and volumes, set log rotation.", "Frequent ops incident.", "`docker system prune -a` after checking what is unused."),
("Scenario-Based", "Container keeps restarting.", "`docker logs`, exit code, OOMKilled, healthcheck, restart policy loop, config missing.", "Diagnosis order matters.", "Exit 137 means OOM or SIGKILL."),
("Scenario-Based", "Database data disappeared after redeploy.", "No volume, or `down -v` used, or volume path wrong. Restore from backup and mount a named volume.", "Data safety.", "Postgres path must be /var/lib/postgresql/data."),
("Scenario-Based", "Critical CVE reported in production image.", "Rebuild on patched base, pin digest, redeploy, add scan gate to CI, automate updates with Renovate/Dependabot.", "Security process.", "openssl vulnerability in base image."),
("Scenario-Based", "Need zero-downtime deploy with Compose.", "Compose alone is limited; use rolling with multiple replicas behind a proxy, or move to Kubernetes/Swarm.", "Knowing the tool's limits.", "Nginx upstream + `--scale api=2` then replace one by one."),
("Scenario-Based", "Different behaviour in dev and prod.", "Ensure the same image is promoted; move differences to env/config; compare `docker inspect`, env and mounts.", "Environment parity.", "Dev used bind mount with different node_modules."),
("Scenario-Based", "App works on Mac M1 but fails on the Linux server.", "Architecture mismatch; build multi-arch or set `--platform linux/amd64`.", "Modern issue.", "`exec format error` in logs."),
("Scenario-Based", "Team wants to run 100 containers across servers.", "Recommend Kubernetes (or ECS): scheduling, self-healing, service discovery, rolling updates.", "Knowing when to move beyond Docker.", "Compose on one host cannot survive node failure."),
("Scenario-Based", "How to secure CI image builds?", "Use rootless BuildKit/Kaniko, no docker.sock, scan and sign, short-lived registry credentials.", "DevSecOps.", "GitHub Actions with OIDC to ECR."),
("Scenario-Based", "A container needs a secret at startup.", "Inject via runtime secret/env from a secret manager; never commit or bake into the image.", "Secrets handling.", "Docker/Kubernetes secret mounted as a file."),
("Scenario-Based", "How do you roll back a bad release?", "Redeploy previous immutable tag/digest; keep last N tags in registry.", "Release safety.", "`docker compose up -d` with `IMAGE_TAG=1.4.2`."),
("Scenario-Based", "Two services need to share files.", "Use a shared named volume (read-only on the consumer) or an object store; avoid bind mounts across hosts.", "Design judgement.", "Uploads volume shared by API and worker."),
("Scenario-Based", "Reduce build time in CI.", "Layer order, BuildKit cache export/import (`--cache-from/--cache-to`), smaller context, parallel stages.", "Pipeline performance.", "Registry cache cut build from 8 to 2 minutes."),
("Troubleshooting-Based", "Port already allocated error?", "Another process/container uses the host port; find it with `ss -tulpn` or `docker ps` and change the mapping.", "Common start failure.", "Two nginx containers mapped to 80."),
("Troubleshooting-Based", "Permission denied on bind mount?", "UID/GID mismatch between host files and container user; fix ownership or use a named volume. SELinux hosts may need `:z`.", "File permission issues.", "Postgres cannot write to a host folder."),
("Troubleshooting-Based", "Container cannot resolve external DNS.", "Check host DNS/resolv.conf, corporate proxy, set `--dns`, test with `nslookup` in the container.", "Networking debug.", "VPN changes DNS and breaks builds."),
("Troubleshooting-Based", "Container cannot reach the internet.", "Check IP forwarding, iptables/firewall rules, proxy variables, MTU.", "Network layers.", "Docker + ufw blocking forward chain."),
("Troubleshooting-Based", "docker build fails at `RUN npm install`.", "Read the error: network/proxy, missing lockfile, native build tools missing on alpine, memory. Reproduce with `docker run -it base sh`.", "Build debugging.", "bcrypt needs python/make on alpine."),
("Troubleshooting-Based", "Container healthy but requests time out.", "App binds to 127.0.0.1, wrong proxy upstream, port mismatch, security group, or DB slowness.", "Layered diagnosis.", "Fix `HOST=0.0.0.0`."),
("Troubleshooting-Based", "`docker logs` is empty.", "App logs to a file instead of stdout, or crashes before logging. Redirect logs to stdout; check `docker inspect` for log driver.", "Logging convention.", "Symlink /var/log/nginx/access.log to /dev/stdout."),
("Troubleshooting-Based", "Image pull fails: rate limit or unauthorized.", "Docker Hub pull limits or missing `docker login`/expired token; use a registry mirror or private registry.", "Registry operations.", "CI hitting Docker Hub limits."),
("Troubleshooting-Based", "Compose changes not applied.", "Need `docker compose up -d` again (recreates changed services); images need `--build`; check `docker compose config`.", "Workflow knowledge.", "Env change requires recreate."),
("Troubleshooting-Based", "Container uses too much memory.", "`docker stats`, profile the app, set limits, watch OOMKilled, check log/tmpfs usage.", "Resource control.", "Node heap growth needs `--max-old-space-size`.")],
cheatsheet={
"Definitions": ["Image: read-only layered template. Container: running instance. Registry: image store.", "Layer: result of one Dockerfile instruction, cached by hash.", "Namespace = SEE; cgroup = USE.", "Volume: Docker-managed persistent storage."],
"Commands": ["`docker build -t app:1.0 .` | `docker run -d --name web -p 8080:80 app:1.0`", "`docker ps [-a]` | `docker logs -f web` | `docker exec -it web sh`", "`docker stop|start|restart|rm web` | `docker images` | `docker rmi img`", "`docker inspect web` | `docker stats` | `docker system df` | `docker system prune`", "`docker network create n` | `docker volume create v`", "`docker compose up -d --build` | `docker compose down [-v]` | `docker compose logs -f svc`", "`docker buildx build --platform linux/amd64,linux/arm64 --push .`"],
"Files": ["Dockerfile", ".dockerignore", "compose.yml (or docker-compose.yml)", ".env", "/etc/docker/daemon.json"],
"Architecture": ["Docker CLI > Docker API > dockerd > containerd > runc > Linux kernel > container"],
"Ports": ["HTTP 80, HTTPS 443, Node 3000, PostgreSQL 5432, MySQL 3306, Redis 6379, MongoDB 27017, Docker API TCP 2375 (insecure) / 2376 (TLS)"],
"Differences": ["Container vs VM: shared kernel vs own OS.", "CMD vs ENTRYPOINT.", "COPY vs ADD.", "EXPOSE vs -p.", "Volume vs bind mount vs tmpfs.", "Compose vs Kubernetes."],
"Troubleshooting commands": ["`docker ps -a` > `docker logs` > `docker inspect` > `docker exec` > `curl` > `docker stats` > `docker events`"],
"Best practices": ["Pin tags/digests, non-root user, multi-stage, .dockerignore, healthchecks, limits, log rotation, scan + sign, volumes for data, one process per container."]}
),
subs={
"docker-basics": dict(
define=dict(simple="Docker puts your app and everything it needs in one box (image) and runs that box (container) anywhere.",
technical="Docker is a container platform: a client (`docker`) talks to a daemon (`dockerd`) that builds OCI images and runs containers as isolated Linux processes using namespaces, cgroups and a layered union filesystem, through containerd and runc.",
why="To eliminate environment differences between dev, test and production and to start workloads quickly.",
without="Manual installs on each server, version drift, 'works on my machine', slow VMs, hard rollbacks.",
use="Microservices, CI builds, reproducible dev environments, packaging apps for Kubernetes.",
avoid="Apps needing a different kernel/OS, strong multi-tenant isolation without extra hardening, or heavy GUI desktop apps.",
analogy="A shipping container: any cargo, same box, any ship or truck can move it."),
internals="""1) You type `docker run`. The **Docker CLI** converts it into a REST API call. 2) **dockerd** receives it, checks whether the image exists locally and pulls missing layers from the registry. 3) It asks **containerd** to create the container. 4) containerd uses **runc**, which asks the **Linux kernel** to create namespaces (own PID, network, mount view) and a cgroup (CPU/memory limits) and starts your process as PID 1. 5) The result is an isolated process that shares the host kernel.""",
realworld=dict(diagram="""Browser -> Nginx (80) -> Node API (3000) -> PostgreSQL (5432)
                              \\-> Redis (6379)""",
text="""In a typical web project each box is one container. Nginx exposes port 80 to the host; API, Postgres and Redis are on a private user-defined network and talk by service name. Postgres data is in a named volume. If the API container crashes, `restart: unless-stopped` restarts it; if Postgres fails, the API healthcheck fails and alerts fire from Prometheus. Deployment is `docker compose pull && up -d`; monitoring uses `docker stats`/cAdvisor."""),
commands=[
("docker ps", "Lists **running** containers.", "`-a` all containers (including stopped), `-q` only IDs, `--filter status=exited`, `--format`.", "CONTAINER ID  IMAGE  COMMAND  CREATED  STATUS  PORTS  NAMES", "Forgetting `-a`, then thinking the container disappeared when it exited.", "Missing container? Run `docker ps -a`, then `docker logs <id>` and check the exit code."),
("docker run -d --name web -p 8080:80 nginx:1.27", "Creates and starts a container from an image.", "`-d` detached, `--name`, `-p host:container`, `-e VAR=v`, `-v vol:/path`, `--rm`, `--restart`, `--memory`, `--cpus`.", "Prints the new container ID.", "Using `-p 80:8080` reversed; running without `-d` and blocking the terminal.", "`Bind for 0.0.0.0:8080 failed`: port used; pick another host port."),
("docker logs -f --tail 100 web", "Shows stdout/stderr of a container.", "`-f` follow, `--tail N`, `--since 10m`, `-t` timestamps.", "Application log lines.", "Expecting file logs; only stdout/stderr are captured.", "Empty logs: app writes to a file, or crashed before logging."),
("docker exec -it web sh", "Runs a command inside a running container.", "`-i` keep stdin, `-t` TTY, `-u user`, `-w dir`.", "A shell prompt inside the container.", "Using `bash` on alpine (only `sh` exists).", "`container is not running`: use `docker run --entrypoint sh` instead."),
("docker system prune -af", "Removes unused containers, networks, images, build cache.", "`-a` all unused images, `--volumes` also volumes (dangerous).", "Reclaimed space total.", "Adding `--volumes` and deleting database data.", "Check `docker system df` first.")],
lab=dict(goal="Run an Nginx web server in a container, view logs, enter it and clean up.", prereq=["Docker Engine or Docker Desktop installed", "Terminal access", "Port 8080 free"],
steps=[("docker run -d --name web -p 8080:80 nginx:1.27", "Pulls the image (first time) and starts a container in the background. Internally: API call > dockerd > containerd > runc > namespaces/cgroups. Output: a long container ID."),
("docker ps\ncurl -I http://localhost:8080", "`docker ps` shows the container and `0.0.0.0:8080->80/tcp`. `curl` should return `HTTP/1.1 200 OK` and `Server: nginx`."),
("docker logs web\ndocker exec -it web sh -c 'ls /usr/share/nginx/html'", "Shows the access log line for your curl and lists the default web files inside the container."),
("docker stop web && docker rm web && docker rmi nginx:1.27", "Graceful stop (SIGTERM), removes the container and finally the image. Data inside the container is gone.")]),
compare=[("docker stop vs docker kill", ["Topic", "stop", "kill"], [["Signal", "SIGTERM, then SIGKILL after 10s", "SIGKILL immediately"], ["Graceful shutdown", "Yes", "No"]])],
mnemonics=[("Container lifecycle", "create > start > pause > stop > rm"), ("Run flags", "d = detach, p = publish, e = env, v = volume, it = interactive terminal")],
hinglish="Image ek **template** hai aur container uska **chalta hua instance**. Container delete karoge to uske andar ka data bhi jayega, isliye volume lagao.",
versions=["`docker container ls` is the modern long form of `docker ps` (both work).", "Docker Desktop on Windows needs WSL2 or Hyper-V."],
practices={"Production": ["Pin versions, set restart policy and limits.", "One process per container."], "Security": ["Do not run as root; do not use `--privileged`."]},
mistakes={"Beginner mistakes": ["Using `latest`.", "Not naming containers.", "Not cleaning up unused images."]},
callouts=[("tip", "Practice loop: run > break it on purpose > read `docker logs` > fix. That is how you learn troubleshooting."), ("warn", "`docker system prune -a --volumes` deletes unused volumes, which may contain database data.")],
qa_extra=[("Intermediate", "What happens internally on `docker run`?", "CLI > API > dockerd pulls the image if needed > containerd > runc creates namespaces + cgroups + mounts > process starts as PID 1.", "Shows internals knowledge.", "First run is slow due to the image pull.")]),

"dockerfile": dict(
define=dict(simple="A Dockerfile is a recipe: step by step instructions to build an image.",
technical="A Dockerfile is a text file of instructions parsed by BuildKit; each filesystem-changing instruction creates a cached layer, and the final layers form an OCI image with metadata (CMD, ENV, EXPOSE, USER).",
why="Reproducible, reviewable and versioned image creation.", without="Manual image creation via `docker commit`, not reproducible.",
use="Every application you ship as a container.", avoid="Do not put secrets or large data in it.", analogy="A cooking recipe: same steps, same dish every time."),
internals="""`docker build` sends the **build context** (files in the folder, minus `.dockerignore`) to BuildKit. BuildKit executes stages in order: each instruction is hashed with its inputs; an unchanged hash reuses the **cached layer**. `COPY --from=build` copies only the final artifacts into a tiny runtime stage, so build tools never reach production. The resulting image has layers + a config (CMD, USER, ENV).""",
config=[("Node.js multi-stage Dockerfile explained", """FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine
WORKDIR /app
ENV NODE_ENV=production
COPY --from=build /app/dist ./dist
COPY --from=build /app/node_modules ./node_modules
USER node
EXPOSE 3000
HEALTHCHECK CMD wget -qO- localhost:3000/health || exit 1
CMD ["node","dist/server.js"]""", [
("FROM node:20-alpine AS build", "Base image: `node` = runtime, `20` = major version (pinned so builds are repeatable), `alpine` = tiny Linux. `AS build` names this stage."),
("WORKDIR /app", "Sets the working directory; creates it if missing so later commands use relative paths."),
("COPY package*.json ./", "Copies only dependency manifests first. If they do not change, the next `RUN npm ci` layer is served from cache."),
("RUN npm ci", "Clean, reproducible install from the lockfile (faster and stricter than `npm install`)."),
("COPY . .", "Copies the rest of the source AFTER dependencies so code edits do not invalidate the install layer."),
("FROM node:20-alpine", "Starts a fresh, small final stage; build tools from stage 1 are left behind."),
("ENV NODE_ENV=production", "Makes frameworks run in production mode."),
("COPY --from=build ...", "Pulls only built artifacts from the build stage."),
("USER node", "Runs as a non-root user to limit damage if the app is compromised."),
("EXPOSE 3000", "Documents the port; does NOT publish it (use `-p`)."),
("HEALTHCHECK ...", "Lets Docker/Compose know if the app is really serving."),
("CMD [\"node\",\"dist/server.js\"]", "Exec form so `node` is PID 1 and receives SIGTERM for graceful shutdown.")])],
lab=dict(goal="Build a small Node.js image, compare cache behaviour and run it.", prereq=["Docker installed", "A folder with package.json, server.js and the Dockerfile above"],
steps=[("docker build -t myapp:1.0 .", "Builds the image. Watch each step; first build has no `CACHED`."),
("echo '// change' >> server.js && docker build -t myapp:1.1 .", "Only layers after `COPY . .` rebuild; `npm ci` shows CACHED, proving correct layer order."),
("docker images myapp && docker history myapp:1.1", "Shows image size and the size contributed by every layer."),
("docker run -d --name app -p 3000:3000 myapp:1.1 && curl localhost:3000/health", "Runs and tests it. Expected: your health response.")]),
compare=[("Base image choices", ["Base", "Size", "Pros", "Cons"], [["ubuntu/debian", "Large", "Familiar, many tools", "Bigger attack surface"], ["slim", "Medium", "Good compatibility", "Fewer tools"], ["alpine", "Small (~5MB)", "Tiny, fast pulls", "musl libc can break some native modules"], ["distroless", "Very small", "No shell, minimal CVEs", "Harder to debug"]])],
commands=[("docker build -t myapp:1.0 -f Dockerfile .", "Builds an image from a Dockerfile and a context folder.", "`-t name:tag`, `-f file`, `--no-cache`, `--target stage`, `--build-arg K=V`, `--platform`.", "Step-by-step build log, then `naming to docker.io/library/myapp:1.0`.", "Building from a huge folder without `.dockerignore`.", "`COPY failed: file not found`: the path is outside the build context.")],
mnemonics=[("Layer order", "Least changing first, most changing last."), ("Cache rule", "One changed layer invalidates everything below it.")],
hinglish="Dockerfile mein **dependencies pehle copy karo, source baad mein**, taaki har code change par npm install dobara na chale. Multi-stage build se final image chhoti aur secure hoti hai.",
practices={"Production": ["Pin base image version or digest.", "Multi-stage, non-root, healthcheck, exec-form CMD."], "Security": ["No secrets in ENV/COPY; use BuildKit `--secret`.", "Scan with Trivy; lint with hadolint."], "Performance": ["Use BuildKit cache mounts and `.dockerignore`."]},
mistakes={"Developer mistakes": ["`COPY . .` before installing dependencies.", "Using shell-form CMD so SIGTERM is ignored.", "Leaving build tools in the final image."], "Security mistakes": ["`COPY .env` into the image.", "Running as root."]},
versions=["BuildKit is the default builder in current Docker; `--mount=type=cache` and `--mount=type=secret` need BuildKit.", "Alpine uses musl libc; some prebuilt binaries need `libc6-compat` or a Debian slim base."],
callouts=[("warn", "Anything you COPY or ENV into a layer stays in image history even if you delete it in a later layer. Never bake secrets.")],
qa_extra=[("Advanced", "How would you pass an npm token during build without leaking it?", "Use BuildKit secrets: `RUN --mount=type=secret,id=npmrc ...` and `docker build --secret id=npmrc,src=.npmrc`. The secret is not stored in layers.", "Secure builds.", "Private npm registry in CI.")]),

"docker-networking-volumes": dict(
define=dict(simple="Networks let containers talk to each other; volumes keep data after a container is deleted.",
technical="Docker networking uses virtual bridges, veth pairs, iptables NAT and an embedded DNS server (127.0.0.11) on user-defined networks. Storage uses named volumes (managed under /var/lib/docker/volumes), bind mounts and tmpfs mounts.",
why="Isolation and service discovery between containers; persistent state.", without="Hard-coded IPs and lost data.", use="Any multi-container app or stateful service.", avoid="Do not use the host network without a reason (no isolation).", analogy="Network = office intercom by name; volume = external hard-disk that survives changing laptops."),
internals="""On a user-defined bridge, Docker creates a Linux bridge and a **veth pair** per container. Containers get private IPs; an embedded **DNS** resolves service names to IPs. `-p 8080:80` adds an **iptables DNAT** rule from the host port to the container IP:port. A **volume** is a directory managed by Docker mounted into the container's mount namespace, so it lives independently of the container's writable layer.""",
realworld=dict(diagram="""host:8080 -> [web:80] --appnet--> [api:3000] --appnet--> [db:5432]
                                                       |
                                                 volume pgdata""", text="Only `web` publishes a port. `api` reaches `db` at `db:5432` using DNS on `appnet`. Postgres data is stored in `pgdata`. If `api` fails, `web` returns 502 and Prometheus alerts; if `db` is recreated, data remains in `pgdata`. Backups are taken by a tar container."),
commands=[("docker network inspect appnet", "Shows subnet, gateway and connected containers with IPs.", "`--format '{{json .Containers}}'`.", "JSON with Containers section.", "Inspecting the wrong network (default `bridge`).", "Container missing from the list? It was started without `--network appnet`."),
("docker volume ls / docker volume inspect pgdata", "Lists volumes / shows mountpoint on host.", "`docker volume prune` removes unused volumes.", "Name, driver local, Mountpoint.", "Pruning volumes that look unused but hold data.", "Verify with `docker ps -a --filter volume=pgdata`.")],
lab=dict(goal="Create a network and a volume, run Postgres + a client and prove data persists.", prereq=["Docker installed"],
steps=[("docker network create appnet && docker volume create pgdata", "Creates a user-defined bridge network and a named volume."),
("docker run -d --name db --network appnet -e POSTGRES_PASSWORD=secret -v pgdata:/var/lib/postgresql/data postgres:16", "Starts Postgres with data stored in the volume."),
("docker run --rm --network appnet postgres:16 psql -h db -U postgres -c 'create table t(id int); insert into t values (1);'", "The client resolves `db` by DNS. Expected: `INSERT 0 1` (password: set PGPASSWORD=secret)."),
("docker rm -f db && docker run -d --name db --network appnet -e POSTGRES_PASSWORD=secret -v pgdata:/var/lib/postgresql/data postgres:16", "New container, same volume: the table `t` still exists. Data survived because it lives in the volume.")]),
compare=[("Network drivers", ["Driver", "Use", "Notes"], [["bridge", "Default single-host networking", "User-defined bridge gives DNS"], ["host", "Share host network stack", "No isolation, no -p; behaves differently on Docker Desktop"], ["overlay", "Multi-host (Swarm)", "VXLAN based"], ["macvlan", "Container gets its own MAC/IP on LAN", "Special cases"], ["none", "No networking", "Fully isolated"]])],
mnemonics=[("Ports", "HOST first, CONTAINER second: -p 8080:80"), ("Storage", "Volume for data, bind for code, tmpfs for secrets")],
hinglish="Default bridge par containers naam se ek dusre ko nahi dhoondh paate. **User-defined network** banao to naam (DNS) se connect ho jata hai. Database ka data hamesha **volume** mein rakho.",
practices={"Production": ["Expose only the reverse proxy port.", "Use named volumes and back them up."], "Security": ["Keep DB on an internal network (`internal: true`)."]},
mistakes={"Beginner mistakes": ["Publishing DB port 5432 to the world.", "Using `localhost` to reach another container."]},
qa_extra=[("Advanced", "How does `-p` work internally?", "Docker adds iptables DNAT rules (and a docker-proxy for some cases) forwarding host:port to containerIP:port on the bridge.", "Debugging connectivity.", "`iptables -t nat -L DOCKER` shows the mapping.")]),

"docker-compose": dict(
define=dict(simple="One YAML file that starts your whole app stack with one command.",
technical="Docker Compose (v2 plugin, Compose Specification) declares services, networks and volumes in YAML and creates/updates them via the Docker Engine API on a single host.",
why="Repeatable multi-container environments.", without="Long `docker run` commands typed by hand and easy to forget.", use="Local development, testing, small single-host deployments.", avoid="Multi-node production needing self-healing/autoscaling: use Kubernetes/ECS.", analogy="A conductor's score for the whole orchestra."),
internals="""`docker compose up` reads the YAML, creates the project network, volumes, then builds/pulls images and starts services in dependency order. Names are prefixed with the project (folder) name. Service names become DNS names on the network. On re-run Compose compares config and recreates only changed services.""",
config=[("Line-by-line: key parts of the 3-tier stack", """api:
    build: ./api
    environment:
      DB_URL: postgres://app:secret@db:5432/app
    depends_on:
      db: { condition: service_healthy }
db:
    image: postgres:16
    volumes: [pgdata:/var/lib/postgresql/data]
    healthcheck:
      test: ["CMD-SHELL","pg_isready -U app"]""", [
("build: ./api", "Build the image from the Dockerfile in ./api (use `image:` to pull instead)."),
("environment:", "Injects config as env variables; port is the container port 5432, not a host port."),
("db:5432", "`db` is the service name resolved by Compose DNS."),
("depends_on ... service_healthy", "Waits until the DB healthcheck passes, avoiding startup race conditions."),
("volumes: pgdata:...", "Persistent named volume for database files."),
("healthcheck test", "`pg_isready` tells Compose the DB accepts connections.")])],
lab=dict(goal="Run a web + Redis stack with Compose.", prereq=["Docker with Compose v2 (`docker compose version`)"],
steps=[("mkdir demo && cd demo && printf 'services:\\n  web:\\n    image: nginx:1.27\\n    ports: [\"8080:80\"]\\n  cache:\\n    image: redis:7-alpine\\n' > compose.yml", "Creates a minimal compose file."),
("docker compose up -d", "Creates network `demo_default`, pulls images, starts both services."),
("docker compose ps && docker compose exec cache redis-cli ping", "Both services Up; Redis replies `PONG`."),
("docker compose down", "Stops and removes containers and network. Add `-v` only if you also want to delete volumes.")]),
compare=[("Ways to run multiple containers", ["Tool", "Scope", "When"], [["docker run", "One container", "Quick test"], ["Compose", "One host", "Dev/small apps"], ["Swarm", "Small cluster", "Simple orchestration"], ["Kubernetes", "Cluster", "Production at scale"]])],
commands=[("docker compose up -d --build", "Builds images if needed and starts all services in the background.", "`--build`, `--force-recreate`, `--scale svc=N`, `-f file`, `--profile`.", "Container xxx Started for each service.", "Editing code but forgetting `--build`.", "Use `docker compose config` to validate and view the merged file.")],
mnemonics=[("Compose lifecycle", "up > ps > logs > exec > down")],
hinglish="Compose se **ek command mein poora stack** start hota hai. `depends_on` sirf start order deta hai; DB ready hone ka wait chahiye to **healthcheck + service_healthy** lagao.",
versions=["Use `docker compose` (v2). `docker-compose` v1 is end-of-life and the top-level `version:` key is obsolete.", "Compose file name: `compose.yaml` is preferred; `docker-compose.yml` still works."],
practices={"Production": ["Use `-f compose.yml -f compose.prod.yml` overrides.", "Do not commit `.env` with secrets."], "Reliability": ["Set `restart: unless-stopped` and healthchecks."]},
mistakes={"DevOps mistakes": ["Using Compose for multi-node production.", "Using `down -v` on a shared/persistent environment."]},
qa_extra=[("Scenario-Based", "How do you run different configs for dev and prod with Compose?", "Base `compose.yml` plus override files (`compose.prod.yml`), env files and profiles.", "Environment management.", "Dev mounts source; prod uses built image and no bind mounts.")]),

"docker-security-internals": dict(
define=dict(simple="Containers are isolated processes; security means limiting what they can see, use and do.",
technical="Container isolation = namespaces (pid, net, mnt, uts, ipc, user, cgroup) + cgroups (resource limits) + capabilities + seccomp/AppArmor/SELinux + optional user namespaces/rootless, executed by containerd/runc according to the OCI spec.",
why="A shared kernel means a container breakout can compromise the host, so we reduce privileges.", without="Root containers with full capabilities: one vulnerable app can own the host.", use="Always.", avoid="N/A", analogy="Apartments in one building (kernel): separate rooms and rules, but one shared structure."),
internals="""runc calls `clone()/unshare()` to create namespaces, sets cgroup limits, drops capabilities, applies the seccomp profile, pivots root into the image's filesystem (overlayfs) and executes the entrypoint. Each layer of protection blocks a different attack: namespaces hide other processes, cgroups stop resource abuse, capabilities/seccomp limit dangerous syscalls, read-only FS stops persistence, image scanning removes known CVEs.""",
config=[("Hardened run flags explained", """docker run -d --read-only --tmpfs /tmp \\
  --cap-drop ALL --security-opt no-new-privileges \\
  --user 10001 --pids-limit 200 myapp:1.0""", [
("--read-only", "Makes the root filesystem read-only, so malware cannot write binaries."),
("--tmpfs /tmp", "Gives the app a writable in-memory temp directory."),
("--cap-drop ALL", "Removes all Linux capabilities; add back only what is required with `--cap-add`."),
("--security-opt no-new-privileges", "Prevents gaining privileges via setuid binaries."),
("--user 10001", "Non-root UID."),
("--pids-limit 200", "Stops fork bombs.")])],
lab=dict(goal="See a PID namespace and scan an image.", prereq=["Linux host or WSL2", "Docker", "Trivy (or use the aquasec/trivy container)"],
steps=[("sudo unshare --pid --fork --mount-proc bash\nps aux", "You are in a new PID namespace; `ps` shows only a few processes, proving isolation without Docker."),
("exit\ndocker run --rm aquasec/trivy image --severity HIGH,CRITICAL nginx:1.27", "Scans the image for HIGH/CRITICAL CVEs and prints a table."),
("docker run --rm --read-only alpine sh -c 'touch /x'", "Fails with `Read-only file system`, proving the hardening flag works.")]),
compare=[("Docker vs containerd vs runc", ["Component", "Role"], [["Docker (dockerd)", "Full tooling: build, network, volumes, API"], ["containerd", "Container lifecycle/image management runtime (used by Kubernetes)"], ["runc", "Low-level OCI runtime that creates the container via kernel"]]), ("Namespaces vs cgroups", ["Topic", "Namespaces", "cgroups"], [["Controls", "What a process can SEE", "What a process can USE"], ["Examples", "pid, net, mnt, user", "cpu, memory, io, pids"]])],
mnemonics=[("Namespace vs cgroups", "SEE vs USE"), ("Hardening", "R-C-N-U: Read-only, Caps dropped, No-new-privileges, User non-root")],
hinglish="Container ek **normal Linux process** hi hai. **Namespace** decide karta hai ki wo kya *dekh* sakta hai, **cgroups** decide karta hai ki wo kitna *use* kar sakta hai. Security ke liye non-root, minimal image, scan aur read-only filesystem lagao.",
practices={"Security": ["Non-root, minimal/distroless images.", "Scan in CI, sign with cosign, produce SBOM, verify at deploy.", "Never mount docker.sock; avoid `--privileged`.", "Use rootless Docker/Podman on shared hosts."]},
mistakes={"Security mistakes": ["`--privileged` for convenience.", "Secrets in image layers or environment printed in logs.", "Ignoring base image updates."]},
versions=["Rootless mode and user-namespace remap have feature limits (low ports, some storage drivers).", "`docker scan` is removed; use `docker scout` or Trivy.", "Docker's default seccomp profile blocks ~44 syscalls; verify in the docs for your version."],
callouts=[("warn", "Containers share the host kernel: a kernel vulnerability affects all containers. For hostile multi-tenant workloads consider gVisor, Kata Containers or VMs.")],
qa_extra=[("Scenario-Based", "How do you prove an image running in production came from your pipeline?", "Sign with cosign in CI, store signature in the registry, and enforce verification with an admission controller (Kyverno/Sigstore policy).", "Supply-chain security.", "Only signed images from Harbor are allowed in the cluster.")])
})
