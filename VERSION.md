# Home-Lab Umstellung – Dokumentenübersicht

## Aktuellste Versionen

| Dokument | Aktuelle Version | Datei |
|---|---|---|
| Schritt-für-Schritt-Anleitung (Befehle) | **v1.1.0** | `Home-Lab_Roadmap_Befehle.md` |
| Roadmap (Übersicht als PDF) | **v1.0.0** | `Home-Lab_Roadmap.pdf` |

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
| v1.1.0 | Befehle (.md) | 2026-10-30 | Migrationssicherheit ergänzt (SMART-Gate, Inventur, Secrets-Export, rsync-Verifikation, Rollback über Alt-Platten, 14-Tage-Beobachtung, nmap-Check) |
| v1.0.0 | Befehle (.md) | 2026-10-30 | Initiale Version: 4 Phasen mit Befehlen und Abschlusstests |
| v1.0.0 | Roadmap (PDF) | 2026-10-30 | Initiale Version: 5-Seiten-Übersicht mit 4 Phasen und Abschlusstests |
