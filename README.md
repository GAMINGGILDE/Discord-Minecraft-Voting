# Automatischer Discord Voting-Reminder

Ein Workflow zum Senden monatlicher automatischer Erinnerungen zum Voten unseres Minecraft Servers.

## 1. Ziel

**Discord-Minecraft-Voting** veröffentlicht einmal pro Monat automatisch eine Voting-Erinnerung im [Minecraft-Chat](https://discord.com/channels/1219625244906754093/1219651063968174110)-Kanal.

Die Ausführung erfolgt vollständig über **GitHub Actions**. Die Nachricht wird dabei als normale Discord-Nachricht versendet.
Sämtliche redaktionell pflegbaren Inhalte befinden sich in der Datei:

```text
vote-reminder.md
```

Die technische Verarbeitung übernimmt ein Python-Script. Die automatische Ausführung erfolgt:

**an jedem 2. des Monats um 17:00 Uhr deutscher Zeit.**

Der grundsätzliche Ablauf:

```text
GitHub Actions
      │
      ▼
vote-reminder.md einlesen
      │
      ▼
aktuellen Monat bestimmen
      │
      ├── Monats-Emoji auswählen
      ├── zufälligen Titel auswählen
      ├── zufälligen Monatstext auswählen
      └── ggf. Januar-Sondertext ergänzen
      │
      ▼
Nachrichtenvorlage zusammensetzen
      │
      ▼
2.000-Zeichen-Limit prüfen
      │
      ▼
Discord Webhook
      │
      ▼
normale Discord-Nachricht
```

## 2. Voraussetzungen

Für die Implementierung werden benötigt:

* Discord-Server
* Discord-Kanal für die Voting-Erinnerung ([Minecraft-Chat](https://discord.com/channels/1219625244906754093/1219651063968174110))
* Berechtigung zum Erstellen bzw. Verwalten eines Discord-Webhooks
* GitHub-Repository
* aktivierte GitHub Actions
* Repository Secret für die Discord-Webhook-URL

Eine eigene PHP-Umgebung oder ein dauerhaft laufender Server wird nicht benötigt.

## 3. Repository-Struktur

Die Implementierung besteht aus drei zentralen Dateien:

```text
repository/
│
├── vote-reminder.md
│
└── .github/
    ├── scripts/
    │   └── send-vote-reminder.py
    │
    └── workflows/
        └── vote-reminder.yml
```

Die Zuständigkeiten sind dabei voneinander getrennt:

```text
vote-reminder.md
        │
        └── Inhalte und Darstellung

send-vote-reminder.py
        │
        └── Verarbeitung und Discord-Versand

vote-reminder.yml
        │
        └── Zeitsteuerung und Ausführung
```

Dadurch können die Inhalte der Discord-Nachricht bearbeitet werden, ohne Änderungen an der GitHub Action oder dem Python-Script vornehmen zu müssen.

## 4. Einrichtung in Discord

### 4.1 Webhook erstellen

Für den automatischen Versand wird im gewünschten Discord-Kanal ein Webhook benötigt.

Dazu:

1. Einstellungen des gewünschten Discord-Kanals öffnen.
2. **Integrationen** auswählen.
3. **Webhooks** öffnen.
4. Einen neuen Webhook erstellen.
5. Einen Namen vergeben.
6. Den gewünschten Zielkanal auswählen.
7. Optional ein Profilbild festlegen.
8. Die Webhook-URL kopieren.

Die Webhook-URL ermöglicht das direkte Senden von Nachrichten in den entsprechenden Discord-Kanal.

> Die Webhook-URL ist wie ein Zugangsschlüssel zu behandeln und darf nicht öffentlich im Repository gespeichert werden.

## 5. GitHub Secret einrichten

Die Discord-Webhook-URL wird als verschlüsseltes GitHub Repository Secret gespeichert.

Im entsprechenden Repository:

**Settings → Secrets and variables → Actions**

Unter **Repository secrets** wird folgendes Secret angelegt:

```text
DISCORD_VOTE_URL
```

Als Wert wird die zuvor aus Discord kopierte Webhook-URL eingetragen.
Die GitHub Action stellt dieses Secret anschließend dem Python-Script als Umgebungsvariable zur Verfügung:

```yaml
env:
  DISCORD_VOTE_URL: ${{ secrets.DISCORD_VOTE_URL }}
```

Die Webhook-URL befindet sich dadurch nicht im Quellcode des Repositorys.

## 6. Die Datei `vote-reminder.md`

Die Datei:

```text
vote-reminder.md
```

ist die zentrale Konfigurations- und Inhaltsdatei des Voting-Reminders.

Sie enthält:

* allgemeine Einstellungen
* die Nachrichtenvorlage
* mögliche Titel
* Monats-Emojis
* mehrere Texte pro Monat
* Fallback-Nachrichten
* Voting-Links
* zusätzliche Informationen zum Voting

In der Implementierung können diese Inhalte unabhängig von der Programmlogik bearbeitet werden.

## 7. Allgemeine Einstellungen

Am Anfang der Markdown-Datei befinden sich grundlegende Einstellungen:

```markdown
## Einstellungen

server_start: 2025-01-01
webhook_username: Minecraft Gilde
mention: @everyone
```

#### `server_start`

Definiert das Startdatum des Servers.
Dieses Datum wird für die Januar-Sonderlogik verwendet.

#### `webhook_username`

Bestimmt den Namen, unter dem der Discord-Webhook die Nachricht veröffentlicht.

#### `mention`

Definiert die Erwähnung am Anfang der Nachricht.

Aktuell:

```text
@everyone
```

Dadurch können alle Mitglieder des Discord-Servers auf die monatliche Voting-Erinnerung aufmerksam gemacht werden, sofern die entsprechenden Discord-Berechtigungen dies zulassen.

## 8. Nachrichtenvorlage

Der Aufbau der späteren Discord-Nachricht wird direkt in `vote-reminder.md` definiert.

Beispiel:

```markdown
## Nachrichtenvorlage

{{MENTION}}

{{EMOJI}} **{{TITLE}}**

{{MESSAGE}}

**Voting-Links**

- [Vote auf minecraft-server.eu](https://minecraft-server.eu/vote/index/2321D)
- [Vote auf minecraft-serverlist.net](https://www.minecraft-serverlist.net/vote/59253)
- [Vote auf serverliste.net](https://serverliste.net/vote/5142)

**Warum für uns voten?**

:sparkles: Jeder Vote bringt uns in den Serverlisten weiter nach oben. So finden neue Spieler leichter zu uns und unsere Community bleibt lebendig.

:loudspeaker: Alle Infos zum Voten: [minecraft-gilde.de/voten](https://minecraft-gilde.de/voten/)
```

## 9. Platzhalter

Innerhalb der Nachrichtenvorlage stehen vier dynamische Platzhalter zur Verfügung.

```text
{{MENTION}}
{{EMOJI}}
{{TITLE}}
{{MESSAGE}}
```

Diese werden unmittelbar vor dem Versand durch das Python-Script ersetzt.

#### `{{MENTION}}`

Wird beispielsweise durch:

```text
@everyone
```

ersetzt.

#### `{{EMOJI}}`

Wird durch das Emoji des aktuellen Monats ersetzt.

Im August beispielsweise:

```text
:camping:
```

#### `{{TITLE}}`

Wird durch einen zufällig ausgewählten Titel ersetzt.

#### `{{MESSAGE}}`

Wird durch einen zufällig ausgewählten Text des aktuellen Monats ersetzt.

Dadurch lässt sich die Position der dynamischen Bestandteile direkt innerhalb der Markdown-Datei bestimmen.

## 10. Zufällige Titel

Unter:

```markdown
## Titel
```

befinden sich mehrere mögliche Überschriften.

Beispielsweise:

```markdown
- Monatlicher Voting-Reminder
- Neuer Monat, neues Voting
- Unterstütze unseren Server mit deinem Vote
- Dein Vote stärkt unsere Community
- In diesem Monat zählt jeder Vote
- Gemeinsam stark – mit euren Votes
- Ein paar Klicks, große Wirkung
- Eure Votes halten den Server aktiv
```

Bei jeder Ausführung wird zufällig einer dieser Titel ausgewählt.

## 11. Monatsspezifische Inhalte

Für jeden Monat existiert ein eigener Abschnitt.

Beispiel:

```markdown
### August

emoji: :camping:

#### Nachrichten

- Im August genießt man oft die letzten richtig warmen Sommertage :sunrise:
  Wenn ihr abends noch ein paar Runden auf dem Server spielt, denkt gern an einen Vote für unser Projekt.

- Der Spätsommer im August eignet sich perfekt für entspannte Gaming-Sessions.
  Wenn euch der Server durch diese Zeit begleitet, freuen wir uns über eure Votes.

- Im August haben viele noch Ferien oder Urlaub :smile:
  Wenn ihr ein paar Klicks übrig habt, votet gern für unseren Server und unterstützt unsere Community.
```

Das Python-Script ermittelt zunächst den aktuellen Monat und verwendet anschließend ausschließlich den dazugehörigen Abschnitt.

## 12. Monatliche Emojis

Jeder Monat besitzt ein eigenes Emoji.

Beispielsweise:

```text
Januar     → :snowflake:
Februar    → :heart:
März       → :four_leaf_clover:
April      → :tulip:
Mai        → :cherry_blossom:
Juni       → :sunny:
Juli       → :watermelon:
August     → :camping:
September  → :fallen_leaf:
Oktober    → :jack_o_lantern:
November   → :maple_leaf:
Dezember   → :christmas_tree:
```

## 13. Zufällige Monatsnachricht

Für jeden Monat stehen mehrere Nachrichtentexte zur Verfügung.
Das Python-Script wählt bei jeder Ausführung zufällig einen davon aus.
Dadurch kann beispielsweise der August-Reminder bei mehreren Ausführungen unterschiedliche Texte verwenden.

Die Auswahl erfolgt nach dem Prinzip:

```text
aktueller Monat
      │
      ▼
passende Nachrichten suchen
      │
      ▼
Nachrichten vorhanden?
      │
      ├── JA → zufällige Monatsnachricht
      │
      └── NEIN → zufällige Fallback-Nachricht
```

## 14. Fallback-Nachrichten

Sollte für einen Monat versehentlich keine Nachricht definiert sein, stehen zusätzliche Fallback-Texte zur Verfügung.

Diese befinden sich unter:

```markdown
## Fallback-Nachrichten
```

Beispielsweise:

```markdown
- Hey zusammen :wave:

  Wenn euch der Server Spaß macht, unterstützt ihn gern mit einem Vote. Das hilft uns, sichtbar zu bleiben und neue Spieler zu erreichen.
```

Damit kann der Workflow auch dann eine Nachricht erzeugen, wenn ein Monatsabschnitt unvollständig ist.

## 15. Januar-Sonderlogik

Im Januar wird zusätzlich das Alter des Servers berechnet.

Als Startdatum ist aktuell:

```text
2025-01-01
```

hinterlegt.

Das Python-Script berechnet anhand dieses Datums das aktuelle Serveralter.

Bei einem Jahr wird sinngemäß folgende Nachricht ergänzt:

```text
Unser Server feiert heute seinen **1. Geburtstag** :birthday: – danke, dass ihr von Anfang an dabei seid.
```

Bei mehreren Jahren:

```text
Unser Server ist jetzt **X Jahre alt** – danke, dass ihr uns schon so lange begleitet :birthday:
```

Der Zusatz wird ausschließlich im Januar an den ausgewählten Monatstext angehängt.

## 16. Python-Script

Die Datei:

```text
.github/scripts/send-vote-reminder.py
```

enthält ausschließlich die technische Logik.

Das Script übernimmt:

1. Laden von `vote-reminder.md`.
2. Auslesen der Einstellungen.
3. Ermittlung des aktuellen Datums nach `Europe/Berlin`.
4. Ermittlung des aktuellen Monats.
5. Auswahl des Monats-Emojis.
6. Zufällige Auswahl eines Titels.
7. Zufällige Auswahl einer Monatsnachricht.
8. Anwendung der Januar-Sonderlogik.
9. Ersetzung der Platzhalter.
10. Prüfung der Nachrichtenlänge.
11. Erstellung der Discord-Webhook-Payload.
12. Versand an Discord.

Die redaktionellen Texte sind dadurch vollständig vom Python-Code getrennt.

## 17. Discord-Zeichenlimit

Normale Discord-Nachrichten unterliegen einem Limit von **2.000 Zeichen**.
Das Python-Script prüft deshalb vor dem Versand die Länge der fertig erzeugten Nachricht.

Der Ablauf:

```text
Nachricht erzeugen
      │
      ▼
Zeichen zählen
      │
      ├── ≤ 2.000 → an Discord senden
      │
      └── > 2.000 → Workflow mit Fehler abbrechen
```

Bei einer zu langen Nachricht erscheint im GitHub-Actions-Log eine entsprechende Fehlermeldung.

Dadurch wird verhindert, dass Discord den Request lediglich aufgrund einer zu langen Nachricht ablehnt.

## 18. GitHub Action

Die automatische Ausführung wird über:

```text
.github/workflows/vote-reminder.yml
```

gesteuert.

Die Workflow-Datei:

```yaml
name: Discord Voting Erinnerung

on:
  schedule:
    # Jeden 2. des Monats um 17:00 Uhr deutscher Zeit
    - cron: "0 17 2 * *"
      timezone: "Europe/Berlin"

  # Manuelle Ausführung zum Testen
  workflow_dispatch:

permissions:
  contents: read

jobs:
  send-vote-reminder:
    runs-on: ubuntu-latest

    steps:
      - name: Repository auschecken
        uses: actions/checkout@v5

      - name: Discord Voting Reminder senden
        env:
          DISCORD_VOTE_URL: ${{ secrets.DISCORD_VOTE_URL }}
        run: |
          python3 .github/scripts/send-vote-reminder.py
```

## 19. Zeitsteuerung

Die automatische Ausführung wird durch:

```yaml
- cron: "0 17 2 * *"
  timezone: "Europe/Berlin"
```

definiert.

Das bedeutet:

```text
Minute:      0
Stunde:      17
Tag:         2
Monat:       jeder
Wochentag:   beliebig
Zeitzone:    Europe/Berlin
```

Der Reminder wird damit automatisch:

**an jedem 2. des Monats um 17:00 Uhr deutscher Zeit**

ausgeführt.

## 20. Manuelles Testen

Zusätzlich zur automatischen Ausführung enthält der Workflow:

```yaml
workflow_dispatch:
```

Dadurch kann der Reminder jederzeit manuell gestartet werden.

Im GitHub-Repository:

**Actions → Discord Voting Erinnerung → Run workflow**

Dies sollte insbesondere nach Änderungen an:

* `vote-reminder.md`
* `send-vote-reminder.py`
* `vote-reminder.yml`
* dem Discord-Webhook

verwendet werden.

## 21. Beispiel einer Ausführung

Am **2. August um 17:00 Uhr** läuft die Automatisierung beispielsweise folgendermaßen:

```text
GitHub Actions startet
        │
        ▼
Repository auschecken
        │
        ▼
vote-reminder.md laden
        │
        ▼
Monat = August
        │
        ├── Emoji = :camping:
        │
        ├── zufälligen Titel auswählen
        │
        └── einen von drei August-Texten auswählen
        │
        ▼
Nachrichtenvorlage laden
        │
        ▼
{{MENTION}} ersetzen
{{EMOJI}} ersetzen
{{TITLE}} ersetzen
{{MESSAGE}} ersetzen
        │
        ▼
Nachrichtenlänge prüfen
        │
        ▼
DISCORD_VOTE_URL laden
        │
        ▼
Discord Webhook aufrufen
        │
        ▼
Nachricht erscheint im Discord-Kanal
```

Eine mögliche Ausgabe könnte dadurch folgendermaßen aussehen:

```text
@everyone

:camping: **Dein Vote stärkt unsere Community**

Der Spätsommer im August eignet sich perfekt für entspannte Gaming-Sessions.
Wenn euch der Server durch diese Zeit begleitet, freuen wir uns über eure Votes.

**Voting-Links**

- Vote auf minecraft-server.eu
- Vote auf minecraft-serverlist.net
- Vote auf serverliste.net

**Warum für uns voten?**
:sparkles: Jeder Vote bringt uns in den Serverlisten weiter nach oben. So finden neue Spieler leichter zu uns und unsere Community bleibt lebendig.
:loudspeaker: Alle Infos zum Voten: minecraft-gilde.de/voten
```

Bei der nächsten Ausführung kann automatisch ein anderer Titel und ein anderer August-Text verwendet werden.

## 22. Pflege der Inhalte

Für reguläre Änderungen muss hauptsächlich:

```text
vote-reminder.md
```

bearbeitet werden.

Beispiele:

```text
Titel hinzufügen
        → vote-reminder.md

Monatstext ändern
        → vote-reminder.md

neuen Monatstext ergänzen
        → vote-reminder.md

Emoji ändern
        → vote-reminder.md

Voting-Link ändern
        → vote-reminder.md

Einleitung ändern
        → vote-reminder.md

Reihenfolge der Nachricht ändern
        → vote-reminder.md
```

Das Python-Script muss dafür nicht verändert werden.

## 23. Sicherheit

Die Discord-Webhook-URL darf nicht innerhalb des Repositorys gespeichert werden.

Insbesondere nicht in:

```text
vote-reminder.md
send-vote-reminder.py
vote-reminder.yml
README.md
```

Stattdessen wird ausschließlich das GitHub Secret:

```text
DISCORD_VOTE_URL
```

verwendet.

Sollte die Webhook-URL versehentlich veröffentlicht oder committed werden, sollte der betreffende Discord-Webhook erneuert und anschließend das GitHub Secret aktualisiert werden.

## 24. Zusammenfassung

Die endgültige Implementierung trennt **Inhalt, Programmlogik, Zeitsteuerung und Zugangsdaten**:

```text
vote-reminder.md
        │
        └── Was soll in Discord stehen?

send-vote-reminder.py
        │
        └── Wie wird die Nachricht erzeugt und versendet?

vote-reminder.yml
        │
        └── Wann wird der Reminder ausgeführt?

DISCORD_VOTE_URL
        │
        └── An welchen Discord-Webhook wird gesendet?
```

Die Nachricht wird **jeden 2. des Monats um 17:00 Uhr deutscher Zeit** automatisch als normale Discord-Nachricht veröffentlicht. Sämtliche relevanten Texte und die Darstellung können zentral über `vote-reminder.md` gepflegt werden, während Python ausschließlich die dynamische Verarbeitung und den Versand übernimmt.
