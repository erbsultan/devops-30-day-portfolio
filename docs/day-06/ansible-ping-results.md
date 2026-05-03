# Day 6 — Ansible Ping Results

## ✅ Цель проверки

Проверить, что локальный Ansible control node на macOS может подключиться по SSH ко всем multi-cloud nodes и выполнить базовый `ping` module.

Проверка закрывает финальную практическую часть Day 6: private inventory заполнен локально, Ansible config подхвачен корректно, все 3 nodes отвечают `pong`.

## 🧭 Inventory overview

Ansible запускался из рабочей папки:

```bash
cd ~/devops-portfolio/infra/ansible
```

Project-local `ansible.cfg` использует private inventory:

```text
inventory = inventory/hosts.ini
```

Файл `infra/ansible/inventory/hosts.ini` содержит реальные public IP и не коммитится. В публичной документации используются только placeholders.

## 🌐 Nodes

| Group | Host | Cloud | Role | Public IP | SSH user | SSH key |
|---|---|---|---|---|---|---|
| `masters` | `oci-k3s-master` | Oracle Cloud | future k3s master | `<ORACLE_PUBLIC_IP>` | `ubuntu` | `~/.ssh/devops_cloud_lab` |
| `workers` | `aws-k3s-worker-1` | AWS EC2 | future k3s worker #1 | `<AWS_PUBLIC_IP>` | `ubuntu` | `~/.ssh/devops_cloud_lab` |
| `workers` | `vultr-k3s-worker-2` | Vultr | future k3s worker #2 | `<VULTR_PUBLIC_IP>` | `devops` | `~/.ssh/devops_cloud_lab` |

Inventory groups:

- `masters`
- `workers`
- `k3s_cluster`

## 🧪 Commands

### Inventory validation

```bash
cd ~/devops-portfolio/infra/ansible
ansible-inventory --list
```

### Ad-hoc Ansible ping

```bash
ansible all -m ping
```

### Ping playbook

```bash
ansible-playbook playbooks/ping.yml
```

## ✅ Results

### `ansible-inventory --list`

Result:

- Inventory is valid.
- Groups are present: `masters`, `workers`, `k3s_cluster`.
- Hosts are present: `oci-k3s-master`, `aws-k3s-worker-1`, `vultr-k3s-worker-2`.
- Users are correct: `ubuntu` for Oracle/AWS, `devops` for Vultr.
- SSH key is configured as `~/.ssh/devops_cloud_lab`.

### `ansible all -m ping`

```text
oci-k3s-master | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
aws-k3s-worker-1 | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
vultr-k3s-worker-2 | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
```

### `ansible-playbook playbooks/ping.yml`

```text
PLAY [Ping all DevOps lab nodes]

TASK [Test SSH connection]
ok: [oci-k3s-master]
ok: [aws-k3s-worker-1]
ok: [vultr-k3s-worker-2]

PLAY RECAP:
aws-k3s-worker-1    : ok=1 changed=0 unreachable=0 failed=0 skipped=0 rescued=0 ignored=0
oci-k3s-master      : ok=1 changed=0 unreachable=0 failed=0 skipped=0 rescued=0 ignored=0
vultr-k3s-worker-2  : ok=1 changed=0 unreachable=0 failed=0 skipped=0 rescued=0 ignored=0
```

Success criteria:

- [x] Inventory validation passed.
- [x] Oracle node returned `pong`.
- [x] AWS node returned `pong`.
- [x] Vultr node returned `pong`.
- [x] Play recap shows `failed=0`.
- [x] Play recap shows `unreachable=0`.

## 🔐 Security notes

- `infra/ansible/inventory/hosts.ini` is private and ignored by Git.
- Real public IPs are not committed.
- SSH access uses key-based authentication.
- SSH ingress should be restricted to `<HOME_PUBLIC_IP>/32`.
- Public docs must use placeholders:
  - `<ORACLE_PUBLIC_IP>`
  - `<AWS_PUBLIC_IP>`
  - `<VULTR_PUBLIC_IP>`
  - `<HOME_PUBLIC_IP>/32`

Private inventory ignore check:

```bash
git check-ignore -v infra/ansible/inventory/hosts.ini
```

Expected result:

```text
.gitignore:11:infra/ansible/inventory/hosts.ini infra/ansible/inventory/hosts.ini
```

## 💸 Cost notes

- All 3 nodes were started temporarily for the Ansible verification.
- After the test:
  - AWS node stopped.
  - Oracle node stopped.
  - Vultr node stopped.
- Hidden costs should still be monitored:
  - persistent block volumes;
  - reserved/static public IPs;
  - snapshots/backups;
  - provider-specific trial credit usage.

## 🛠️ Troubleshooting checklist

- [ ] Wrong public IP in private `hosts.ini`.
- [ ] Wrong SSH user for provider.
- [ ] Security group, Security List, or cloud firewall blocks SSH.
- [ ] Host firewall blocks SSH.
- [ ] Host key changed or stale `known_hosts` entry.
- [ ] Private key permissions are too open.
- [ ] Node is stopped.
- [ ] Local public IP changed and no longer matches `<HOME_PUBLIC_IP>/32`.
- [ ] Command was not run from `infra/ansible`, so project `ansible.cfg` was not loaded.

## 🏁 Final checklist

- [x] `ansible-inventory --list` passed.
- [x] `ansible all -m ping` returned `pong` from all 3 nodes.
- [x] `ansible-playbook playbooks/ping.yml` completed successfully.
- [x] `hosts.ini` remains private and ignored by Git.
- [x] Public documentation contains placeholders only.
- [x] All 3 cloud nodes were stopped after verification.
