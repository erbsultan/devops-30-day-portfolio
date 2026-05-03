# Security Hardening Notes

Day 5 security goal: оставить только минимальный SSH access и не публиковать реальные IP или cloud identifiers.

## 🔐 SSH Access Policy

| Layer | AWS | Vultr |
|---|---|---|
| External firewall | AWS Security Group | Vultr Firewall Group |
| Host firewall | UFW | UFW |
| Allowed source | `<HOME_PUBLIC_IP>/32` | `<HOME_PUBLIC_IP>/32` |
| Allowed port | `22/TCP` | `22/TCP` |

SSH доступ должен быть key-based. Password login и root login будут ужесточаться позже отдельным шагом.

## 🛡️ AWS Security Group

AWS Security Group `devops-aws-worker-ssh` работает как внешний firewall перед VM:

| Type | Protocol | Port | Source |
|---|---|---|---|
| SSH | TCP | 22 | `<HOME_PUBLIC_IP>/32` |

Это снижает exposure: даже если внутри VM есть OpenSSH rule в UFW, снаружи AWS пропустит SSH только от домашнего IP.

## 🧱 Vultr Firewall + UFW

На Vultr используется два слоя:

- Vultr Firewall Group restricts SSH to `<HOME_PUBLIC_IP>/32`.
- UFW внутри VM тоже restricts SSH to `<HOME_PUBLIC_IP>/32`.

Wide UFW rules были удалены:

- `22/tcp Anywhere`
- `OpenSSH Anywhere`
- `22/tcp Anywhere v6`
- `OpenSSH Anywhere v6`

## 👤 Why Not Work as Root Permanently

Постоянная работа под `root` увеличивает blast radius ошибки:

- случайный destructive command сразу выполняется с максимальными правами;
- сложнее разделять admin workflow и normal user workflow;
- хуже готовность к automation через Ansible;
- сложнее включать policy-driven hardening.

Поэтому на Vultr создан `devops` user с sudo.

## ✅ Why `devops` User Was Created

- Использовать non-root login для ежедневных admin tasks.
- Проверить будущую модель Ansible access.
- Оставить sudo для controlled privilege escalation.
- Подготовить будущий шаг: disable direct root SSH.

Root SSH нужно отключать позже только после повторной проверки:

- `devops` can SSH successfully.
- `devops` has sudo.
- emergency access path понятен.
- firewall rules не блокируют текущую admin workstation.

## 🚫 Closed Ports

Day 5 intentionally did not open:

| Port | Protocol | Future use | Day 5 status |
|---|---|---|---|
| 80 | TCP | ingress / demo HTTP | closed |
| 443 | TCP | ingress / demo HTTPS | closed |
| 6443 | TCP | Kubernetes API | closed |
| 3000 | TCP | app / Grafana demo | closed |
| 9090 | TCP | Prometheus | closed |
| 51820 | UDP | WireGuard | closed |

## 🔮 Reserved for Later

- `51820/UDP`: WireGuard VPN.
- `6443/TCP`: Kubernetes API, only via VPN or SSH tunnel.
- `80/TCP` and `443/TCP`: later ingress / demo exposure.
- `3000/TCP` and `9090/TCP`: only via port-forward, VPN, or restricted IP.

## ✅ Security Checklist

- [x] Public docs use placeholders.
- [x] AWS SSH source restricted to `<HOME_PUBLIC_IP>/32`.
- [x] Vultr SSH source restricted to `<HOME_PUBLIC_IP>/32`.
- [x] AWS UFW active.
- [x] Vultr UFW active.
- [x] Vultr wide SSH UFW rules removed.
- [x] `devops` user created on Vultr.
- [ ] Disable root SSH later after access is confirmed again.
- [ ] Add WireGuard only after VPN design is documented.
