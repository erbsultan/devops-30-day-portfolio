# Cost Control Notes

Day 5 добавил новые cloud resources, поэтому контроль расходов стал отдельной ежедневной задачей.

## 💸 Current Resource Model

| Cloud | Resource | Status | Cost note |
|---|---|---|---|
| Oracle Cloud | `oci-k3s-master` | stopped | A2 trial-credit VM, not Always Free A1 |
| AWS EC2 | `aws-k3s-worker-1` | stopped | compute stopped, storage / IPv4 may still cost money |
| Vultr | `vultr-k3s-worker-2` | stopped / powered off | allocated VM can still be billed |

## ⚠️ Oracle A2 Trial Credits

В исходном плане Oracle был Always Free A1. Фактически сейчас используется:

- Shape: `VM.Standard.A2.Flex`
- OCPU: `4`
- RAM: `24 GB`
- Payment source: Oracle trial credits / Universal Credits

Это осознанное решение для скорости bootcamp, но оно требует ежедневной проверки Oracle Billing / Usage / Cost Analysis.

## ☁️ AWS Cost Notes

AWS EC2 was stopped after setup, but stopped resources can still create charges:

- EBS / gp3 volume
- public IPv4
- snapshots
- elastic IP or related networking resources if added later
- CloudWatch logs / metrics if enabled later

Check daily:

- AWS Billing
- AWS Cost Explorer
- AWS Budgets

## 🌐 Vultr Cost Notes

Vultr server was stopped / powered off after setup, but allocated instances can still be billed.

Check daily:

- Vultr billing
- remaining credits
- allocated VM cost
- snapshots
- backups

Backups were disabled on Day 5, but this should be rechecked after future changes.

## 🧾 Hidden Costs Checklist

- [ ] AWS EBS volumes
- [ ] AWS public IPv4
- [ ] AWS snapshots
- [ ] Vultr allocated VM
- [ ] Vultr snapshots
- [ ] Vultr backups
- [ ] Oracle boot volume
- [ ] Oracle block volumes
- [ ] Oracle snapshots / backups
- [ ] Any idle load balancers or reserved IPs added later

## 📅 Daily Cost Check

Каждый день bootcamp:

- [ ] Open Oracle Billing / Usage / Cost Analysis.
- [ ] Confirm Oracle trial credits remaining.
- [ ] Open AWS Billing / Cost Explorer.
- [ ] Confirm AWS EC2 compute is stopped when not needed.
- [ ] Check AWS EBS / public IPv4 / snapshots.
- [ ] Open Vultr billing / credits.
- [ ] Confirm Vultr server state and allocated charges.
- [ ] Update inventory if any resource was started, stopped, destroyed, or recreated.

## 🧹 End-of-Trial Cleanup Plan

Before trial credits end or if bootcamp pauses:

- [ ] Terminate / destroy unneeded resources.
- [ ] Delete boot volumes if not needed.
- [ ] Delete unattached block volumes.
- [ ] Delete snapshots and backups.
- [ ] Release unused public IPv4 / reserved IP resources.
- [ ] Confirm no load balancers or managed services are left running.
- [ ] Update `docs/inventory.md`.
- [ ] Keep only resources that have a clear purpose and known cost.
