# Home-Lab Umstellung – Dokumentenübersicht

## Aktuellste Versionen

| Dokument | Aktuelle Version | Datei |
|---|---|---|
| **Gesamtanleitung (PDF, zum Lesen)** | **v1.3.0** | `Home-Lab_Roadmap_Gesamt.pdf` |
| Gesamtanleitung (Markdown, Arbeits-/Quellversion) | **v1.3.0** | `Home-Lab_Roadmap_Befehle.md` |

> **Hinweis:** Beide Dateien haben denselben Inhalt – das PDF wird aus dem Markdown erzeugt (`md2pdf.py`). Das frühere, separat gepflegte Übersichts-PDF (`Home-Lab_Roadmap.pdf`, v1.0.0) wurde zugunsten des gemeinsamen Dokuments eingestellt.

> **Regel:** Jede inhaltliche Änderung erhöht die Versionsnummer
> (Semantik: MAJOR.MINOR.PATCH – neue Phase = MINOR, Korrekturen = PATCH)
> und erhält einen Eintrag im Changelog am Dokumentanfang sowie ein Git-Tag
> mit derselben Versionsnummer. Das jeweils aktuelle Dokument ist an der
> höchsten Versionsnummer im Changelog erkennbar.

## Versionierung im Detail

- **Im Dokument**: Changelog-Tabelle am Anfang jedes Dokuments; die oberste Zeile ist immer die aktuelle Version.
- **Im Git**: Jede Version wird als Tag markiert (`git tag v1.1.0`), änderungen zwischen Versionen sichtbar über:
  - GitHub: *Tags* bzw. *Releases* → Commit-Vergleich `v1.0.0...v1.1.0`
  - Lokal: `git diff v1.0.0 v1.1.0`
  - Commit-Messages referenzieren die Änderung (z. B. „v1.1.0: SMART-Gate ergänzt")

## Changelog (global)

| Version | Dokument | Datum | Änderungen |
|---|---|---|---|
| v1.2.0 | Gesamt (md+pdf) | 2026-10-31 | gemeinsames Dokument: PDF aus Markdown erzeugt, altes separates Roadmap-PDF eingestellt; inhaltlich identisch mit v1.2.0-Beschlüssen |
| v1.3.0 | Gesamt (md+pdf) | 2026-11-23 | Beschluss „kein Tailscale" (WireGuard auf UDM = einziger Remote-Zugang); Phase-1-Review: Backends bis Phase 2 auf Unraid + Firewall-Regel 2 temporär, NPM-Admin per SSH-Tunnel, CrowdSec-Log-Mount korrigiert, restic-Zugang Futro ergänzt |
| v1.2.0 | Befehle (.md) | 2026-10-30 | Beschlüsse aus Alternativ-Anleitungs-Vergleich: Alt-Platten bleiben eingebaut (Migration über temp. bulk-Pool), tank-Mirror + dedizierter backup-Pool mit strikter Abfolge, sanoid/syncoid-Replikation (readonly-Schutz), USB-Platte als lokales restic-Tier, DMZ Option B (Futro in eigenem VLAN, 5-Regel-Set), TrueNAS geprüft und verworfen |
| v1.1.0 | Befehle (.md) | 2026-10-30 | Migrationssicherheit ergänzt (SMART-Gate, Inventur, Secrets-Export, rsync-Verifikation, Rollback über Alt-Platten, 14-Tage-Beobachtung, nmap-Check) |
| v1.0.0 | Befehle (.md) | 2026-10-30 | Initiale Version: 4 Phasen mit Befehlen und Abschlusstests |
| v1.0.0 | Roadmap (PDF) | 2026-10-30 | Initiale Version: 5-Seiten-Übersicht mit 4 Phasen und Abschlusstests |

## v1.2.3 (2026-11-01) – Phase-0-Abnahme & Architektur-Beschlüsse

Phase 0 formell abgenommen (außer UDM-Hardening-Block): SMART-Gate bestanden
(sdc formell, sdb via Zonen-Vollltest-Kompensation), restic-Initial 536,6 GiB
auf Hetzner, Cron scharf, lokale Vollkopie verifiziert.

Neue verbindliche Beschlüsse: Storage-Layout (Dataset-Besitzer-Matrix),
Paperless-Philosophie A, Vaultwarden-first-Migrationsreihenfolge,
Credential-Handling, GPU/Coral-Ausbau, 10G-Verzicht.

## v1.3.0 (2026-11-23) – Beschluss „Kein Tailscale" + Phase-1-Review

Verbindlicher Beschluss: WireGuard auf der UDM Pro bleibt einziger Remote-Zugang; Tailscale wird nicht eingeführt (kein Mehrwert bei öffentlicher WAN-IP und einem Standort, Funnel würde den DMZ-Rand umgehen, fremder Control-Plane unerwünscht). Tailscale SSH kann später isoliert nachgerüstet werden; dann `100.64.0.0/10` firewall-seitig wie `<WG_NETZ>` behandeln.

Phase-1-Korrekturen: (1) NPM-Proxy-Hosts `cloud.`/`vault.` zeigen bis Phase 2 auf `<UNRAID_IP>`, Firewall-Regel 2 temporär um die Backend-Ports erweitern und nach Phase 2 entfernen; (2) NPM-Admin-UI nur per SSH-Tunnel (`ssh -L 8181:127.0.0.1:81 <USER>@<FUTRO_IP>` → `http://127.0.0.1:8181`); (3) CrowdSec mountet NPM-Logs korrekt über `./npm-data/log/nginx`; (4) Futro bekommt eigenen restic-Sub-Account/-Key + Cron für das `~/edge`-Config-Backup.
