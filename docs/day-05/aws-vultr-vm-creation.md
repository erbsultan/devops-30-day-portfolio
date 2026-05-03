# Day 5 — AWS + Vultr VM Creation

Day 5 расширяет lab до multi-cloud foundation: к Oracle VM добавлены AWS и Vultr worker nodes для будущего k3s кластера.

## 🎯 Цель дня

- Создать AWS EC2 instance для будущей worker-ноды.
- Создать Vultr instance для будущей worker или monitoring-ноды.
- Выполнить baseline Linux setup на обеих VM.
- Ограничить SSH доступ только с домашнего IP: `<HOME_PUBLIC_IP>/32`.
- Не открывать Kubernetes, web, monitoring и WireGuard порты раньше времени.
- Остановить все cloud nodes после настройки, чтобы контролировать бюджет.

## 🧱 Architecture Role

| Cloud | Node | Future role | Current status |
|---|---|---|---|
| Oracle Cloud | `oci-k3s-master` | future k3s master | stopped |
| AWS EC2 | `aws-k3s-worker-1` | future k3s worker #1 | stopped |
| Vultr | `vultr-k3s-worker-2` | future k3s worker #2 / monitoring | stopped |

Oracle сейчас используется не как Always Free A1, а как paid trial-credit VM:

- Shape: `VM.Standard.A2.Flex`
- OCPU: `4`
- RAM: `24 GB`
- Payment source: Oracle trial credits / Universal Credits

Это осознанное решение, чтобы пройти bootcamp быстрее и без нехватки ресурсов. Oracle Billing / Usage / Cost Analysis нужно проверять каждый день.

## 📦 Node Inventory

| Node | Cloud | Role | Hostname | Public IP | OS | Arch | Status | Notes |
|---|---|---|---|---|---|---|---|---|
| Oracle | Oracle Cloud | future k3s master | `oci-k3s-master` | `<ORACLE_PUBLIC_IP>` | Ubuntu 24.04.4 LTS | arm64 | stopped | A2 trial-credit VM |
| AWS | AWS EC2 | future k3s worker #1 | `aws-k3s-worker-1` | `<AWS_PUBLIC_IP>` | Ubuntu 24.04.4 LTS | arm64 | stopped | `t4g.micro` |
| Vultr | Vultr | future k3s worker #2 / monitoring | `vultr-k3s-worker-2` | `<VULTR_PUBLIC_IP>` | Ubuntu 24.04.4 LTS | x86-64 | stopped | `vc2-2c-4gb` |

Public IP values are placeholders in public docs. Real IPs are stored privately and are not committed.

## ☁️ AWS Setup Summary

| Field | Value |
|---|---|
| Name | `aws-k3s-worker-1` |
| Role | future k3s worker node |
| Region | Frankfurt / Europe (`<AWS_REGION>`) |
| Instance type | `t4g.micro` |
| Architecture | arm64 |
| OS | Ubuntu 24.04.4 LTS |
| Kernel | Linux 6.17.0-1012-aws |
| Virtualization | amazon |
| Hardware model | `t4g.micro` |
| Public IP | `<AWS_PUBLIC_IP>` |
| Instance ID | `<AWS_INSTANCE_ID>` |
| Key pair | `devops-cloud-lab` |
| Security Group | `devops-aws-worker-ssh` |
| Storage | 20 GiB gp3 |

AWS Security Group rule:

| Type | Protocol | Port | Source |
|---|---|---|---|
| SSH | TCP | 22 | `<HOME_PUBLIC_IP>/32` |

## 🌐 Vultr Setup Summary

| Field | Value |
|---|---|
| Name / Hostname | `vultr-k3s-worker-2` |
| Label | `vultr-k3s-worker-2` |
| Role | future k3s worker node / monitoring node |
| Region | Frankfurt, DE (`<VULTR_REGION>`) |
| Plan | Shared CPU / Cloud Compute |
| Size | `vc2-2c-4gb` |
| CPU / RAM | 2 vCPU / 4 GB RAM |
| Storage | 80 GB SSD |
| Price | $20/month |
| OS | Ubuntu 24.04.4 LTS x64 |
| Architecture | x86-64 |
| Provider model | VC2 |
| Public IP | `<VULTR_PUBLIC_IP>` |
| SSH key | `devops-cloud-lab` |
| Firewall Group | `vultr-k3s-worker-firewall` |
| Backups | disabled |
| DDoS protection | disabled |
| VPC | off |
| Cloud-init user data | off |
| Public IPv4 | enabled |

