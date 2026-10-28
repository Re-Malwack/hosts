"""Build the commit messages used by the update workflow.

Usage (from the repository root, after the update scripts have run):
    python scripts/commit_message.py data [--previous OLD_STATS_JSON] [--run N]
    python scripts/commit_message.py docs

Messages follow the 50/72 convention: a capitalized, imperative subject of at
most 50 characters, a blank line, then a body wrapped at 72 columns.
"""
import argparse
import json
import os
import textwrap

STATS_FILE = "stats.json"
CHECKSUM_FILE = "checksums.txt"
WIDTH = 72


def load_stats(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def totals(stats, section):
    return {item["name"]: item["domains"] for item in stats.get(section, [])}


def stamp(stats):
    """'2026-10-04T04:13:42Z' -> '2026-10-04 04:13'"""
    return stats["generated_at"].replace("T", " ")[:16]


def change(new, old):
    if old is None:
        return "new"
    if new == old:
        return "no change"
    return f"{new - old:+,}"


def count_table(title, current, previous):
    width = max(len(name) for name in current)
    lines = [title]
    for name, total in current.items():
        line = f"  {name:<{width}}  {total:>9,}"
        if previous is not None:
            line += f"  ({change(total, previous.get(name))})"
        lines.append(line)
    return "\n".join(lines)


def paragraph(text):
    return textwrap.fill(text, width=WIDTH)


def checksum_count():
    if not os.path.exists(CHECKSUM_FILE):
        return 0
    with open(CHECKSUM_FILE, "r", encoding="utf-8") as f:
        return sum(1 for line in f if line.strip())


def data_message(stats, previous_stats=None, run=None):
    subject = f"Update hosts and blocklists ({stamp(stats)})"
    intro = paragraph(
        "Rebuild the host profiles and blocklists from their upstream "
        f"sources and refresh {CHECKSUM_FILE} ({checksum_count()} files)."
    )

    sections = [intro]
    for title, key in (("Profiles (domains):", "profiles"), ("Blocklists (domains):", "blocklists")):
        current = totals(stats, key)
        if current:
            previous = totals(previous_stats, key) if previous_stats is not None else None
            sections.append(count_table(title, current, previous))

    footer = [f"Generated: {stats['generated_at']}"]
    if run:
        footer.append(f"Workflow run: #{run}")
    sections.append("\n".join(footer))

    return subject + "\n\n" + "\n\n".join(sections) + "\n"


def docs_message(stats):
    subject = f"Update README and stats ({stamp(stats)})"
    body = paragraph(
        "Regenerate the profile and blocklist tables in README.md and "
        "refresh stats.json so they match the data commit."
    )
    return f"{subject}\n\n{body}\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("kind", choices=("data", "docs"))
    parser.add_argument("--previous", help="stats.json from before this run, to show per-list changes")
    parser.add_argument("--run", help="workflow run number to mention in the message")
    args = parser.parse_args()

    stats = load_stats(STATS_FILE)
    if args.kind == "docs":
        print(docs_message(stats), end="")
        return

    previous = None
    if args.previous and os.path.exists(args.previous):
        previous = load_stats(args.previous)
    print(data_message(stats, previous, args.run), end="")


if __name__ == "__main__":
    main()
