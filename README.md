# Automatischer Discord Voting-Reminder

Ein Workflow zum Senden monatlicher automatischer Erinnerungen zum Voten unseres Minecraft Servers.

## 1. Ziel

**Discord-Minecraft-Voting** veröffentlicht automatisch einmal pro Monat eine Voting-Erinnerung in einem definierten Discord-Kanal.

Die Ausführung erfolgt über **GitHub Actions**. Sämtliche redaktionell pflegbaren Inhalte befinden sich in einer Markdown-Datei. Die technische Verarbeitung übernimmt ein Python-Script.
Der Workflow ist für eine automatische Ausführung **an jedem 2. des Monats um 17:00 Uhr deutscher Zeit** konfiguriert.

Der Ablauf sieht vereinfacht so aus:

```text
GitHub Repository
      │
      ├── vote-reminder.md
      │
      ▼
Python-Script
      │
      ├── aktuellen Monat bestimmen
      ├── Theme auswählen
      ├── zufälligen Titel auswählen
      ├── zufälligen Monatstext auswählen
      ├── Januar-Sonderlogik anwenden
      ├── Discord-Embed erzeugen
      └── Webhook aufrufen
      │
      ▼
Discord Webhook
      │
      ▼
Discord-Kanal
```

---

# 2. Voraussetzungen

Für die Implementierung werden benötigt:

* Discord-Server
* Discord-Kanal für die Voting-Erinnerung (aktuell Minecraft-Chat)
* Berechtigung zum Erstellen bzw. Verwalten eines Discord-Webhooks
* GitHub-Repository
* GitHub Actions
* Repository Secret für die Webhook-URL

---

# 3. Repository-Struktur

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

Die Aufgaben sind klar voneinander getrennt:

```text
vote-reminder.md
        │
        └── Inhalte und Konfiguration

send-vote-reminder.py
        │
        └── Verarbeitungs- und Versandlogik

vote-reminder.yml
        │
        └── Zeitsteuerung und Ausführung
```

Dadurch können beispielsweise Texte, Links oder Emojis geändert werden, ohne dass die eigentliche Programmlogik angepasst werden muss.

---

# 4. Einrichtung in Discord

## 4.1 Webhook erstellen

Für den Versand der Nachricht wird im gewünschten Discord-Kanal ein Webhook eingerichtet.

Dazu:

1. Einstellungen des gewünschten Discord-Kanals öffnen.
2. **Integrationen** auswählen.
3. **Webhooks** öffnen.
4. Einen neuen Webhook erstellen.
5. Einen Namen vergeben.
6. Den Zielkanal festlegen.
7. Optional ein Profilbild für den Webhook definieren.
8. Die Webhook-URL kopieren.

Die Webhook-URL darf nicht öffentlich gespeichert werden.

---

# 5. GitHub Secret

Die Discord-Webhook-URL wird als Repository Secret hinterlegt.

Im GitHub-Repository:

**Settings → Secrets and variables → Actions**

Unter **Repository secrets** wird folgendes Secret angelegt:

```text
DISCORD_VOTE_URL
```

Als Wert wird die zuvor aus Discord kopierte Webhook-URL eingetragen.

Der Workflow stellt dieses Secret dem Python-Script als Umgebungsvariable zur Verfügung:

```yaml
env:
  DISCORD_VOTE_URL: ${{ secrets.DISCORD_VOTE_URL }}
```

Dadurch befindet sich die Webhook-URL zu keinem Zeitpunkt direkt im Repository.

---

# 6. Inhalt der `vote-reminder.md`

Die Datei

```text
vote-reminder.md
```

enthält sämtliche editierbaren Inhalte des Voting-Reminders.

Dazu gehören unter anderem:

* Server-Startdatum
* Webhook-Name
* Footer-Text
* Footer-Icon
* `@everyone`-Erwähnung
* zufällige Titel
* monatsspezifische Farben
* monatsspezifische Emojis
* mehrere Nachrichtentexte pro Monat
* Fallback-Nachrichten
* Voting-Links
* Erklärung zum Voting

Die frühere PHP-Lösung enthielt diese Inhalte direkt im PHP-Code. Die neue Struktur trennt Inhalt und Programmlogik voneinander. Die ursprüngliche PHP-Datei enthielt beispielsweise für jeden Monat eigene Farben und Emojis.

---

# 7. Monatsspezifische Inhalte

Für jeden Monat existiert innerhalb der Markdown-Datei ein eigener Abschnitt.

