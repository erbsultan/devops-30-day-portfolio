# Day 8 — WireGuard Multi-Cloud VPN Network

Day 8 создал private VPN network между Oracle, AWS и Vultr для будущего multi-cloud k3s cluster.

## 🎯 Цель дня

- Установить WireGuard на все 3 cloud nodes.
- Настроить приватные VPN IP `10.50.0.0/24`.
- Открыть `51820/UDP` только между cloud peers.
- Оставить SSH доступ только с `<HOME_PUBLIC_IP>/32`.
- Проверить WireGuard handshakes и VPN ping между всеми nodes.
- Подготовить сеть для Day 9: k3s master на Oracle через `10.50.0.1`.

## 🧠 Почему WireGuard нужен перед k3s

k3s master/worker communication не должен идти через публичный интернет. Kubernetes API `6443` также не должен открываться публично на этом этапе.

WireGuard решает эту задачу:

- создаёт encrypted tunnel между разными cloud providers;
- даёт стабильные private VPN IP для k3s nodes;
- позволяет использовать `10.50.0.1` как private endpoint для k3s server;
- оставляет публичные firewall rules минимальными: SSH с home IP и WireGuard между peers.

## 🖥️ Node Table

| Node | Cloud | Hostname | Public IP | VPN IP | Role | Status |
|---|---|---|---|---|---|---|
| Oracle | Oracle Cloud | `oci-k3s-master` | `<ORACLE_PUBLIC_IP>` | `10.50.0.1` | future k3s master | stopped after Day 8 |
| AWS | AWS EC2 | `aws-k3s-worker-1` | `<AWS_PUBLIC_IP>` | `10.50.0.2` | future k3s worker #1 | stopped after Day 8 |
| Vultr | Vultr | `vultr-k3s-worker-2` | `<VULTR_PUBLIC_IP>` | `10.50.0.3` | future k3s worker #2 / monitoring | stopped after Day 8 |

## ☁️ Cloud Firewall Rules

| Cloud | Rule |
|---|---|
| Oracle Security List | SSH `22/tcp` from `<HOME_PUBLIC_IP>/32` |
| Oracle Security List | WireGuard `51820/udp` from `<AWS_PUBLIC_IP>/32` |
| Oracle Security List | WireGuard `51820/udp` from `<VULTR_PUBLIC_IP>/32` |
| AWS Security Group | SSH `22/tcp` from `<HOME_PUBLIC_IP>/32` |
| AWS Security Group | WireGuard `51820/udp` from `<ORACLE_PUBLIC_IP>/32` |
| AWS Security Group | WireGuard `51820/udp` from `<VULTR_PUBLIC_IP>/32` |
| Vultr Firewall | SSH `22/tcp` from `<HOME_PUBLIC_IP>/32` |
| Vultr Firewall | WireGuard `51820/udp` from `<ORACLE_PUBLIC_IP>/32` |
| Vultr Firewall | WireGuard `51820/udp` from `<AWS_PUBLIC_IP>/32` |

Vultr accidental broad SSH rule `0.0.0.0/0` was removed.

## 🧱 UFW Rules

| Node | Final UFW Rules |
|---|---|
| Oracle | `51820/udp` from `<AWS_PUBLIC_IP>`; `51820/udp` from `<VULTR_PUBLIC_IP>`; `22/tcp` from `<HOME_PUBLIC_IP>` |
| AWS | `51820/udp` from `<ORACLE_PUBLIC_IP>`; `51820/udp` from `<VULTR_PUBLIC_IP>`; `22/tcp` from `<HOME_PUBLIC_IP>` |
| Vultr | `51820/udp` from `<ORACLE_PUBLIC_IP>`; `51820/udp` from `<AWS_PUBLIC_IP>`; `22/tcp` from `<HOME_PUBLIC_IP>` |

All nodes also allow wg0 traffic:

```bash
sudo ufw allow in on wg0
sudo ufw allow out on wg0
```

UFW also generated IPv6 wg0 rules. That is acceptable. Public SSH IPv6 Anywhere rules were removed where necessary.

## 🔐 WireGuard Config Overview

Public documentation uses placeholders for WireGuard public keys. Private keys are never shown or committed.

### Oracle `/etc/wireguard/wg0.conf`

