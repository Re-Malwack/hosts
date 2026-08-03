import urllib.request
import re
import os
from datetime import datetime, timezone
import fnmatch
from concurrent.futures import ThreadPoolExecutor
import threading

RE_MALWACK_RAW_URL = "https://raw.githubusercontent.com/ZG089/Re-Malwack/main"
DOMAIN_REGEX = re.compile(r'^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9-]{2,24}$')
SOURCES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "sources")

source_cache = {}
cache_lock = threading.Lock()


def load_sources(filepath):
    sources = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("#", 1)
            url = parts[0].strip()
            provider = parts[1].strip() if len(parts) > 1 else url
            sources.append({"url": url, "provider": provider})
    return sources


def load_brand_sources(filepath):
    brands = {}
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            hash_parts = line.split("#", 1)
            provider = hash_parts[1].strip() if len(hash_parts) > 1 else ""
            pipe_parts = hash_parts[0].split("|", 1)
            brand = pipe_parts[0].strip()
            url = pipe_parts[1].strip() if len(pipe_parts) > 1 else ""
            if brand and url:
                brands[brand] = {"url": url, "provider": provider}
    return brands


def fetch_url_text(url, timeout=30):
    try:
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (Re-Malwack blocklist updater)'}
        )
        with urllib.request.urlopen(req, timeout=timeout) as response:
            data = response.read().decode('utf-8', errors='ignore')
            print(f"[OK] {url} ({len(data)} bytes)")
            return data
    except Exception as e:
        print(f"[FAIL] {url}: {e}")
        return ""


def parse_whitelist(text):
    domains = set()
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        domain = line.split("#")[0].strip().lower()
        if domain:
            domains.add(domain)
    return domains


def extract_domains_from_hosts(hosts_text):
    domains = set()
    for line in hosts_text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if not parts:
            continue

        first = parts[0]
        is_ip = re.match(r'^(\d{1,3}\.){3}\d{1,3}$', first) or ":" in first

        if is_ip:
            for candidate in parts[1:]:
                candidate = candidate.split("#")[0].strip().lower()
                if DOMAIN_REGEX.match(candidate):
                    domains.add(candidate)
        else:
            candidate = first.split("#")[0].strip().lower()
            if DOMAIN_REGEX.match(candidate):
                domains.add(candidate)
    return domains


def get_domains_for_url(url):
    with cache_lock:
        if url in source_cache:
            return source_cache[url]

    raw_content = fetch_url_text(url)
    if not raw_content:
        with cache_lock:
            source_cache[url] = set()
        return set()

    domains = extract_domains_from_hosts(raw_content)
    with cache_lock:
        source_cache[url] = domains
    print(f"[PARSED] {url}: {len(domains)} domains")
    return domains


