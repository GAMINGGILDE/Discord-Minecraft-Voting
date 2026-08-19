#!/usr/bin/env python3
import os
import re
import json
import random
import urllib.request
import urllib.error
from datetime import datetime, date
from zoneinfo import ZoneInfo
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTENT_FILE = ROOT / "vote-reminder.md"
MAX_CONTENT_LENGTH = 2000

MONTHS = [
    "Januar", "Februar", "März", "April", "Mai", "Juni",
    "Juli", "August", "September", "Oktober", "November", "Dezember"
]

def section(text, heading, level=2):
    marker = "#" * level + " " + heading
    start = text.find(marker)
    if start == -1:
        return ""
    start += len(marker)
    next_heading = re.search(rf"(?m)^{'#' * level} ", text[start:])
    end = start + next_heading.start() if next_heading else len(text)
    return text[start:end].strip()

def parse_settings(text):
    raw = section(text, "Einstellungen", 2)
    settings = {}
    for line in raw.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            settings[key.strip()] = value.strip()
    return settings

def parse_titles(text):
    raw = section(text, "Titel", 2)
    return [line[2:].strip() for line in raw.splitlines() if line.startswith("- ")]

def parse_markdown_list(raw):
    items = []
    current = []
    for line in raw.splitlines():
        if line.startswith("- "):
            if current:
                items.append("\n".join(current).strip())
            current = [line[2:]]
        elif current:
            if line.startswith("  "):
                current.append(line[2:])
            elif line.strip() == "":
                current.append("")
            else:
                current.append(line)
    if current:
        items.append("\n".join(current).strip())
    return [item for item in items if item]

def parse_month(text, month_name):
    raw = section(section(text, "Monate", 2), month_name, 3)
    emoji_match = re.search(r"(?m)^emoji:\s*(.+?)\s*$", raw)
    msg_raw = section(raw, "Nachrichten", 4)
    return {
        "emoji": emoji_match.group(1).strip() if emoji_match else "",
        "messages": parse_markdown_list(msg_raw),
    }

def server_age_note(server_start):
    start = date.fromisoformat(server_start)
    today = datetime.now(ZoneInfo("Europe/Berlin")).date()
    years = today.year - start.year - ((today.month, today.day) < (start.month, start.day))

    if years == 1:
        return "Unser Server feiert heute seinen **1. Geburtstag** :birthday: – danke, dass ihr von Anfang an dabei seid."
    return f"Unser Server ist jetzt **{years} Jahre alt** – danke, dass ihr uns schon so lange begleitet :birthday:"

def render_message(template, mention, emoji, title, message):
    replacements = {
        "{{MENTION}}": mention,
        "{{EMOJI}}": emoji,
        "{{TITLE}}": title,
        "{{MESSAGE}}": message,
    }
    rendered = template
    for placeholder, value in replacements.items():
        rendered = rendered.replace(placeholder, value)
    return rendered.strip()

def send_webhook(url, username, content):
    payload = {
        "content": content,
        "username": username,
        "allowed_mentions": {"parse": ["everyone"]},
    }

    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "GitHub-Actions-Discord-Vote-Reminder/2.0",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req) as response:
            if response.status not in (200, 204):
                raise RuntimeError(
                    f"Discord Webhook fehlgeschlagen: HTTP {response.status}"
                )
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"Discord Webhook fehlgeschlagen: HTTP {exc.code} - {body}"
        ) from exc

def main():
    webhook_url = os.environ.get("DISCORD_VOTE_URL")
    if not webhook_url:
        raise RuntimeError("DISCORD_VOTE_URL wurde nicht gesetzt.")

    text = CONTENT_FILE.read_text(encoding="utf-8")
    settings = parse_settings(text)
    template = section(text, "Nachrichtenvorlage", 2)
    titles = parse_titles(text)

    now = datetime.now(ZoneInfo("Europe/Berlin"))
    month_number = now.month
    month_name = MONTHS[month_number - 1]
    month = parse_month(text, month_name)

    messages = month["messages"]
    if not messages:
        messages = parse_markdown_list(section(text, "Fallback-Nachrichten", 2))

    if not titles:
        raise RuntimeError("Keine Titel in vote-reminder.md gefunden.")
    if not messages:
        raise RuntimeError("Keine Nachrichten in vote-reminder.md gefunden.")
    if not template:
        raise RuntimeError("Keine Nachrichtenvorlage in vote-reminder.md gefunden.")

    title = random.choice(titles)
    message = random.choice(messages)

    if month_number == 1:
        note = server_age_note(settings["server_start"])
        if note:
            message += "\n\n" + note

    content = render_message(
        template=template,
        mention=settings.get("mention", "@everyone"),
        emoji=month["emoji"],
        title=title,
        message=message,
    )

    if len(content) > MAX_CONTENT_LENGTH:
        raise RuntimeError(
            f"Die erzeugte Discord-Nachricht ist mit {len(content)} Zeichen "
            f"zu lang. Discord erlaubt maximal {MAX_CONTENT_LENGTH} Zeichen."
        )

    send_webhook(
        webhook_url,
        settings.get("webhook_username", "Minecraft Gilde"),
        content,
    )

    print(
        f"Voting-Reminder für {month_name} erfolgreich gesendet "
        f"({len(content)} Zeichen)."
    )

if __name__ == "__main__":
    main()
