# Day 8 — WireGuard Security Notes

## 🔐 Secrets Hygiene

- Never commit WireGuard private keys.
- Never commit `/etc/wireguard/wg0.conf` from a real server.
- Never commit private SSH keys.
- Public docs must use placeholders instead of real public IPs and real WireGuard public keys.
- Public WireGuard key placeholders:
  - `<OCI_WG_PUBLIC_KEY>`
  - `<AWS_WG_PUBLIC_KEY>`
  - `<VULTR_WG_PUBLIC_KEY>`

## 🌐 Network Exposure

Only the minimum public access was allowed:

| Access | Rule |
|---|---|
| SSH | `22/tcp` only from `<HOME_PUBLIC_IP>/32` |
| WireGuard | `51820/udp` only between cloud node public IPs |
| Kubernetes API | not opened publicly |
| Grafana / Prometheus | not opened |
| HTTP / HTTPS | not opened yet |

## 🧱 Layered Security

Day 8 uses two firewall layers:

1. Cloud firewall / security list / security group.
2. Host firewall with UFW.

This means a packet must pass both the cloud provider firewall and the local Linux firewall before reaching WireGuard.

## ☸️ Kubernetes Security Direction

Day 9 should install k3s server on Oracle using VPN IP `10.50.0.1`.

Expected k3s direction:

- `--node-ip 10.50.0.1`
- `--advertise-address 10.50.0.1`
- no public `6443/tcp` exposure
- worker nodes join over VPN IPs
- monitoring should use `kubectl port-forward`, SSH tunnel, VPN-only access, or tightly restricted firewall rules

## ✅ Public Docs Checklist

- [x] Real public IPs replaced with placeholders.
- [x] Private keys omitted.
- [x] Real WireGuard public keys replaced with placeholders.
- [x] No `.env` files committed.
- [x] No kubeconfig committed.
- [x] No `terraform.tfstate` committed.
- [x] No private Ansible inventory committed.
