# Day 6 — Terraform + Ansible Skeleton

## ✅ Goal

Day 6 prepared the Infrastructure as Code and configuration management foundation for the multi-cloud DevOps lab.

The goal was not to fully provision the cluster yet. The goal was to create a clean Terraform/Ansible skeleton, validate local tooling, protect private inventory data, and finish with a real Ansible ping across all cloud nodes.

## 🧰 Local tooling

| Tool | Version | Status |
|---|---:|---|
| Terraform | `v1.15.1` | installed locally |
| Ansible | `core 2.20.5` | installed locally |

## 📁 Created structure

Terraform provider folders:

```text
infra/terraform/aws/
infra/terraform/vultr/
infra/terraform/oracle/
```

Ansible folders:

```text
infra/ansible/inventory/
infra/ansible/playbooks/
infra/ansible/roles/
```

Key Ansible files:

```text
infra/ansible/ansible.cfg
infra/ansible/inventory/hosts.example.ini
infra/ansible/inventory/hosts.ini
infra/ansible/playbooks/ping.yml
```

## 🧭 Inventory policy

| File | Purpose | Git status |
|---|---|---|
| `hosts.example.ini` | public inventory template with placeholders | committed |
| `hosts.ini` | private inventory with real public IPs | ignored |

Public inventory placeholders:

```text
<ORACLE_PUBLIC_IP>
<AWS_PUBLIC_IP>
<VULTR_PUBLIC_IP>
<HOME_PUBLIC_IP>/32
```

Private inventory ignore check:

```bash
git check-ignore -v infra/ansible/inventory/hosts.ini
```

Expected result:

```text
.gitignore:11:infra/ansible/inventory/hosts.ini infra/ansible/inventory/hosts.ini
```

## ⚙️ Ansible config

Ansible config was loaded correctly from:

```text
/Users/erbol/devops-portfolio/infra/ansible/ansible.cfg
```

Relevant config:

```ini
[defaults]
inventory = inventory/hosts.ini
host_key_checking = False
retry_files_enabled = False
interpreter_python = auto_silent

[ssh_connection]
pipelining = True
```

## 🧪 Validation

### Inventory validation

Command:

```bash
cd ~/devops-portfolio/infra/ansible
ansible-inventory --list
```

Result:

- [x] Inventory validation passed.
- [x] Groups are present: `masters`, `workers`, `k3s_cluster`.
- [x] Hosts are present: `oci-k3s-master`, `aws-k3s-worker-1`, `vultr-k3s-worker-2`.
- [x] SSH users are correct:
  - Oracle: `ubuntu`
  - AWS: `ubuntu`
  - Vultr: `devops`
- [x] SSH key is configured as `~/.ssh/devops_cloud_lab`.

### Ansible ping verification

Command:

```bash
ansible all -m ping
```

Result:

- [x] `oci-k3s-master` returned `pong`.
- [x] `aws-k3s-worker-1` returned `pong`.
- [x] `vultr-k3s-worker-2` returned `pong`.

Playbook command:

```bash
ansible-playbook playbooks/ping.yml
```

Result:

- [x] Playbook completed successfully.
- [x] Play recap showed `failed=0`.
- [x] Play recap showed `unreachable=0`.

Detailed ping report: [Ansible Ping Results](ansible-ping-results.md)

## 🔐 Security notes

- Real public IPs are stored only in private `hosts.ini`.
- `hosts.ini` is ignored by Git.
- Public docs use placeholders only.
- SSH access uses `~/.ssh/devops_cloud_lab`.
- SSH ingress is restricted to `<HOME_PUBLIC_IP>/32`.
- No sensitive credentials, billing details, or cloud account identifiers are committed.

## 💸 Cost notes

- All 3 nodes were started only for final Ansible verification.
- After the verification:
  - AWS stopped.
  - Oracle stopped.
  - Vultr stopped.
- Hidden costs still need monitoring: volumes, snapshots, reserved IPs, backups, and trial-credit usage.

## 📌 GitHub reference

Initial skeleton commit already exists:

```text
a641c52 Add Terraform and Ansible skeleton for Day 6
```

This document records the final practical verification completed after that skeleton commit.

## 🏁 Final Day 6 checklist

- [x] Terraform installed locally: `v1.15.1`.
- [x] Ansible installed locally: `core 2.20.5`.
- [x] `infra/terraform/{aws,vultr,oracle}` created.
- [x] `infra/ansible/{inventory,playbooks,roles}` created.
- [x] `hosts.example.ini` created.
- [x] Private `hosts.ini` created locally and ignored by Git.
- [x] `ansible.cfg` loaded correctly.
- [x] `ansible-inventory --list` validation passed.
- [x] Ansible ping to all multi-cloud nodes passed.
- [x] Day 6 practical verification completed.