Beispiel:

```markdown
### August

color: 3718648
emoji: :camping:

#### Nachrichten

- Im August genießt man oft die letzten richtig warmen Sommertage :sunrise:

  Wenn ihr abends noch ein paar Runden auf dem Server spielt, denkt gern an einen Vote für unser Projekt.

- Der Spätsommer im August eignet sich perfekt für entspannte Gaming-Sessions.

  Wenn euch der Server durch diese Zeit begleitet, freuen wir uns über eure Votes.
```

Das Python-Script erkennt automatisch den aktuellen Monat und verwendet ausschließlich die dazugehörigen Daten.

Die bisherige PHP-Implementierung arbeitete nach demselben Prinzip und enthielt beispielsweise drei unterschiedliche Texte für August.

---

# 8. Zufällige Nachricht

Für jeden Monat sind mehrere Nachrichtentexte hinterlegt.
Bei jeder Ausführung wird zufällig eine dieser Nachrichten ausgewählt.
Dadurch wird nicht jeden Monat bzw. bei manuellen Tests immer exakt derselbe Text ausgegeben.

---

# 9. Zufälliger Titel

Zusätzlich enthält `vote-reminder.md` mehrere mögliche Titel.

Beispielsweise:

```markdown
## Titel

- Monatlicher Voting-Reminder
- Neuer Monat, neues Voting
- Unterstütze unseren Server mit deinem Vote
- Dein Vote stärkt unsere Community
- In diesem Monat zählt jeder Vote
- Gemeinsam stark – mit euren Votes
- Ein paar Klicks, große Wirkung
- Eure Votes halten den Server aktiv
```

Das Python-Script wählt bei jeder Ausführung zufällig einen dieser Titel aus.

---

# 10. Januar-Sonderlogik

Im Januar wird zusätzlich das Alter des Servers berechnet.

Als Startdatum ist aktuell:

```text
2025-01-01
```

hinterlegt.

Das Python-Script berechnet daraus die Anzahl der vergangenen Jahre.

Im Januar kann dadurch beispielsweise folgende Zusatzinformation erscheinen:

```text
Unser Server feiert heute seinen 1. Geburtstag 🎂
```

bzw. bei einem höheren Alter:

```text
Unser Server ist jetzt 2 Jahre alt ...
```

Die Altersinformation wird ausschließlich im Januar an die ausgewählte Nachricht angehängt.

---

# 11. Discord-Embed

Die Nachricht wird nicht nur als einfacher Text versendet, sondern als Discord-Embed aufgebaut.

Das Embed enthält unter anderem:

* Emoji und zufälligen Titel
* zufälligen Monatstext
* monatsspezifische Farbe
* Voting-Links
* Erklärung zum Nutzen der Votes
* Footer
* optional `@everyone`

---

# 12. Voting-Links

Die Voting-Links werden direkt aus `vote-reminder.md` gelesen.

Beispiel:

```markdown
### Voting-Links

- [Vote auf minecraft-server.eu](https://minecraft-server.eu/vote/index/2321D)
- [Vote auf minecraft-serverlist.net](https://www.minecraft-serverlist.net/vote/59253)
- [Vote auf serverliste.net](https://serverliste.net/vote/5142)
```

Werden Links geändert oder ergänzt, muss nur die Markdown-Datei angepasst werden.

---

# 13. Python-Script

Das Script

```text
.github/scripts/send-vote-reminder.py
```

übernimmt ausschließlich die technische Verarbeitung.

Zu seinen Aufgaben gehören:

1. Lesen der Markdown-Datei.
2. Auslesen der allgemeinen Einstellungen.
3. Ermittlung des aktuellen Monats nach `Europe/Berlin`.
4. Auswahl des passenden Monatsthemes.
5. Zufallsauswahl eines Titels.
6. Zufallsauswahl einer Monatsnachricht.
7. Berechnung des Serveralters im Januar.
8. Erstellung der Discord-Payload.
9. Versand der Nachricht an den Webhook.
10. Fehlerbehandlung bei fehlgeschlagenem Versand.

Die Discord-Webhook-URL wird dabei ausschließlich aus

```text
DISCORD_VOTE_URL
```

gelesen.

---

# 14. GitHub Action

Der eigentliche GitHub-Workflow befindet sich unter:

```text
.github/workflows/vote-reminder.yml
```

Die zentrale Konfiguration lautet:

