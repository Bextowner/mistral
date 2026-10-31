# Home-Lab Umstellung – Gesamtanleitung

Migration Unraid → Proxmox mit Netzwerk-Konsolidierung, DMZ, ZFS-Storage und 3-2-1-Backup.

## 📄 Dokumente

| Datei | Zweck |
|---|---|
| **`Home-Lab_Roadmap_Gesamt.pdf`** | **Die Gesamtanleitung zum Lesen** (Laptop/Tab) – alle Phasen, Befehle und Abschlusstests in einem Dokument |
| `Home-Lab_Roadmap_Befehle.md` | Arbeits- und Quellversion (Markdown) – Basis für das PDF, zum direkten Copy-Paste der Befehle |

**Beide Dateien haben denselben Inhalt (v1.2.0)** – das PDF wird aus dem Markdown erzeugt. Bei Änderungen: Markdown anpassen, PDF neu generieren, Version in beiden erhöhen (siehe `VERSION.md`).

## 🏷️ Versionierung

Aktuelle Version: **v1.2.0** (siehe `VERSION.md` für das vollständige Changelog und die Regeln). Jede Version erhält ein Git-Tag – Versionsvergleich über [Tags](https://github.com/Bextowner/mistral/tags).

## Architektur (Beschlüsse)

- **UDM Pro**: einzige Firewall, gehärtet, WireGuard-VPN
- **Futro S920 #1**: Edge-Box im eigenen DMZ-VLAN (AdGuard, NPM, CrowdSec, DDNS) · **Futro #2**: Kaltreserve
- **Hauptserver**: Proxmox auf 250-GB-SSD, ZFS (`fast` NVMe, `tank` 2×3-TB-Mirror, `backup`-Replikatpool via sanoid/syncoid), Dienste als LXC
- **HP T630**: unverändert (HA, MQTT, Zigbee2MQTT als LXCs), ins Backup integriert
- **Backup 3-2-1(+1)**: ZFS-Snapshots → syncoid-Replikation auf backup-Pool → restic verschlüsselt → Hetzner Storage Box + lokale USB-Platte
- Verzicht: OPNsense, Frigate, Coral, GPU, TrueNAS (jeweils geprüft und bewusst verworfen)
