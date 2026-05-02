# Day 2 — Security List SSH Hardening 🔐

## 🎯 Цель

Зафиксировать, как был усилен SSH-доступ к Oracle VM на уровне Oracle Security List и почему это важно для публичной cloud VM.

## 🧱 Что такое Oracle Security List

Oracle Security List — это cloud-level firewall для subnet в Oracle Cloud Infrastructure.

В контексте нашей лабы Security List контролирует, какой входящий и исходящий network traffic разрешён для VM, находящейся в public subnet.

| Уровень | Инструмент | Где работает |
|---|---|---|
| Cloud firewall | Oracle Security List | На уровне subnet / VNIC path |
| Host firewall | UFW | Внутри Ubuntu VM |
| SSH authentication | SSH key | На уровне доступа к серверу |

## 🧭 Как мы нашли Security List

Security List была найдена через Oracle Console:

```text
Instance
→ Networking
→ Primary VNIC
→ Subnet
→ Security
→ Security Lists
→ Default Security List
→ Security rules
```

После этого были изменены ingress rules для SSH.

## ⚠️ Почему нельзя оставлять `0.0.0.0/0` на SSH

Правило:

```text
0.0.0.0/0 → TCP 22
```

означает, что SSH-порт доступен из любого IPv4-адреса в интернете.

Для публичной VM это опасно:

- [ ] сервер постоянно виден automated scanners;
- [ ] растёт количество brute-force attempts;
- [ ] повышается риск эксплуатации ошибок в SSH configuration;
- [ ] security posture проекта выглядит слабее;
- [ ] это плохая baseline-практика для production-like окружения.

Даже если вход разрешён только по SSH key, публичный SSH для всего интернета лучше не оставлять.

## ✅ Какое правило оставили

Оставили только узкое ingress rule:

```text
<HOME_PUBLIC_IP>/32 → TCP 22
```

| Поле | Значение |
|---|---|
| Source CIDR | `<HOME_PUBLIC_IP>/32` |
| Protocol | TCP |
| Destination port | `22` |
| Purpose | SSH access from trusted home IP |

Широкое правило было удалено:

```text
0.0.0.0/0 → TCP 22
```

## 🤝 Почему UFW и Oracle Security List работают вместе

Oracle Security List и UFW не заменяют друг друга. Они работают на разных уровнях.

| Layer | Tool | Responsibility |
|---|---|---|
| Cloud network | Oracle Security List | Не пропускает нежелательный traffic к VM |
| OS firewall | UFW | Ограничивает traffic уже на самой Ubuntu VM |

На Day 2 итоговая модель такая:

```text
Internet
→ Oracle Security List: allow only <HOME_PUBLIC_IP>/32 to TCP 22
→ Ubuntu VM
→ UFW: allow OpenSSH, deny incoming by default
→ SSH daemon
```

Важно: UFW может показывать `OpenSSH` from `Anywhere`, но реальный внешний доступ всё равно ограничивается Oracle Security List.

## 🏠 Что делать, если домашний IP изменится

Если провайдер поменял public IP, SSH может перестать подключаться с timeout.

### 1. Узнать текущий public IP

```bash
curl ifconfig.me
```

### 2. Обновить Oracle Security List

В Oracle Console заменить source CIDR для SSH:

```text
<HOME_PUBLIC_IP>/32 → TCP 22
```

на новый актуальный `/32` адрес.

### 3. Проверить SSH

```bash
ssh -i ~/.ssh/devops_cloud_lab ubuntu@<ORACLE_PUBLIC_IP>
```

Expected result:

```text
Successful SSH login as ubuntu
```

## 🧪 Quick verification checklist

- [x] `0.0.0.0/0 → TCP 22` удалён.
- [x] `<HOME_PUBLIC_IP>/32 → TCP 22` добавлен.
- [x] SSH login проверен.
- [x] UFW enabled.
- [x] UFW default incoming policy set to deny.

## 🔜 Какие порты откроем позже

| Port | Protocol | Когда / зачем |
|---:|---|---|
| `80` | TCP | Позже для web/demo HTTP |
| `443` | TCP | Позже для web/demo HTTPS |
| `6443` | TCP | Kubernetes API только через VPN или SSH tunnel |
| `3000` | TCP | Только временно или через `kubectl port-forward` |
| `9090` | TCP | Только временно или через `kubectl port-forward` |
| `51820` | UDP | Позже для WireGuard VPN |

## ✅ Финальный checklist

- [x] Security List найдена через VNIC → Subnet path.
- [x] SSH доступ ограничен до trusted source CIDR.
- [x] Wide-open SSH удалён.
- [x] UFW и Security List описаны как layered defense.
- [x] План действий при смене домашнего IP задокументирован.
- [x] Future port exposure policy зафиксирована.