```ini
[Interface]
Address = 10.50.0.1/24
ListenPort = 51820
PrivateKey = <PRIVATE_KEY_NOT_DOCUMENTED>

[Peer]
PublicKey = <AWS_WG_PUBLIC_KEY>
AllowedIPs = 10.50.0.2/32
Endpoint = <AWS_PUBLIC_IP>:51820
PersistentKeepalive = 25

[Peer]
PublicKey = <VULTR_WG_PUBLIC_KEY>
AllowedIPs = 10.50.0.3/32
Endpoint = <VULTR_PUBLIC_IP>:51820
PersistentKeepalive = 25
```

### AWS `/etc/wireguard/wg0.conf`

```ini
[Interface]
Address = 10.50.0.2/24
ListenPort = 51820
PrivateKey = <PRIVATE_KEY_NOT_DOCUMENTED>

[Peer]
PublicKey = <OCI_WG_PUBLIC_KEY>
AllowedIPs = 10.50.0.1/32
Endpoint = <ORACLE_PUBLIC_IP>:51820
PersistentKeepalive = 25

[Peer]
PublicKey = <VULTR_WG_PUBLIC_KEY>
AllowedIPs = 10.50.0.3/32
Endpoint = <VULTR_PUBLIC_IP>:51820
PersistentKeepalive = 25
```

### Vultr `/etc/wireguard/wg0.conf`

```ini
[Interface]
Address = 10.50.0.3/24
ListenPort = 51820
PrivateKey = <PRIVATE_KEY_NOT_DOCUMENTED>

[Peer]
PublicKey = <OCI_WG_PUBLIC_KEY>
AllowedIPs = 10.50.0.1/32
Endpoint = <ORACLE_PUBLIC_IP>:51820
PersistentKeepalive = 25

[Peer]
PublicKey = <AWS_WG_PUBLIC_KEY>
AllowedIPs = 10.50.0.2/32
Endpoint = <AWS_PUBLIC_IP>:51820
PersistentKeepalive = 25
```

## ✅ Verification Commands

```bash
sudo systemctl status wg-quick@wg0 --no-pager
sudo wg show
ip addr show wg0
ping -c 4 10.50.0.1
ping -c 4 10.50.0.2
ping -c 4 10.50.0.3
```

## 📊 Successful Results Summary

- Oracle showed handshakes with AWS and Vultr.
- AWS showed handshakes with Oracle and Vultr.
- Vultr showed handshakes with Oracle and AWS.
- Vultr → Oracle `10.50.0.1`: `0% packet loss`.
- Vultr → AWS `10.50.0.2`: `0% packet loss`.
- AWS → Oracle `10.50.0.1`: `0% packet loss`.
- AWS → Vultr `10.50.0.3`: `0% packet loss`.

## 🛠️ Troubleshooting Notes

- Oracle UFW SSH rule was accidentally deleted while removing broad OpenSSH access. It was re-added with `<HOME_PUBLIC_IP>/32`, and SSH was verified from a new terminal.
- AWS UFW commands were initially run on the Oracle prompt. The prompt mismatch was detected and commands were re-run on `ubuntu@aws-k3s-worker-1`.
- Vultr `wg-quick@wg0` failed at first because of a config/key issue, most likely a missing trailing `=` in an AWS public key. After editing the config, the service started successfully.

## 🔐 Security Notes

- Real public IPs are not committed.
- WireGuard private keys are never committed.
- Real WireGuard public keys are not published in portfolio docs; placeholders are used.
- SSH is restricted to `<HOME_PUBLIC_IP>/32`.
- WireGuard `51820/udp` is restricted to peer public IPs.
- Kubernetes API `6443` was not opened publicly.
- Grafana, Prometheus, HTTP and HTTPS were not opened.
- Cloud firewall plus UFW gives layered security.

## 💸 Cost Notes

All three cloud servers were stopped after verification to control idle compute cost.

## ✅ Final Checklist

- [x] WireGuard installed on Oracle, AWS and Vultr.
- [x] Keys generated on all nodes.
- [x] Private keys kept out of documentation and Git.
- [x] Cloud firewall rules restricted.
- [x] UFW rules hardened.
- [x] `wg0` enabled and started.
- [x] Handshakes verified on all nodes.
- [x] VPN ping tests passed.
- [x] Nodes stopped after Day 8.

## ➡️ Next Step

Day 9 — install k3s master on Oracle using VPN IP `10.50.0.1`.
