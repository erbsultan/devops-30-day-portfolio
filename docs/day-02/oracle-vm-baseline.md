# Day 2 — Oracle VM Baseline 🚀

## 🎯 Цель дня

Подготовить Oracle Cloud VM как базовый сервер для дальнейшей DevOps-лабы и будущего `k3s` master node.

Основной фокус Day 2:

- [x] создать Oracle VM;
- [x] настроить безопасный SSH-доступ;
- [x] выполнить базовую настройку Ubuntu;
- [x] включить host firewall через UFW;
- [x] зафиксировать архитектурные, security и cost decisions в документации.

## 🧱 Итоговая архитектурная роль сервера

Сервер `oci-k3s-master` будет использоваться как будущий control-plane node для lightweight Kubernetes-кластера на базе `k3s`.

| Параметр | Значение |
|---|---|
| Role | Future `k3s` master node |
| Access model | SSH only from trusted home public IP |
| Public exposure | Minimal, only TCP 22 at Day 2 |
| Host firewall | UFW enabled |
| Cloud firewall | Oracle Security List |
| Cost model | Paid trial-credit resource |

## 🖥️ VM Details

| Поле | Значение |
|---|---|
| Cloud | Oracle Cloud Infrastructure |
| Region | Germany Central / Frankfurt |
| Instance name | `oci-k3s-master` |
| Shape | `VM.Standard.A2.Flex` |
| OCPU | `4` |
| RAM | `24 GB` |
| OS | Ubuntu `24.04.4 LTS` |
| Architecture | `arm64` |
| Kernel | Linux `6.17.0-1010-oracle` |
| Username | `ubuntu` |
| Hostname | `oci-k3s-master` |
| Public IP | `<ORACLE_PUBLIC_IP>` |
| Payment source | Oracle trial credits / Universal Credits |
| Free tier status | Not Always Free A1 |

## 🌐 Network / Security Settings

| Setting | Value |
|---|---|
| Compartment | `<ORACLE_COMPARTMENT>` |
| VCN | `<VCN_NAME>` |
| Subnet | `<SUBNET_NAME>` |
| Subnet type | Public subnet |
| SSH ingress | `<HOME_PUBLIC_IP>/32 → TCP 22` |
| Removed SSH ingress | `0.0.0.0/0 → TCP 22` |
| ICMP default rules | Kept |
| HTTP / HTTPS | Not opened |
| Kubernetes API | Not opened |
| Monitoring ports | Not opened |
| VPN ports | Not opened |

## ✅ Что сделали пошагово

1. Создали Oracle Cloud VM в регионе Frankfurt.
2. Выбрали shape `VM.Standard.A2.Flex` с `4 OCPU` и `24 GB RAM`.
3. Установили Ubuntu `24.04.4 LTS` для `arm64`.
4. Определили роль сервера как future `k3s` master node.
5. Нашли Security List через Oracle Console:

```text
Instance
→ Networking
→ Primary VNIC
→ Subnet
→ Security
→ Security Lists
→ Default Security List
→ Security rules
```

6. Добавили узкое SSH-правило:

```text
<HOME_PUBLIC_IP>/32 → TCP 22
```

7. Удалили широкое SSH-правило:

```text
0.0.0.0/0 → TCP 22
```

8. Проверили SSH-подключение к серверу.
9. Обновили систему и установили базовые пакеты.
10. Настроили hostname `oci-k3s-master`.
11. Включили UFW с политикой deny incoming / allow outgoing.

## 🧰 Команды

### SSH connection

```bash
ssh -i ~/.ssh/devops_cloud_lab ubuntu@<ORACLE_PUBLIC_IP>
```

### System update

```bash
sudo apt update && sudo apt upgrade -y
```

### Base packages

```bash
sudo apt install -y \
  curl \
  wget \
  git \
  vim \
  htop \
  unzip \
  jq \
  ca-certificates \
  gnupg \
  lsb-release \
  ufw \
  net-tools
```

