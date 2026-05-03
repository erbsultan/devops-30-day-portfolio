# Day 5 Commands — AWS + Vultr VM Creation

Команды сохранены для audit trail и будущего повторения. Public IP values intentionally use placeholders.

## ☁️ AWS SSH

```bash
ssh -i ~/.ssh/devops_cloud_lab ubuntu@<AWS_PUBLIC_IP>
```

## ☁️ AWS Baseline

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl wget git vim htop unzip jq ca-certificates gnupg lsb-release ufw net-tools
```

## 🏷️ AWS Hostname

```bash
sudo hostnamectl set-hostname aws-k3s-worker-1
hostname
hostnamectl
```

## 🔥 AWS UFW

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow OpenSSH
sudo ufw enable
sudo ufw status verbose
```

## 🌐 Vultr Root SSH

```bash
ssh -i ~/.ssh/devops_cloud_lab root@<VULTR_PUBLIC_IP>
```

## 🌐 Vultr Cloud-init Check

```bash
cloud-init status
```

## 🌐 Vultr Apt Upgrade

```bash
apt update && apt upgrade -y
apt install -y curl wget git vim htop unzip jq ca-certificates gnupg lsb-release ufw net-tools
```

During `apt upgrade`:

- PAM config: selected package maintainer version.
- `sshd_config`: kept the local version currently installed.

## 🏷️ Vultr Hostname

```bash
hostnamectl set-hostname vultr-k3s-worker-2
hostname
hostnamectl
```

## 👤 Vultr Devops User Creation

```bash
adduser devops
usermod -aG sudo devops
```

## 🔑 Copy Authorized Keys

```bash
mkdir -p /home/devops/.ssh
cp /root/.ssh/authorized_keys /home/devops/.ssh/authorized_keys
chown -R devops:devops /home/devops/.ssh
chmod 700 /home/devops/.ssh
chmod 600 /home/devops/.ssh/authorized_keys
```

## 👤 SSH as Devops

```bash
ssh -i ~/.ssh/devops_cloud_lab devops@<VULTR_PUBLIC_IP>
whoami
```

Expected result:

```text
devops
```

## 🔎 Detect Current SSH Client IP

```bash
CLIENT_IP=$(echo "$SSH_CLIENT" | awk '{print $1}')
echo "$CLIENT_IP"
```

In public docs this value must be represented as:

```text
<HOME_PUBLIC_IP>/32
```

## 🔥 UFW Allow Exact IP

```bash
sudo ufw allow from "$CLIENT_IP"/32 to any port 22 proto tcp
sudo ufw status numbered
```

## 🧹 UFW Delete Broad Rules

Rules were deleted from the end of the numbered list to avoid index shifting:

```bash
sudo ufw delete 5
sudo ufw delete 4
sudo ufw delete 2
sudo ufw delete 1
sudo ufw status numbered
```

## ✅ Final Checks

```bash
hostname
hostnamectl
sudo ufw status verbose
whoami
sudo -v
```

Expected final state:

- AWS hostname: `aws-k3s-worker-1`
- Vultr hostname: `vultr-k3s-worker-2`
- AWS UFW: active
- Vultr UFW: active
- SSH source: `<HOME_PUBLIC_IP>/32`
- AWS instance: stopped
- Vultr server: stopped / powered off
