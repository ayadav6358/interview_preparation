EXT = dict(
guide=dict(
bigpicture=dict(
problem="""**Problem it solves:** Almost every server, container, CI runner and cloud VM runs Linux. If you cannot operate Linux from the command line, you cannot deploy, debug or secure anything else in DevOps. Linux gives a stable, scriptable, free operating system where **everything is a file** and every task can be automated.""",
chain=["PROBLEM: servers have no GUI and must be managed remotely and at scale",
       "TRADITIONAL APPROACH: click through a GUI on each machine",
       "PAIN: slow, not repeatable, impossible for 100 servers",
       "TECHNOLOGY: Linux shell + core utilities + systemd + SSH + bash scripts",
       "SOLUTION: text commands that can be combined, scripted and run over SSH",
       "REAL-WORLD BENEFIT: fast troubleshooting, automation, consistent servers"],
text="""Linux is the **kernel**; a **distribution** (Ubuntu, RHEL, Amazon Linux) adds package manager, init system and tools. Containers use the host's Linux kernel features (namespaces, cgroups), so Linux knowledge is also container knowledge."""),
e2e=dict(diagram="""Engineer laptop
   | ssh user@server  (key-based)
   v
sshd (port 22) authenticates
   v
Shell (bash) reads your command
   v
Kernel system call (open/read/fork/exec)
   v
Process runs (managed by systemd or shell)
   v
Output -> stdout / stderr / log files (/var/log, journalctl)
   v
Monitor: top, free, df, ss, journalctl  -> fix -> script it""",
text="""You connect with **SSH**; `sshd` verifies your key and starts a **shell**. The shell parses your command, finds the program in `PATH` and asks the **kernel** (via `fork` and `exec`) to run it as a **process**. The process reads/writes files (including devices and sockets) using **permissions** of your user. Long-running services are supervised by **systemd**. Output goes to the terminal, to files in `/var/log` or to the **journal**. When something is wrong you check CPU/memory/disk/network with standard tools, fix the cause and turn the fix into a script so it is repeatable."""),
tools=dict(rows=[
["bash / zsh", "Command interpreter", "Commands/scripts", "Process output", "Every session"],
["coreutils (ls, cp, mv, cat)", "File operations", "Paths", "File changes/listings", "Daily admin"],
["grep / sed / awk / jq", "Text processing", "Text/log/JSON", "Filtered text", "Log analysis"],
["systemd / systemctl / journalctl", "Service manager and logs", "Unit files", "Running services, logs", "Servers"],
["ssh / scp / rsync", "Remote access and copy", "Keys, hosts", "Remote shell/files", "Remote admin"],
["apt / dnf / yum", "Package management", "Package names", "Installed software", "Provisioning"],
["top / htop / vmstat / iostat / ss", "Performance and network view", "Kernel stats", "Live metrics", "Troubleshooting"],
["cron / systemd timers", "Scheduling", "Schedule + command", "Periodic runs", "Backups/cleanup"]],
why="**apt vs dnf/yum:** Debian/Ubuntu use apt/dpkg, RHEL/Amazon Linux/Fedora use dnf/yum/rpm. **cron vs systemd timers:** cron is simple and universal; timers give logging, dependencies and calendar features."),
compare=[
("Hard link vs Soft (symbolic) link", ["Topic", "Hard link", "Soft link"], [["Points to", "Same inode (data)", "A path"], ["If original deleted", "Data still accessible", "Link breaks"], ["Cross filesystem", "No", "Yes"], ["Directories", "No", "Yes"]]),
("Process vs Thread vs Service", ["Topic", "Process", "Thread", "Service"], [["Meaning", "Running program with own memory", "Execution path inside a process", "Long-running process managed by systemd"], ["Example", "`nginx` master", "Worker thread", "`nginx.service`"]]),
("SIGTERM vs SIGKILL", ["Topic", "SIGTERM (15)", "SIGKILL (9)"], [["Can be handled", "Yes (graceful shutdown)", "No"], ["Use", "Default `kill`", "Last resort"]]),
("chmod numeric vs symbolic", ["Topic", "Numeric", "Symbolic"], [["Example", "`chmod 750 f`", "`chmod u=rwx,g=rx,o= f`"], ["Values", "r=4 w=2 x=1", "u/g/o/a and +/-/="]]),
("cron vs systemd timer", ["Topic", "cron", "systemd timer"], [["Logging", "Mail/manual", "journalctl"], ["Dependencies", "No", "Yes"], ["Missed runs", "Skipped", "`Persistent=true` catches up"]])],
troubleshooting=[
("Server is slow", "High CPU, memory pressure/swap, disk I/O wait, network", "`uptime`, `top`/`htop`, `free -h`, `vmstat 1`, `iostat -x 1`", "Identify the top consumer, restart/scale/tune; fix leak.", "Monitoring and alerts on load, memory, disk."),
("Disk full (No space left on device)", "Logs, old artifacts, deleted-but-open files, inode exhaustion", "`df -h`, `df -i`, `du -xh / --max-depth=2 | sort -h`, `lsof +L1`", "Delete/rotate logs, clean packages, restart process holding deleted file.", "logrotate, disk alerts at 80%."),
("Permission denied", "Wrong owner/mode, missing group, SELinux/AppArmor, ACL", "`ls -l`, `id`, `namei -l path`, `getenforce`", "`chown`/`chmod` minimal needed, add to group.", "Use groups and umask policies."),
("Service fails to start", "Bad config, port in use, missing dependency", "`systemctl status svc`, `journalctl -u svc -xe`, `ss -tulpn`", "Fix config, free port, restart.", "Config validation (`nginx -t`) before reload."),
("Cannot SSH", "Wrong key/permissions, firewall/security group, sshd down", "`ssh -vvv`, key perms 600, `systemctl status sshd`, `ss -tlnp | grep 22`", "Fix key mode, open port, restart sshd.", "Keep a second admin access path."),
("Out of memory (OOM killer)", "Process exceeded RAM", "`dmesg -T | grep -i oom`, `free -h`", "Add memory, fix leak, set limits.", "cgroup/systemd limits and monitoring.")],
practices={
"Development": ["Use shell scripts with `set -euo pipefail`; test in a clean container/VM."],
"Production": ["Run services under systemd as non-root users; keep packages patched; use config management for consistency."],
"Security": ["SSH keys only, disable root login and password auth; least privilege with sudo; firewall (ufw/nftables/security groups); fail2ban; auditd.", "Set correct file permissions (600 for keys)."],
"Performance": ["Know the baseline (load, memory, IO); tune limits (`ulimit`, sysctl) based on evidence."],
"Reliability": ["Auto-restart services (`Restart=on-failure`); logrotate; NTP time sync."],
"Cost Optimization": ["Right-size instances; clean unused packages/logs/images."],
"Monitoring & Logging": ["Centralize logs (`journald` > Loki/ELK); node_exporter metrics."],
"Backup & Disaster Recovery": ["Automate backups (rsync/tar/snapshots) and test restores."]},
mistakes={
"Beginner mistakes": ["`chmod 777` to fix permissions.", "Running everything as root.", "`rm -rf` with a variable that might be empty."],
"Developer mistakes": ["Scripts without error handling or quoting variables.", "Relative paths in cron jobs."],
"DevOps mistakes": ["Editing servers by hand (config drift).", "No log rotation.", "Ignoring inode usage."],
"Production mistakes": ["Restarting services without checking config.", "Filling disk with debug logs."],
"Security mistakes": ["Password SSH login with weak passwords.", "World-readable secrets/keys.", "Blind `curl | sudo bash` from unknown sources."]},
versions=[
"Package managers differ: apt (Debian/Ubuntu), dnf (RHEL 8+/Fedora/Amazon Linux 2023), yum (older RHEL/Amazon Linux 2).",
"`ifconfig`/`netstat` (net-tools) are deprecated: use `ip` and `ss`.",
"Firewall front-ends differ: ufw (Ubuntu), firewalld (RHEL), nftables underneath; iptables is legacy on modern distros.",
"cgroups v2 is the default on modern distributions; some tooling paths differ from v1.",
"On WSL2 and macOS some commands (systemctl, /proc) behave differently or are missing."],
hinglish="""Linux mein **sab kuch file hai** (devices, sockets bhi). Server par GUI nahi hota, isliye hum **commands + SSH + scripts** use karte hain. **Process** chalta hua program hai, **service** wo process hai jo systemd manage karta hai. Permission `rwx` teen logon ke liye hoti hai: **owner, group, others**. Server slow ho to pehle **CPU, memory, disk, network** check karo, phir logs dekho.""",
mnemonics=[
("Permissions", "r=4, w=2, x=1; 7=rwx, 6=rw-, 5=r-x, 4=r--"),
("Owner/Group/Other", "u-g-o: 'User, Group, Others' = 3 blocks of rwx"),
("Troubleshoot triage", "USE method: Utilization, Saturation, Errors for CPU/Mem/Disk/Net"),
("Signals", "15 = please stop, 9 = forced stop, 1 = reload (HUP)"),
("Pipe order", "grep (filter) > sort > uniq -c > sort -nr > head")],
client=dict(
s30="""Linux is the operating system that runs almost all servers and cloud infrastructure. We manage it through secure remote commands and scripts, which makes our systems fast to operate, easy to automate and simple to secure.""",
m2="""Our applications run on Linux servers in the cloud and inside containers. Linux is stable, secure and fully scriptable, so we can manage hundreds of machines the same way. Administrators connect with SSH keys, services are supervised by systemd so they restart automatically, and logs and metrics are collected centrally. We apply security basics: least-privilege users, key-only SSH, firewalls and regular patching. This gives you reliability, faster troubleshooting and lower operational cost because tasks are automated instead of manual.""",
m5="""I will explain in four parts. **Foundation:** Linux is an open-source kernel with distributions like Ubuntu or Amazon Linux; its principle is that everything is a file and every tool does one job, so tools can be combined. **Operations:** we manage access with users, groups and permissions, run applications as systemd services with restart policies, and manage software through package managers. **Reliability:** we monitor CPU, memory, disk and network, rotate logs, keep time in sync and back up data. **Security and automation:** SSH keys only, no root login, firewalls, patching, audit logging, and configuration by scripts or Ansible so servers are identical and rebuildable. Containers and Kubernetes build directly on Linux features (namespaces and cgroups), so this base skill benefits the whole platform."""),
roadmap=[
("Beginner", ["Terminal navigation: ls, cd, pwd", "Files: cp, mv, rm, cat, less", "Users and permissions", "Editors: nano/vim"]),
("Intermediate", ["Pipes and redirection", "grep/sed/awk/find", "Processes and signals", "systemd services", "SSH and networking commands", "Package management"]),
("Advanced", ["Bash scripting", "LVM, filesystems, mounts", "Performance tuning: vmstat, iostat, perf", "Kernel parameters, ulimits", "cgroups and namespaces"]),
("Production", ["Hardening and patching", "Logging and monitoring", "Backups and DR", "Config management (Ansible)"]),
("Interview", ["Troubleshoot slow server", "Explain boot process", "Permissions and special bits", "Write a log-analysis one-liner"])],
miniproject=dict(title="Provision and monitor a hardened web server by script",
arch="""Laptop --ssh key--> Ubuntu VM
   nginx (systemd service) + ufw firewall + logrotate
   cron: backup /var/www -> /backup (rsync) ; health-check script -> log
   Monitoring: node_exporter (9100) / df, free alerts""",
steps=[
("Step 1: Create user and harden SSH", """sudo adduser deploy && sudo usermod -aG sudo deploy
sudo -u deploy mkdir -p ~deploy/.ssh && sudo chmod 700 ~deploy/.ssh
# put your public key in ~deploy/.ssh/authorized_keys (chmod 600)
sudo sed -i 's/^#\\?PermitRootLogin.*/PermitRootLogin no/; s/^#\\?PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config
sudo sshd -t && sudo systemctl reload ssh""", "Creates a non-root admin, then disables root and password login. `sshd -t` validates the config BEFORE reload so you do not lock yourself out. Service name is `ssh` on Ubuntu, `sshd` on RHEL."),
("Step 2: Install and firewall", """sudo apt update && sudo apt install -y nginx ufw
sudo ufw allow OpenSSH && sudo ufw allow 'Nginx Full' && sudo ufw --force enable
systemctl status nginx --no-pager""", "Installs nginx, allows only SSH and HTTP/HTTPS. Allow SSH BEFORE enabling the firewall."),
("Step 3: Health check script", """#!/usr/bin/env bash
set -euo pipefail
LOG=/var/log/health.log
disk=$(df / --output=pcent | tail -1 | tr -dc '0-9')
if [ "$disk" -gt 80 ]; then echo "$(date -Is) DISK ${disk}%" >> "$LOG"; fi
curl -fsS -o /dev/null http://localhost || echo "$(date -Is) nginx down" >> "$LOG\"""", "`set -euo pipefail` stops on errors and undefined variables; quotes protect values; it logs problems instead of failing silently."),
("Step 4: Schedule and verify", """sudo install -m 755 health.sh /usr/local/bin/health.sh
( crontab -l 2>/dev/null; echo '*/5 * * * * /usr/local/bin/health.sh' ) | crontab -
sudo journalctl -u nginx -n 20 --no-pager
ss -tulpn | grep -E ':80|:22'""", "Runs the check every 5 minutes (use absolute paths in cron). Then confirm service logs and listening ports.")]),
interview=[
("Beginner", "What is Linux?", "A free open-source Unix-like operating system kernel; distributions package it with tools.", "Basics.", "Ubuntu, RHEL, Amazon Linux."),
("Beginner", "What does `ls -l` show?", "Long listing: permissions, links, owner, group, size, date, name.", "Everyday command.", "`-rwxr-xr-- 1 root dev`."),
("Beginner", "Explain rwx and chmod 755.", "Owner rwx (7), group r-x (5), others r-x (5).", "Permissions are heavily tested.", "Scripts are 755, private keys 600."),
("Beginner", "Absolute vs relative path?", "Absolute starts at `/`; relative starts from the current directory.", "Navigation.", "`/etc/nginx` vs `../conf`."),
("Beginner", "What is `sudo`?", "Runs a command as another user (root) if permitted by sudoers.", "Privilege control.", "`sudo systemctl restart nginx`."),
("Beginner", "How to view a large file?", "`less`, `head`, `tail -f` for live logs.", "Log reading.", "`tail -f /var/log/nginx/error.log`."),
("Beginner", "What is a package manager?", "Tool that installs/updates/removes software and dependencies.", "Provisioning.", "`apt install nginx`."),
("Beginner", "Difference between `>` and `>>`?", "`>` overwrites, `>>` appends.", "Redirection.", "`echo x >> file`."),
("Beginner", "How do you find a file?", "`find / -name file` or `locate`.", "Basic search.", "`find /var/log -name '*.log' -mtime +7`."),
("Beginner", "What is the root user?", "Superuser with UID 0 and full privileges.", "Security.", "Avoid daily use."),
("Intermediate", "Explain pipes and redirection.", "Pipe `|` sends stdout of one command to stdin of another; redirection sends streams to files; stderr is fd 2.", "Command composition.", "`grep ERROR app.log | sort | uniq -c`."),
("Intermediate", "What is a process vs daemon?", "Process is a running program; a daemon is a background service process.", "System concepts.", "sshd is a daemon."),
("Intermediate", "How to check listening ports?", "`ss -tulpn` (modern) or `netstat -tulpn`.", "Networking debugging.", "Find what uses port 8080."),
("Intermediate", "What is systemd and a unit file?", "Init system/service manager; unit files define services, timers, mounts.", "Service management.", "`/etc/systemd/system/app.service`."),
("Intermediate", "Explain inode.", "Metadata structure for a file (owner, permissions, block pointers); filenames map to inodes.", "Filesystem depth.", "`df -i` shows inode exhaustion."),
("Intermediate", "Hard link vs symlink?", "Hard link is another name for the same inode; symlink is a path pointer.", "Classic question.", "`ln -s /opt/app-v2 /opt/app`."),
("Intermediate", "Special permissions setuid/setgid/sticky?", "setuid runs as owner, setgid group inheritance/run as group, sticky prevents deleting others' files in a directory.", "Security.", "`/tmp` has sticky bit."),
("Intermediate", "How does SSH key authentication work?", "Client proves possession of private key matching a public key in `authorized_keys` via challenge signature; no password sent.", "Secure access.", "`ssh-keygen -t ed25519`."),
("Intermediate", "What is cron syntax?", "`m h dom mon dow command`.", "Scheduling.", "`0 2 * * * backup.sh`."),
("Intermediate", "grep vs sed vs awk?", "grep searches, sed edits streams, awk processes columns/fields.", "Text processing.", "`awk '{print $1}' access.log`."),
("Intermediate", "What is `/etc/fstab`?", "Defines filesystems mounted at boot.", "Storage.", "Mount EBS at /data with `nofail`."),
("Intermediate", "What are environment variables?", "Key-value pairs inherited by processes; `PATH` decides where commands are found.", "Scripting/config.", "`export DB_URL=...`."),
("Intermediate", "What is load average?", "Average number of runnable/uninterruptible tasks over 1, 5, 15 minutes; compare with CPU count.", "Performance.", "Load 8 on 4 CPUs means overloaded."),
("Intermediate", "How to check memory usage?", "`free -h`, `vmstat`, `top`; look at 'available' not just 'free'.", "Common confusion.", "Cache is reclaimable."),
("Intermediate", "What is `nohup` and `&`?", "`&` runs in background; `nohup` keeps running after logout; prefer systemd/tmux for services.", "Process control.", "Long job over SSH."),
("Advanced", "Explain the Linux boot process.", "BIOS/UEFI > bootloader (GRUB) > kernel + initramfs > systemd (PID 1) > targets/services > login.", "Deep system knowledge.", "Rescue mode by editing GRUB."),
("Advanced", "Explain namespaces and cgroups.", "Namespaces isolate views (pid, net, mnt, uts, ipc, user); cgroups limit/account resources; together they form containers.", "Links Linux to Docker.", "`unshare`, `systemd-run --property=MemoryMax=`."),
("Advanced", "How does the OOM killer choose a victim?", "Kernel scores processes by memory use and `oom_score_adj`; kills the highest to free memory.", "Memory incidents.", "Protect sshd with negative adj."),
("Advanced", "Explain LVM.", "Physical volumes > volume group > logical volumes; allows resizing/snapshots without repartitioning.", "Storage management.", "`lvextend -r` to grow online."),
("Advanced", "What is `strace` used for?", "Traces system calls to see what a process is doing (files, network, errors).", "Deep debugging.", "Find a missing config path."),
("Advanced", "Explain iowait and how to find the cause.", "CPU waiting for disk I/O. Use `iostat -x`, `iotop`, `pidstat -d`, check saturation/latency.", "Performance.", "Backup job saturating disk."),
("Advanced", "TCP connection states and TIME_WAIT?", "TIME_WAIT keeps closed connections briefly for delayed packets; many are normal on busy clients but may exhaust ports.", "Network tuning.", "`ss -s`."),
("Advanced", "How would you harden a Linux server?", "Patching, key-only SSH, no root login, firewall, least privilege sudo, minimal packages, auditd, fail2ban, CIS benchmarks, SELinux/AppArmor enforcing.", "Security.", "Ansible hardening role."),
("Advanced", "What are ulimits and file descriptors?", "Per-process limits such as open files; too low causes 'Too many open files'. Set in limits.conf or systemd `LimitNOFILE`.", "High-traffic servers.", "Nginx with 100k connections."),
("Advanced", "Difference between `kill`, `pkill`, `killall`?", "`kill` targets PID; `pkill` matches name pattern; `killall` kills all by exact name.", "Process control.", "`pkill -f gunicorn`."),
("Advanced", "Explain swap and swappiness.", "Swap extends memory using disk; swappiness controls tendency to swap; heavy swapping means memory pressure.", "Memory tuning.", "Kubernetes nodes usually disable swap."),
("Advanced", "How do you troubleshoot a zombie process?", "A zombie is a finished child not reaped by its parent; fix the parent (or kill it); zombies use no resources except a PID entry.", "Process knowledge.", "PID 1 in containers must reap children."),
("Advanced", "What is `journald` and how to filter logs?", "systemd's binary log; `journalctl -u svc --since '1 hour ago' -p err`.", "Modern logging.", "Persistent storage configured in journald.conf."),
("Advanced", "Explain rsync vs scp.", "rsync transfers only differences, supports resume/delete/permissions; scp copies whole files.", "Data transfer.", "Backup with `rsync -aHAX --delete`."),
("Advanced", "tmpfs and /proc /sys?", "tmpfs is RAM-backed FS; /proc and /sys are virtual filesystems exposing kernel/process info.", "Kernel interfaces.", "`cat /proc/meminfo`."),
("Scenario-Based", "Server disk is 100% full at night.", "`df -h` find FS, `du` for big dirs, check logs and deleted-open files with `lsof +L1`, rotate/truncate logs, expand volume, add alert.", "Frequent incident.", "Nginx debug log grew to 40GB."),
("Scenario-Based", "You cannot SSH to a server.", "Check network/security group, key permissions and username, verbose ssh, console access, sshd status/config.", "Access problems.", "Key file mode 644 rejected."),
("Scenario-Based", "A service keeps restarting.", "`systemctl status`, `journalctl -u`, exit code, config test, resource limits, dependencies, `Restart=` policy.", "Service debugging.", "Wrong environment file path."),
("Scenario-Based", "High CPU on a production box.", "`top` to find process, `pidstat`/`perf`, check recent deploy, threads, runaway loop; mitigate by restart/scale, then fix root cause.", "Incident handling.", "Regex catastrophic backtracking."),
("Scenario-Based", "Need to analyse 5GB log for top IPs.", "`awk '{print $1}' access.log | sort | uniq -c | sort -nr | head`, or use `zcat` for rotated logs.", "Text processing.", "Find abusive clients."),
("Scenario-Based", "Give a developer limited access to deploy only.", "Dedicated user/group, sudo rule for specific command, SSH key, restrict shell/directory permissions.", "Least privilege.", "sudoers: `deploy ALL=(root) NOPASSWD: /bin/systemctl restart app`."),
("Scenario-Based", "Automate nightly backup.", "Script with rsync/tar to remote/S3, cron or systemd timer, logging, retention, restore test, alerts on failure.", "Automation.", "Timer with `Persistent=true`."),
("Scenario-Based", "Time drift causes TLS/auth errors.", "Enable chrony/NTP, check `timedatectl`, firewall for UDP 123.", "Common hidden issue.", "Kerberos/JWT expiry failing."),
("Scenario-Based", "New disk must be added without downtime.", "Attach, partition or LVM pv/vg/lv, create FS, mount, add to fstab with UUID and nofail.", "Storage ops.", "Grow EBS then `growpart` and `resize2fs`."),
("Scenario-Based", "Application says 'Too many open files'.", "Check `ulimit -n`, systemd LimitNOFILE, leaks via `lsof -p PID | wc -l`, raise limits and fix leak.", "Limits.", "Proxy under load."),
("Scenario-Based", "Reduce attack surface on a fleet.", "Remove unused packages/services, patch, config management, CIS baseline, central logging, immutable images.", "Security at scale.", "Golden AMI with Packer."),
("Scenario-Based", "Script works manually but fails in cron.", "cron has a minimal environment: use absolute paths, set PATH, redirect output, check cron logs.", "Classic gotcha.", "`node` not found in cron."),
("Scenario-Based", "Move files between servers reliably.", "rsync over SSH with checksums/resume, or object storage; verify with `sha256sum`.", "Data movement.", "Migrating uploads."),
("Scenario-Based", "Container host is out of inodes.", "`df -i`, find directories with many tiny files (`find | wc`), clean images/logs.", "Hidden capacity issue.", "Millions of session files."),
("Scenario-Based", "Prevent accidental `rm -rf /` type mistakes.", "Use least privilege, quoting and `set -u`, `--preserve-root` default, backups, review scripts, dry runs (`echo`).", "Operational safety.", "Empty variable expanded to `/`."),
("Troubleshooting-Based", "`Permission denied` running a script.", "No execute bit or noexec mount or wrong shebang; `chmod +x`, check `ls -l`, `mount`.", "Permissions.", "Script from a noexec /tmp."),
("Troubleshooting-Based", "`command not found`.", "Not installed or not in PATH; check `which`, `echo $PATH`, use full path.", "Environment.", "Different PATH in sudo/cron."),
("Troubleshooting-Based", "`Address already in use`.", "Another process on the port: `ss -tulpn | grep PORT`, stop it or change port.", "Networking.", "Old process still running."),
("Troubleshooting-Based", "System is swapping heavily.", "`free -h`, `vmstat 1`, find memory hog, add RAM/limit process.", "Memory.", "JVM heap too large."),
("Troubleshooting-Based", "Log file exists but deleted space not freed.", "A process still has it open: `lsof +L1`, restart process or truncate.", "Disk.", "Rotated log not reopened."),
("Troubleshooting-Based", "DNS fails on a server.", "`resolvectl status`/`/etc/resolv.conf`, `dig @8.8.8.8 host`, firewall UDP/TCP 53.", "Network.", "systemd-resolved stub misconfigured."),
("Troubleshooting-Based", "Cannot write to a file although permissions look fine.", "Check ACLs (`getfacl`), immutable attribute (`lsattr`), read-only mount, disk full, SELinux.", "Permissions depth.", "`chattr +i` set."),
("Troubleshooting-Based", "Sudden reboot of the server.", "`last -x`, `journalctl -b -1`, `dmesg`, check OOM/kernel panic/hardware, cloud events.", "Postmortem data.", "OOM causing panic."),
("Troubleshooting-Based", "Command hangs on network mount.", "NFS server unreachable; use `timeout`, `mount -o soft`, `showmount`, check network.", "Storage.", "`df` blocks on stale NFS."),
("Troubleshooting-Based", "sudo: unable to resolve host.", "Hostname missing in /etc/hosts; add entry or fix hostname.", "Config detail.", "After cloning a VM.")],
cheatsheet={
"Definitions": ["Kernel vs distro; process vs service; inode; permissions rwx (4/2/1).", "Everything is a file; stdin(0), stdout(1), stderr(2)."],
"Commands": ["`ls -la` `cd` `pwd` `cp -r` `mv` `rm -r` `mkdir -p` `find` `du -sh` `df -h`", "`cat` `less` `head` `tail -f` `grep -Ri` `sed -i` `awk` `sort | uniq -c` `wc -l`", "`chmod` `chown` `id` `sudo` `useradd` `usermod -aG`", "`ps aux` `top` `kill -15/-9` `systemctl status|start|stop|enable` `journalctl -u`", "`ss -tulpn` `ip a` `curl -v` `ping` `dig` `ssh -i key user@host` `scp` `rsync -avz`", "`free -h` `vmstat 1` `iostat -x 1` `uptime` `dmesg -T`", "`apt update && apt install x` / `dnf install x`"],
"Files": ["/etc/passwd /etc/group /etc/shadow /etc/sudoers /etc/fstab /etc/hosts /etc/resolv.conf /etc/ssh/sshd_config", "/var/log/* /etc/systemd/system/*.service ~/.ssh/authorized_keys ~/.bashrc"],
"Architecture": ["User > shell > system call > kernel > hardware; systemd is PID 1."],
"Ports": ["SSH 22, HTTP 80, HTTPS 443, DNS 53, NTP 123, SMTP 25, MySQL 3306, PostgreSQL 5432"],
"Differences": ["hard vs soft link; SIGTERM vs SIGKILL; cron vs timer; apt vs dnf; > vs >>."],
"Troubleshooting commands": ["`uptime; free -h; df -h; df -i; top; ss -tulpn; journalctl -xe; dmesg -T`"],
"Best practices": ["Key-only SSH, non-root services, least privilege, patch, logrotate, backups tested, automate with scripts/Ansible."]}
),
subs={
"filesystem-commands": dict(
define=dict(simple="The filesystem is the tree of folders and files starting at `/`; these commands let you move around and manage it.",
technical="Linux uses a single hierarchical namespace rooted at `/` with mount points; files are inodes referenced by directory entries; standard streams and pipes connect commands.",
why="Everything in Linux (config, devices, logs) is reached through files.", without="You cannot inspect or change the system.", use="Always.", avoid="Destructive commands (`rm -rf`) without checking the path.", analogy="A building directory: floors (directories) and rooms (files)."),
internals="""When you run `ls /etc`, the shell forks a child and executes `/bin/ls`. `ls` uses system calls (`openat`, `getdents`) to read the directory inode's entries and `stat` for metadata, then writes text to stdout. Pipes connect one process's stdout to another's stdin through a kernel buffer.""",
commands=[("ls -lah", "Lists files with permissions, sizes (human readable) and hidden files.", "`-l` long, `-a` all, `-h` human sizes, `-t` sort by time, `-R` recursive.", "drwxr-xr-x 2 user group 4.0K Sep 19 10:00 dir", "Forgetting `-a` and missing dotfiles.", "`No such file`: check `pwd` and spelling."),
("find /var/log -name '*.log' -mtime +7 -size +10M", "Finds files by name/age/size.", "`-name`, `-type f|d`, `-mtime`, `-size`, `-exec cmd {} \\;`.", "List of matching paths.", "Searching `/` as non-root (permission noise).", "Use `2>/dev/null` and narrow the path."),
("du -sh * | sort -h", "Shows size of each item, sorted.", "`-s` summary, `-h` human, `--max-depth=N`, `-x` one filesystem.", "Sizes with names.", "Confusing `du` with `df`.", "Disk full but du small: deleted-open files (`lsof +L1`).")],
lab=dict(goal="Practise navigation and file operations safely.", prereq=["Linux/WSL terminal"],
steps=[("mkdir -p ~/lab/{logs,app} && cd ~/lab && pwd", "Creates a tree and moves into it."),
("echo 'hello' > app/a.txt && cp app/a.txt logs/ && ls -l logs app", "Creates and copies a file; compare with `ls`."),
("find ~/lab -type f -name '*.txt'", "Locates files."),
("rm -r ~/lab", "Removes the lab. ALWAYS double-check the path before recursive delete.")]),
mnemonics=[("Paths", "`.` here, `..` up, `~` home, `/` root"), ("Streams", "0 in, 1 out, 2 error")],
hinglish="Linux mein pura system ek **tree** hai jo `/` se shuru hota hai. `rm -rf` bina soche mat chalao: path do baar check karo.",
practices={"Production": ["Use absolute paths in scripts.", "Test destructive commands with `echo` first."]},
mistakes={"Beginner mistakes": ["`rm -rf $VAR/` with empty VAR.", "Using `cd` without checking success in scripts."]},
qa_extra=[("Scenario-Based", "Find and delete logs older than 30 days safely.", "Preview with `find /var/log/app -name '*.log' -mtime +30 -print`, then add `-delete`, or use logrotate.", "Safe operations.", "Never run delete first.")]),

"users-permissions": dict(
define=dict(simple="Users and groups decide who can read, write or run a file.",
technical="Each file has an owner UID, group GID and mode bits (rwx for user/group/other) plus optional ACLs and special bits; the kernel checks the process's effective UID/GIDs against them.",
why="Multi-user security and least privilege.", without="Anyone could read secrets or change system files.", use="Always.", avoid="`chmod 777`.", analogy="Keys and doors in an office: who holds which key."),
internals="""On each file access the kernel compares the process's UID/GID with the file's owner/group and mode: owner bits if UID matches, group bits if in group, otherwise other bits. Root (UID 0) bypasses checks (except some MAC systems). `sudo` runs a command as another user after checking `/etc/sudoers`.""",
config=[("Permission string explained", """-rwxr-x--- 1 deploy app 1024 Sep 19 app.sh
# type  owner group other
# -     rwx   r-x   ---""", [("-", "File type: `-` file, `d` directory, `l` link."), ("rwx", "Owner can read/write/execute."), ("r-x", "Group can read and execute."), ("---", "Others have no access."), ("deploy app", "Owner and group.")])],
commands=[("chmod 640 secret.env && chown deploy:app secret.env", "Sets mode and owner: owner rw, group r, others none.", "`-R` recursive, symbolic `u+x`.", "No output on success.", "`chmod -R 777` for convenience.", "Denied? Check ownership and parent directory execute bit (`namei -l path`)."),
("id; sudo -l", "Shows your UID/groups and sudo rights.", "`id user`.", "uid=1000(user) gid=1000 groups=...", "Group change not applied until re-login.", "Use `newgrp` or log in again.")],
lab=dict(goal="Create a user and restrict a directory to a group.", prereq=["sudo access on a test machine"],
steps=[("sudo groupadd app && sudo useradd -m -G app alice && sudo useradd -m bob", "alice is in group app, bob is not."),
("sudo mkdir /srv/app && sudo chown root:app /srv/app && sudo chmod 770 /srv/app", "Only root and group app can enter."),
("sudo -u alice touch /srv/app/ok; sudo -u bob ls /srv/app", "alice succeeds; bob gets `Permission denied`.")]),
mnemonics=[("Numeric", "4+2+1: r w x"), ("Directory x", "x on a directory means 'can enter'")],
hinglish="Permission teen logon ke liye hoti hai: **owner, group, others**. Directory par `x` ka matlab **andar ja sakte ho**. `777` kabhi mat lagao.",
practices={"Security": ["Least privilege; use groups not shared accounts; sudo for specific commands; keys 600; umask 027 for services."]},
mistakes={"Security mistakes": ["World-writable files.", "Shared root password."]},
qa_extra=[("Intermediate", "What does umask do?", "It subtracts permission bits from newly created files: umask 022 gives files 644 and directories 755.", "Default permissions.", "umask 027 for private services.")]),

"process-systemd": dict(
define=dict(simple="A process is a running program; systemd starts and supervises the important ones (services).",
technical="Processes are kernel tasks with PID, memory space and signals; systemd (PID 1) manages units, dependencies, cgroups, logging and restart policies.",
why="Services must start at boot, restart on failure and be observable.", without="Manual restarts and no dependency ordering.", use="Every server application.", avoid="`nohup &` for production services.", analogy="systemd is the shift supervisor ensuring each worker is at their post."),
internals="""`systemctl start app` makes systemd read the unit file, create a cgroup, fork and exec `ExecStart` as the configured user, track the main PID and capture stdout/stderr into the journal. If the process exits and `Restart=on-failure` is set, systemd waits `RestartSec` and starts it again.""",
config=[("Service unit explained", """[Unit]
Description=My API
After=network-online.target
Wants=network-online.target

[Service]
User=app
WorkingDirectory=/opt/api
EnvironmentFile=/etc/api.env
ExecStart=/usr/bin/node server.js
Restart=on-failure
RestartSec=5
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target""", [("After/Wants", "Start after the network is up."), ("User=app", "Run unprivileged."), ("EnvironmentFile", "Configuration outside the unit; keep secrets out of Git."), ("ExecStart", "Absolute path command; not run through a shell."), ("Restart=on-failure", "Auto-restart on crashes."), ("LimitNOFILE", "Raises open-file limit."), ("WantedBy=multi-user.target", "Start at normal boot when enabled.")])],
commands=[("systemctl status app", "Shows state, PID, recent logs.", "`start|stop|restart|reload|enable|disable|is-active`, `daemon-reload` after unit edits.", "Active: active (running).", "Editing the unit without `daemon-reload`.", "failed: `journalctl -u app -xe`."),
("kill -15 PID / kill -9 PID", "Send SIGTERM (graceful) or SIGKILL (forced).", "`kill -l` lists signals; `pkill -f pattern`.", "None.", "Starting with -9.", "Process ignores SIGTERM: check the signal handler, then -9.")],
lab=dict(goal="Run a small script as a systemd service.", prereq=["Linux with systemd", "sudo"],
steps=[("printf '#!/bin/bash\\nwhile true; do date >> /tmp/beat.log; sleep 5; done\\n' | sudo tee /usr/local/bin/beat.sh && sudo chmod +x /usr/local/bin/beat.sh", "Creates a loop script."),
("Create /etc/systemd/system/beat.service with [Service] ExecStart=/usr/local/bin/beat.sh and Restart=always, then: sudo systemctl daemon-reload && sudo systemctl enable --now beat", "Registers, starts and enables at boot."),
("sudo systemctl status beat; sudo pkill -f beat.sh; sleep 6; systemctl is-active beat", "It restarts automatically: proves supervision.")]),
mnemonics=[("Signals", "15 polite, 9 forced, 1 reload"), ("systemctl", "enable = at boot; start = now; enable --now = both")],
hinglish="Production service kabhi `nohup &` se mat chalao. **systemd unit** banao taaki crash par **auto-restart** ho aur logs `journalctl` mein milein.",
practices={"Reliability": ["Restart policy, limits, dependencies."], "Security": ["Dedicated user; ProtectSystem/NoNewPrivileges hardening options."]},
mistakes={"DevOps mistakes": ["No `daemon-reload`.", "Running services as root."]},
qa_extra=[("Advanced", "What is PID 1 and why does it matter?", "The first process (systemd); it adopts orphans and reaps zombies; in containers your app is PID 1 and must handle signals.", "Links to Docker.", "Use tini in containers.")]),

"text-processing": dict(
define=dict(simple="Tools that search and transform text: logs, configs and command output.",
technical="grep filters lines by regex, sed edits streams, awk processes records/fields, sort/uniq/cut/tr/jq combine in pipelines operating on stdin/stdout.",
why="Logs and configs are text; DevOps solves problems by filtering them.", without="Scrolling through huge files manually.", use="Log analysis, config edits, reports.", avoid="Parsing structured JSON with regex (use jq).", analogy="Sieves and scissors for text."),
internals="""Each tool reads a stream line by line, applies a rule and writes results, so they can be chained: `grep` reduces lines, `awk` extracts a column, `sort | uniq -c` counts, `sort -nr | head` ranks.""",
commands=[("awk '{print $1}' access.log | sort | uniq -c | sort -nr | head", "Top 10 client IPs in an nginx log.", "awk `-F,` sets separator; `$1` first field, `NF` count.", "Count and IP pairs.", "Forgetting `sort` before `uniq`.", "Wrong columns? Print with `awk '{print NF, $0}' | head`."),
("grep -RIn --exclude-dir=.git 'ERROR' /var/log/app", "Search recursively with line numbers.", "`-i` ignore case, `-v` invert, `-E` regex, `-A/-B` context.", "path:line:text.", "Unquoted pattern expanded by the shell.", "No output? Check permissions and path."),
("sed -i.bak 's/old/new/g' file", "In-place replacement with backup.", "`-n` + `p`, `-E`, addresses.", "None.", "Editing without a backup.", "macOS sed needs `-i ''`.")],
lab=dict(goal="Analyse a sample access log.", prereq=["Linux terminal"],
steps=[("printf '1.1.1.1 GET /a 200\\n2.2.2.2 GET /b 500\\n1.1.1.1 GET /c 200\\n' > log.txt", "Creates sample data."),
("awk '{print $1}' log.txt | sort | uniq -c | sort -nr", "Counts requests per IP: `2 1.1.1.1` first."),
("awk '$4>=500' log.txt", "Shows only server errors."),
("echo '{\"a\":1}' | jq .a", "jq extracts JSON fields properly.")]),
mnemonics=[("Pipeline", "Filter > Extract > Sort > Count > Rank")],
hinglish="Log dekhna ho to **grep** se filter, **awk** se column nikalo, **sort | uniq -c** se count karo. JSON ke liye **jq** use karo.",
practices={"Production": ["Use `zcat`/`zgrep` for rotated logs."]}, mistakes={"Beginner mistakes": ["`uniq` without `sort`."]},
qa_extra=[("Scenario-Based", "Find which endpoint returns most 5xx.", "`awk '$9>=500 {print $7}' access.log | sort | uniq -c | sort -nr | head` (columns depend on log format).", "Real log analysis.", "Check field numbers first.")]),

"networking-ssh": dict(
define=dict(simple="Commands to see and test a server's network, and SSH to log in securely.",
technical="Linux exposes networking via `ip`/`ss` (netlink), DNS resolvers and firewall (nftables); SSH provides an encrypted channel with key-based authentication, port forwarding and file transfer.",
why="Servers are remote and services talk over the network.", without="No remote access or diagnosis.", use="Always.", avoid="Password SSH on the internet.", analogy="SSH is a locked, private tunnel to the machine."),
internals="""SSH: TCP connect > key exchange establishes an encrypted session > server sends its host key (verified against `known_hosts`) > client proves identity by signing a challenge with the private key > shell/subsystem starts.""",
commands=[("ss -tulpn", "Lists listening TCP/UDP sockets with processes.", "`-t` TCP, `-u` UDP, `-l` listening, `-p` process, `-n` numeric.", "LISTEN 0 511 0.0.0.0:80 users:((nginx...))", "Needs sudo for process names.", "Not listening? service down or bound to 127.0.0.1."),
("ssh -i ~/.ssh/key.pem -L 5433:db:5432 user@bastion", "SSH with local port forward through a bastion.", "`-L` local, `-R` remote, `-J` jump host, `-vvv` debug.", "Shell on the bastion; localhost:5433 reaches db.", "Wrong key permissions (must be 600).", "`Permission denied (publickey)`: user, key, authorized_keys perms."),
("curl -v http://host:port/health", "Tests HTTP with verbose details.", "`-I` headers, `-k` insecure, `--resolve`, `-w`.", "Request/response info.", "Confusing DNS vs connection failure.", "Use `dig`, `nc -zv host port`.")],
lab=dict(goal="Set up key-based SSH.", prereq=["Two Linux machines/VMs or WSL + a VM"],
steps=[("ssh-keygen -t ed25519 -C 'me@laptop'", "Creates a key pair in ~/.ssh."),
("ssh-copy-id user@server", "Adds your public key to `~/.ssh/authorized_keys` on the server."),
("ssh user@server 'hostname'", "Logs in without a password."),
("ss -tulpn | grep :22", "On the server confirm sshd is listening.")]),
mnemonics=[("Debug network", "Layer by layer: link (ip a) > route (ip r) > DNS (dig) > port (nc/ss) > app (curl)")],
hinglish="SSH mein **private key kabhi share mat karo**, sirf public key server par daalo. Network problem ho to **layer by layer** check karo.",
practices={"Security": ["Key-only, disable root login, use bastion/SSM, fail2ban, rotate keys."]}, mistakes={"Security mistakes": ["Key permissions 644.", "Sharing private keys."]},
versions=["`ip`/`ss` replace `ifconfig`/`netstat`.", "Ed25519 keys are preferred over RSA-2048 where supported."],
qa_extra=[("Advanced", "How would you access a private DB safely?", "Via bastion/SSM with SSH tunnel or port forward, no public DB exposure, audited access.", "Secure access.", "SSM Session Manager port forwarding.")]),

"disk-storage": dict(
define=dict(simple="How disks are split, formatted, mounted and how software is installed.",
technical="Block devices are partitioned (MBR/GPT) or managed by LVM, formatted with a filesystem (ext4/xfs), mounted in the tree (fstab/UUID); package managers resolve dependencies from repositories.",
why="Applications need storage and software.", without="No place to store data or install tools.", use="Provisioning and capacity work.", avoid="Editing fstab without `nofail` on cloud disks.", analogy="Buying land (disk), fencing it (partition), building on it (filesystem)."),
internals="""New disk > `lsblk` sees device > partition/PV > format (`mkfs`) > `mount` attaches it at a directory > `/etc/fstab` makes it persistent using **UUID** (names like /dev/sdb can change). Packages: `apt install` reads the repo index, resolves dependencies, downloads and installs, and records them in the package database.""",
lab=dict(goal="Add and mount a new disk (test VM only).", prereq=["Extra disk attached, sudo"],
steps=[("lsblk", "Identify the new disk (for example /dev/sdb). Be certain: formatting destroys data."),
("sudo mkfs.ext4 /dev/sdb && sudo mkdir /data && sudo mount /dev/sdb /data", "Formats and mounts."),
("sudo blkid /dev/sdb; echo 'UUID=<uuid> /data ext4 defaults,nofail 0 2' | sudo tee -a /etc/fstab && sudo mount -a", "Persistent mount; `mount -a` validates fstab before reboot.")]),
compare=[("ext4 vs xfs", ["Topic", "ext4", "xfs"], [["Strength", "General purpose, shrinkable", "Large files, parallel IO, RHEL default"], ["Shrink", "Yes", "No"]])],
mnemonics=[("Disk steps", "Partition > Format > Mount > fstab")],
hinglish="Naya disk: **lsblk → mkfs → mount → fstab (UUID ke saath, nofail)**. Format karne se pehle device ka naam do baar check karo.",
practices={"Reliability": ["Use UUID and `nofail`; monitor disk and inode usage; LVM for flexibility."]}, mistakes={"Production mistakes": ["Formatting the wrong disk.", "fstab typo preventing boot."]},
versions=["apt for Debian/Ubuntu; dnf/yum for RHEL family. Cloud disks may appear as /dev/nvme*."],
qa_extra=[("Scenario-Based", "EBS volume was enlarged in AWS; how to use the space?", "`growpart /dev/xvda 1` then `resize2fs` (ext4) or `xfs_growfs` (xfs); verify with `df -h`.", "Common cloud task.", "No downtime needed.")]),

"performance-troubleshooting": dict(
define=dict(simple="A method to find why a server is slow or failing.",
technical="Use the USE method (Utilization, Saturation, Errors) for CPU, memory, disk and network, correlating metrics with logs and recent changes.",
why="Fast, structured diagnosis reduces downtime.", without="Guessing and random restarts.", use="Incidents and capacity reviews.", avoid="Changing many things at once.", analogy="A doctor takes vitals before prescribing."),
internals="""Start with `uptime` (load) > `top` (who?) > `free -h` (memory/swap) > `vmstat 1` (run queue, swap, iowait) > `iostat -x 1` (disk latency/util) > `ss -s` (connections) > logs (`journalctl`, app logs). Each tool answers one question and narrows the suspect.""",
commands=[("vmstat 1 5", "CPU, memory, swap and IO snapshot every second.", "`-s` memory stats, `-d` disk.", "Columns r b swpd free si so bi bo us sy id wa.", "Reading only the first line (since boot).", "High `wa` = disk waiting; high `si/so` = swapping."),
("iostat -x 1", "Per-device IO utilisation and latency.", "`-x` extended, `-d` device only.", "%util, await.", "`iostat` package missing (sysstat).", "%util near 100 and high await: disk saturated.")],
lab=dict(goal="Create and diagnose CPU load.", prereq=["Linux terminal"],
steps=[("yes > /dev/null & yes > /dev/null &", "Starts two CPU hogs."),
("uptime; top -bn1 | head -15", "Load rises; `yes` processes at the top."),
("pkill yes; uptime", "Load falls gradually (1-minute average).")]),
mnemonics=[("USE", "Utilization, Saturation, Errors for every resource")],
hinglish="Server slow ho to **pehle vitals dekho**: `uptime`, `top`, `free`, `vmstat`, `iostat`. Ek ek karke suspect kam karo, andaaza mat lagao.",
practices={"Monitoring & Logging": ["Baseline metrics with node_exporter/Prometheus so you know what 'normal' is."]}, mistakes={"DevOps mistakes": ["Restarting before capturing evidence."]},
qa_extra=[("Scenario-Based", "Load average is 20 but CPU idle is high. Why?", "Load includes tasks in uninterruptible IO wait; likely disk or NFS problem. Check iowait, `iostat`, D-state processes.", "Understanding load.", "Slow disk.")]),

"bash-scripting": dict(
define=dict(simple="A file of shell commands with logic that automates repeated tasks.",
technical="Bash is an interpreter supporting variables, conditionals, loops, functions, exit codes, traps and pipelines; scripts are executed via shebang with strict mode for safety.",
why="Automation is repeatable and reviewable.", without="Manual, error-prone steps.", use="Small automation and glue tasks.", avoid="Complex logic and data structures (use Python).", analogy="A recipe the computer follows exactly."),
internals="""The kernel reads the shebang (`#!/usr/bin/env bash`) and runs bash with the script. Bash expands variables, runs commands, and each command returns an exit code (0 = success). `set -e` stops on failure, `-u` on unset variables, `pipefail` on failures inside pipelines. `trap` runs cleanup on exit.""",
config=[("Safe script template explained", """#!/usr/bin/env bash
set -euo pipefail
trap 'echo "failed at line $LINENO" >&2' ERR
TARGET="${1:?usage: $0 <dir>}"
for f in "$TARGET"/*.log; do
  [ -e "$f" ] || continue
  gzip -f "$f"
done""", [("#!/usr/bin/env bash", "Finds bash in PATH."), ("set -euo pipefail", "Exit on error, unset variable or failed pipe."), ("trap ... ERR", "Reports where it failed."), ("${1:?usage}", "Requires an argument and prints usage if missing."), ("\"$TARGET\"", "Quoting prevents word-splitting and globbing bugs."), ("[ -e \"$f\" ] || continue", "Handles the no-match case.")])],
lab=dict(goal="Write a backup script with logging.", prereq=["Linux terminal"],
steps=[("cat > backup.sh <<'EOF'\n#!/usr/bin/env bash\nset -euo pipefail\nSRC=\"${1:?src}\"; DEST=\"${2:?dest}\"\nmkdir -p \"$DEST\"\ntar czf \"$DEST/backup-$(date +%F).tgz\" -C \"$SRC\" .\necho \"$(date -Is) backup ok\" >> \"$DEST/backup.log\"\nEOF\nchmod +x backup.sh", "Creates an executable script."),
("./backup.sh ~/lab /tmp/bk && ls -l /tmp/bk", "Runs it; check the archive and log."),
("./backup.sh", "Prints the usage error thanks to `${1:?}`.")]),
mnemonics=[("Strict mode", "set -euo pipefail = Exit, Unset, Pipefail"), ("Exit codes", "0 = success, non-zero = failure")],
hinglish="Script ke top par **`set -euo pipefail`** lagao aur variables ko **quotes** mein rakho. Cron mein script chalao to **absolute paths** use karo.",
practices={"Development": ["Use shellcheck; functions; logging; idempotent steps."], "Security": ["Never echo secrets; validate inputs."]},
mistakes={"Developer mistakes": ["Unquoted variables.", "Parsing `ls` output.", "No error handling."]},
qa_extra=[("Intermediate", "What does `$?` and `$@` mean?", "`$?` is the last exit code; `$@` is all arguments (quote it as \"$@\").", "Scripting basics.", "Wrapper scripts forwarding args.")])
})