Vultr Firewall rule:

| Type | Protocol | Port | Source |
|---|---|---|---|
| SSH | TCP | 22 | `<HOME_PUBLIC_IP>/32` |

## ✅ Что было сделано

- [x] AWS EC2 worker создан.
- [x] AWS baseline packages установлены.
- [x] AWS hostname установлен в `aws-k3s-worker-1`.
- [x] AWS UFW включен: deny incoming, allow outgoing, OpenSSH allowed.
- [x] AWS Security Group ограничивает SSH снаружи до `<HOME_PUBLIC_IP>/32`.
- [x] Vultr worker создан.
- [x] Vultr baseline packages установлены.
- [x] Vultr hostname установлен в `vultr-k3s-worker-2`.
- [x] На Vultr создан non-root user `devops`.
- [x] SSH authorized keys перенесены с `root` на `devops`.
- [x] Проверен SSH вход под `devops`.
- [x] Проверено, что `devops` имеет sudo.
- [x] Vultr UFW hardened: оставлено SSH правило только для `<HOME_PUBLIC_IP>/32`.
- [x] Wide SSH rules `Anywhere` и `Anywhere v6` удалены.
- [x] Все три cloud nodes остановлены после настройки.

## 🔐 Security Notes

- SSH открыт только с `<HOME_PUBLIC_IP>/32`.
- AWS использует Security Group как внешний firewall.
- Vultr использует Vultr Firewall как внешний firewall и UFW внутри VM.
- UFW включен на AWS и Vultr.
- Постоянная работа под `root` не используется как целевой подход.
- На Vultr создан `devops` user с sudo для будущих административных задач.
- Root SSH login нужно отключать позже, только после повторной проверки `devops` access и sudo.

## 💸 Cost Notes

- Oracle VM сейчас является A2 trial-credit resource, а не Always Free A1.
- AWS EC2 instance остановлен после baseline setup.
- Vultr server остановлен / powered off после baseline setup.
- Stopped EC2 still may have EBS, public IPv4, snapshot or related costs.
- Powered-off Vultr instance can still be billed while allocated.
- Каждый день нужно проверять:
  - Oracle Billing / Usage / Cost Analysis
  - AWS Billing / Cost Explorer / Budgets
  - Vultr billing / credits

## 🚫 Что НЕ открывали

| Port | Protocol | Purpose | Status |
|---|---|---|---|
| 80 | TCP | HTTP ingress / demo | not opened |
| 443 | TCP | HTTPS ingress / demo | not opened |
| 6443 | TCP | Kubernetes API | not opened |
| 3000 | TCP | app / Grafana demo | not opened |
| 9090 | TCP | Prometheus | not opened |
| 51820 | UDP | WireGuard | reserved for later |

Kubernetes API должен быть доступен через VPN или SSH tunnel, а не публично. WireGuard port `51820/UDP` будет открыт позже, когда будет готов VPN design.

## 🧾 Final Checklist

- [x] Oracle node documented as future master.
- [x] AWS node documented as future worker #1.
- [x] Vultr node documented as future worker #2 / monitoring.
- [x] Public docs use placeholders instead of real IPs.
- [x] AWS and Vultr SSH access restricted to `<HOME_PUBLIC_IP>/32`.
- [x] No broad SSH access remains documented as final state.
- [x] Cost-control notes documented.
- [x] All nodes are stopped.

## ➡️ Next Steps для Day 6

- Подготовить Terraform skeleton для AWS, Vultr и Oracle inventory.
- Подготовить Ansible inventory и baseline playbook skeleton.
- Не хранить secrets, real IPs, tokens, account IDs или state-файлы в repo.
- Спланировать WireGuard VPN перед открытием `51820/UDP`.
- Планировать Kubernetes API access только через VPN / SSH tunnel.