```yaml
name: Discord Voting Erinnerung

on:
  schedule:
    - cron: "0 17 2 * *"
      timezone: "Europe/Berlin"

  workflow_dispatch:

permissions:
  contents: read

jobs:
  send-vote-reminder:
    runs-on: ubuntu-latest

    steps:
      - name: Repository auschecken
        uses: actions/checkout@v4

      - name: Discord Voting Reminder senden
        env:
          DISCORD_VOTE_URL: ${{ secrets.DISCORD_VOTE_URL }}
        run: |
          python3 .github/scripts/send-vote-reminder.py
```

---

# 15. Zeitsteuerung

Die Ausführung erfolgt über:

```yaml
- cron: "0 17 2 * *"
  timezone: "Europe/Berlin"
```

Das bedeutet:

```text
Minute:      0
Stunde:      17
Tag:         2
Monat:       jeder Monat
Wochentag:   beliebig
Zeitzone:    Europe/Berlin
```

Der Voting-Reminder wird damit automatisch:

**an jedem 2. des Monats um 17:00 Uhr deutscher Zeit**

ausgeführt.

Durch die Verwendung von:

```text
Europe/Berlin
```

wird die lokale deutsche Zeitzone verwendet.

---

# 16. Manuelle Ausführung

Zusätzlich zur monatlichen Ausführung enthält der Workflow:

```yaml
workflow_dispatch:
```

Damit lässt sich die Action jederzeit manuell starten.

Im GitHub-Repository:

**Actions → Discord Voting Erinnerung → Run workflow**

Dies eignet sich insbesondere:

* nach Änderungen an `vote-reminder.md`
* nach Änderungen am Python-Script
* nach Änderungen am Webhook
* zum Testen der Discord-Darstellung

---

# 17. Ablauf einer automatischen Ausführung

Am Beispiel des **2. August um 17:00 Uhr**:

```text
02. August, 17:00 Uhr
        │
        ▼
GitHub startet vote-reminder.yml
        │
        ▼
Repository wird ausgecheckt
        │
        ▼
send-vote-reminder.py wird gestartet
        │
        ├── erkennt August
        │
        ├── liest August-Theme
        │
        ├── Farbe auswählen
        │
        ├── Emoji auswählen
        │
        ├── zufälligen Titel auswählen
        │
        └── zufälligen August-Text auswählen
        │
        ▼
Voting-Links und weitere Felder ergänzen
        │
        ▼
Discord-Payload erzeugen
        │
        ▼
DISCORD_VOTE_URL verwenden
        │
        ▼
Nachricht an Discord senden
```

---

# 18. Pflege der Inhalte

Für normale redaktionelle Änderungen muss ausschließlich

```text
vote-reminder.md
```

bearbeitet werden.

Beispiele:

```text
Neuen Monatstext hinzufügen
        → vote-reminder.md

Voting-Link ändern
        → vote-reminder.md

Embed-Farbe ändern
        → vote-reminder.md

Emoji ändern
        → vote-reminder.md

Footer ändern
        → vote-reminder.md

Titel ergänzen
        → vote-reminder.md
```

Die technische Implementierung muss dafür nicht angepasst werden.

---

# 19. Sicherheit

Die Discord-Webhook-URL darf nicht innerhalb von:

* `vote-reminder.md`
* `send-vote-reminder.py`
* `vote-reminder.yml`
* README-Dateien
* Commits
* öffentlichen Dokumentationen

gespeichert werden.

Stattdessen wird ausschließlich das GitHub Repository Secret

```text
DISCORD_VOTE_URL
```

verwendet.

Sollte die Webhook-URL versehentlich veröffentlicht werden, sollte der Webhook in Discord erneuert und anschließend das GitHub Secret aktualisiert werden.

---

# 20. Zusammenfassung

Die Implementierung trennt Inhalt, Programmlogik und Zeitsteuerung konsequent voneinander:

```text
vote-reminder.md
        │
        └── Was soll veröffentlicht werden?

send-vote-reminder.py
        │
        └── Wie wird die Nachricht verarbeitet?

vote-reminder.yml
        │
        └── Wann wird die Nachricht veröffentlicht?

DISCORD_VOTE_URL
        │
        └── Wohin wird die Nachricht gesendet?
```

Damit ist der Voting-Reminder ohne PHP-Laufzeit vollständig über **GitHub Actions, Python und eine zentral gepflegte Markdown-Datei** automatisiert.
