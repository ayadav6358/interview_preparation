TOPIC = dict(slug="05-docker", title="Docker & Containers", intro="'Mere machine pe chal raha hai' ka solution. App + dependencies ek image mein pack hote hain aur har jagah same chalte hain.", subs=[

dict(slug="docker-basics", title="Docker Basics: Images & Containers", level="Basic",
intro="Image = read-only template. Container = running instance. VM poora OS chalata hai, container host kernel share karta hai isliye halka aur fast hai.",
diagram="""
VM:        App | Bins | Guest OS | Hypervisor | Host
Container: App | Bins |  Docker Engine (shares host kernel) | Host

Dockerfile --build--> Image --run--> Container
                        |--push--> Registry (Docker Hub / ECR)
""",
install="""# Ubuntu
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER && newgrp docker
docker run hello-world
# Windows/Mac: Docker Desktop (WSL2 backend)""",
examples=[("Essential commands","""docker pull nginx:1.27
docker run -d --name web -p 8080:80 nginx:1.27
docker ps; docker ps -a
docker logs -f web
docker exec -it web sh
docker stop web && docker rm web
docker images; docker rmi nginx:1.27
docker system prune -af          # cleanup unused"""),
("Run with env and resource limits","""docker run -d --name api -p 3000:3000 \\
  -e NODE_ENV=production --memory=256m --cpus=0.5 \\
  --restart unless-stopped myapp:1.0""")],
problems=[("Port already allocated","Another process/container uses 8080","`docker ps`, `ss -tulpn | grep 8080`; change host port."),
("Disk full on Docker host","Old images/containers/build cache","`docker system df`; `docker system prune -a --volumes` (careful); schedule cleanup."),
("Container exits immediately","Main process ended / crashed","`docker logs <c>`; a container lives as long as PID 1 runs.")],
qa=[("Container vs VM?","Containers share host kernel, lightweight, seconds start; VMs have full OS, stronger isolation."),
("What is a Docker image layer?","Each Dockerfile instruction creates a read-only layer; cached and shared."),
("docker stop vs kill?","stop sends SIGTERM then SIGKILL after grace; kill sends SIGKILL immediately."),
("How to see resource usage?","`docker stats`."),
("What is Docker daemon?","`dockerd` background service managing images, containers, networks, volumes.")]),

dict(slug="dockerfile", title="Dockerfile & Image Optimization", level="Intermediate",
intro="Dockerfile image ka recipe hai. Layer order, cache, multi-stage builds, non-root user aur chhoti image production ke liye zaroori hain.",
diagram="""
Stage 1 (build): node:20 + devDeps + compile  --\\
                                                 +--> COPY artifacts only
Stage 2 (run):   node:20-alpine (small) <-------/     => 1GB -> ~100MB
""",
install="docker build -t myapp:1.0 .\nwinget/apt install hadolint dive   # lint + inspect layers",
examples=[("Optimized multi-stage Dockerfile","""FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./          # copy deps first -> cache friendly
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
CMD ["node","dist/server.js"]"""),
(".dockerignore","""node_modules
.git
.env
*.log"""),
("Python example","""FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
USER 1000
CMD ["gunicorn","-b","0.0.0.0:8000","app:app"]"""),
("Multi-arch build","""docker buildx build --platform linux/amd64,linux/arm64 -t user/app:1.0 --push .""")],
problems=[("Every code change reinstalls all dependencies (slow builds)","COPY . before package install breaks cache","Copy manifest first, install, then copy source."),
("Image is 1.2GB","Full base image, build tools included","Multi-stage, slim/alpine/distroless, .dockerignore."),
("App can't be stopped gracefully","Shell form CMD makes shell PID 1","Use exec form `CMD [\"node\",...]`; use `tini`.")],
qa=[("CMD vs ENTRYPOINT?","ENTRYPOINT is fixed executable; CMD provides default args (overridable). Combine for flexible CLIs."),
("COPY vs ADD?","ADD also extracts tar and fetches URLs; prefer COPY."),
("Why multi-stage builds?","Smaller, safer final image without build tools."),
("How to reduce image size?","Slim base, multi-stage, combine RUN, clean caches, .dockerignore."),
("Why not run as root?","Limits impact of container breakout; use USER.")]),

dict(slug="docker-networking-volumes", title="Docker Networking & Volumes", level="Intermediate",
intro="Containers ko aapas mein baat karwana (networks) aur data persist karna (volumes). Container delete hone par uska data chala jata hai, isliye volumes.",
diagram="""
Custom bridge network 'appnet':
  [web] --http--> [api] --tcp 5432--> [db]   (resolve by service name)
  host:8080 -> web:80 (port publish)

Storage: volume (managed by Docker) | bind mount (host path) | tmpfs (memory)
""",
install="# built into Docker",
examples=[("User-defined network & volume","""docker network create appnet
docker volume create pgdata
docker run -d --name db --network appnet -e POSTGRES_PASSWORD=secret -v pgdata:/var/lib/postgresql/data postgres:16
docker run -d --name api --network appnet -e DB_HOST=db -p 3000:3000 myapp:1.0
docker network inspect appnet; docker volume ls"""),
("Backup a volume","""docker run --rm -v pgdata:/data -v $PWD:/backup alpine tar czf /backup/pgdata.tgz -C /data .""")],
problems=[("API can't connect to DB by name","Default bridge has no DNS","Use user-defined network so container names resolve."),
("Data lost after `docker rm`","No volume used","Mount named volume for stateful paths."),
("Permission denied on bind mount","UID mismatch","Match user IDs / `chown`, or use named volumes.")],
qa=[("Volume vs bind mount?","Volume managed by Docker (portable, preferred); bind mount maps host path (dev convenience)."),
("Network drivers?","bridge, host, overlay (multi-host), macvlan, none."),
("How do containers on same network talk?","By container/service name via embedded DNS."),
("EXPOSE vs -p?","EXPOSE documents port only; `-p` actually publishes to host."),
("How to persist DB data?","Mount volume at DB data dir.")]),

dict(slug="docker-compose", title="Docker Compose (Multi-container Apps)", level="Intermediate",
intro="Ek YAML mein pura stack: web + api + db + redis. Local development aur small deployments ke liye best.",
diagram="""
docker-compose.yml
   ├── web (nginx)  :80 ──> api
   ├── api (node)   :3000 ──> db, redis
   ├── db (postgres) volume pgdata
   └── redis
""",
install="docker compose version   # bundled with modern Docker",
examples=[("3-tier stack","""services:
  web:
    image: nginx:1.27
    ports: ["80:80"]
    volumes: ["./nginx.conf:/etc/nginx/conf.d/default.conf:ro"]
    depends_on: [api]
  api:
    build: ./api
    environment:
      DB_URL: postgres://app:secret@db:5432/app
      REDIS: redis:6379
    depends_on:
      db: { condition: service_healthy }
  db:
    image: postgres:16
    environment: { POSTGRES_USER: app, POSTGRES_PASSWORD: secret, POSTGRES_DB: app }
    volumes: [pgdata:/var/lib/postgresql/data]
    healthcheck:
      test: ["CMD-SHELL","pg_isready -U app"]
      interval: 5s
  redis:
    image: redis:7
volumes:
  pgdata:"""),
("Commands","""docker compose up -d --build
docker compose ps; docker compose logs -f api
docker compose exec db psql -U app
docker compose down -v      # -v removes volumes""")],
problems=[("API starts before DB is ready and crashes","depends_on only orders start","Use healthcheck + `condition: service_healthy` and retries in app."),
("Secrets in compose file committed","Hard-coded passwords","Use `.env` (gitignored) or Docker secrets.")],
qa=[("Compose vs Kubernetes?","Compose: single host, simple. K8s: multi-node orchestration, self-healing, scaling."),
("depends_on guarantees readiness?","No, only start order unless healthcheck condition used."),
("How to override for prod?","Multiple files: `-f compose.yml -f compose.prod.yml`."),
("How to scale a service?","`docker compose up -d --scale api=3` (needs no fixed host port)."),
("Where are env variables loaded from?","`environment:`, `env_file:`, and `.env` for variable substitution.")]),

dict(slug="docker-security-internals", title="Container Security & Internals", level="Advanced",
intro="Container = Linux process + namespaces + cgroups. Security: non-root, minimal images, scanning, read-only FS, dropped capabilities, signing.",
diagram="""
Container = process with
  namespaces: pid, net, mnt, uts, ipc, user   (isolation)
  cgroups   : cpu, memory, io limits           (resource control)
  overlayfs : layered filesystem
  runtime   : containerd -> runc
""",
install="""# Trivy scanner
sudo apt install trivy   # or: docker run aquasec/trivy image nginx:1.27
# cosign for signing: https://github.com/sigstore/cosign""",
examples=[("Hardened run","""docker run -d --read-only --tmpfs /tmp \\
  --cap-drop ALL --security-opt no-new-privileges \\
  --user 10001 --pids-limit 200 myapp:1.0"""),
("Scan and sign","""trivy image --severity HIGH,CRITICAL --exit-code 1 myapp:1.0
cosign sign --key cosign.key registry/myapp:1.0
syft myapp:1.0 -o spdx-json > sbom.json"""),
("See namespaces in action","""sudo unshare --pid --fork --mount-proc bash   # own PID namespace
ps aux    # only shows processes in this namespace""")],
problems=[("Critical CVE found in production image","Old base image","Rebuild on updated base, pin digest, automate with Renovate/Dependabot, gate in CI."),
("Container can access host","Mounted /var/run/docker.sock or --privileged","Never mount docker.sock; avoid privileged; use rootless/Kaniko in CI.")],
qa=[("What makes containers isolated?","Namespaces (what you see) and cgroups (what you can use)."),
("What is --privileged?","Gives near-full host access; avoid."),
("Docker vs containerd vs runc?","Docker is full tooling; containerd is runtime manager; runc is low-level OCI runtime."),
("How to secure images in CI?","Scan (Trivy), minimal base, sign (cosign), SBOM, admission policy verification."),
("What is distroless?","Images with only app + runtime, no shell/package manager; smaller attack surface.")]),
])
