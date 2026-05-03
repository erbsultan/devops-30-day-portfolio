# DevOps 30-Day Portfolio

30-day DevOps portfolio project focused on building a practical, production-like DevOps lab from scratch.

The project documents daily infrastructure work, operational decisions, security tradeoffs, troubleshooting, and verification steps. It is designed to be readable as a portfolio for resume, GitHub, and freelance work.

## 🎯 Project Overview

The lab starts with account safety, billing controls, SSH hardening, Linux baseline setup, Docker fundamentals, and Docker Compose. It then moves toward a multi-cloud Kubernetes/k3s environment managed with Terraform and Ansible.

Current cloud layout:

- Oracle Cloud: future k3s master node.
- AWS EC2: future k3s worker #1.
- Vultr: future k3s worker #2 / monitoring node.
- macOS workstation: Git, SSH, Terraform, Ansible, documentation, and portfolio work.

## ✅ Current Status

Week 1 is completed.

Week 1 result:

- Multi-cloud account, billing, and security baseline completed.
- GitHub portfolio repository created and documented.
- Oracle VM baseline completed.
- Docker basics completed.
- Docker Compose stack completed.
- AWS and Vultr worker nodes created and hardened.
- Terraform and Ansible skeleton created.
- Ansible ping across all 3 cloud nodes completed successfully.
- All cloud nodes stopped after verification.

## 🧭 Architecture Summary

The current architecture is a secured multi-cloud lab foundation. Kubernetes is not installed yet.

| Node | Cloud | Role | Public IP | Status |
|---|---|---|---|---|
| `oci-k3s-master` | Oracle Cloud | future k3s master | `<ORACLE_PUBLIC_IP>` | stopped |
| `aws-k3s-worker-1` | AWS EC2 | future k3s worker #1 | `<AWS_PUBLIC_IP>` | stopped |
| `vultr-k3s-worker-2` | Vultr | future k3s worker #2 / monitoring | `<VULTR_PUBLIC_IP>` | stopped |

Week 2 will add WireGuard and k3s.

## 📈 Progress

### Day 1 — Accounts, Billing Safety, Git Foundation

- Vultr account, billing, credit, notifications, and MFA checked.
- AWS account checked and budget alerts configured.
- AWS root and IAM MFA enabled.
- GitHub SSH verified.
- Portfolio repository created and pushed.

### Day 2 — Oracle VM Baseline

- Oracle VM created as `oci-k3s-master`.
- Actual shape: `VM.Standard.A2.Flex`, using trial credits.
- Ubuntu 24.04.4 LTS arm64 baseline configured.
- SSH restricted to `<HOME_PUBLIC_IP>/32`.
- Base packages, UFW, hostname, and SSH verified.

### Day 3 — Docker Basics on Oracle VM

- Docker Engine installed.
- Docker Compose plugin installed.
- Python Docker demo app created.
- Image `day3-python-app:v1` built and tested.
- Docker troubleshooting documented.

### Day 4 — Docker Compose Stack

- `apps/compose-api-stack` created.
- Flask API, PostgreSQL, and Redis composed.
- Healthchecks configured.
- Example environment file created and private environment file kept out of Git.
- API bound to localhost only.
- PostgreSQL and Redis not exposed publicly.

### Day 5 — AWS + Vultr VM Creation

- AWS EC2 worker `aws-k3s-worker-1` created.
- Vultr worker `vultr-k3s-worker-2` created.
- Vultr `devops` sudo user created and tested.
- SSH hardened with provider firewalls and UFW.
- All 3 nodes stopped after setup.

### Day 6 — Terraform + Ansible Skeleton

- Terraform installed locally: `v1.15.1`.
- Ansible installed locally: `core 2.20.5`.
- Terraform skeleton created under `infra/terraform/`.
- Ansible skeleton created under `infra/ansible/`.
- Private inventory ignored by Git.
- Ansible inventory validated.
- Ansible ping completed successfully: 3/3 nodes returned `pong`.
- All 3 nodes stopped after verification.

### Day 7 — Week 1 Review + Documentation

- Week 1 reviewed and summarized.
- Architecture, security, cost, and Week 2 preparation docs created.
- Public documentation checked for placeholders and sensitive data hygiene.
- Portfolio docs prepared for Week 2 Kubernetes/k3s work.

## 📚 Documentation

- [Documentation index](docs/index.md)
- [Week 1 Review](docs/week-01-review.md)
- [Architecture](docs/architecture.md)
- [Cloud Node Inventory](docs/inventory.md)
- [Security Summary](docs/security-summary.md)
- [Cost Notes](docs/cost-notes.md)
- [Next Steps: Week 2](docs/next-steps-week-02.md)
- [Day 7 Documentation](docs/day-07/week-01-documentation.md)

Daily docs:

- [Day 1 — Accounts, Billing Safety, Git Foundation](docs/day-01/accounts-billing-git-foundation.md)
- [Day 2 — Oracle VM Baseline](docs/day-02/oracle-vm-baseline.md)
- [Day 3 — Docker Basics on Oracle VM](docs/day-03/docker-basics-on-oracle.md)
- [Day 4 — Docker Compose Stack](docs/day-04/docker-compose-stack.md)
- [Day 5 — AWS + Vultr VM Creation](docs/day-05/aws-vultr-vm-creation.md)
- [Day 6 — Terraform + Ansible Skeleton](docs/day-06/terraform-ansible-skeleton.md)
- [Day 6 — Ansible Ping Results](docs/day-06/ansible-ping-results.md)

## 🔐 Public Documentation Rules

- Real public IPs are not committed.
- Private inventory is not committed.
- Sensitive credentials and cloud account identifiers are not committed.
- Public docs use placeholders such as `<ORACLE_PUBLIC_IP>`, `<AWS_PUBLIC_IP>`, `<VULTR_PUBLIC_IP>`, and `<HOME_PUBLIC_IP>/32`.
