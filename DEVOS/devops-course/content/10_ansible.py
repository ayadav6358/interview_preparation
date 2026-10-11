TOPIC = dict(slug="10-ansible", title="Configuration Management: Ansible", intro="Servers ka setup, patching, app deploy: agentless, SSH par chalta hai, YAML playbooks. Terraform infra banata hai, Ansible usko configure karta hai.", subs=[

dict(slug="ansible-basics", title="Ansible Basics: Inventory, Ad-hoc & Playbooks", level="Basic",
intro="Control node se SSH karke managed nodes par tasks run hote hain. Modules idempotent hote hain: dobara chalao to same result.",
diagram="""
Control node (ansible) --SSH--> web1, web2, db1   (inventory groups)
playbook.yml -> plays -> tasks -> modules (apt, copy, template, service)
""",
install="""pip install ansible      # or: sudo apt install ansible -y   (Windows: use WSL2)
ansible --version""",
examples=[("Inventory and ad-hoc","""# inventory.ini
[web]
web1 ansible_host=10.0.1.10
web2 ansible_host=10.0.1.11
[db]
db1 ansible_host=10.0.2.10
[all:vars]
ansible_user=ubuntu
ansible_ssh_private_key_file=~/.ssh/id_ed25519

ansible all -i inventory.ini -m ping
ansible web -i inventory.ini -m shell -a "uptime"
ansible web -i inventory.ini -b -m apt -a "name=nginx state=present" """),
("First playbook","""- name: Setup web servers
  hosts: web
  become: true
  vars: { http_port: 80 }
  tasks:
    - name: Install nginx
      apt: { name: nginx, state: present, update_cache: true }
    - name: Deploy index
      copy: { content: "Hello from {{ inventory_hostname }}", dest: /var/www/html/index.html }
      notify: restart nginx
    - name: Ensure running
      service: { name: nginx, state: started, enabled: true }
  handlers:
    - name: restart nginx
      service: { name: nginx, state: restarted }

# ansible-playbook -i inventory.ini site.yml --check --diff   (dry-run first)""")],
problems=[("UNREACHABLE! SSH error","Wrong user/key/host key checking","Test `ssh` manually; set `ansible_user`; `-vvv` for details."),
("`command`/`shell` tasks always show changed","Not idempotent","Use proper modules or `creates:`/`changed_when:`.")],
qa=[("Why is Ansible agentless?","Uses SSH/WinRM, no daemon on nodes."),
("What is idempotency?","Repeated runs produce the same state without extra changes."),
("Handlers?","Tasks that run only when notified by a change (e.g. restart service)."),
("`command` vs `shell`?","shell uses a shell (pipes, redirects); command doesn't; prefer modules."),
("Ansible vs Terraform?","Terraform provisions infra (declarative, state); Ansible configures software (procedural-ish, stateless).")]),

dict(slug="ansible-roles-templates", title="Roles, Templates, Variables & Vault", level="Intermediate",
intro="Playbook bada ho jaye to roles mein todo. Jinja2 templates se config files generate karo. Vault se secrets encrypt karo.",
diagram="""
roles/nginx/
  ├── tasks/main.yml
  ├── handlers/main.yml
  ├── templates/nginx.conf.j2
  ├── defaults/main.yml   (lowest precedence vars)
  └── vars/ , files/ , meta/
""",
install="ansible-galaxy init roles/nginx\nansible-galaxy install geerlingguy.docker",
examples=[("Template","""# templates/app.conf.j2
server {
  listen {{ http_port }};
  server_name {{ domain }};
  location / { proxy_pass http://127.0.0.1:{{ app_port }}; }
}
# task
- template: { src: app.conf.j2, dest: /etc/nginx/conf.d/app.conf, validate: 'nginx -t -c /etc/nginx/nginx.conf' }
  notify: reload nginx"""),
("Loops, conditions, tags","""- apt: { name: "{{ item }}", state: present }
  loop: [git, curl, htop]
  when: ansible_os_family == "Debian"
  tags: [packages]
# ansible-playbook site.yml --tags packages --limit web1"""),
("Vault","""ansible-vault create group_vars/prod/vault.yml
ansible-playbook site.yml --ask-vault-pass    # or --vault-password-file"""),
("Rolling update","""- hosts: web
  serial: 1          # one server at a time
  max_fail_percentage: 0
  tasks: [ ... ]""")],
problems=[("Variable precedence confusion","Same var defined in many places","Keep defaults in role, env values in group_vars; use `ansible-inventory --host`."),
("Config change broke nginx on all servers","No validation, no serial","Use `validate:`, `serial`, `--check`.")],
qa=[("What is a role?","Reusable structured unit of tasks, templates, vars."),
("Ansible Galaxy?","Repository of community roles/collections."),
("How do you keep secrets safe?","Ansible Vault or external secret lookup (Vault, AWS SSM)."),
("Dynamic inventory?","Inventory generated from cloud API (aws_ec2 plugin)."),
("How to do zero-downtime rolling update?","`serial`, drain from LB with `delegate_to`, health-check before next batch.")]),

dict(slug="ansible-real-usage", title="Real Use Cases: Hardening, Patching, Packer & AWX", level="Advanced",
intro="Production mein Ansible: server hardening, patching, AMI baking (Packer), testing (Molecule), aur AWX UI.",
diagram="""
Packer + Ansible -> Golden AMI -> Terraform launches ASG with AMI
Nightly: Ansible patch playbook (serial) -> verify -> report
Molecule: role -> docker instance -> converge -> verify (CI)
""",
install="pip install molecule molecule-plugins[docker] ansible-lint\nwinget/apt install packer",
examples=[("Hardening tasks","""- name: Disable root SSH and passwords
  lineinfile: { path: /etc/ssh/sshd_config, regexp: '^#?{{ item.k }}', line: '{{ item.k }} {{ item.v }}' }
  loop: [{ k: PermitRootLogin, v: 'no' }, { k: PasswordAuthentication, v: 'no' }]
  notify: reload ssh
- name: Enable UFW
  ufw: { state: enabled, policy: deny }
- ufw: { rule: allow, port: '22', proto: tcp }"""),
("Packer template using Ansible","""source "amazon-ebs" "ubuntu" {
  region = "ap-south-1"; instance_type = "t3.micro"
  source_ami_filter { filters = { name = "ubuntu/images/*22.04-amd64-server-*" } owners = ["099720109477"] most_recent = true }
  ssh_username = "ubuntu"; ami_name = "app-{{timestamp}}"
}
build {
  sources = ["source.amazon-ebs.ubuntu"]
  provisioner "ansible" { playbook_file = "site.yml" }
}"""),
("Lint & test","""ansible-lint site.yml
molecule test""")],
problems=[("Patching reboots all servers together","No serial/ordering","`serial: 20%`, reboot with `reboot` module and health check."),
("Playbook takes hours on 500 hosts","Default forks=5, gather_facts","Raise forks, `gather_facts: false`, pipelining, mitogen.")],
qa=[("Mutable vs immutable infra?","Mutable: patch in place (Ansible). Immutable: bake new image and replace (Packer+ASG)."),
("What is AWX?","Open-source web UI/API/RBAC for Ansible (upstream of Automation Controller)."),
("How to test roles?","Molecule with Docker/Vagrant, ansible-lint, CI."),
("Pull mode?","`ansible-pull` runs from Git on the node itself via cron."),
("Performance tips?","forks, pipelining, fact caching, async tasks, strategy free.")]),
])
