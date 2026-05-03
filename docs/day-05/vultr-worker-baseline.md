# Vultr Worker Baseline

Vultr instance `vultr-k3s-worker-2` подготовлен как future k3s worker #2 или monitoring node.

## 🎯 Назначение

- Cloud: Vultr
- Role: future k3s worker node / monitoring node
- Future cluster role: worker #2 or monitoring
- Current status: stopped / powered off

## 📦 Instance Details

| Field | Value |
|---|---|
| Name / Hostname | `vultr-k3s-worker-2` |
| Label | `vultr-k3s-worker-2` |
| Region | Frankfurt, DE (`<VULTR_REGION>`) |
| Plan | Shared CPU / Cloud Compute |
| Size | `vc2-2c-4gb` |
| CPU / RAM | 2 vCPU / 4 GB RAM |
| Storage | 80 GB SSD |
| Price | $20/month |
| OS | Ubuntu 24.04.4 LTS x64 |
| Architecture | x86-64 |
| Provider | Vultr |
| Model | VC2 |
| Public IP | `<VULTR_PUBLIC_IP>` |
| SSH key | `devops-cloud-lab` |
| Firewall Group | `vultr-k3s-worker-firewall` |
| Backups | disabled |
| DDoS protection | disabled |
| VPC | off |
| Cloud-init user data | off |
| Public IPv4 | enabled |

## 🔐 Vultr Firewall

Firewall Group: `vultr-k3s-worker-firewall`

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

WireGuard `51820/UDP` будет открыт позже.

## 🛠️ Initial Root Login

Fresh VM сначала была доступна через `root`:

```bash
ssh -i ~/.ssh/devops_cloud_lab root@<VULTR_PUBLIC_IP>
```

Во время `apt upgrade` были package prompts:

- PAM config: выбран maintainer version.
- `sshd_config`: оставлена current local version, чтобы не сломать SSH access.

## 🧰 Baseline Setup

```bash
cloud-init status

apt update && apt upgrade -y
apt install -y curl wget git vim htop unzip jq ca-certificates gnupg lsb-release ufw net-tools

hostnamectl set-hostname vultr-k3s-worker-2
hostname
hostnamectl
```

Результат:

- Hostname: `vultr-k3s-worker-2`
- OS: Ubuntu 24.04.4 LTS x64

## 👤 Devops User Creation

Чтобы не работать постоянно под `root`, создан отдельный user:

```bash
adduser devops
usermod -aG sudo devops
```

SSH authorized keys скопированы из `root`:

```bash
mkdir -p /home/devops/.ssh
cp /root/.ssh/authorized_keys /home/devops/.ssh/authorized_keys
chown -R devops:devops /home/devops/.ssh
chmod 700 /home/devops/.ssh
chmod 600 /home/devops/.ssh/authorized_keys
```

Проверен вход:

```bash
ssh -i ~/.ssh/devops_cloud_lab devops@<VULTR_PUBLIC_IP>
whoami
```

Результат:

```text
devops
```

`devops` использовал sudo, значит sudo доступ работает.

## 🔥 UFW Hardening

Изначально в UFW были широкие SSH rules:

- `22/tcp Anywhere`
- `OpenSSH Anywhere`
- `22/tcp Anywhere v6`
- `OpenSSH Anywhere v6`

Определили текущий SSH client IP и добавили точное правило:

```bash
CLIENT_IP=$(echo "$SSH_CLIENT" | awk '{print $1}')
echo "$CLIENT_IP"

sudo ufw allow from "$CLIENT_IP"/32 to any port 22 proto tcp
sudo ufw status numbered
```

Потом широкие правила удалены с конца списка:

```bash
sudo ufw delete 5
sudo ufw delete 4
sudo ufw delete 2
sudo ufw delete 1
sudo ufw status numbered
```

Финальное состояние:

- UFW active
- SSH разрешен только с `<HOME_PUBLIC_IP>/32`
- Wide `Anywhere` rules удалены

## 💸 Why Server Was Stopped

Vultr server выключен после настройки, чтобы снизить риск лишних расходов во время простоя.

Важно: powered-off Vultr instance can still be billed while allocated. Нужно проверять:

- Vultr billing
- credits
- allocated VM charges
- snapshots / backups

## ✅ Final Checklist

- [x] VM created.
- [x] Backups disabled.
- [x] DDoS protection disabled.
- [x] Firewall Group configured.
- [x] Baseline packages installed.
- [x] Hostname configured.
- [x] `devops` user created.
- [x] `devops` sudo access verified.
- [x] SSH access hardened.
- [x] UFW active.
- [x] Server stopped / powered off after setup.
