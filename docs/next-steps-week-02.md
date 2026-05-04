# Next Steps — Week 2 Kubernetes / k3s

## 🎯 Week 2 Target

Week 2 moves from infrastructure foundation to Kubernetes/k3s foundation.

Planned outcomes:

- WireGuard VPN between cloud nodes.
- k3s master on Oracle.
- AWS worker joined to cluster.
- Vultr worker joined to cluster.
- Kubernetes namespaces.
- Test workload.
- Ingress controller.
- Basic monitoring preparation.

## ✅ Day 8 Completed

Day 8 completed the WireGuard multi-cloud VPN network.

VPN IP plan:

| Node | Hostname | VPN IP |
|---|---|---|
| Oracle | `oci-k3s-master` | `10.50.0.1` |
| AWS | `aws-k3s-worker-1` | `10.50.0.2` |
| Vultr | `vultr-k3s-worker-2` | `10.50.0.3` |

Security plan:

- `51820/UDP` opened only between cloud node public IPs.
- SSH restricted to `<HOME_PUBLIC_IP>/32`.
- WireGuard handshakes verified between all nodes.
- VPN ping tests passed.
- Kubernetes API is not exposed publicly.
- All nodes stopped after verification.

## ➡️ Day 9 Next

Day 9 target: install k3s server on Oracle using VPN IP `10.50.0.1`.

Command pattern to document and adapt during Day 9:

```bash
curl -sfL https://get.k3s.io | \
INSTALL_K3S_EXEC="server \
--node-name oci-k3s-master \
--node-ip 10.50.0.1 \
--advertise-address 10.50.0.1 \
--write-kubeconfig-mode 644" \
sh -
```

## 🧱 Week 2 Roadmap

| Day | Focus | Expected result |
|---|---|---|
| Day 8 | WireGuard | DONE: private network between nodes |
| Day 9 | k3s master | Oracle runs k3s server |
| Day 10 | join workers | AWS and Vultr join cluster |
| Day 11 | namespaces/test workload | cluster workload validation |
| Day 12 | ingress | ingress controller prepared |
| Day 13 | service exposure strategy | MetalLB/load balancer strategy documented |
| Day 14 | documentation | Week 2 review and cleanup |

## ✅ Checklist Before Week 2

- [ ] Confirm AWS billing.
- [ ] Confirm Oracle Cost Analysis.
- [ ] Confirm Vultr billing.
- [ ] Start nodes only while working.
- [ ] Update private inventory if public IPs changed.
- [ ] Verify SSH to all nodes.
- [ ] Back up docs through Git.
- [ ] Keep real public IPs out of public docs.
- [ ] Keep private inventory out of Git.
