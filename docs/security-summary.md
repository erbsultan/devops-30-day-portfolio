# Security Summary

## 🔐 MFA

| Area | Status |
|---|---|
| AWS root user MFA | enabled |
| AWS IAM user MFA | enabled |
| Vultr MFA | enabled |
| Oracle security | checked and hardened for SSH |

## 🔑 SSH

- Dedicated SSH key: `devops_cloud_lab`.
- No private keys committed.
- SSH restricted to `<HOME_PUBLIC_IP>/32` where possible.
- Public-anywhere SSH exposure removed where it appeared.

## ☁️ Cloud Firewall Rules

| Provider | Control | Current SSH rule |
|---|---|---|
| Oracle Cloud | Security List | TCP 22 from `<HOME_PUBLIC_IP>/32` |
| AWS | Security Group | TCP 22 from `<HOME_PUBLIC_IP>/32` |
| Vultr | Vultr Firewall + UFW | TCP 22 from `<HOME_PUBLIC_IP>/32` |

## 👤 Vultr User Hardening

- Initial root login used only for setup.
- `devops` user created.
- `devops` added to sudo.
- SSH authorized keys copied.
- `devops` SSH tested.
- No permanent root workflow planned.

## 🧾 Secrets and Private Files

Ignored or kept private:

- `.env`
- `infra/ansible/inventory/hosts.ini`
- `terraform.tfstate`
- private SSH keys

Public docs use placeholders:

- `<ORACLE_PUBLIC_IP>`
- `<AWS_PUBLIC_IP>`
- `<VULTR_PUBLIC_IP>`
- `<HOME_PUBLIC_IP>/32`
- `<AWS_INSTANCE_ID>`
- `<ORACLE_REGION>`
- `<AWS_REGION>`
- `<VULTR_REGION>`

## 🚪 Ports Not Opened Yet

These ports are not opened publicly in Week 1:

| Port | Purpose | Week 1 status |
|---:|---|---|
| 80 | HTTP | not opened |
| 443 | HTTPS | not opened |
| 6443 | Kubernetes API | not opened |
| 3000 | Grafana / apps | not opened |
| 9090 | Prometheus | not opened |
| 51820 | WireGuard | not opened |

## 🔮 Week 2 Future Ports

- `51820/UDP` for WireGuard between cloud nodes only.
- `6443` Kubernetes API via VPN or SSH tunnel only.
- No public Kubernetes API exposure.
