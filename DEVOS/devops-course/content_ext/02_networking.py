EXT = dict(
guide=dict(
bigpicture=dict(
problem="""**Problem it solves:** Applications, users, databases and cloud services are on different machines. Networking is the set of rules (protocols) and devices that lets them find each other and exchange data reliably and securely. Most production incidents ("site is down", "timeout", "cannot connect to DB") are network problems until proven otherwise.""",
chain=["PROBLEM: computers must find and talk to each other across the world",
       "TRADITIONAL APPROACH: point-to-point cables and fixed addresses",
       "PAIN: not scalable, no naming, no security, no routing",
       "TECHNOLOGY: TCP/IP stack, IP addressing, DNS, HTTP/TLS, routers, load balancers, firewalls",
       "SOLUTION: layered protocols; each layer solves one problem",
       "REAL-WORLD BENEFIT: any client can reach any service by name, securely, with load spread and failures hidden"],
text="""The **OSI model** (7 layers) is a teaching map; real networks use **TCP/IP** (Link, Internet, Transport, Application). Each layer only talks to the same layer on the other side and to the layer below."""),
e2e=dict(diagram="""User types https://shop.example.com
   |
   v
DNS lookup (browser cache > OS > resolver > root > TLD > authoritative)  => IP 203.0.113.10
   |
   v
TCP 3-way handshake (SYN, SYN-ACK, ACK) to port 443
   |
   v
TLS handshake (certificate check, keys)
   |
   v
HTTP request (GET /) --> CDN / WAF --> Load Balancer --> Reverse proxy (Nginx) --> App --> DB
   |
   v
HTTP response (200 + HTML) travels back
   |
   v
Browser renders; connection kept alive or closed""",
text="""First the browser needs an IP, so **DNS** resolves the name. Then the client opens a **TCP** connection (three-way handshake) to the server's port 443 so data is delivered reliably and in order. **TLS** then authenticates the server with a certificate and creates encryption keys. Only now is the **HTTP** request sent. Traffic passes through edge components (CDN, WAF), the **load balancer** which chooses a healthy backend, a **reverse proxy** and the application, which may call a database. The response returns along the same path. Failures can occur at any hop, so troubleshooting means testing each step in order."""),
tools=dict(rows=[
["DNS (Route 53, CoreDNS)", "Name to IP", "Hostname", "IP address(es)", "Before any connection"],
["Router / NAT gateway", "Move packets between networks", "IP packets", "Forwarded packets", "Between subnets/internet"],
["Load balancer (ALB/NLB/HAProxy)", "Distribute traffic, health checks", "Client connections", "Balanced backend traffic", "In front of app tier"],
["Reverse proxy (Nginx)", "Routing, TLS termination, caching", "HTTP requests", "Upstream requests", "Edge of app"],
["Firewall / Security Group / NACL", "Allow or deny traffic", "Packets + rules", "Allowed/blocked traffic", "Every boundary"],
["CDN (CloudFront)", "Cache near users", "Static/dynamic content", "Fast responses", "Global edge"],
["tcpdump / Wireshark", "Capture packets", "Network traffic", "Packet trace", "Deep debugging"],
["curl / dig / traceroute / nc / mtr", "Test and diagnose", "Host/port", "Diagnostic output", "Troubleshooting"]],
why="**ALB vs NLB:** ALB is Layer 7 (HTTP routing, headers, paths); NLB is Layer 4 (TCP/UDP, extreme performance, static IP). **Security Group vs NACL:** SG is stateful and attached to instances; NACL is stateless and attached to subnets."),
compare=[
("TCP vs UDP", ["Topic", "TCP", "UDP"], [["Connection", "Connection-oriented (handshake)", "Connectionless"], ["Reliability", "Ordered, retransmits", "Best effort"], ["Use", "HTTP, SSH, DB", "DNS queries, video, VoIP, QUIC"]]),
("HTTP vs HTTPS", ["Topic", "HTTP", "HTTPS"], [["Encryption", "None", "TLS encrypted"], ["Port", "80", "443"], ["Identity", "Not verified", "Certificate verifies server"]]),
("Layer 4 vs Layer 7 load balancer", ["Topic", "L4", "L7"], [["Sees", "IP + port", "HTTP host, path, headers, cookies"], ["Speed", "Faster", "More features"], ["Example", "NLB", "ALB, Nginx"]]),
("Forward proxy vs Reverse proxy", ["Topic", "Forward", "Reverse"], [["Sits in front of", "Clients", "Servers"], ["Purpose", "Filter/anonymise client traffic", "Load balance, TLS, cache, protect servers"]]),
("Public vs Private IP", ["Topic", "Public", "Private (RFC1918)"], [["Ranges", "Internet-routable", "10/8, 172.16/12, 192.168/16"], ["Reachable from internet", "Yes", "No (needs NAT)"]]),
("Security Group vs NACL", ["Topic", "Security Group", "NACL"], [["State", "Stateful", "Stateless"], ["Level", "Instance/ENI", "Subnet"], ["Rules", "Allow only", "Allow and deny"]])],
troubleshooting=[
("Website not reachable", "DNS wrong, port blocked, service down, TLS problem, LB unhealthy", "`dig site`, `nc -zv host 443`, `curl -vI https://site`, `traceroute`/`mtr`", "Fix at the failing layer: DNS record, SG/firewall, service, certificate.", "Synthetic monitoring, health checks."),
("Connection timeout vs connection refused", "Timeout = packets dropped (firewall/route); refused = host reachable but nothing listening", "`nc -zv host port`, `ss -tulpn` on server, SG rules", "Timeout: open firewall/route. Refused: start service or bind correct interface.", "Document ports; test after deploy."),
("DNS resolves wrong/old IP", "TTL caching, wrong record, split-horizon", "`dig +short host`, `dig @8.8.8.8`, `dig +trace`", "Fix record; wait TTL; flush cache.", "Lower TTL before migrations."),
("TLS/certificate error", "Expired, wrong hostname, missing intermediate, clock skew", "`openssl s_client -connect host:443 -servername host`, `curl -v`", "Renew/replace cert, install full chain.", "Automate renewals (cert-manager/ACM) and alert on expiry."),
("502 / 504 from proxy or LB", "Backend down or slow, wrong upstream port, timeout too low", "Proxy error log, backend health, `curl` backend directly", "Fix backend; adjust timeouts; correct upstream.", "Health checks and readiness gates."),
("Intermittent packet loss / latency", "Congestion, bad link, MTU, DNS delay", "`mtr host`, `ping -c 50`, `ip -s link`", "Fix network path; MTU; provider ticket.", "Network monitoring.")],
practices={
"Development": ["Use service names not IPs; test connectivity with curl/nc from the same network as the app."],
"Production": ["Multi-AZ, health checks, timeouts and retries with backoff; DNS TTL planning."],
"Security": ["TLS everywhere (1.2+), least-privilege security groups, private subnets for databases, WAF, no open 0.0.0.0/0 admin ports."],
"Performance": ["Keep-alive, HTTP/2, CDN caching, compression, connection pooling."],
"Reliability": ["Redundant load balancers, multiple DNS records/health-based routing, graceful failover."],
"Cost Optimization": ["Reduce NAT gateway/inter-AZ transfer, use VPC endpoints and CDN."],
"Monitoring & Logging": ["Flow logs, LB access logs, latency and error-rate dashboards."]},
mistakes={
"Beginner mistakes": ["Confusing port with protocol.", "Testing from your laptop and assuming the server can reach it too."],
"Developer mistakes": ["Hard-coded IPs.", "No timeouts on outbound calls."],
"DevOps mistakes": ["Overlapping CIDR blocks between VPCs.", "Forgetting return routes or security group rules."],
"Production mistakes": ["Certificate expiry.", "Long DNS TTL during migration."],
"Security mistakes": ["SSH/DB open to the world.", "Terminating TLS without re-encrypting where required."]},
versions=[
"`ifconfig`, `netstat`, `nslookup` are legacy: prefer `ip`, `ss`, `dig`.",
"TLS 1.0/1.1 are deprecated; use TLS 1.2 or 1.3. HTTP/3 uses QUIC over UDP.",
"IPv6 support varies across cloud services: verify per service.",
"Cloud specifics: AWS security groups are stateful, Azure NSGs and GCP firewall rules differ in defaults and priorities."],
hinglish="""Network mein sabse pehle **DNS** naam ko IP mein badalta hai, phir **TCP** connection banta hai, phir **TLS** encryption, phir **HTTP** request. **Timeout** ka matlab packets drop ho rahe hain (firewall/route), **refused** ka matlab machine mil gayi par us port par koi service nahi sun rahi. Problem ho to **layer by layer** test karo: DNS > IP reachability > port > TLS > HTTP.""",
mnemonics=[
("OSI layers (top to bottom)", "All People Seem To Need Data Processing = Application, Presentation, Session, Transport, Network, Data link, Physical"),
("Troubleshoot order", "D-P-P-T-H: DNS, Ping, Port, TLS, HTTP"),
("TCP handshake", "SYN, SYN-ACK, ACK"),
("Private ranges", "10/8, 172.16/12, 192.168/16"),
("CIDR", "/24 = 256 addresses; each /1 doubles or halves")],
client=dict(
s30="""Networking is how our users, applications and databases find and talk to each other securely. We design it so traffic is encrypted, spread across healthy servers and protected by firewalls, which keeps the service fast and available.""",
m2="""When a customer opens your website, DNS turns the name into an address, a secure connection is created with TLS, and a load balancer sends the request to a healthy server. Our design places public components such as load balancers in public subnets and applications and databases in private subnets, controlled by firewalls that only allow required ports. We add a CDN for speed, health checks for automatic failover, and monitoring for latency and errors. This gives you availability across multiple data centres, protection from attacks and clear visibility when something breaks.""",
m5="""Let me walk through a request. **Name resolution:** DNS records in Route 53 map the domain to a load balancer, with health-based routing for failover. **Secure transport:** TLS certificates, issued and renewed automatically, encrypt traffic; we enforce TLS 1.2+. **Distribution:** an application load balancer routes by host and path to targets in multiple availability zones and removes unhealthy ones. **Segmentation:** a VPC with public subnets (load balancer, NAT) and private subnets (apps, databases); security groups allow only necessary flows such as LB to app on 8080 and app to database on 5432. **Performance and protection:** CDN caching, WAF rules, rate limiting, HTTP/2 and keep-alive. **Operations:** flow logs, load balancer logs and dashboards, and a troubleshooting runbook: DNS, port, TLS, HTTP. The business benefit is availability, security and predictable performance."""),
roadmap=[
("Beginner", ["IP address, ports, protocol", "OSI vs TCP/IP", "DNS basics", "HTTP basics, status codes"]),
("Intermediate", ["Subnetting/CIDR", "TCP handshake, TLS", "NAT, routing", "curl/dig/nc/ss usage", "Reverse proxy and load balancing"]),
("Advanced", ["VPC design, peering, transit", "L4 vs L7 balancing, HTTP/2, QUIC", "tcpdump/Wireshark", "Service mesh, mTLS", "BGP/CDN basics"]),
("Production", ["High availability, DNS failover", "Certificates automation", "Flow logs and network monitoring"]),
("Interview", ["What happens when you type a URL", "Subnetting calculation", "504 vs 502", "Design VPC for 3 tiers"])],
miniproject=dict(title="Build and debug a small network path: DNS > Nginx > app",
arch="""client (curl) --> DNS name app.local (/etc/hosts)
   --> Nginx :80 (reverse proxy, TLS optional)
   --> app :3000 (private)
Tools: dig/curl/ss/tcpdump to prove each hop""",
steps=[
("Step 1: Run app and proxy", """docker network create demo
docker run -d --name app --network demo hashicorp/http-echo -text=hello -listen=:3000
cat > default.conf <<'EOF'
server { listen 80; location / { proxy_pass http://app:3000; proxy_set_header Host $host; } }
EOF
docker run -d --name proxy --network demo -p 8080:80 -v $PWD/default.conf:/etc/nginx/conf.d/default.conf:ro nginx:1.27""", "App is only reachable inside the `demo` network; Nginx is the single public entry on host port 8080. `proxy_pass` uses the container name (Docker DNS)."),
("Step 2: Test each hop", """curl -i http://localhost:8080
docker exec proxy sh -c 'getent hosts app'
docker exec proxy curl -s http://app:3000""", "First proves the full path, second proves DNS inside the network, third proves proxy to app connectivity."),
("Step 3: Break it and read the symptoms", """docker stop app
curl -i http://localhost:8080   # 502 Bad Gateway
docker logs proxy | tail -3""", "Proxy is up but upstream is down: 502 with a connect error in the log. Restart app to recover."),
("Step 4: Capture traffic", """sudo tcpdump -i any -nn port 8080 -c 10   # Linux host
curl -s http://localhost:8080 >/dev/null""", "Shows the TCP handshake and HTTP request/response packets. On Docker Desktop, run tcpdump inside a container instead.")]),
interview=[
("Beginner", "What is an IP address?", "A numerical address identifying a device on a network (IPv4 32-bit, IPv6 128-bit).", "Foundation.", "192.168.1.10."),
("Beginner", "What is a port?", "A 16-bit number identifying a service on a host.", "Services share one IP.", "HTTPS 443, SSH 22."),
("Beginner", "What is DNS?", "System that translates domain names to IP addresses.", "Every request starts here.", "google.com to an IP."),
("Beginner", "TCP vs UDP?", "TCP reliable and ordered; UDP fast connectionless.", "Protocol choice.", "HTTP uses TCP; DNS queries use UDP."),
("Beginner", "What is HTTP status 200/404/500?", "200 OK, 404 not found, 500 server error.", "Debugging basics.", "502/503/504 are gateway/availability errors."),
("Beginner", "What is a firewall?", "Filters traffic by rules (IP, port, protocol).", "Security.", "Allow 443, block others."),
("Beginner", "What is NAT?", "Translates private IPs to a public IP so many hosts share one address.", "Internet access from private networks.", "NAT gateway for private subnets."),
("Beginner", "What is a subnet?", "A segment of an IP network defined by a mask/CIDR.", "Network design.", "10.0.1.0/24."),
("Beginner", "What is a load balancer?", "Distributes traffic across multiple servers and removes unhealthy ones.", "Availability.", "ALB in front of EC2."),
("Beginner", "What is HTTPS?", "HTTP over TLS: encrypted and authenticated.", "Security basics.", "Padlock in browser."),
("Intermediate", "What happens when you type a URL in the browser?", "DNS resolution, TCP handshake, TLS handshake, HTTP request through CDN/LB/proxy to app, response rendered.", "Classic full-stack question.", "See e2e diagram."),
("Intermediate", "Explain the TCP three-way handshake.", "SYN, SYN-ACK, ACK establish sequence numbers before data flows.", "Transport fundamentals.", "Visible in tcpdump."),
("Intermediate", "Explain CIDR: how many hosts in /24, /16, /28?", "/24=256 addresses (254 usable), /16=65,536, /28=16 (cloud providers reserve some addresses, for example AWS reserves 5 per subnet).", "Subnetting skill.", "AWS /28 gives 11 usable."),
("Intermediate", "Public vs private subnet in AWS?", "Public has a route to an Internet Gateway; private routes outbound via NAT and is not directly reachable.", "VPC design.", "DB in private subnet."),
("Intermediate", "Explain DNS record types.", "A (IPv4), AAAA (IPv6), CNAME (alias), MX (mail), TXT (verification/SPF), NS (name servers), SOA, SRV.", "DNS depth.", "CNAME can't be at zone apex; use alias."),
("Intermediate", "What is TTL in DNS?", "How long resolvers may cache a record.", "Migrations.", "Lower TTL before cutover."),
("Intermediate", "Reverse proxy vs load balancer?", "Reverse proxy fronts servers (TLS, caching, routing); load balancer distributes across many; often one component does both (Nginx, ALB).", "Terminology.", "Nginx doing both."),
("Intermediate", "Load balancing algorithms?", "Round robin, least connections, IP hash, weighted.", "Traffic distribution.", "Sticky sessions via cookie/IP hash."),
("Intermediate", "What is TLS termination?", "The proxy/LB decrypts TLS and forwards plain or re-encrypted traffic to backends.", "Cert management.", "ALB with ACM cert."),
("Intermediate", "502 vs 503 vs 504?", "502 bad response from upstream; 503 service unavailable/no healthy backend; 504 upstream timeout.", "Incident triage.", "504 means slow backend."),
("Intermediate", "What is a CDN?", "Global cache network serving content near users.", "Performance.", "CloudFront."),
("Intermediate", "What is the difference between stateful and stateless firewall?", "Stateful tracks connections so return traffic is automatically allowed; stateless needs explicit rules both ways.", "SG vs NACL.", "NACL needs ephemeral ports rule."),
("Intermediate", "How to test a port is open?", "`nc -zv host port`, `curl`, `telnet`, `Test-NetConnection` on Windows.", "Debugging.", "`nc -zv db 5432`."),
("Intermediate", "What is MTU and why does it matter?", "Maximum packet size; mismatch causes fragmentation or hangs, especially with VPNs/tunnels.", "Subtle issues.", "Large uploads hang over VPN."),
("Advanced", "Explain the OSI vs TCP/IP model.", "OSI has 7 layers, TCP/IP 4; mapping: application layers 5-7 to Application, Transport, Internet (Network), Link (Data link + Physical).", "Framework knowledge.", "Firewalls L3/L4; WAF L7."),
("Advanced", "Explain the TLS handshake.", "ClientHello (versions, ciphers, SNI), ServerHello + certificate, key exchange (ECDHE), verification of chain, session keys derived, encrypted traffic (TLS 1.3 needs 1 round trip).", "Security depth.", "`openssl s_client`."),
("Advanced", "What is mTLS?", "Both client and server present certificates for mutual authentication.", "Zero trust.", "Service mesh between pods."),
("Advanced", "HTTP/1.1 vs HTTP/2 vs HTTP/3?", "1.1 has head-of-line blocking per connection; 2 multiplexes streams over one TCP connection; 3 uses QUIC (UDP) to avoid TCP head-of-line blocking.", "Performance.", "Enable HTTP/2 on LB."),
("Advanced", "How does DNS resolution work recursively?", "Stub resolver > recursive resolver > root > TLD > authoritative; answers cached by TTL.", "DNS depth.", "`dig +trace`."),
("Advanced", "How does ARP work?", "Maps IP to MAC on a local network via broadcast request and reply.", "L2/L3 link.", "Duplicate IP causes ARP conflicts."),
("Advanced", "How do you design a VPC for 3 tiers?", "Public subnets (ALB, NAT), private app subnets, private DB subnets across 2-3 AZs, SGs chained (ALB > app > DB), route tables, endpoints.", "Architecture.", "See AWS VPC topic."),
("Advanced", "What is anycast?", "Same IP announced from many locations; routing sends users to the nearest.", "Global services.", "CDN and DNS providers."),
("Advanced", "TCP congestion control and retransmission?", "TCP adapts window size to network conditions and retransmits lost segments; causes latency during loss.", "Performance tuning.", "Lossy links slow uploads."),
("Advanced", "Explain conntrack exhaustion.", "Stateful NAT/firewall keeps connection table; full table drops new connections.", "Real production problem.", "Kubernetes nodes with many short connections."),
("Advanced", "What is SNI?", "TLS extension telling the server which hostname the client wants, enabling many certificates on one IP.", "TLS hosting.", "Multi-tenant ingress."),
("Advanced", "Explain BGP at high level.", "Protocol exchanging routing information between autonomous systems on the internet.", "Internet routing.", "Route leaks cause outages."),
("Advanced", "Symmetric vs asymmetric encryption in TLS?", "Asymmetric authenticates and exchanges keys; symmetric encrypts bulk data quickly.", "Crypto basics.", "ECDHE + AES-GCM."),
("Advanced", "How would you reduce latency to global users?", "CDN, edge caching, regional deployments, anycast/latency routing, keep-alive, HTTP/3, database read replicas.", "Architecture.", "Route 53 latency routing."),
("Advanced", "What is a bastion host?", "Hardened jump server for admin access to private networks; alternatives include SSM Session Manager.", "Secure access.", "SSH via bastion to private DB."),
("Advanced", "Explain VPN vs Direct Connect/peering.", "VPN is encrypted over the internet; Direct Connect is a dedicated link; peering connects VPCs privately (non-transitive).", "Hybrid networking.", "Peering doesn't route through third VPC."),
("Scenario-Based", "Users in one country cannot reach the site.", "Check DNS resolution from there, CDN/edge, geo-blocking/WAF, ISP routing; use external probes.", "Regional issues.", "WAF rule blocking a country."),
("Scenario-Based", "Application cannot connect to database after deploy.", "Security group, subnet route/NACL, DNS name, port, credentials, DB max connections.", "Layered thinking.", "SG missing app to DB rule."),
("Scenario-Based", "Site slow only at peak.", "Check LB metrics, backend CPU/DB, connection limits, autoscaling, CDN hit ratio.", "Capacity.", "Connection pool exhaustion."),
("Scenario-Based", "Migrate domain to a new server with no downtime.", "Lower TTL in advance, deploy new server, test with hosts file, switch record, monitor, restore TTL, keep old for rollback.", "Change planning.", "TTL 60s day before."),
("Scenario-Based", "Certificate expired on production.", "Renew and deploy immediately (full chain), reload proxy, add expiry monitoring and auto-renewal.", "Ops maturity.", "cert-manager/ACM."),
("Scenario-Based", "Design secure access for developers to private databases.", "Bastion/SSM tunnel, IAM auth, short-lived credentials, audit logs, no public DB.", "Security design.", "SSM port forwarding."),
("Scenario-Based", "Two VPCs have overlapping CIDR and must connect.", "Cannot peer; re-address one, use NAT/PrivateLink for specific services.", "Design consequence.", "Plan CIDRs company-wide."),
("Scenario-Based", "API intermittently returns 504.", "Increase upstream timeouts only after finding the slow dependency; check backend latency, DB, retries and idle timeouts (LB idle timeout vs app keep-alive).", "Root cause vs symptom.", "ALB idle timeout 60s vs app 30s."),
("Scenario-Based", "Traffic must be restricted to office IPs.", "Security group/WAF IP allow-list, VPN, or Zero Trust access proxy.", "Access control.", "Admin panel behind VPN."),
("Scenario-Based", "Prevent DDoS impact.", "CDN/edge absorption, AWS Shield/WAF rate limits, autoscaling, blackhole abusers, cache.", "Availability.", "Rate limit per IP."),
("Scenario-Based", "Choose ALB or NLB.", "ALB for HTTP path/host routing and WAF; NLB for TCP/UDP, static IPs, ultra-low latency.", "Service selection.", "gRPC/TCP service on NLB."),
("Scenario-Based", "Internal services must resolve names privately.", "Private hosted zones/Route 53 resolver, CoreDNS in Kubernetes.", "Private DNS.", "db.internal."),
("Scenario-Based", "A microservice cannot reach the internet from a private subnet.", "Check route to NAT gateway, NAT in public subnet with EIP, SG/NACL egress, DNS.", "Common VPC issue.", "Missing 0.0.0.0/0 route."),
("Scenario-Based", "Load balancer shows targets unhealthy.", "Health check path/port/response, SG allowing LB to target, app not listening.", "LB debugging.", "Health check returns 302."),
("Scenario-Based", "Need to inspect encrypted traffic problem.", "Use `openssl s_client`, curl -v, decrypt with proxy in dev, or examine handshake alerts in tcpdump.", "TLS debugging.", "Protocol mismatch."),
("Troubleshooting-Based", "`Connection timed out`.", "Packets dropped: firewall/SG/NACL/route/host down. Test with `nc`, `traceroute`, check rules both sides.", "Symptom mapping.", "SG missing rule."),
("Troubleshooting-Based", "`Connection refused`.", "Host reachable, no listener or wrong interface/port. `ss -tulpn` on server.", "Symptom mapping.", "App bound to 127.0.0.1."),
("Troubleshooting-Based", "`Could not resolve host`.", "DNS failure: check resolver, record, network; `dig` against different resolvers.", "DNS.", "Wrong /etc/resolv.conf."),
("Troubleshooting-Based", "`SSL certificate problem: unable to get local issuer`.", "Missing CA/intermediate; fix chain or trust store.", "TLS.", "Corporate proxy CA."),
("Troubleshooting-Based", "Ping works but the app does not.", "ICMP allowed but TCP port blocked or service down; test with `nc`/`curl`.", "Layer separation.", "SG allows ICMP only."),
("Troubleshooting-Based", "Works by IP but not by name.", "DNS issue or virtual host/SNI requires Host header; check `dig`, `curl --resolve`.", "Naming.", "Ingress needs Host."),
("Troubleshooting-Based", "Random resets (ECONNRESET).", "Idle timeout mismatch, proxy/LB closing, app crash, conntrack; check timeouts and logs.", "Connection lifecycle.", "Keep-alive shorter than LB idle."),
("Troubleshooting-Based", "Very slow first request, fast later.", "DNS latency, TLS handshake, cold start, connection pool warm-up; measure with `curl -w`.", "Latency breakdown.", "`curl -w '%{time_namelookup} %{time_connect} %{time_appconnect} %{time_total}'`."),
("Troubleshooting-Based", "Cannot reach service in another VPC.", "Peering route tables both sides, SG referencing, NACL, DNS resolution options, overlapping CIDR.", "Peering.", "Missing return route."),
("Troubleshooting-Based", "Intermittent failures to one backend.", "One unhealthy node; check LB health, per-target logs, run `mtr`.", "Partial failures.", "One AZ misconfigured.")],
cheatsheet={
"Definitions": ["IP identifies host; port identifies service; DNS maps names; TCP reliable; UDP fast; TLS encrypts; NAT translates; CIDR /n notation."],
"Commands": ["`ip a` `ip r` `ss -tulpn` `ping -c 4 host` `traceroute/mtr host`", "`dig +short host` `dig @8.8.8.8 host` `dig +trace host` `nslookup host`", "`curl -vI https://host` `curl --resolve host:443:IP https://host` `nc -zv host port`", "`openssl s_client -connect host:443 -servername host` `tcpdump -i any -nn port 443`"],
"Files": ["/etc/hosts /etc/resolv.conf /etc/nginx/nginx.conf /etc/haproxy/haproxy.cfg"],
"Architecture": ["Client > DNS > CDN/WAF > LB > reverse proxy > app > DB, with public/private subnets."],
"Ports": ["HTTP 80, HTTPS 443, SSH 22, DNS 53, SMTP 25/587, RDP 3389, MySQL 3306, PostgreSQL 5432, Redis 6379"],
"Differences": ["TCP vs UDP; L4 vs L7 LB; SG vs NACL; forward vs reverse proxy; 502 vs 504; timeout vs refused."],
"Troubleshooting commands": ["DNS: dig | Reachability: ping/mtr | Port: nc/ss | TLS: openssl | HTTP: curl -v | Packets: tcpdump"],
"Best practices": ["TLS 1.2+, least-privilege SGs, private subnets for data, multi-AZ, health checks, timeouts/retries, auto-renew certs."]}
),
subs={
"osi-tcpip": dict(
define=dict(simple="Layered rules that let any two computers exchange data; each layer has one job.",
technical="The OSI model (7 layers) and TCP/IP (4 layers) describe encapsulation: application data is wrapped in TCP/UDP segments, IP packets, and link-layer frames, then unwrapped at the destination.",
why="Divides a complex problem so devices from different vendors interoperate.", without="Incompatible proprietary networks.", use="Reasoning and troubleshooting.", avoid="N/A", analogy="Postal system: letter (application), envelope with address (IP), truck (link)."),
internals="""The application produces data > TCP adds ports and sequence numbers (segment) > IP adds source/destination IP (packet) > Ethernet adds MAC addresses (frame) > bits on the wire. Each router reads only the IP header and forwards; the receiver reverses the process.""",
realworld=dict(diagram="""L7 HTTP GET /  ->  L4 TCP :443  ->  L3 IP 10.0.1.5 -> 203.0.113.10  ->  L2 Ethernet frame  ->  L1 wire/wifi""", text="A request from a laptop to a web server is encapsulated at each layer. The router forwards based on IP; the switch on MAC; the load balancer on port (L4) or HTTP path (L7)."),
lab=dict(goal="See layers in real traffic.", prereq=["Linux/WSL with tcpdump or Wireshark", "curl"],
steps=[("sudo tcpdump -i any -nn -c 15 port 80 or port 443", "Starts capture in one terminal."),
("curl -s http://example.com >/dev/null", "Generates traffic."),
("Read the output", "You will see SYN, SYN-ACK, ACK (TCP layer), then HTTP data. IP addresses appear at layer 3.")]),
mnemonics=[("OSI", "All People Seem To Need Data Processing"), ("TCP/IP", "Link, Internet, Transport, Application")],
hinglish="Har layer ka ek kaam hai. **Router IP dekhta hai (L3), switch MAC (L2), load balancer port (L4) ya HTTP (L7)**. Problem kaunsi layer par hai ye pehchano.",
practices={"Production": ["Use layer-based troubleshooting."]}, mistakes={"Beginner mistakes": ["Memorising layers without mapping tools to layers."]},
qa_extra=[("Intermediate", "At which layer do firewall, WAF and LB operate?", "Classic firewalls L3/L4, WAF L7, load balancers L4 (NLB) or L7 (ALB).", "Mapping tools to layers.", "ALB path routing = L7.")]),

"ip-subnetting": dict(
define=dict(simple="IP addressing gives every device an address; subnetting splits a big network into smaller ones.",
technical="IPv4 address = 32 bits split into network and host parts by the prefix length (CIDR). A /n prefix leaves 32-n host bits, giving 2^(32-n) addresses.",
why="Organise, secure and route networks efficiently.", without="One flat network with no isolation.", use="VPC/subnet design.", avoid="Overlapping CIDRs.", analogy="City > district > street > house number."),
internals="""Network address = IP AND mask. Example 10.0.1.37/24: mask 255.255.255.0, network 10.0.1.0, broadcast 10.0.1.255, hosts 10.0.1.1-254. Routers compare the destination with route table prefixes and pick the longest match.""",
config=[("CIDR quick table", """/16 = 65,536 addresses  (255.255.0.0)
/20 = 4,096
/24 = 256               (255.255.255.0)
/26 = 64
/28 = 16
# AWS reserves 5 addresses per subnet (first 4 and last 1)""", [("/24", "8 host bits, 256 addresses, 254 usable normally."), ("/28", "16 addresses; AWS usable = 11."), ("Longest prefix match", "More specific route wins.")])],
lab=dict(goal="Design a VPC address plan.", prereq=["Paper or spreadsheet; python3 optional"],
steps=[("python3 -c \"import ipaddress as i; n=i.ip_network('10.0.0.0/16'); print(list(n.subnets(new_prefix=24))[:4])\"", "Splits a /16 into /24s to plan subnets."),
("Assign: 10.0.0.0/24 public-a, 10.0.1.0/24 public-b, 10.0.10.0/24 app-a, 10.0.11.0/24 app-b, 10.0.20.0/24 db-a, 10.0.21.0/24 db-b", "Two AZs, three tiers, room to grow."),
("python3 -c \"import ipaddress as i; print(i.ip_address('10.0.10.5') in i.ip_network('10.0.10.0/24'))\"", "Checks membership: True.")]),
mnemonics=[("Hosts", "2^(32-prefix)"), ("Private", "10, 172.16-31, 192.168")],
hinglish="**/24 ka matlab 256 addresses.** Prefix jitna bada, network utna chhota. VPC banate waqt CIDR overlap se bacho warna peering nahi hogi.",
practices={"Production": ["Plan CIDRs company-wide; leave growth room; separate tiers/AZs."]}, mistakes={"DevOps mistakes": ["Overlapping CIDRs.", "Too-small subnets for EKS pods."]},
qa_extra=[("Scenario-Based", "How many /24 subnets fit in a /16?", "256 (2^(24-16)).", "Subnetting math.", "Plan for multi-AZ.")]),

"dns": dict(
define=dict(simple="DNS is the internet's phone book: names to IP addresses.",
technical="Hierarchical distributed database; recursive resolvers query root, TLD and authoritative servers; records have types and TTLs; caching happens at multiple levels.",
why="Humans use names; machines use IPs; IPs change.", without="Remember IP addresses.", use="Every service.", avoid="Hard-coded IPs.", analogy="Phone contacts."),
internals="""Browser cache > OS cache > recursive resolver (ISP/8.8.8.8) > root server (points to TLD) > .com TLD (points to authoritative) > authoritative server returns the A record > answer cached for TTL.""",
commands=[("dig +short api.example.com A", "Queries a record type and prints only the answer.", "`+trace` full path, `@server` choose resolver, `-x` reverse lookup.", "203.0.113.10", "Testing with a cached resolver and assuming global state.", "Compare `dig @8.8.8.8` and `dig @authoritative-ns`.")],
lab=dict(goal="Trace DNS resolution.", prereq=["dig installed (dnsutils/bind-utils)"],
steps=[("dig +trace example.com", "Shows root > TLD > authoritative delegation."),
("dig example.com MX +short; dig example.com TXT +short", "Other record types."),
("dig @1.1.1.1 example.com; dig @8.8.8.8 example.com", "Compare resolvers.")]),
compare=[("DNS record types", ["Type", "Purpose"], [["A/AAAA", "Name to IPv4/IPv6"], ["CNAME", "Alias to another name (not at apex)"], ["MX", "Mail servers"], ["TXT", "Verification, SPF/DKIM"], ["NS", "Delegation"], ["Route 53 Alias", "AWS-specific alias allowed at apex"]])],
mnemonics=[("Resolution", "Cache > Recursive > Root > TLD > Authoritative")],
hinglish="DNS problem ho to **`dig`** use karo aur different resolvers se compare karo. **TTL** kam karo migration se pehle.",
practices={"Reliability": ["Health-checked failover records; low TTL for changing endpoints."]}, mistakes={"Production mistakes": ["Long TTL during cutover."]},
qa_extra=[("Troubleshooting-Based", "Some users see the old IP after a change.", "Caching until TTL expires at resolvers/clients; verify authoritative answer, wait or flush caches.", "TTL.", "Prevent with lower TTL.")]),

"http-tls": dict(
define=dict(simple="HTTP is how browsers and servers talk; TLS makes it private and verified.",
technical="HTTP is a stateless request/response protocol (methods, headers, status codes); TLS provides confidentiality, integrity and server authentication via X.509 certificates issued by trusted CAs.",
why="Web communication needs a common protocol and protection from eavesdropping.", without="Plain-text passwords on the wire.", use="All web traffic.", avoid="Plain HTTP in production.", analogy="HTTP is a postcard; HTTPS is a sealed, signed envelope."),
internals="""After TCP connects, TLS: ClientHello (SNI, ciphers) > ServerHello + certificate > client validates chain against trusted CAs and hostname > key exchange (ECDHE) > symmetric session keys > encrypted HTTP.""",
commands=[("curl -vI https://example.com", "Shows TLS details, headers and status.", "`-k` ignore cert errors (debug only), `--http2`, `-w` timing, `--resolve`.", "TLS handshake lines then HTTP/2 200.", "Using `-k` and forgetting the real issue.", "Cert errors: `openssl s_client -connect host:443 -servername host -showcerts`."),
("openssl x509 -noout -dates -subject -in cert.pem", "Displays certificate validity and subject.", "`-issuer`, `-ext subjectAltName`.", "notBefore/notAfter.", "Checking only leaf, not the chain.", "Verify chain with `openssl verify`.")],
lab=dict(goal="Inspect a certificate and status codes.", prereq=["curl, openssl"],
steps=[("echo | openssl s_client -connect example.com:443 -servername example.com 2>/dev/null | openssl x509 -noout -dates -issuer", "Prints issuer and validity."),
("curl -s -o /dev/null -w '%{http_code}\\n' https://example.com/nope", "Shows a 404."),
("curl -w 'dns=%{time_namelookup} connect=%{time_connect} tls=%{time_appconnect} total=%{time_total}\\n' -o /dev/null -s https://example.com", "Latency breakdown.")]),
compare=[("Status code groups", ["Range", "Meaning", "Examples"], [["2xx", "Success", "200, 201, 204"], ["3xx", "Redirect", "301, 302, 304"], ["4xx", "Client error", "400, 401, 403, 404, 429"], ["5xx", "Server error", "500, 502, 503, 504"]])],
mnemonics=[("401 vs 403", "401 = who are you? (unauthenticated); 403 = I know you, not allowed")],
hinglish="HTTPS = HTTP + **TLS**. Certificate **chain, expiry aur hostname** teeno check karo. 401 = login nahi, 403 = permission nahi.",
practices={"Security": ["TLS 1.2+, HSTS, automated renewals, strong ciphers."]}, mistakes={"Production mistakes": ["Missing intermediate cert.", "Expired certs."]},
versions=["TLS 1.3 is preferred; SSL and TLS 1.0/1.1 are obsolete.", "Let's Encrypt certs are valid for a short period: automation is required."],
qa_extra=[("Advanced", "What does HSTS do?", "Header telling browsers to use HTTPS only for the domain for a period, preventing downgrade attacks.", "Web security.", "`Strict-Transport-Security: max-age=31536000`.")]),

"load-balancing-proxy": dict(
define=dict(simple="A load balancer shares traffic among servers; a reverse proxy sits in front of servers; a firewall filters traffic.",
technical="L4 balancers forward TCP/UDP flows; L7 balancers/proxies parse HTTP to route by host/path/header, terminate TLS, cache and apply WAF rules; firewalls apply allow/deny rules by IP/port/protocol.",
why="Availability, scaling and security.", without="Single point of failure.", use="All production web apps.", avoid="Session state stored only on one server.", analogy="Restaurant host seating guests at free tables."),
internals="""Client > LB (health checks mark targets healthy/unhealthy) > algorithm picks a healthy target > request forwarded > response returned. For HTTPS, LB terminates TLS with a certificate and may re-encrypt to backends. Unhealthy targets are removed until checks pass.""",
config=[("Nginx reverse proxy + load balancing explained", """upstream api {
    least_conn;
    server 10.0.10.11:3000 max_fails=3 fail_timeout=10s;
    server 10.0.10.12:3000;
}
server {
    listen 443 ssl;
    server_name api.example.com;
    ssl_certificate     /etc/ssl/fullchain.pem;
    ssl_certificate_key /etc/ssl/privkey.pem;
    location / {
        proxy_pass http://api;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_read_timeout 60s;
    }
}""", [("upstream api", "Named backend pool."), ("least_conn", "Send to the server with fewest active connections."), ("max_fails/fail_timeout", "Passive health check: skip a failing server for 10s."), ("ssl_certificate", "Full chain and key for TLS termination."), ("proxy_set_header Host", "Preserves the original host for the app."), ("X-Forwarded-For", "Passes the client's real IP."), ("proxy_read_timeout", "How long to wait for the backend before returning 504.")])],
lab=dict(goal="Load balance two backends with Nginx in Docker.", prereq=["Docker"],
steps=[("docker network create lb && for i in 1 2; do docker run -d --name web$i --network lb hashicorp/http-echo -text=server$i -listen=:5678; done", "Two backends answering their names."),
("Create nginx.conf with upstream {server web1:5678; server web2:5678;} and location / { proxy_pass http://app; } then run nginx with it mounted on port 8080", "Nginx balances round robin."),
("for i in 1 2 3 4; do curl -s localhost:8080; done", "Alternates server1/server2. Stop one backend and see all requests go to the other.")]),
compare=[("Load balancer types", ["Type", "Layer", "Best for"], [["ALB", "7", "HTTP/HTTPS path/host routing, WAF"], ["NLB", "4", "TCP/UDP, static IP, high performance"], ["Nginx/HAProxy", "4/7", "Self-managed, flexible"], ["Gateway LB", "3", "Third-party network appliances"]])],
mnemonics=[("LB checklist", "Health checks, Algorithm, TLS, Timeouts, Stickiness")],
hinglish="Load balancer **healthy servers** ko hi traffic deta hai. **Health check aur timeouts** sahi set karo warna 502/504 aayenge.",
practices={"Reliability": ["Multi-AZ LB, connection draining, correct health-check path."], "Security": ["WAF, TLS policy, restrict backend SG to LB only."]}, mistakes={"DevOps mistakes": ["Health check hits a heavy endpoint.", "Backends open to the internet."]},
qa_extra=[("Scenario-Based", "Users get logged out randomly behind a load balancer.", "Session stored in server memory: use shared session store (Redis), JWT, or sticky sessions as a stopgap.", "Statelessness.", "Move sessions to Redis.")]),

"net-troubleshooting": dict(
define=dict(simple="A step-by-step method to find where a network connection fails.",
technical="Test each layer in order with a specific tool and interpret the symptom (timeout, refused, reset, TLS error, HTTP code).",
why="Network incidents are common and time-critical.", without="Random guesses.", use="Any connectivity problem.", avoid="Changing firewall rules blindly.", analogy="Checking each link of a chain to find the break."),
internals="""Order: local config (`ip a`, `ip r`) > DNS (`dig`) > reachability (`ping`/`mtr`) > port (`nc -zv`) > TLS (`openssl s_client`) > HTTP (`curl -v`) > server side (`ss -tulpn`, logs). Compare from multiple vantage points (client, bastion, same subnet).""",
commands=[("nc -zv db.internal 5432", "Tests if a TCP port accepts connections.", "`-z` scan, `-v` verbose, `-w 3` timeout.", "Connection to db.internal 5432 port [tcp] succeeded!", "Testing from the wrong host.", "Timeout: firewall/route. Refused: nothing listening."),
("mtr -rwc 50 host", "Combines traceroute and ping to find loss per hop.", "`-r` report, `-c` count, `-T` TCP mode.", "Per-hop loss and latency.", "Reading loss at one hop that does not propagate.", "Loss that continues to the last hop is real.")],
lab=dict(goal="Diagnose a broken path on purpose.", prereq=["Docker"],
steps=[("docker run -d --name web -p 8081:80 nginx:1.27 && curl -sI localhost:8081 | head -1", "Working baseline: HTTP 200."),
("docker stop web && curl -sI localhost:8081", "Connection refused: nothing listens."),
("docker start web && sudo iptables -I INPUT -p tcp --dport 8081 -j DROP 2>/dev/null; curl -m 3 localhost:8081; sudo iptables -D INPUT -p tcp --dport 8081 -j DROP 2>/dev/null", "Timeout when packets are dropped (needs Linux + sudo; skip on Docker Desktop). You have now seen refused vs timeout.")]),
mnemonics=[("Order", "Config > DNS > Ping > Port > TLS > HTTP > Server logs")],
hinglish="**Timeout = drop, Refused = koi sun nahi raha.** Har layer ek ek karke test karo aur client/server dono side se dekho.",
practices={"Monitoring & Logging": ["VPC flow logs, LB logs, synthetic checks."]}, mistakes={"DevOps mistakes": ["Testing only from your laptop."]},
qa_extra=[("Troubleshooting-Based", "curl works from bastion but not from app server. Why?", "Difference in route/SG/NACL/DNS between the two hosts; compare rules and run `mtr`/`nc` from the app host.", "Vantage points.", "SG allows only bastion CIDR.")])
})