def build_blocklist_file(name, sources, is_whitelisted, output_dir):
    """Build a single blocklist file from given sources."""
    all_domains = set()
    source_stats = []

    for src in sources:
        url = src["url"]
        provider = src["provider"]
        with cache_lock:
            raw_domains = source_cache.get(url, set())
        clean_domains = {d for d in raw_domains if not is_whitelisted(d)}
        source_stats.append({
            "provider": provider,
            "url": url,
            "count": len(clean_domains)
        })
        all_domains.update(clean_domains)

    sorted_domains = sorted(all_domains)
    total_count = len(sorted_domains)

    utc_now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    header_lines = [
        f"# Re-Malwack Blocklist - {name.replace('-', ' ').title()}",
        f"# Last Update: {utc_now}",
        f"# Total Blocked Domains: {total_count}",
        "#",
        "# --- Sources Details ---"
    ]
    for idx, stat in enumerate(source_stats, 1):
        header_lines.append(f"# {idx}. {stat['provider']}")
        header_lines.append(f"#    Source: {stat['url']}")
        header_lines.append(f"#    Count:  {stat['count']} domains")
        header_lines.append("#")
    header_lines.append("# --- End of Sources ---")
    header_lines.append("")

    content = "\n".join(header_lines)
    if sorted_domains:
        content += "\n".join(f"0.0.0.0 {d}" for d in sorted_domains) + "\n"
    else:
        content += "\n"

    file_path = os.path.join(output_dir, name)
    count_path = os.path.join(output_dir, f"{name}.count")

    with open(file_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    with open(count_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(str(total_count) + "\n")

    print(f"  -> {name}: {total_count} domains written.")

    sources_html = "<details><summary>View Sources</summary><ul>"
    for stat in source_stats:
        sources_html += f"<li><a href='{stat['url']}'>{stat['provider']}</a></li>"
    sources_html += "</ul></details>"

    raw_link = f"https://raw.githubusercontent.com/Re-Malwack/hosts/main/blocklists/{name}"
    if name.startswith("trackers-"):
        brand = name[len("trackers-"):].replace('-', ' ').title()
        display_name = f"Trackers ({brand})"
    else:
        display_name = name.replace('-', ' ').title()
    return f"| **{display_name}** | `{total_count:,}` | {sources_html} | `{raw_link}` |"


def main():
    print("=== Re-Malwack Blocklist Updater ===\n")

    # Fetch whitelists
    print("Fetching whitelists...")
    whitelist_txt = fetch_url_text(f"{RE_MALWACK_RAW_URL}/whitelist.txt")
    social_whitelist_txt = fetch_url_text(f"{RE_MALWACK_RAW_URL}/social_whitelist.txt")
    wildcard_whitelist_txt = fetch_url_text(f"{RE_MALWACK_RAW_URL}/whitelist_wildcard.txt")

    global_whitelist = parse_whitelist(whitelist_txt)
    global_whitelist.update(parse_whitelist(social_whitelist_txt))
    wildcard_patterns = parse_whitelist(wildcard_whitelist_txt)
    print(f"Whitelist: {len(global_whitelist)} direct, {len(wildcard_patterns)} wildcard patterns.\n")

    def is_whitelisted(domain):
        if domain in global_whitelist:
            return True
        for pattern in wildcard_patterns:
            if fnmatch.fnmatch(domain, pattern):
                return True
        return False

    # Load sources from external files
    blocklist_names = ["porn", "gambling", "fakenews", "social"]
    blocklist_sources = {}
    for bl_name in blocklist_names:
        blocklist_sources[bl_name] = load_sources(os.path.join(SOURCES_DIR, f"{bl_name}.txt"))

    trackers_base = load_sources(os.path.join(SOURCES_DIR, "trackers_base.txt"))
    trackers_brands = load_brand_sources(os.path.join(SOURCES_DIR, "trackers_brands.txt"))

    # Collect all unique URLs to prefetch
    all_urls = set()
    for sources in blocklist_sources.values():
        for src in sources:
            all_urls.add(src["url"])
    for src in trackers_base:
        all_urls.add(src["url"])
    for brand_src in trackers_brands.values():
        all_urls.add(brand_src["url"])

    print(f"Fetching {len(all_urls)} unique source URLs in parallel...")
    with ThreadPoolExecutor(max_workers=8) as executor:
        list(executor.map(get_domains_for_url, list(all_urls)))

    output_dir = "blocklists"
    os.makedirs(output_dir, exist_ok=True)

    blocklist_table_rows = []

    # Build standard blocklists (porn, gambling, fakenews, social)
    for bl_name in blocklist_names:
        print(f"\nBuilding blocklist: {bl_name}")
        row = build_blocklist_file(bl_name, blocklist_sources[bl_name], is_whitelisted, output_dir)
        if row: blocklist_table_rows.append(row)

    # Build trackers: base (general trackers only)
    print(f"\nBuilding blocklist: trackers")
    row = build_blocklist_file("trackers", trackers_base, is_whitelisted, output_dir)
    if row: blocklist_table_rows.append(row)

    # Build trackers: per-brand (base + brand-specific)
    for brand, brand_src in trackers_brands.items():
        combined_sources = trackers_base + [brand_src]
        bl_name = f"trackers-{brand}"
        print(f"\nBuilding blocklist: {bl_name}")
        row = build_blocklist_file(bl_name, combined_sources, is_whitelisted, output_dir)
        if row: blocklist_table_rows.append(row)

    # Update README.md
    readme_path = "README.md"
    if os.path.exists(readme_path) and blocklist_table_rows:
        with open(readme_path, "r", encoding="utf-8") as f:
            readme_content = f.read()

        table_content = "<!-- BLOCKLISTS_TABLE_START -->\n"
        table_content += "| Blocklist | Domains | Sources | Raw Link |\n"
        table_content += "|-----------|---------|---------|----------|\n"
        table_content += "\n".join(blocklist_table_rows) + "\n"
        table_content += "<!-- BLOCKLISTS_TABLE_END -->"

        readme_content = re.sub(
            r"<!-- BLOCKLISTS_TABLE_START -->.*?<!-- BLOCKLISTS_TABLE_END -->",
            table_content,
            readme_content,
            flags=re.DOTALL
        )

        with open(readme_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(readme_content)

    print("\nDone.")


if __name__ == "__main__":
    main()
