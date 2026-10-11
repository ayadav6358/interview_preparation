TOPIC = dict(slug="01-linux", title="Linux", intro="DevOps ka 90% kaam Linux servers par hota hai. Yeh foundation strong karo, baaki sab tools iske upar chalte hain.", subs=[

dict(slug="filesystem-commands", title="Filesystem & Basic Commands", level="Basic",
intro="Linux mein sab kuch file hai. Root `/` se tree shuru hota hai. Pehle directory structure aur daily commands aani chahiye.",
diagram="""
/
├── etc     -> config files (nginx.conf, ssh/sshd_config)
├── var     -> changing data (logs in /var/log, web in /var/www)
├── home    -> user directories (/home/anup)
├── usr     -> installed programs (/usr/bin, /usr/local)
├── opt     -> third-party software
├── tmp     -> temp files (cleared on reboot)
├── proc    -> virtual FS: process + kernel info
└── dev     -> devices (/dev/sda, /dev/null)
""",
install="""# Windows: WSL2 (PowerShell as admin)
wsl --install -d Ubuntu
# or use VirtualBox / multipass / AWS EC2 free tier
lsb_release -a     # verify distro""",
examples=[("Daily navigation and file ops","""pwd; ls -lah
mkdir -p project/{src,logs,conf}
cd project && touch src/app.py
cp -r src src_backup
mv src_backup /tmp/
rm -rf /tmp/src_backup          # careful: no undo
cat /etc/os-release
head -n 5 /var/log/syslog; tail -f /var/log/syslog   # live follow
find /var/log -name "*.log" -mtime -1 -size +10M
du -sh * | sort -h              # what is eating space
ln -s /opt/app/current /var/www/app   # symlink (used in deployments)"""),
("Pipes and redirection","""ls /etc | wc -l
ps aux | grep nginx | grep -v grep
echo "hello" > a.txt      # overwrite
echo "more"  >> a.txt     # append
command 2> err.log        # stderr
command > all.log 2>&1    # both
export APP_ENV=prod; echo $APP_ENV; echo $PATH""")],
problems=[("`rm -rf` ne galat folder delete kar diya","Variable empty tha: `rm -rf $DIR/*` became `rm -rf /*`","Always `set -u` in scripts, quote variables, use `${DIR:?}`; keep backups; use `--preserve-root`."),
("Command not found after installing tool","Binary not in `$PATH`","`which tool`, add to `~/.bashrc`: `export PATH=$PATH:/opt/tool/bin` then `source ~/.bashrc`.")],
qa=[("Difference between hard link and soft link?","Hard link points to the same inode (survives deletion of original, cannot cross filesystems, not for directories). Soft link is a separate file holding a path; breaks if target is removed."),
("What is /proc?","Virtual filesystem exposing kernel and process info in memory, e.g. `/proc/cpuinfo`, `/proc/<pid>/status`. No disk usage."),
("How to find a file bigger than 100MB modified in last 2 days?","`find / -type f -size +100M -mtime -2 2>/dev/null`"),
("What does `2>&1` mean?","Redirect file descriptor 2 (stderr) to where fd 1 (stdout) currently points."),
("Difference between `>` and `>>`?","`>` truncates and writes, `>>` appends."),
("What is an inode?","Metadata structure storing file attributes (owner, perms, size, block pointers) but not the filename. 'No space left' can occur due to inode exhaustion (`df -i`).")]),

dict(slug="users-permissions", title="Users, Groups & Permissions", level="Basic",
intro="Linux multi-user OS hai. Har file ke owner, group aur others ke permissions hote hain: read(4), write(2), execute(1). Security ka base yahi hai.",
diagram="""
-rwxr-xr--  1  anup  devs  1200  app.sh
 |||||||||
 |||||||└─ others: r--  (4)
 ||||└┴── group : r-x  (5)
 |└┴┴──── owner : rwx  (7)   => chmod 754 app.sh
 └ file type (- file, d dir, l link)
""",
install="# built in. Useful: sudo apt install acl -y   (for setfacl)",
examples=[("Create user, group, give sudo","""sudo adduser deploy
sudo groupadd devs && sudo usermod -aG devs deploy
sudo usermod -aG sudo deploy         # sudo access
id deploy; groups deploy"""),
("chmod / chown","""chmod 750 deploy.sh          # rwx r-x ---
chmod +x script.sh; chmod -R g+w /var/www
sudo chown -R www-data:www-data /var/www/app
umask 022                     # default: files 644, dirs 755
# special bits
chmod u+s /usr/bin/x   # setuid; chmod g+s dir (inherit group); chmod +t /tmp (sticky)"""),
("Fine-grained ACL","""setfacl -m u:anup:rwx /data/reports
getfacl /data/reports""")],
problems=[("Nginx returns 403 for static files","www-data user cannot traverse parent directories (missing `x` bit)","`namei -l /var/www/app/index.html` to inspect every path component; fix with `chmod o+x` on dirs or correct owner."),
("Someone used `chmod 777` to 'fix' an app","Real cause was ownership mismatch; 777 is a security hole","Set correct owner with `chown`, use 750/640, use groups.")],
qa=[("What does chmod 644 mean?","Owner rw-, group r--, others r--."),
("What is sticky bit?","On directories, only file owner (or dir owner/root) can delete files - used in `/tmp`."),
("Difference between su and sudo?","`su` switches user with target's password; `sudo` runs a command as another user using your own credentials per `/etc/sudoers` policy, with audit log."),
("Where are users and passwords stored?","`/etc/passwd` (accounts), `/etc/shadow` (hashed passwords, root-only), `/etc/group`."),
("What is setuid?","Executable runs with the file owner's privileges (e.g. `passwd`). Risky if misused."),
("How to give a user access to only one command via sudo?","Edit with `visudo`: `deploy ALL=(ALL) NOPASSWD: /bin/systemctl restart myapp`.")]),

dict(slug="process-systemd", title="Processes, Signals & systemd", level="Intermediate",
intro="Running program = process. DevOps engineer ko services start/stop, hung process kill, aur logs (journalctl) dekhna aana chahiye. Modern Linux mein services systemd manage karta hai.",
diagram="""
systemd (PID 1)
   ├── sshd.service
   ├── nginx.service ── master ── worker, worker
   └── myapp.service  (your app: Restart=always)

Signals: SIGTERM(15) graceful | SIGKILL(9) force | SIGHUP(1) reload | SIGINT(2) Ctrl+C
""",
install="# systemd is default on Ubuntu/RHEL. WSL2: enable in /etc/wsl.conf -> [boot] systemd=true",
examples=[("Inspect and control processes","""ps aux --sort=-%mem | head
top     # or htop; press M sort by mem, P by cpu
pgrep -a nginx
kill -15 1234        # graceful; then kill -9 1234 if stuck
nice -n 10 ./job.sh; renice 5 -p 1234
nohup ./long.sh > out.log 2>&1 &  ; jobs ; fg"""),
("Create a systemd service for your app","""# /etc/systemd/system/myapp.service
[Unit]
Description=My Node App
After=network.target

[Service]
User=deploy
WorkingDirectory=/opt/myapp
ExecStart=/usr/bin/node server.js
Restart=always
RestartSec=5
Environment=NODE_ENV=production

[Install]
WantedBy=multi-user.target

# then
sudo systemctl daemon-reload
sudo systemctl enable --now myapp
systemctl status myapp
journalctl -u myapp -f --since "10 min ago"
"""),
("systemd timer instead of cron","""# backup.timer -> OnCalendar=*-*-* 02:00:00 ; Persistent=true
systemctl list-timers""")],
problems=[("Service keeps restarting (crash loop)","App exits due to missing env var / port in use","`journalctl -u myapp -n 100`, `ss -tulpn | grep 3000`; fix config; add `StartLimitBurst`."),
("Zombie processes accumulating","Parent not calling wait() on children","Fix parent app or restart parent; zombies cannot be killed directly (`ps -eo stat,ppid,pid | grep Z`)."),
("App killed randomly at night","OOM killer","`dmesg -T | grep -i oom`; add memory, set limits, fix leak.")],
qa=[("Difference between SIGTERM and SIGKILL?","SIGTERM can be caught for graceful shutdown; SIGKILL cannot be caught/ignored, kernel terminates immediately."),
("What is a zombie vs orphan process?","Zombie: finished but not reaped by parent (entry remains). Orphan: parent died; adopted by init/systemd."),
("How to run a process in background that survives logout?","`nohup cmd &`, `tmux/screen`, or better a systemd service."),
("What is PID 1?","First process (systemd/init). In containers, your app becomes PID 1 and must handle signals/reap zombies (use `tini`)."),
("What does `systemctl enable` do vs `start`?","enable = start on boot (symlink); start = start now."),
("Load average 8 on 4-core machine, meaning?","Avg number of runnable+uninterruptible tasks; 8 on 4 cores = overloaded (queueing). Check CPU vs IO wait.")]),

dict(slug="text-processing", title="Text Processing: grep, sed, awk", level="Intermediate",
intro="Logs aur config par kaam karne ke liye grep/sed/awk/cut/sort/uniq roz use hote hain. Incident ke time 5 minute mein answer nikalne ki power.",
diagram="""
access.log --grep 500--> awk '{print $1}' --> sort --> uniq -c --> sort -rn --> head
(filter)                 (pick field)         (group)   (count)     (rank)
""",
install="# built-in. Extra: sudo apt install jq -y   (JSON)",
examples=[("Top 10 IPs hitting server","""awk '{print $1}' /var/log/nginx/access.log | sort | uniq -c | sort -rn | head"""),
("Count 5xx errors per URL","""awk '$9 ~ /^5/ {print $7}' access.log | sort | uniq -c | sort -rn | head"""),
("grep power","""grep -rn "ERROR" /var/log/app/ --include="*.log"
grep -E "timeout|refused" app.log
grep -B2 -A5 "Exception" app.log      # context lines
zgrep "ERROR" app.log.*.gz"""),
("sed replace in config","""sed -i 's/^port=.*/port=8080/' app.conf
sed -n '10,20p' file; sed '/^#/d' file    # print range; delete comments"""),
("jq for JSON","""curl -s api/users | jq '.[] | select(.active) | .email'
aws ec2 describe-instances | jq -r '.Reservations[].Instances[].InstanceId'""")],
problems=[("Need to find which deploy caused errors spike","Logs are huge","`grep -c ERROR` per hour: `awk '{print substr($4,2,14)}' | uniq -c` to see spike time and correlate with deploy."),
("`sed -i` broke a config file","No backup taken","Use `sed -i.bak ...` and diff; keep configs in Git.")],
qa=[("grep vs egrep vs fgrep?","grep basic regex; `grep -E` (egrep) extended regex; `grep -F` (fgrep) fixed strings, fastest."),
("How to print 2nd column of a CSV?","`awk -F',' '{print $2}' file` or `cut -d',' -f2 file`."),
("Why sort before uniq?","uniq only collapses adjacent duplicates."),
("How to tail multiple logs and filter?","`tail -F a.log b.log | grep --line-buffered ERROR`"),
("How to replace text across many files?","`grep -rl old . | xargs sed -i 's/old/new/g'`"),
("What is xargs used for?","Converts stdin into command arguments: `find . -name '*.tmp' | xargs rm`; use `-0` with `find -print0` for spaces.")]),

dict(slug="networking-ssh", title="Linux Networking & SSH", level="Intermediate",
intro="Server se connect karna, ports check karna, aur connectivity debug karna. SSH remote access ka standard hai, keys use karo, passwords nahi.",
diagram="""
Laptop --ssh (22)--> Bastion (public subnet) --ssh--> Private server
        key-based auth            ProxyJump

Debug ladder:  ping IP -> dig DNS -> curl -v URL -> ss -tulpn (is port listening?) -> firewall (ufw/iptables/SG)
""",
install="sudo apt install openssh-server net-tools dnsutils tcpdump -y",
examples=[("SSH keys and config","""ssh-keygen -t ed25519 -C "anup@laptop"
ssh-copy-id user@server
# ~/.ssh/config
Host prod
  HostName 10.0.1.5
  User ubuntu
  IdentityFile ~/.ssh/id_ed25519
  ProxyJump bastion
# then just: ssh prod"""),
("Tunnels and file copy","""ssh -L 5432:db.internal:5432 bastion      # local port forward to private DB
scp file.tar.gz prod:/tmp/ ; rsync -avz --progress ./dist/ prod:/var/www/app/"""),
("Network debugging","""ip a; ip route
ss -tulpn                    # who listens on which port
curl -v https://example.com/health
dig +short example.com; dig @8.8.8.8 example.com
sudo tcpdump -i eth0 port 80 -nn
sudo ufw allow 22/tcp && sudo ufw enable"""),
("Harden SSH","""# /etc/ssh/sshd_config
PermitRootLogin no
PasswordAuthentication no
# sudo systemctl reload ssh""")],
problems=[("Permission denied (publickey)","Wrong key, wrong user, or perms on ~/.ssh too open","`chmod 700 ~/.ssh; chmod 600 ~/.ssh/authorized_keys`; `ssh -vvv` for details."),
("Port 8080 app running but not reachable from outside","App bound to 127.0.0.1 or firewall/security group closed","`ss -tulpn` shows 127.0.0.1:8080 -> bind 0.0.0.0; open SG/ufw."),
("Servers see brute-force attempts","Public SSH with passwords","Disable passwords, use fail2ban, restrict SG to office IP/bastion.")],
qa=[("How to check which process uses port 80?","`sudo ss -tulpn | grep :80` or `lsof -i :80`."),
("Difference between ssh -L and -R?","-L forwards local port to remote destination; -R exposes a local service via a port on the remote server (reverse)."),
("How does SSH key auth work?","Server has your public key; it sends a challenge encrypted with it; only your private key can answer. Private key never leaves your machine."),
("Ping works but curl fails. Why?","ICMP allowed but TCP port blocked/app down/TLS issue/DNS to different name. Test with `curl -v`, `nc -zv host port`."),
("What is a bastion host?","Hardened public jump server used to reach private instances, with logging and restricted access."),
("How to see DNS resolution path?","`dig +trace example.com`; check `/etc/resolv.conf`, `resolvectl status`.")]),

dict(slug="disk-storage", title="Disk, Storage & Package Management", level="Intermediate",
intro="Disk full ho jana production ka classic issue hai. Disks mount karna, LVM se resize, aur apt/yum se software manage karna aana chahiye.",
diagram="""
Disk /dev/sdb -> partition /dev/sdb1 -> filesystem (ext4/xfs) -> mount /data
LVM:  PV (disk) -> VG (pool) -> LV (volume, resizable) -> filesystem
""",
install="sudo apt update && sudo apt install lvm2 -y",
examples=[("Add and mount a new disk","""lsblk
sudo mkfs.ext4 /dev/sdb
sudo mkdir /data && sudo mount /dev/sdb /data
blkid /dev/sdb    # copy UUID
echo 'UUID=xxxx /data ext4 defaults,nofail 0 2' | sudo tee -a /etc/fstab
sudo mount -a     # test fstab BEFORE reboot"""),
("Extend LVM volume online","""sudo lvextend -L +10G /dev/vg0/data
sudo resize2fs /dev/vg0/data       # xfs_growfs /data for xfs"""),
("Find disk hogs","""df -hT; df -i
sudo du -xh / --max-depth=2 | sort -h | tail
sudo lsof +L1     # deleted files still held open"""),
("Packages","""sudo apt update && sudo apt install -y nginx
apt list --installed | grep nginx; apt-cache policy nginx
sudo apt remove --purge nginx; sudo apt autoremove
# RHEL: dnf install / dnf history undo""")],
problems=[("Disk shows 100% but du shows less","Deleted log file still open by a process","`lsof +L1` then restart process or truncate: `: > /proc/<pid>/fd/<n>`."),
("Server fails to boot after fstab edit","Wrong UUID/entry, no `nofail`","Boot rescue mode, fix fstab; always test with `mount -a`."),
("'No space left' but df has space","Inode exhaustion (millions of small files)","`df -i`; delete session/tmp files; tune fs for small files.")],
qa=[("ext4 vs xfs?","ext4 general purpose, can shrink; xfs great for large files/parallel IO, can only grow."),
("What is LVM advantage?","Flexible resize, snapshots, spanning multiple disks."),
("What is RAID 1/5/10?","1 mirror; 5 striping + parity (1 disk fail); 10 striped mirrors (performance + redundancy)."),
("How to clean a huge log safely?","`truncate -s 0 file` (not rm while in use); set up logrotate."),
("What does `apt update` vs `apt upgrade` do?","update refreshes package index; upgrade installs newer versions."),
("Why test `mount -a`?","Catches fstab errors before reboot to avoid boot failure.")]),

dict(slug="performance-troubleshooting", title="Performance & Troubleshooting", level="Advanced",
intro="Production issue mein systematic approach chahiye: CPU, memory, disk IO, network. USE method (Utilization, Saturation, Errors) follow karo.",
diagram="""
Slow server?
 ├─ CPU?     top / mpstat        -> high %us (app) / %sy (kernel) / %wa (IO wait)
 ├─ Memory?  free -m / vmstat    -> swapping (si/so) / OOM in dmesg
 ├─ Disk?    iostat -xz 1        -> %util, await high
 ├─ Network? sar -n DEV / ss -s  -> retransmits, drops
 └─ App?     strace -p PID / logs / profiler
""",
install="sudo apt install sysstat htop iotop strace lsof -y",
examples=[("60-second checklist","""uptime; dmesg -T | tail
vmstat 1 5; mpstat -P ALL 1 3
free -m; iostat -xz 1 3
sar -n DEV 1 3; ss -s; top -bn1 | head -15"""),
("Find what a hung process is doing","""strace -f -p <pid> -e trace=network,file
lsof -p <pid> | head
cat /proc/<pid>/status | grep -E 'VmRSS|Threads'"""),
("Tune kernel parameters","""sysctl net.core.somaxconn
echo 'net.core.somaxconn=1024' | sudo tee /etc/sysctl.d/99-app.conf; sudo sysctl --system
ulimit -n; # 'too many open files' -> raise LimitNOFILE in systemd unit""")],
problems=[("High load but CPU idle","Processes stuck in IO wait (slow disk/NFS)","`iostat`, `iotop`; check `%wa`; move logs off slow disk."),
("'Too many open files'","fd limit 1024","Set `LimitNOFILE=65535` in unit or `/etc/security/limits.conf`; fix fd leak."),
("Memory keeps growing","Leak or page cache misunderstanding","`free -m` look at `available` not `free`; use `smem`/pmap; restart + profile.")],
qa=[("Explain load average.","1/5/15 min avg of tasks running or waiting (incl. IO on Linux). Compare with core count."),
("What is swap and when bad?","Disk space used as RAM overflow; heavy swapping (si/so) kills performance."),
("What is OOM killer?","Kernel kills a process (highest oom_score) when memory exhausted. See `dmesg`."),
("How to find which process is using most IO?","`iotop -o` or `pidstat -d 1`."),
("What is strace?","Traces system calls of a process; reveals file/network calls and blocking points."),
("What are cgroups and namespaces?","Kernel features: cgroups limit/account resources, namespaces isolate views (pid, net, mnt...). Together they make containers.")]),

dict(slug="bash-scripting", title="Bash Scripting for DevOps", level="Intermediate",
intro="Repetitive kaam automate karne ke liye Bash script. Safe scripts likho: `set -euo pipefail`, quotes, functions, logging.",
diagram="""
script.sh --> args/env --> checks --> do work --> log --> exit code (0 ok / non-zero fail)
                                  └─ trap cleanup on EXIT/ERR
""",
install="sudo apt install shellcheck -y   # lint your scripts",
examples=[("Production-style script template","""#!/usr/bin/env bash
set -euo pipefail
trap 'echo "failed at line $LINENO" >&2' ERR

log() { echo "[$(date +%F' '%T)] $*"; }
usage() { echo "Usage: $0 <env>"; exit 1; }
[[ $# -eq 1 ]] || usage
ENV="$1"

log "Deploying to $ENV"
for host in $(cat hosts_$ENV.txt); do
  ssh "$host" 'sudo systemctl restart myapp' && log "$host OK" || log "$host FAILED"
done"""),
("Backup with rotation","""#!/usr/bin/env bash
set -euo pipefail
SRC=/var/www; DEST=/backup; KEEP=7
tar czf "$DEST/site-$(date +%F).tar.gz" "$SRC"
find "$DEST" -name 'site-*.tar.gz' -mtime +$KEEP -delete
# cron: 0 2 * * * /opt/scripts/backup.sh >> /var/log/backup.log 2>&1"""),
("Health check","""code=$(curl -s -o /dev/null -w '%{http_code}' http://localhost:3000/health)
[[ "$code" == 200 ]] || { echo "unhealthy: $code"; exit 2; }""")],
problems=[("Script continues after a failed command and corrupts data","No `set -e`","Use `set -euo pipefail`; check with shellcheck."),
("Cron job works manually but not from cron","Minimal PATH/env in cron","Use absolute paths, set PATH at top, redirect output to log.")],
qa=[("What does set -euo pipefail do?","-e exit on error, -u error on unset var, -o pipefail pipeline fails if any command fails."),
("Difference between `$@` and `$*`?","`\"$@\"` keeps each argument separate; `\"$*\"` joins into one string."),
("How to check if a file exists?","`[[ -f file ]]` (file), `-d` dir, `-s` non-empty."),
("What is exit code and how to read?","0 success; `$?` gives last command status."),
("What is a here-doc?","`cat <<EOF ... EOF` passes multi-line text to a command."),
("How do you make a script idempotent?","Check state before acting (e.g. `mkdir -p`, `grep -q || append`), so re-running gives same result.")]),
])
