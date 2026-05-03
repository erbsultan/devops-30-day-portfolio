# DevOps 30-Day Portfolio

30-day DevOps portfolio project focused on building a practical, production-like DevOps lab from scratch.

The project documents daily infrastructure work, operational decisions, security tradeoffs, and verification steps. It is designed to be readable as a portfolio for resume, GitHub, and freelance work.

## Focus Areas

- Docker and Docker Compose
- Kubernetes / k3s
- CI/CD pipelines
- Terraform and Ansible
- Monitoring with Prometheus, Grafana, Loki
- Multi-cloud infrastructure: Oracle Cloud, AWS, Vultr

## Goal

Build a strong DevOps portfolio for resume, GitHub, and Upwork.

## Current Lab Direction

The first stage prepares a cloud VM that will later become a lightweight Kubernetes environment. Early days focus on account safety, cost awareness, SSH hardening, baseline Linux setup, Docker fundamentals, and multi-container application stacks.

## Progress

### Day 1 — Accounts, Billing Safety, Git Foundation

- Done

### Day 2 — Oracle VM Baseline

- Oracle VM created
- Security List hardened for SSH
- SSH connection tested
- Base packages installed
- Hostname configured
- UFW enabled

### Day 3 — Docker Basics on Oracle VM

- Docker Engine installed
- Docker Compose plugin installed
- Docker group configured
- Nginx test container launched
- Python Docker demo app built and tested
- Docker troubleshooting documented

### Day 4 — Docker Compose Stack

- Multi-container stack created
- Flask API containerized
- PostgreSQL service added
- Redis service added
- Healthchecks configured
- Port binding hardened to localhost
- Compose troubleshooting documented

## Documentation

- [Documentation index](docs/index.md)
- [Progress tracker](docs/progress.md)
- [Day 1 — Accounts, Billing Safety, Git Foundation](docs/day-01/accounts-billing-git-foundation.md)
- [Day 2 — Oracle VM Baseline](docs/day-02/oracle-vm-baseline.md)
- [Day 2 — Security List SSH Hardening](docs/day-02/security-list-ssh-hardening.md)
- [Day 2 — Oracle Cost Monitoring](docs/day-02/oracle-cost-monitoring.md)
- [Day 3 — Docker Basics on Oracle VM](docs/day-03/docker-basics-on-oracle.md)
- [Day 3 — Docker Troubleshooting](docs/day-03/docker-troubleshooting.md)
- [Day 3 — Docker Commands](docs/day-03/docker-commands.md)
- [Day 3 — Python Docker Demo App](apps/day3-docker-demo/README.md)
- [Day 4 — Docker Compose Stack](docs/day-04/docker-compose-stack.md)
- [Day 4 — Docker Compose Commands](docs/day-04/docker-compose-commands.md)
- [Day 4 — Docker Compose Troubleshooting](docs/day-04/docker-compose-troubleshooting.md)
- [Day 4 — Compose Security Notes](docs/day-04/compose-security-notes.md)
- [Day 4 — Compose API Stack App](apps/compose-api-stack/README.md)
