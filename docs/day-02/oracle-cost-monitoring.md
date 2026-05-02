# Day 2 — Oracle Cost Monitoring 💰

## 🎯 Цель

Зафиксировать cost baseline для Oracle VM и не допустить неожиданных расходов во время 30-дневного DevOps bootcamp.

## 🧾 Почему A2 — платный trial-credit resource

Созданная VM использует shape:

```text
VM.Standard.A2.Flex
```

Это не Always Free A1 instance. Такой ресурс потребляет Oracle trial credits / Universal Credits.

| Параметр | Значение |
|---|---|
| Shape | `VM.Standard.A2.Flex` |
| OCPU | `4` |
| RAM | `24 GB` |
| Free tier | Not Always Free A1 |
| Payment source | Oracle trial credits / Universal Credits |
| Risk | Credits can be consumed if resource stays active |

## ✅ Почему это осознанное решение

Мы остаёмся на A2 временно, потому что:

- [x] цель — пройти bootcamp за месяц;
- [x] ресурса достаточно для будущего `k3s` master node;
- [x] есть trial credits / Universal Credits;
- [x] решение принято осознанно, с ежедневным cost monitoring;
- [x] в конце trial будет принято решение: перейти на Always Free A1 или удалить paid resources.

## 📊 Что нужно проверять каждый день

Проверять Oracle Billing / Usage / Cost Analysis каждый день.

| Что проверить | Почему важно |
|---|---|
| Credits remaining | Понять, сколько trial credits осталось |
| Credit used | Увидеть скорость расхода credits |
| Active resources | Найти всё, что продолжает billing |
| Boot volumes | Boot volume может остаться после terminate |
| Public IP | Public IP может иметь cost implications в зависимости от состояния |
| Block volumes | Detached volumes могут продолжать стоить денег |

## 🧭 Daily checklist

- [ ] Открыть Oracle Console.
- [ ] Проверить Billing / Usage / Cost Analysis.
- [ ] Проверить credits remaining.
- [ ] Проверить credit used за день.
- [ ] Проверить active compute instances.
- [ ] Проверить boot volumes.
- [ ] Проверить block volumes.
- [ ] Проверить public IP resources.
- [ ] Убедиться, что нет забытых paid resources.
- [ ] Зафиксировать любые неожиданные расходы в notes.

## 🔎 Active resources checklist

| Resource | Expected Day 2 state | Action |
|---|---|---|
| Compute instance | `oci-k3s-master` active | Monitor daily |
| Boot volume | Exists for VM | Keep while VM is needed |
| Block volumes | None unless created intentionally | Delete unused |
| Public IP | Assigned to VM | Monitor |
| Load balancers | None | Delete if accidentally created |
| NAT gateways | None unless intentionally created | Monitor |
| Object storage | None unless intentionally created | Monitor |

## 🧯 Что сделать в конце trial

В конце trial нужно выбрать один из вариантов.

### Option A — перейти на Always Free A1

- [ ] Создать Always Free compatible A1 instance, если capacity доступна.
- [ ] Перенести нужные configs и manifests.
- [ ] Проверить SSH и firewall rules.
- [ ] Удалить paid A2 VM после миграции.

### Option B — terminate paid VM

- [ ] Terminate `oci-k3s-master`.
- [ ] Проверить, удалён ли boot volume.
- [ ] Delete boot volume, если он больше не нужен.
- [ ] Проверить detached block volumes.
- [ ] Проверить public IP resources.
- [ ] Проверить Cost Analysis после удаления.

## ⚠️ Cost safety rules

- Не создавать новые paid resources без явной причины.
- Не оставлять detached volumes без необходимости.
- Не оставлять paid VM running после окончания bootcamp или trial.
- Не хранить payment details, subscription ID, OCID или личные данные в публичном repository.
- Все sensitive values в документации заменять на placeholders.

## ✅ Финальный checklist

- [x] A2 billing model задокументирован.
- [x] Риск trial-credit consumption понятен.
- [x] Daily monitoring checklist создан.
- [x] End-of-trial actions описаны.
- [x] Sensitive billing details не добавлены в repository.
