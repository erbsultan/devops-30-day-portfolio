# AWS Worker Baseline

AWS EC2 instance `aws-k3s-worker-1` подготовлен как future k3s worker #1 для multi-cloud lab.

## 🎯 Назначение

- Cloud: AWS EC2
- Role: future k3s worker node
- Future cluster role: worker #1
- Current status: stopped

## 📦 Instance Details

| Field | Value |
|---|---|
| Name | `aws-k3s-worker-1` |
| Region | Frankfurt / Europe (`<AWS_REGION>`) |
| Instance type | `t4g.micro` |
| Architecture | arm64 |
| OS | Ubuntu 24.04.4 LTS |
| Kernel | Linux 6.17.0-1012-aws |
| Virtualization | amazon |
| Hardware model | `t4g.micro` |
| Public IP | `<AWS_PUBLIC_IP>` |
| Instance ID | `<AWS_INSTANCE_ID>` |
| Storage | 20 GiB gp3 |
| Key pair | `devops-cloud-lab` |

## 🔐 Security Group

Security Group: `devops-aws-worker-ssh`

| Type | Protocol | Port | Source |
|---|---|---|---|
| SSH | TCP | 22 | `<HOME_PUBLIC_IP>/32` |

Не открывались:

- `80/TCP`
- `443/TCP`
- `6443/TCP`
- `3000/TCP`
- `9090/TCP`
- `51820/UDP`

WireGuard port `51820/UDP` будет открыт позже, когда будет готов VPN design.

## 🛠️ Baseline Packages

На VM выполнены package update / upgrade и установка базовых инструментов:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl wget git vim htop unzip jq ca-certificates gnupg lsb-release ufw net-tools
```

Пакеты нужны для дальнейших Day 6+ задач: SSH troubleshooting, automation, network checks, Ansible/Terraform preparation и будущая установка k3s.

## 🏷️ Hostname

Hostname установлен явно:

```bash
sudo hostnamectl set-hostname aws-k3s-worker-1
hostname
hostnamectl
```

Результат:

- Hostname: `aws-k3s-worker-1`

## 🔥 UFW

Внутри VM включен host firewall:

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow OpenSSH
sudo ufw enable
sudo ufw status verbose
```

Финальное состояние:

- UFW active
- Default incoming: deny
- Default outgoing: allow
- OpenSSH allowed inside VM
- External SSH access дополнительно ограничен AWS Security Group до `<HOME_PUBLIC_IP>/32`

## 💸 Why Instance Was Stopped

Instance остановлен сразу после baseline setup, чтобы не тратить бюджет во время простоя.

Важно: stopped EC2 still may have costs:

- EBS / gp3 storage
- public IPv4 allocation or related IPv4 charges
- snapshots
- other attached resources

## ✅ Cost Checklist

- [x] EC2 instance stopped after setup.
- [x] Security Group kept minimal.
- [x] Storage documented.
- [ ] Check AWS Billing.
- [ ] Check AWS Cost Explorer.
- [ ] Check AWS Budgets.
- [ ] Delete unused EBS volumes / snapshots if the node is destroyed later.
