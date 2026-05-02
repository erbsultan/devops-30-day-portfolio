# Day 1 — Accounts, Billing Safety, Git Foundation

## Цель дня

Подготовить основу проекта до создания инфраструктуры: завести репозиторий, определить правила публичной документации, зафиксировать cost-safety подход и подготовить Git workflow для ежедневного DevOps portfolio.

Day 1 не про сервер и команды на VM. Это foundational day: без него легко случайно опубликовать secrets, потерять структуру документации или создать paid cloud resources без контроля расходов.

## Что было сделано

1. Создан GitHub repository для 30-day DevOps portfolio.
2. Определена цель проекта: собрать публичное портфолио с практической DevOps-лабораторией.
3. Зафиксированы основные technical areas: Docker, Kubernetes, CI/CD, Terraform, Ansible, monitoring, multi-cloud.
4. Принято правило: реальные IP, OCID, email, payment details, subscription ID и private keys не публикуются.
5. Определён подход к billing safety перед созданием cloud resources.
6. Подготовлена начальная Markdown-структура документации.

## Repository Baseline

| Area | Decision |
|---|---|
| Repository purpose | Public DevOps portfolio |
| Main intro page | `README.md` |
| Documentation entry point | `docs/index.md` |
| Daily progress tracking | `docs/progress.md` |
| Daily technical notes | `docs/day-XX/*.md` |
| Secrets policy | Use placeholders only |

## Git Foundation

Минимальный Git workflow для проекта:

```bash
git status
git add README.md docs/
git commit -m "docs: initialize devops portfolio"
git push
```

Перед каждым commit нужно проверять diff:

```bash
git diff --staged
```

## Public Documentation Rules

| Value type | Public docs rule |
|---|---|
| Public IP | Replace with `<ORACLE_PUBLIC_IP>` |
| Home public IP | Replace with `<HOME_PUBLIC_IP>` |
| Oracle compartment | Replace with `<ORACLE_COMPARTMENT>` |
| VCN / subnet names | Use placeholders if sensitive |
| OCID | Never publish |
| Private SSH key | Never commit |
| Payment details | Never document |
| Email / address | Never document |

## Billing Safety Baseline

Перед созданием cloud resources нужно понимать:

- какой cloud provider используется;
- какой free tier или trial-credit model применяется;
- какие resources могут стоить денег;
- что нужно проверять каждый день;
- как удалить resources после завершения lab.

Day 1 decision: любые paid или trial-credit resources должны быть явно описаны в документации, а не появляться как случайные side effects.

## Security Baseline

На старте проекта приняты базовые security rules:

- не открывать cloud resources шире, чем нужно;
- не оставлять SSH доступ с `0.0.0.0/0`, если можно ограничить trusted IP;
- не хранить secrets в репозитории;
- использовать SSH keys вместо password-based access;
- документировать security decisions вместе с инфраструктурой.

## Documentation Structure

Целевая структура после Day 1:

```text
README.md
docs/
  index.md
  progress.md
  day-01/
    accounts-billing-git-foundation.md
```

Следующие дни добавляют отдельные technical docs в `docs/day-XX/`.

## Финальный checklist

- [x] Repository purpose defined.
- [x] Intro page separated from progress tracking.
- [x] Documentation index prepared.
- [x] Progress tracker location defined.
- [x] Secrets policy documented.
- [x] Billing safety baseline documented.
- [x] Git workflow documented.
