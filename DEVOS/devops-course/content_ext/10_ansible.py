EXT = dict(
guide=dict(
bigpicture=dict(
problem="""**Problem it solves:** After servers exist, each one still needs packages, users, config files, patches and app deployments. Doing that by hand or with one-off scripts makes servers different from each other (configuration drift). **Ansible** describes the desired configuration in simple YAML and applies it to many servers over SSH, safely repeatable (idempotent), with no agent to install.""",
chain=["PROBLEM: many servers must be configured, patched and deployed consistently",
       "TRADITIONAL APPROACH: SSH into each server and run commands or copy scripts",
       "PAIN: drift, mistakes, no record, slow at scale",
       "TECHNOLOGY: Ansible (inventory + playbooks + modules over SSH)",
       "SOLUTION: YAML playbooks describe desired state; modules make only needed changes",
       "REAL-WORLD BENEFIT: identical servers, fast patching, documented, repeatable operations"],
text="""**Idempotent** means running the playbook again changes nothing if the server is already correct. Ansible is **agentless**: the control node connects with SSH (Linux) or WinRM (Windows), copies small modules, runs them and removes them."""),
e2e=dict(diagram="""Terraform creates servers
   v
Inventory (static file or dynamic AWS/Azure plugin)
   v
ansible-playbook site.yml   (control node)
   v
SSH to each managed node (parallel, forks=5 default)
   v
Module runs (apt, copy, template, service...) -> reports ok / changed / failed
   v
Handlers run if something changed (e.g. restart nginx)
   v
Recap: ok=12 changed=3 failed=0
   v
Re-run later: changed=0 (idempotent)  -> use in CI / AWX for scheduling""",
text="""The **control node** reads the **inventory** to know which hosts exist and their groups. For each **play**, it connects to the hosts in parallel over **SSH**, executes **tasks** in order using **modules** (small programs that check current state and change only if needed), and reports `ok`, `changed`, `failed` or `unreachable`. **Handlers** are special tasks triggered only when notified by a change, for example restart nginx after its config file changed. The **recap** summarises results. Because modules are idempotent, the same playbook can be run repeatedly to enforce state."""),
tools=dict(rows=[
["Ansible core (ansible-playbook)", "Run playbooks", "Inventory + playbook", "Configured servers", "Control node/CI"],
["Inventory (static/dynamic)", "Which hosts and groups", "Host list or cloud API", "Host set + variables", "Start of every run"],
["Roles / Collections / Galaxy", "Reusable content", "Role structure", "Tasks, templates", "Standardisation"],
["Jinja2 templates", "Config files with variables", "Variables", "Rendered files", "nginx.conf.j2"],
["Ansible Vault", "Encrypt secrets", "Secret vars", "Encrypted files", "Playbooks/vars"],
["Terraform", "Create infrastructure", "HCL", "Servers with IPs", "Before Ansible"],
["Packer", "Build golden images", "Template + Ansible provisioner", "AMI/image", "Immutable infra"],
["AWX / Automation Platform", "UI, RBAC, scheduling", "Projects/inventories", "Job runs, audit", "Enterprise operations"]],
why="**Ansible vs Terraform:** Terraform creates infrastructure; Ansible configures inside servers. **Ansible vs Puppet/Chef:** Ansible is agentless and uses push over SSH with simple YAML; Puppet/Chef use agents and pull models (strong for continuous enforcement at large scale). **Ansible vs shell scripts:** modules are idempotent, structured, cross-platform and give clear change reporting."),
compare=[
("Ansible vs Terraform", ["Topic", "Ansible", "Terraform"], [["Purpose", "Configure/deploy software", "Provision infrastructure"], ["Model", "Ordered tasks, idempotent modules", "Declarative graph + state"], ["State", "No state file", "State file required"]]),
("Ansible vs Puppet/Chef", ["Topic", "Ansible", "Puppet/Chef"], [["Agent", "None (SSH)", "Agent on each node"], ["Language", "YAML", "Ruby DSL"], ["Model", "Push", "Pull (typically)"]]),
("command/shell vs modules", ["Topic", "command/shell", "Modules (apt, copy...)"], [["Idempotent", "No (unless guarded)", "Yes"], ["Change reporting", "Always changed", "Accurate"], ["Use", "Last resort", "Preferred"]]),
("role vs playbook vs collection", ["Item", "Meaning"], [["Playbook", "YAML that maps hosts to roles/tasks"], ["Role", "Reusable structured set of tasks, templates, vars, handlers"], ["Collection", "Distribution format bundling roles, modules, plugins"]]),
("Ad-hoc vs playbook", ["Topic", "Ad-hoc", "Playbook"], [["Use", "One-off quick tasks", "Repeatable, versioned procedures"], ["Example", "`ansible all -m ping`", "`ansible-playbook site.yml`"]])],
troubleshooting=[
("`UNREACHABLE! Permission denied (publickey)`", "Wrong user/key, key not on host, SSH config", "`ansible host -m ping -vvv`, `ssh -i key user@host`", "Set `ansible_user`, `ansible_ssh_private_key_file`; fix authorized_keys.", "Standardise SSH access and use SSM/bastion configuration."),
("Task always shows `changed`", "Using command/shell without `creates`/`changed_when`", "Run twice and compare recap", "Use proper module or add `creates:`/`changed_when`.", "Lint with ansible-lint."),
("`sudo: a password is required`", "become needs a password or NOPASSWD sudo", "Run with `-K` or check sudoers", "Configure passwordless sudo for the automation user or pass `--ask-become-pass`.", "Dedicated automation user with scoped sudo."),
("Variable is undefined", "Wrong precedence/scope, typo, missing var file", "`ansible-playbook -vv`, `debug: var=...`", "Define in group_vars/host_vars or defaults; use `default()` filter.", "Use `defaults/main.yml` in roles."),
("Playbook slow", "Fact gathering, serial tasks, many forks", "`ANSIBLE_STDOUT_CALLBACK=profile_tasks`", "`gather_facts: false`, enable pipelining, increase forks, use `async`.", "Cache facts; ControlPersist SSH."),
("Python not found on target", "Minimal images without Python", "Error mentions interpreter", "Install python or set `ansible_python_interpreter`; use `raw` module to bootstrap.", "Bake Python into images.")],
practices={
"Development": ["Use roles; keep tasks small; name every task; use `--check --diff` before applying; lint with ansible-lint and yamllint."],
"Production": ["Separate inventories per environment; group_vars; run from CI/AWX; `serial` for rolling changes; tags for partial runs."],
"Security": ["Encrypt secrets with Ansible Vault or pull from a secret manager; least-privilege become; SSH keys not passwords; pin collection versions; `no_log: true` for secret tasks."],
"Performance": ["Pipelining, SSH multiplexing, `gather_facts` off when not needed, more forks, `strategy: free` where safe."],
"Reliability": ["Idempotent tasks, handlers for restarts, `serial` and `max_fail_percentage`, health checks between batches."],
"Cost Optimization": ["Automate patching and start/stop schedules; bake images with Packer to avoid repeated configuration."],
"Monitoring & Logging": ["Store run logs in AWX/CI; alert on failed runs; callbacks to Slack."],
"Backup & Disaster Recovery": ["Playbooks in Git rebuild servers; back up vault passwords securely."]},
mistakes={
"Beginner mistakes": ["Using `shell` for everything.", "Indentation errors in YAML."],
"Developer mistakes": ["Hard-coded values instead of variables.", "Huge single playbooks instead of roles."],
"DevOps mistakes": ["Not running in check mode first.", "Unpinned roles/collections."],
"Production mistakes": ["Running on all hosts at once (no `serial`).", "Restarting services on every run instead of via handlers."],
"Security mistakes": ["Plain-text secrets in vars.", "Committing the vault password."]},
versions=[
"Use fully qualified collection names (FQCN) such as `ansible.builtin.apt`; modules moved into collections since Ansible 2.10.",
"`ansible` (package with collections) vs `ansible-core` (minimal): check which you install; core versions require specific Python versions.",
"Windows targets use WinRM/`ansible.windows` collection; network devices use dedicated connection plugins.",
"Package manager modules differ per OS: `apt` (Debian), `dnf`/`yum` (RHEL family), or the generic `package` module."],
hinglish="""Ansible ek **agentless** tool hai jo SSH se servers configure karta hai. **Inventory** batata hai kaunse servers, **playbook** batata hai kya karna hai, **modules** kaam karte hain, aur **handlers** sirf tab chalte hain jab kuch change ho (jaise config badla to nginx restart). **Idempotent** ka matlab: playbook dobara chalao to kuch change nahi hoga agar server pehle se sahi hai. Passwords ko **Ansible Vault** se encrypt karo.""",
mnemonics=[("Ansible parts", "I-P-M-H-R: Inventory, Playbook, Modules, Handlers, Roles"), ("Idempotent", "Run twice, change once"), ("Safe run", "check > diff > apply"), ("Result words", "ok, changed, failed, unreachable, skipped")],
client=dict(
s30="""Ansible is our tool for configuring servers automatically and consistently. We describe the desired setup once, and it applies it to any number of servers, so patching and deployments are fast, repeatable and auditable.""",
m2="""When new servers are created, they still need software, security settings and application configuration. Doing this manually leads to differences between servers and mistakes. With Ansible we write the desired configuration as simple, versioned playbooks and run them over SSH without installing agents. Running the playbook again only fixes what is out of line, so it also detects and corrects drift. We use it for hardening, patching and application deployment, keep secrets encrypted, and run it from a pipeline or a central platform that records who ran what. You get consistency, speed and audit trails.""",
m5="""Let me cover the model, the practice and the controls. **Model:** an inventory lists hosts and groups (static or from the cloud API), playbooks map groups to roles, roles contain idempotent tasks, templates and handlers. **Practice:** Terraform creates the infrastructure, Ansible then applies the OS baseline (users, SSH hardening, packages), deploys applications and performs rolling patching with batches and health checks; for immutable setups we use Ansible inside Packer to build golden images. **Controls:** secrets in Vault or an external secret manager, least-privilege escalation, check mode and diff before changes, code review in Git and execution through AWX or CI with role-based access and logging. Result: reduced drift, faster patch cycles and evidence for compliance audits."""),
roadmap=[
("Beginner", ["SSH keys and Linux basics", "Inventory and ad-hoc commands", "First playbook with apt/service/copy", "YAML syntax"]),
("Intermediate", ["Variables, facts, conditionals, loops", "Handlers", "Templates (Jinja2)", "Roles", "Vault"]),
("Advanced", ["Dynamic inventory (AWS)", "Collections and Galaxy", "Rolling updates (serial)", "Testing with Molecule", "Performance tuning"]),
("Production", ["AWX/AAP", "CI integration", "Hardening/patching pipelines", "Packer images"]),
("Interview", ["Idempotency explained", "Roles vs playbooks", "Handlers and notify", "Ansible vs Terraform"])],
miniproject=dict(title="Deploy hardened Nginx to a fleet with roles, template, handler and vault",
arch="""Control node --SSH--> web1, web2 (group [web])
 role nginx: install > template nginx.conf > ensure started > handler reload
 group_vars/web.yml (vars) + vault.yml (secrets)
 ansible-playbook -i inventory site.yml --check --diff  then apply, serial: 1""",
steps=[
("Step 1: Inventory", """# inventory.ini
[web]
web1 ansible_host=10.0.10.11
web2 ansible_host=10.0.10.12

[web:vars]
ansible_user=ubuntu
ansible_ssh_private_key_file=~/.ssh/deploy.pem""", "Hosts and shared connection variables. Test with `ansible web -i inventory.ini -m ping`, expecting `pong`."),
("Step 2: Role tasks (roles/nginx/tasks/main.yml)", """- name: Install nginx
  ansible.builtin.apt:
    name: nginx
    state: present
    update_cache: true
  become: true

- name: Render site config
  ansible.builtin.template:
    src: site.conf.j2
    dest: /etc/nginx/conf.d/site.conf
    mode: "0644"
  become: true
  notify: Reload nginx

- name: Ensure nginx is running and enabled
  ansible.builtin.service:
    name: nginx
    state: started
    enabled: true
  become: true""", "`apt` with `state: present` installs only if missing (idempotent). `template` renders Jinja2 with variables; if the file changes it `notify`s the handler. `become: true` uses sudo. Each task has a `name` for readable output."),
("Step 3: Handler and template", """# roles/nginx/handlers/main.yml
- name: Reload nginx
  ansible.builtin.service:
    name: nginx
    state: reloaded
  become: true

# roles/nginx/templates/site.conf.j2
server {
    listen {{ nginx_port | default(80) }};
    server_name {{ server_name }};
    location / { proxy_pass http://127.0.0.1:{{ app_port }}; }
}""", "The handler runs once at the end of the play, only if notified. Template variables come from `group_vars/web.yml`; `default(80)` provides a safe fallback."),
("Step 4: Playbook and safe run", """# site.yml
- hosts: web
  serial: 1
  roles: [nginx]

# commands
ansible-playbook -i inventory.ini site.yml --check --diff
ansible-playbook -i inventory.ini site.yml
ansible-playbook -i inventory.ini site.yml   # second run: changed=0
ansible-vault encrypt group_vars/web/vault.yml""", "`serial: 1` updates one server at a time, keeping the service available. `--check --diff` previews changes. The second run demonstrates idempotency (`changed=0`). Vault encrypts secrets before they are committed.")]),
interview=[
("Beginner", "What is Ansible?", "An agentless automation tool for configuration management, deployment and orchestration using YAML playbooks.", "Foundation.", "Configure 50 web servers with one command."),
("Beginner", "What does agentless mean?", "No software is installed on managed nodes; Ansible uses SSH/WinRM and Python already present.", "Key differentiator.", "Compared to Puppet agents."),
("Beginner", "What is an inventory?", "A list of managed hosts organised in groups with variables.", "Core concept.", "[web], [db] groups."),
("Beginner", "What is a playbook?", "YAML file with plays that map hosts to tasks/roles.", "Core concept.", "site.yml."),
("Beginner", "What is a module?", "A unit of work such as apt, copy, service that does one thing idempotently.", "Building block.", "`ansible.builtin.copy`."),
("Beginner", "What is idempotency?", "Applying the same operation multiple times gives the same result without extra changes.", "Most asked.", "Second run shows changed=0."),
("Beginner", "What is `ansible all -m ping`?", "Ad-hoc command testing connectivity and Python on all hosts.", "First check.", "Returns pong."),
("Beginner", "What is a task and a handler?", "A task is one action; a handler runs only when notified by a changed task.", "Flow control.", "Restart service after config change."),
("Beginner", "What are facts?", "System information gathered automatically (OS, IPs, memory) available as variables.", "Conditionals.", "`ansible_os_family`."),
("Beginner", "How do you run a playbook?", "`ansible-playbook -i inventory playbook.yml`.", "Basics.", "Add `--check` first."),
("Intermediate", "What is a role?", "A standard directory structure (tasks, handlers, templates, defaults, vars, files, meta) to package reusable automation.", "Reuse.", "Role `nginx` used by many playbooks."),
("Intermediate", "Variable precedence in Ansible?", "Many levels; from lowest: role defaults < inventory/group_vars < host_vars < play vars < task vars < extra vars (`-e`) highest.", "Debugging vars.", "`-e` overrides everything."),
("Intermediate", "Jinja2 templates?", "Text templates with variables/filters/loops rendered on the control node.", "Config generation.", "nginx.conf.j2."),
("Intermediate", "What is Ansible Vault?", "Encrypts sensitive variables/files with a password; decrypted at runtime.", "Secrets.", "`ansible-vault encrypt vars.yml`."),
("Intermediate", "Loops and conditionals?", "`loop:` (or `with_items`) and `when:` conditions.", "Logic.", "Install a list of packages."),
("Intermediate", "What does `become` do?", "Privilege escalation (sudo) for tasks or plays.", "Permissions.", "`become: true`."),
("Intermediate", "command vs shell vs raw?", "`command` runs without shell; `shell` uses shell features; `raw` sends a raw SSH command without Python; all are non-idempotent by default.", "Module choice.", "Bootstrapping Python with raw."),
("Intermediate", "How do you make command tasks idempotent?", "Use `creates`, `removes`, `changed_when` and `when` guards, or prefer real modules.", "Best practice.", "`creates: /opt/app/.installed`."),
("Intermediate", "What are tags?", "Labels to run a subset of tasks.", "Efficiency.", "`--tags config`."),
("Intermediate", "Dynamic inventory?", "Inventory generated from cloud APIs/plugins so hosts stay current.", "Cloud usage.", "amazon.aws.aws_ec2 plugin."),
("Intermediate", "What is `--check` and `--diff`?", "Check mode simulates without changes; diff shows file differences.", "Safe changes.", "Review before prod."),
("Intermediate", "How to run ordered rolling updates?", "`serial`, `max_fail_percentage`, health checks between batches, `delegate_to` for load balancer drain.", "Zero-downtime.", "Update 1 of N servers at a time."),
("Intermediate", "What is Ansible Galaxy?", "Repository/CLI for sharing roles and collections.", "Reuse.", "`ansible-galaxy install`."),
("Advanced", "Explain how Ansible executes a module.", "Control node generates module code with args, copies it to a temp directory on the target via SSH (or pipelines it), executes with Python, returns JSON, then cleans up.", "Internals.", "Pipelining reduces SSH ops."),
("Advanced", "How would you speed up large playbook runs?", "Pipelining, ControlPersist, increase forks, disable/cached facts, `async`/`poll`, strategy free, mitogen where suitable.", "Performance.", "Patching 500 hosts."),
("Advanced", "Design a patching workflow.", "Dynamic inventory groups, drain from LB, snapshot/backup, patch in batches (serial), reboot if required, health check, re-add, stop on failure, report.", "Ops design.", "Rolling kernel patching."),
("Advanced", "Testing roles?", "Molecule with containers/VMs, ansible-lint, yamllint, idempotence test, CI.", "Quality.", "Molecule scenario for nginx role."),
("Advanced", "Collections vs roles?", "Collections package modules, plugins and roles with versioning and namespaces; roles are simpler content units.", "Modern structure.", "amazon.aws, community.general."),
("Advanced", "How do you manage secrets at scale?", "Vault with vault-ids, or lookup plugins for HashiCorp Vault/AWS Secrets Manager, `no_log`, AWX credentials.", "Security.", "Fetch DB password at runtime."),
("Advanced", "What is AWX/Ansible Automation Platform?", "Web UI/API with RBAC, credentials, scheduling, inventories, job templates and audit for Ansible.", "Enterprise use.", "Self-service patching jobs."),
("Advanced", "Ansible with Packer and Terraform: how?", "Terraform provisions, Packer + Ansible builds golden images, Ansible handles remaining runtime config or is replaced by immutable images.", "Toolchain design.", "AMI pipeline."),
("Advanced", "Handling Windows hosts?", "WinRM/SSH connection, `ansible.windows` collection, win_* modules.", "Heterogeneous fleets.", "IIS deployment."),
("Advanced", "What is `delegate_to` and `run_once`?", "`delegate_to` runs a task on another host (e.g. LB API); `run_once` runs on one host only.", "Orchestration.", "DB migration once."),
("Advanced", "Callback plugins and logging?", "Customise output/notifications (profile_tasks, JSON, Slack).", "Observability.", "Send failures to Slack."),
("Advanced", "Error handling in playbooks?", "`ignore_errors`, `block/rescue/always`, `failed_when`, `any_errors_fatal`.", "Robustness.", "Rollback in rescue."),
("Advanced", "Pull mode with ansible-pull?", "Nodes fetch playbooks from Git and run locally on a schedule; useful for edge/autoscaled hosts.", "Alternative model.", "Cron + ansible-pull."),
("Scenario-Based", "Patch 200 servers without downtime.", "Group by role, serial batches (10%), drain from LB, patch, reboot, health check, re-enable; abort on failures.", "Ops scenario.", "AWS ALB deregistration via delegate_to."),
("Scenario-Based", "Config drifted on some servers.", "Run playbook in check mode to see drift, apply to correct, add scheduled run and restrict manual access.", "Drift control.", "Nightly AWX job."),
("Scenario-Based", "New joiner needs SSH access on all servers.", "Role managing users/authorized_keys via `ansible.posix.authorized_key` from a central vars file; offboarding removes.", "Access management.", "Remove leavers quickly."),
("Scenario-Based", "Secrets are in plain text in vars.", "Encrypt with Vault, rotate exposed secrets, add pre-commit scan, move to secret manager.", "Security fix.", "Vault ids per environment."),
("Scenario-Based", "Different config per environment.", "Separate inventories/group_vars for dev/stage/prod and the same roles.", "Structure.", "inventories/prod/group_vars."),
("Scenario-Based", "A play must change only one host of a group.", "`--limit host`, or `delegate_to`/`when: inventory_hostname == ...`.", "Targeting.", "Test change on canary host."),
("Scenario-Based", "Deploy an app then run DB migration once.", "Deploy on all hosts, run migration task with `run_once: true` and `delegate_to` one host.", "Orchestration.", "Rails migrate."),
("Scenario-Based", "Terraform created hosts with dynamic IPs; how does Ansible find them?", "Dynamic inventory via aws_ec2 plugin filtering by tags, or Terraform outputs to inventory.", "Toolchain integration.", "tag:Role=web."),
("Scenario-Based", "Run playbooks from CI securely.", "Runner with vault password from secret store, SSH via bastion/SSM with short-lived keys, check mode on PR, apply after merge.", "CI usage.", "GitHub Actions with OIDC."),
("Scenario-Based", "Harden Linux servers to CIS level.", "Use a maintained hardening role, review, test in staging with Molecule, apply with check mode first, exceptions documented.", "Compliance.", "dev-sec hardening collection."),
("Scenario-Based", "Slow playbook due to fact gathering.", "Disable facts where unnecessary, use fact caching, gather subsets.", "Performance.", "gather_subset: min."),
("Scenario-Based", "Need to roll back a config change.", "Templates in Git: revert and re-run; use `backup: true` for copy/template; snapshots for risky changes.", "Recovery.", "Keep last config file."),
("Troubleshooting-Based", "`UNREACHABLE` for some hosts.", "SSH, DNS/IP, security groups, host key checking, wrong user, jump host config.", "Connectivity.", "Bastion not configured."),
("Troubleshooting-Based", "`Failed to connect to the host via ssh: Host key verification failed`.", "New/changed host key; add to known_hosts (or set `host_key_checking` deliberately for ephemeral labs).", "SSH.", "Rebuilt server."),
("Troubleshooting-Based", "YAML syntax error / mapping values not allowed.", "Indentation or missing quotes (especially with `:` or `{{ }}`); validate with `ansible-playbook --syntax-check` and yamllint.", "Syntax.", "Quote strings starting with `{{`."),
("Troubleshooting-Based", "Template renders wrong/empty values.", "Undefined variable/precedence; `-vvv`, `debug`, check `ansible_facts`.", "Vars.", "Wrong group name."),
("Troubleshooting-Based", "Handler did not run.", "No task reported changed, or the play failed before handlers ran (use `meta: flush_handlers`), or name mismatch.", "Handlers.", "Name typo in notify."),
("Troubleshooting-Based", "`Missing sudo password`.", "Set passwordless sudo or `-K`.", "Privilege.", "Automation user lacks NOPASSWD."),
("Troubleshooting-Based", "Module not found.", "Collection not installed or wrong FQCN; `ansible-galaxy collection install`.", "Collections.", "community.docker."),
("Troubleshooting-Based", "Playbook hangs.", "Waiting on prompts/background process holding SSH; use `async`, `-vvv`, timeouts, avoid interactive commands.", "Debugging.", "Service start attached to session."),
("Troubleshooting-Based", "Changes work in check mode but fail on real run.", "Some modules cannot fully simulate (command/shell); test in staging.", "Limitations.", "`shell` tasks skip in check."),
("Troubleshooting-Based", "Vault decryption failed.", "Wrong password/vault-id or file encrypted with another id.", "Vault.", "Use `--vault-id prod@prompt`.")],
cheatsheet={
"Definitions": ["Control node, managed node, inventory, playbook, play, task, module, role, handler, facts, idempotent, vault."],
"Commands": ["`ansible all -m ping -i inventory` `ansible web -m apt -a 'name=nginx state=present' -b`", "`ansible-playbook site.yml --check --diff` `--limit host` `--tags x` `-e var=val` `-vvv`", "`ansible-vault create|edit|encrypt|decrypt file` `ansible-galaxy install -r requirements.yml` `ansible-doc module` `ansible-inventory --graph` `ansible-lint`"],
"Files": ["ansible.cfg inventory.ini/yml site.yml group_vars/ host_vars/ roles/<name>/{tasks,handlers,templates,files,defaults,vars,meta}/ requirements.yml"],
"Architecture": ["Control node > SSH > managed nodes; modules executed remotely; handlers at end; results JSON."],
"Ports": ["SSH 22, WinRM 5985/5986, AWX web 80/443"],
"Differences": ["Ansible vs Terraform; command vs shell vs modules; role vs collection; ad-hoc vs playbook; push vs pull."],
"Troubleshooting commands": ["`ansible host -m ping -vvv` > `--syntax-check` > `--check --diff` > `debug: var=` > `ansible-inventory --host x`"],
"Best practices": ["Roles, FQCN modules, check+diff, vault, serial, handlers, lint, dynamic inventory, CI/AWX, idempotency."]}
),
subs={
"ansible-basics": dict(
define=dict(simple="Ansible runs commands and tasks on many servers over SSH using simple YAML files.",
technical="Ansible parses inventory and playbooks, connects via SSH, executes modules that compare desired vs current state, and returns structured results.",
why="Consistent configuration at scale.", without="Manual SSH loops.", use="Config, patching, deployments.", avoid="Provisioning cloud resources at scale (use Terraform).", analogy="A conductor giving the same instructions to a whole orchestra."),
internals="""For each task and host, Ansible builds a small Python module payload, uploads it to `~/.ansible/tmp` via SSH (or pipes it), runs it, receives JSON (`changed`, `failed`, results) and deletes it. Hosts run in parallel up to `forks`. Facts are collected first by the `setup` module unless disabled.""",
config=[("Simple playbook explained", """- name: Web baseline
  hosts: web
  become: true
  tasks:
    - name: Install nginx
      ansible.builtin.apt: { name: nginx, state: present, update_cache: true }
    - name: Start nginx
      ansible.builtin.service: { name: nginx, state: started, enabled: true }""", [("hosts: web", "Targets the group from inventory."), ("become: true", "Run as root using sudo."), ("ansible.builtin.apt", "Fully-qualified module name; `state: present` = ensure installed."), ("service enabled: true", "Start now and at boot.")])],
lab=dict(goal="Ping hosts and run a first playbook.", prereq=["Ansible installed (`pip install ansible`)", "One reachable Linux host with SSH key access (a local VM/container works)"],
steps=[("printf '[web]\\nhost1 ansible_host=<IP> ansible_user=<user>\\n' > inventory.ini && ansible web -i inventory.ini -m ping", "Expect `SUCCESS ... pong`."), ("Save the playbook above as site.yml and run: ansible-playbook -i inventory.ini site.yml --check --diff", "Preview."), ("ansible-playbook -i inventory.ini site.yml (twice)", "First run: changed=2; second run: changed=0.")]),
mnemonics=[("Run order", "Inventory > Playbook > Play > Task > Module")], hinglish="Pehle `ping` module se connectivity check karo, phir `--check` se preview, tab actual run.",
practices={"Development": ["Name tasks; FQCN; lint."]}, mistakes={"Beginner mistakes": ["shell instead of modules."]},
qa_extra=[("Intermediate", "What does `changed=0` on the second run prove?", "That the tasks are idempotent and the server already matches the desired state.", "Idempotency.", "Drift detection.")]),

"ansible-roles-templates": dict(
define=dict(simple="Roles package reusable automation; templates make config files from variables; Vault encrypts secrets.",
technical="Roles follow a standard layout loaded automatically by Ansible; Jinja2 templates are rendered on the control node; Vault uses AES256 to encrypt vars/files.",
why="Reusability and clean structure.", without="Copy-pasted, unmaintainable playbooks.", use="All non-trivial automation.", avoid="Over-nesting roles.", analogy="Roles are reusable recipe cards; templates are recipe cards with blanks to fill."),
internals="""When a play includes a role, Ansible loads `defaults/main.yml` (lowest precedence vars), `vars/main.yml`, then runs `tasks/main.yml`; handlers are registered from `handlers/main.yml`; `template:` looks in `templates/`. Vault-encrypted files are decrypted in memory with the supplied password.""",
config=[("Role layout explained", """roles/nginx/
  defaults/main.yml   # default variables (easy to override)
  tasks/main.yml      # what to do
  handlers/main.yml   # restart/reload actions
  templates/*.j2      # config files with variables
  files/              # static files
  meta/main.yml       # dependencies""", [("defaults", "Lowest precedence: safe defaults callers can override."), ("tasks", "Entry point."), ("handlers", "Triggered by notify."), ("templates", "Rendered with Jinja2."), ("meta", "Role dependencies and metadata.")])],
lab=dict(goal="Create a role and encrypt a secret.", prereq=["Ansible"],
steps=[("ansible-galaxy init roles/nginx", "Creates the standard structure."), ("printf 'db_password: s3cret\\n' > vault.yml && ansible-vault encrypt vault.yml", "Encrypts; the file now looks like $ANSIBLE_VAULT;1.1;AES256..."), ("ansible-playbook site.yml -e @vault.yml --ask-vault-pass", "Uses the secret at runtime without it being stored in plain text.")]),
mnemonics=[("Role dirs", "d-t-h-t-f-m: defaults, tasks, handlers, templates, files, meta")], hinglish="Playbook bada ho jaye to **role** banao. Secrets **Vault** mein encrypt karo aur vault password Git mein mat daalo.",
practices={"Security": ["Vault with ids; `no_log: true`."]}, mistakes={"Security mistakes": ["Vault password committed."]},
qa_extra=[("Advanced", "Where should default values live in a role?", "`defaults/main.yml`, so users can override them easily; `vars/` is high precedence and hard to override.", "Role design.", "nginx_port default.")]),

"ansible-real-usage": dict(
define=dict(simple="Real uses: harden servers, patch fleets, build images with Packer, run everything centrally with AWX.",
technical="Hardening roles enforce baseline settings (SSH, sysctl, auditd); patching playbooks use serial batches with health checks; Packer's Ansible provisioner builds golden images; AWX adds RBAC, scheduling and logging.",
why="Turn theory into operations.", without="Ad-hoc, risky changes.", use="Fleet operations.", avoid="Patching all hosts at once.", analogy="A maintenance crew following a checklist bay by bay."),
internals="""Rolling patch: for each batch (`serial`) the play removes hosts from the load balancer (delegate to LB), updates packages, reboots if required, waits for health, re-adds hosts, and stops if failures exceed `max_fail_percentage`. Packer starts a temporary instance, runs the Ansible provisioner, creates an AMI and terminates the builder.""",
config=[("Rolling patch play explained", """- hosts: web
  serial: "20%"
  max_fail_percentage: 10
  become: true
  tasks:
    - name: Upgrade packages
      ansible.builtin.apt: { upgrade: dist, update_cache: true }
      register: up
    - name: Reboot if required
      ansible.builtin.reboot:
      when: up.changed
    - name: Health check
      ansible.builtin.uri: { url: "http://{{ inventory_hostname }}/health", status_code: 200 }
      delegate_to: localhost
      retries: 10
      delay: 5""", [("serial: 20%", "Patch a fifth of the fleet at a time."), ("max_fail_percentage", "Abort if too many hosts fail."), ("register/when", "Reboot only when something changed."), ("uri health check", "Proves the host is healthy before the next batch."), ("delegate_to: localhost", "Run the check from the control node.")])],
lab=dict(goal="Dry-run a hardening/patch play.", prereq=["Test VM(s)", "Ansible"],
steps=[("Write the play above targeting a test VM", "Start small."), ("ansible-playbook patch.yml --check --diff", "Preview package changes."), ("ansible-playbook patch.yml", "Apply in a staging group first; read the recap.")]),
mnemonics=[("Rolling patch", "Drain > Patch > Reboot > Health > Re-add")], hinglish="Patching **batch mein** karo (`serial`) aur har batch ke baad **health check**. Sab servers ek saath patch mat karo.",
practices={"Reliability": ["serial, health checks, max_fail_percentage."], "Security": ["Use maintained hardening roles; document exceptions."]}, mistakes={"Production mistakes": ["No serial: outage risk."]},
versions=["`ansible.builtin.reboot` requires Ansible 2.7+. Packer's Ansible provisioner and AMI builder options change by version; consult the docs."],
qa_extra=[("Scenario-Based", "How would you keep Ansible-built servers from drifting?", "Prefer immutable golden images built with Packer and replaced on change; otherwise schedule check-mode runs/AWX jobs to detect and correct drift and restrict manual SSH.", "Long-term ops.", "Nightly drift report.")])
})