### Hostname

```bash
sudo hostnamectl set-hostname oci-k3s-master
hostname
hostnamectl
```

### UFW baseline

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow OpenSSH
sudo ufw enable
sudo ufw status verbose
```

## 🔍 Проверки

### Hostname check

```text
Static hostname: oci-k3s-master
Operating System: Ubuntu 24.04.4 LTS
Architecture: arm64
Virtualization: kvm
```

### UFW check

```text
Status: active
Logging: on (low)
Default: deny incoming, allow outgoing, disabled routed
OpenSSH: allowed
```

### SSH check

```bash
ssh -i ~/.ssh/devops_cloud_lab ubuntu@<ORACLE_PUBLIC_IP>
```

Expected result:

```text
Successful SSH login as ubuntu
```

## 🔐 Security notes

- SSH открыт только с текущего домашнего public IP: `<HOME_PUBLIC_IP>/32`.
- Широкий доступ `0.0.0.0/0 → TCP 22` удалён.
- UFW показывает `OpenSSH` as allowed from `Anywhere`, но внешний доступ дополнительно ограничен Oracle Security List.
- Oracle Security List работает как cloud-level firewall.
- UFW работает как host-level firewall внутри Ubuntu.
- Реальные public IP, OCID, email, address, payment details и subscription ID не должны попадать в публичный репозиторий.

## 💰 Cost notes

| Item | Note |
|---|---|
| Shape | `VM.Standard.A2.Flex` |
| Billing type | Paid trial-credit resource |
| Always Free | No |
| Decision | Остаёмся на A2, потому что цель — пройти bootcamp за месяц |
| Daily action | Проверять Billing / Usage / Cost Analysis каждый день |

Важно: это не Always Free A1 instance. Ресурс использует Oracle trial credits / Universal Credits.

## 🚫 Что НЕ открывали

| Port | Protocol | Purpose | Status |
|---:|---|---|---|
| `80` | TCP | Web / demo HTTP | Not opened |
| `443` | TCP | Web / demo HTTPS | Not opened |
| `3000` | TCP | App demo / Grafana-like local testing | Not opened |
| `6443` | TCP | Kubernetes API | Not opened |
| `9090` | TCP | Prometheus | Not opened |
| `51820` | UDP | WireGuard VPN | Not opened |

## 🧯 Troubleshooting notes

| Симптом | Что проверить |
|---|---|
| SSH timeout | Security List содержит `<HOME_PUBLIC_IP>/32 → TCP 22` |
| SSH permission denied | Используется правильный ключ `~/.ssh/devops_cloud_lab` |
| SSH не работает после смены IP | Обновить source CIDR в Oracle Security List |
| UFW active, но SSH недоступен | Проверить `sudo ufw status verbose` и cloud firewall |
| Hostname не изменился | Выполнить `hostnamectl` и открыть новую SSH-сессию |
| Неожиданные расходы | Проверить active resources, boot volumes, public IP и Cost Analysis |

## 🧭 Next steps

- [ ] Day 3: подготовить Git/GitHub workflow и IaC структуру.
- [ ] Позже установить Docker и Docker Compose.
- [ ] Позже установить `k3s` на `oci-k3s-master`.
- [ ] Открывать новые порты только под конкретную задачу.
- [ ] Для Kubernetes API использовать VPN или SSH tunnel, а не public access.
- [ ] Каждый день проверять Oracle Billing / Usage / Cost Analysis.

## ✅ Финальный checklist

- [x] Oracle VM создана.
- [x] Shape и billing model осознанно выбраны.
- [x] SSH key-based access проверен.
- [x] Public SSH ограничен до `<HOME_PUBLIC_IP>/32`.
- [x] Правило `0.0.0.0/0 → TCP 22` удалено.
- [x] Base packages установлены.
- [x] Hostname настроен.
- [x] UFW включён.
- [x] Реальные sensitive values не задокументированы.
- [x] Next steps зафиксированы.
