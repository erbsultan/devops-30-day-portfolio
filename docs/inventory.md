# Cloud Node Inventory

Public inventory for the DevOps 30-Day multi-cloud lab.

| Node | Cloud | Role | Hostname | Public IP | VPN IP | OS | Arch | Status | Notes |
|---|---|---|---|---|---|---|---|---|---|
| Oracle | Oracle Cloud | future k3s master | oci-k3s-master | `<ORACLE_PUBLIC_IP>` | `10.50.0.1` | Ubuntu 24.04.4 LTS | arm64 | stopped after Day 8 | A2 trial-credit VM |
| AWS | AWS EC2 | future k3s worker #1 | aws-k3s-worker-1 | `<AWS_PUBLIC_IP>` | `10.50.0.2` | Ubuntu 24.04.4 LTS | arm64 | stopped after Day 8 | t4g.micro |
| Vultr | Vultr | future k3s worker #2 / monitoring | vultr-k3s-worker-2 | `<VULTR_PUBLIC_IP>` | `10.50.0.3` | Ubuntu 24.04.4 LTS | x86-64 | stopped after Day 8 | vc2-2c-4gb |

## Notes

- Public IP values are placeholders in public docs.
- Real IPs are stored privately and not committed.
- IPs may change after start / stop.
- Oracle is currently an A2 trial-credit VM, not an Always Free A1 VM.
- WireGuard VPN IPs were configured on Day 8.
- All nodes are stopped after Day 8 WireGuard verification to reduce idle compute cost.
