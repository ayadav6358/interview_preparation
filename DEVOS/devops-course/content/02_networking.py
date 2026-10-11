TOPIC = dict(slug="02-networking", title="Networking", intro="Deployment, load balancer, DNS, firewall, VPC: sab networking par based. Issues debug karne ke liye yeh must-have skill hai.", subs=[

dict(slug="osi-tcpip", title="OSI, TCP/IP & How the Web Works", level="Basic",
intro="Data layers se hokar jaata hai. Interview ka sabse common sawal: 'Browser mein URL daalne par kya hota hai?'",
diagram="""
OSI (7)                TCP/IP (4)        Example
7 Application  ┐
6 Presentation ├──>   Application        HTTP, DNS, SSH, TLS
5 Session      ┘
4 Transport    ──>    Transport          TCP / UDP (ports)
3 Network      ──>    Internet           IP, ICMP, routing
2 Data Link    ┐
1 Physical     ┘──>   Link               Ethernet, WiFi, MAC

URL -> DNS -> TCP handshake -> TLS handshake -> HTTP request -> response -> render
""",
install="# nothing to install; tools: sudo apt install dnsutils curl traceroute -y",
examples=[("Trace the whole journey of a URL","""dig +short example.com                    # 1. DNS -> IP
traceroute example.com                    # 2. path of routers
curl -v https://example.com 2>&1 | head -40   # 3. TCP, TLS, HTTP details
curl -w 'dns:%{time_namelookup} connect:%{time_connect} tls:%{time_appconnect} total:%{time_total}\\n' -o /dev/null -s https://example.com""")],
problems=[("Website slow only for some users","DNS resolves to far region / no CDN","Use `curl -w` timing to find the slow phase; add CDN, GeoDNS.")],
qa=[("What happens when you type google.com in browser?","Browser cache -> DNS resolution (recursive resolver -> root -> TLD -> authoritative) -> TCP 3-way handshake -> TLS handshake -> HTTP GET -> server response -> browser renders, loading more resources."),
("TCP vs UDP?","TCP: reliable, ordered, connection-oriented (web, SSH). UDP: connectionless, faster, no guarantee (DNS, video, QUIC)."),
("Explain TCP 3-way handshake.","SYN -> SYN-ACK -> ACK. Connection closes with FIN/ACK exchanges."),
("Which layer do load balancers L4 and L7 work at?","L4 at transport (IP+port), L7 at application (HTTP path/header based)."),
("What is MTU?","Max packet size on a link (1500 typical). Mismatch causes fragmentation or dropped large packets.")]),

dict(slug="ip-subnetting", title="IP Addressing & Subnetting (CIDR)", level="Basic",
intro="VPC design karne ke liye CIDR aana chahiye. /24 = 256 addresses, /16 = 65,536. Private ranges: 10/8, 172.16/12, 192.168/16.",
diagram="""
10.0.0.0/16  (VPC: 65,536 IPs)
 ├─ 10.0.1.0/24  public-a   (256 IPs; AWS reserves 5)
 ├─ 10.0.2.0/24  public-b
 ├─ 10.0.11.0/24 private-a
 └─ 10.0.21.0/24 db-a

/n means first n bits are network. Hosts = 2^(32-n) - 2
""",
install="pip install ipcalc  # or: sudo apt install ipcalc -y",
examples=[("Calculate subnets","""ipcalc 10.0.1.0/24
python3 -c "import ipaddress as i; n=i.ip_network('10.0.0.0/16'); print([str(s) for s in list(n.subnets(new_prefix=24))[:4]])"
"""),
("Plan a 3-tier, 2-AZ network","""VPC 10.0.0.0/16
public   10.0.1.0/24, 10.0.2.0/24      (ALB, NAT)
private  10.0.11.0/24, 10.0.12.0/24    (app)
database 10.0.21.0/24, 10.0.22.0/24    (RDS)""")],
problems=[("Cannot peer two VPCs","Overlapping CIDR blocks","Plan non-overlapping ranges org-wide from day 1; use IPAM."),
("EKS runs out of IPs","Subnets too small (/24) for pod IPs","Use larger subnets (/19), or secondary CIDR / prefix delegation.")],
qa=[("How many usable IPs in /27?","32 - 2 = 30 (AWS: 27)."),
("Public vs private IP?","Private ranges are non-routable on Internet (RFC1918); public are globally routable."),
("What is NAT?","Translates private IPs to public for outbound access; NAT gateway in cloud."),
("What is 0.0.0.0/0?","All IPv4 addresses (default route)."),
("What is a default gateway?","Router IP used to reach networks outside the local subnet.")]),

dict(slug="dns", title="DNS Deep Dive", level="Intermediate",
intro="DNS name ko IP mein badalta hai. Aadhe production outages DNS ki wajah se hote hain. Records, TTL aur resolution flow samjho.",
diagram="""
Browser -> Resolver(ISP/8.8.8.8) -> Root (.) -> TLD (.com) -> Authoritative (Route53) -> IP
                 └── cache (TTL) ──┘

Records: A (IPv4) | AAAA (IPv6) | CNAME (alias) | MX (mail) | TXT (SPF/verify) | NS | SRV
""",
install="sudo apt install dnsutils -y   # dig, nslookup",
examples=[("Query records","""dig example.com A +short
dig example.com MX; dig example.com TXT
dig +trace example.com
dig @1.1.1.1 example.com                # bypass local resolver
nslookup -type=NS example.com"""),
("Route53 weighted record (Terraform)","""resource "aws_route53_record" "app" {
  zone_id = var.zone_id
  name    = "app.example.com"
  type    = "A"
  set_identifier = "blue"
  weighted_routing_policy { weight = 90 }
  alias { name = aws_lb.blue.dns_name  zone_id = aws_lb.blue.zone_id  evaluate_target_health = true }
}""")],
problems=[("After migration, some users still hit old server","High TTL (86400) cached","Lower TTL to 60s a day BEFORE migration, raise after."),
("Pods can't resolve external names","CoreDNS/ndots issue or upstream DNS blocked","`kubectl exec -it pod -- nslookup google.com`; check CoreDNS logs/configmap.")],
qa=[("CNAME vs A record?","A maps name to IP; CNAME maps name to another name. CNAME cannot exist at zone apex (use ALIAS)."),
("What is TTL?","How long resolvers cache the record."),
("Recursive vs authoritative DNS?","Recursive resolver does lookups for clients; authoritative holds the actual zone records."),
("What is split-horizon DNS?","Different answers for internal vs external queries (private hosted zone)."),
("Why does DNS use UDP 53 and sometimes TCP?","UDP for small fast queries; TCP for large responses, zone transfers, DNSSEC.")]),

dict(slug="http-tls", title="HTTP, HTTPS & TLS/SSL", level="Intermediate",
intro="Web ki language HTTP hai. HTTPS = HTTP + TLS encryption. Certificates, status codes aur headers debugging mein roz kaam aate hain.",
diagram="""
Client                                Server
  | ---- ClientHello (ciphers) ------> |
  | <--- ServerHello + Certificate ---- |
  | verify cert chain (CA)              |
  | ---- key exchange ----------------> |
  | <=== encrypted HTTP traffic =====> |

Status: 2xx ok | 3xx redirect | 4xx client error (401 auth, 403 forbidden, 404, 429) | 5xx server (500, 502 bad gw, 503, 504 timeout)
""",
install="sudo apt install certbot python3-certbot-nginx openssl -y",
examples=[("Inspect requests/certs","""curl -I https://example.com
curl -X POST -H 'Content-Type: application/json' -d '{"a":1}' https://api/x -v
openssl s_client -connect example.com:443 -servername example.com </dev/null | openssl x509 -noout -dates -issuer
echo | openssl s_client -connect example.com:443 2>/dev/null | openssl x509 -noout -enddate"""),
("Free HTTPS with Let's Encrypt","""sudo certbot --nginx -d example.com -d www.example.com
sudo certbot renew --dry-run""")],
problems=[("502 Bad Gateway from Nginx","Upstream app down or wrong port","`systemctl status app`; check `proxy_pass`; nginx error.log."),
("Browser shows 'certificate expired'","Renewal cron failed","`certbot renew`, monitor expiry with Prometheus blackbox `probe_ssl_earliest_cert_expiry`."),
("504 Gateway Timeout","Upstream too slow","Increase `proxy_read_timeout` only after finding slow query; add caching.")],
qa=[("Difference between 401 and 403?","401 not authenticated; 403 authenticated but not permitted."),
("502 vs 503 vs 504?","502 invalid response from upstream, 503 service unavailable/overloaded, 504 upstream timeout."),
("How does HTTPS work?","Certificate verification, asymmetric key exchange to derive symmetric session keys, then symmetric encrypted traffic."),
("HTTP/1.1 vs HTTP/2 vs HTTP/3?","2 multiplexes over one TCP connection; 3 uses QUIC (UDP) avoiding head-of-line blocking."),
("What is HSTS?","Header forcing browsers to use HTTPS only for a domain.")]),

dict(slug="load-balancing-proxy", title="Load Balancers, Reverse Proxy & Firewalls", level="Intermediate",
intro="Traffic ko multiple servers mein baantna (LB), backend ko chhupana (reverse proxy), aur security rules (firewall/security groups).",
diagram="""
        Internet
           |
        [ WAF / CDN ]
           |
        [ ALB (L7) ]  -- health checks --
        /     |     \\
     App1   App2   App3   (private subnets)
           |
        [ DB ]   SG: DB accepts 5432 only from App SG

Algorithms: round-robin | least-connections | ip-hash | weighted
""",
install="sudo apt install nginx haproxy -y",
examples=[("Nginx as load balancer","""upstream backend {
    least_conn;
    server 10.0.11.10:3000 max_fails=3 fail_timeout=10s;
    server 10.0.11.11:3000;
}
server {
    listen 80;
    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}"""),
("Security group vs NACL","""SG   : stateful, allow rules only, attached to ENI/instance
NACL : stateless, allow+deny, attached to subnet, evaluated in order""")],
problems=[("Users get logged out randomly behind LB","Session stored in server memory; requests hit different servers","Sticky sessions (short-term) or external session store (Redis)."),
("App sees LB IP not client IP","Missing forwarded headers","Use `X-Forwarded-For` / proxy protocol; configure app to trust proxy.")],
qa=[("L4 vs L7 load balancer?","L4 routes on IP/port (fast, protocol-agnostic - NLB); L7 routes on HTTP host/path/headers (ALB)."),
("Forward vs reverse proxy?","Forward proxy acts for clients; reverse proxy acts for servers."),
("SG vs NACL?","SG stateful, instance level; NACL stateless, subnet level, ordered rules."),
("How do health checks work?","LB periodically probes an endpoint; unhealthy targets are removed from rotation."),
("What is a CDN?","Edge cache network serving content near users, reducing latency and origin load.")]),

dict(slug="net-troubleshooting", title="Network Troubleshooting Playbook", level="Advanced",
intro="Systematic approach: kaha tak packet ja raha hai? Layer by layer test karo.",
diagram="""
1. Local:   ip a / ip route         (IP? gateway?)
2. DNS:     dig name               (resolves?)
3. Reach:   ping / traceroute / mtr (path OK?)
4. Port:    nc -zv host 443        (TCP open?)
5. App:     curl -v                (TLS/HTTP OK?)
6. Firewall: SG / NACL / iptables / route table
7. Packets: tcpdump / Wireshark    (final truth)
""",
install="sudo apt install netcat-openbsd mtr tcpdump nmap -y",
examples=[("Debug script","""HOST=example.com; PORT=443
dig +short $HOST
nc -zv -w3 $HOST $PORT
mtr -rwc 10 $HOST
sudo tcpdump -i any host $HOST and port $PORT -c 20 -nn"""),
("AWS reachability checklist","""1 Route table has route (IGW/NAT)?
2 SG inbound/outbound allows port?
3 NACL allows both directions (ephemeral ports 1024-65535)?
4 Instance OS firewall/app listening on 0.0.0.0?
Use: VPC Reachability Analyzer""")],
problems=[("EC2 in private subnet can't reach internet","No NAT route","Add `0.0.0.0/0 -> nat-gw` to private route table; NAT lives in public subnet."),
("Intermittent connection resets","Idle timeout on LB/NAT (350s) or conntrack table full","Enable TCP keepalive shorter than timeout; `sysctl net.netfilter.nf_conntrack_max`.")],
qa=[("Connection timeout vs connection refused?","Timeout: packets dropped (firewall/route). Refused: reached host but nothing listening (RST)."),
("How to test a port without telnet?","`nc -zv host port` or `curl -v telnet://host:port`, or bash `</dev/tcp/host/port`."),
("What is conntrack?","Kernel connection tracking table for stateful NAT/firewall; when full, new connections drop."),
("What does mtr show?","Combined traceroute + ping showing loss and latency per hop."),
("Why can pod-to-pod fail while node-to-node works?","CNI issues, NetworkPolicy, MTU/overlay problems, SG rules for pod ports.")]),
])
