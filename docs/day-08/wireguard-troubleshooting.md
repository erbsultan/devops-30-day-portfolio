# Day 8 — WireGuard Troubleshooting

## 🧯 Issue 1: Deleted Correct SSH UFW Rule

What happened:

- Correct SSH rule from `<HOME_PUBLIC_IP>/32` was added on Oracle.
- While removing broad OpenSSH access, the correct SSH rule was accidentally deleted.

Fix:

```bash
sudo ufw allow from <HOME_PUBLIC_IP>/32 to any port 22 proto tcp
sudo ufw status numbered
```

Verification:

- Opened a new terminal.
- Confirmed SSH still worked.
- Removed broad OpenSSH IPv6 Anywhere rule where necessary.

## 🧯 Issue 2: Ran AWS UFW Commands on Oracle

What happened:

- AWS UFW commands were accidentally entered while the prompt still showed `ubuntu@oci-k3s-master`.
- The mistake was caught by checking the shell prompt.

Fix:

- Connected to `ubuntu@aws-k3s-worker-1`.
- Re-ran the AWS UFW rules on the correct server.
- Confirmed AWS UFW became active.

Useful checks:

```bash
hostname
whoami
sudo ufw status numbered
```

## 🧯 Issue 3: Vultr `wg-quick@wg0` Failed

What happened:

- `sudo systemctl start wg-quick@wg0` failed on Vultr.
- Cause was a config/key issue, most likely missing trailing `=` in the AWS public key.

Fix:

```bash
sudo nano /etc/wireguard/wg0.conf
sudo systemctl start wg-quick@wg0
sudo systemctl status wg-quick@wg0 --no-pager -l
```

Result:

- `wg-quick@wg0` started successfully.
- Handshake with Oracle and AWS was verified.

## 🔎 Debug Workflow

Service status:

```bash
sudo systemctl status wg-quick@wg0 --no-pager -l
```

Journal logs:

```bash
sudo journalctl -xeu wg-quick@wg0.service --no-pager -n 80
```

WireGuard state:

```bash
sudo wg show
ip addr show wg0
```

VPN ping:

```bash
ping -c 4 10.50.0.1
ping -c 4 10.50.0.2
ping -c 4 10.50.0.3
```

Firewall checks:

```bash
sudo ufw status numbered
```

Also check provider firewall rules:

- Oracle Security List
- AWS Security Group
- Vultr Firewall

## ✅ Common Root Causes

| Symptom | Likely Cause | Check |
|---|---|---|
| `wg-quick@wg0` fails to start | invalid config or key format | `journalctl -xeu wg-quick@wg0.service` |
| no handshake | peer endpoint/firewall issue | cloud firewall + UFW |
| ping fails but handshake exists | `AllowedIPs` or route issue | `sudo wg show`, `ip route` |
| SSH access risk | broad SSH rule still present | cloud firewall + `sudo ufw status numbered` |
| commands affect wrong node | wrong SSH session | `hostname` and shell prompt |
