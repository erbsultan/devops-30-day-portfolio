# Cost Notes

## 💸 Budget Overview

Week 1 prioritized cost control before and after creating cloud resources.

Current policy:

- Start nodes only while actively working.
- Stop nodes after verification.
- Check cloud billing dashboards daily.
- Avoid managed services unless intentionally planned.

## ☁️ AWS

- AWS account is paid / no Free Tier by design.
- AWS Budget: `$30`.
- AWS early-warning budget: `$1`.
- Budget alerts configured.
- EC2 worker stopped after setup.
- Continue monitoring:
  - EBS volumes;
  - public IPv4 charges;
  - snapshots;
  - data transfer;
  - future load balancers.

## ☁️ Vultr

- Vultr credit exists.
- VM upgraded to `vc2-2c-4gb`, around `$20/month`.
- Backups disabled.
- VM powered off after setup.
- Important: allocated VM can still bill while not destroyed.

## ☁️ Oracle

- Oracle node uses A2 paid trial-credit VM, not Always Free A1.
- Shape: `VM.Standard.A2.Flex`.
- Payment source: Oracle trial credits / Universal Credits.
- Check Oracle Cost Analysis daily.

## 🧾 Hidden Costs Checklist

- [ ] Public IPv4.
- [ ] Boot volumes.
- [ ] Block volumes.
- [ ] Snapshots.
- [ ] Backups.
- [ ] Load balancers.
- [ ] NAT gateway.
- [ ] Managed Kubernetes.
- [ ] Data transfer.
- [ ] Trial-credit expiration.

## 🧹 End-of-Trial Cleanup Plan

- Export or keep important docs in GitHub.
- Stop all nodes before trial end.
- Destroy cloud resources that are no longer needed.
- Remove snapshots/backups if not needed.
- Release reserved/static public IPs if used.
- Confirm final billing dashboards show no unexpected active resources.
