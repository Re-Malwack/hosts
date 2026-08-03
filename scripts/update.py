import urllib.request
import re
import os
import json
from datetime import datetime, timezone
import fnmatch
from concurrent.futures import ThreadPoolExecutor
import threading

# Configuration
RE_MALWACK_RAW_URL = "https://raw.githubusercontent.com/ZG089/Re-Malwack/main"
PROFILES = ["lite", "balanced", "default", "aggressive"]
DOMAIN_REGEX = re.compile(r'^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9-]{2,24}$')
STATS_FILE = "stats.json"

# Global cache for source URLs: url -> set(domains)
source_cache = {}
cache_lock = threading.Lock()

def fetch_url_text(url, timeout=30):
    try:
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (Re-Malwack hosts updater)'}
        )
        with urllib.request.urlopen(req, timeout=timeout) as response:
            data = response.read().decode('utf-8', errors='ignore')
            print(f"[OK] {url} ({len(data)} bytes)")
            return data
    except Exception as e:
        print(f"[FAIL] {url}: {e}")
        return ""

def parse_profile_sources(profile_text):
    sources = []
    for line in profile_text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("#", 1)
        url = parts[0].strip()
        provider = parts[1].strip() if len(parts) > 1 else url
        sources.append({"url": url, "provider": provider})
    return sources

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


def update_stats_json(section_key, items):
    data = {}
    if os.path.exists(STATS_FILE):
        try:
            with open(STATS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError):
            data = {}
    data["generated_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    data[section_key] = items
    with open(STATS_FILE, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def main():
    print("=== Re-Malwack Hosts Profile Updater ===\n")

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

    # Collect all unique source URLs across profiles
    all_urls = set()
    profile_sources = {}

    PROFILE_DESCRIPTIONS = {
        "lite": "Only basic ads and trackers. Very safe, minimal breakage.",
        "balanced": "Blocks ads, trackers, telemetry, and common annoyances. Recommended for most users.",
        "default": "More aggressive blocking. Might break some referral links or minor site functionalities.",
        "aggressive": "Maximum protection. **Warning:** Will break sites, apps, and services. Only for advanced users who know how to whitelist."
    }

    profile_table_rows = []

    for profile in PROFILES:
        profile_url = f"{RE_MALWACK_RAW_URL}/module/profiles/{profile}.txt"
        profile_text = fetch_url_text(profile_url)
        if not profile_text:
            continue
        sources = parse_profile_sources(profile_text)
        profile_sources[profile] = sources
        for src in sources:
            all_urls.add(src["url"])

    print(f"\nFetching {len(all_urls)} unique source URLs in parallel...")
    with ThreadPoolExecutor(max_workers=8) as executor:
        list(executor.map(get_domains_for_url, list(all_urls)))

    os.makedirs("hosts", exist_ok=True)

    profiles_stats = []

    for profile, sources in profile_sources.items():
        print(f"\nBuilding profile: {profile}")
        all_profile_domains = set()
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
            all_profile_domains.update(clean_domains)

        sorted_domains = sorted(all_profile_domains)
        total_count = len(sorted_domains)

        utc_now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        header_lines = [
            f"# Re-Malwack Hosts - {profile.capitalize()} Profile",
            f"# Last Update: {utc_now}",
            f"# Total Blocked Domains: {total_count}",
            "#",
            "# --- Host Sources Details ---"
        ]
        for idx, stat in enumerate(source_stats, 1):
            header_lines.append(f"# {idx}. {stat['provider']}")
            header_lines.append(f"#    Source: {stat['url']}")
            header_lines.append(f"#    Count:  {stat['count']} domains")
            header_lines.append("#")
        header_lines.append("# --- End of Sources ---")
        header_lines.append("")

        hosts_content = "\n".join(header_lines)
        if sorted_domains:
            hosts_content += "\n".join(f"0.0.0.0 {d}" for d in sorted_domains) + "\n"
        else:
            hosts_content += "\n"

        with open(os.path.join("hosts", profile), "w", encoding="utf-8", newline="\n") as f:
            f.write(hosts_content)

        count_lines = [f"{stat['url']}|{stat['count']}" for stat in source_stats]
        with open(os.path.join("hosts", f"{profile}.count"), "w", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(count_lines) + "\n")

        print(f"  -> {profile}: {total_count} domains written.")

        sources_html = "<details><summary>View Sources</summary><ul>"
        for stat in source_stats:
            sources_html += f"<li><a href='{stat['url']}'>{stat['provider']}</a></li>"
        sources_html += "</ul></details>"

        raw_link = f"https://raw.githubusercontent.com/Re-Malwack/hosts/main/hosts/{profile}"
        desc = PROFILE_DESCRIPTIONS.get(profile, "")
        profile_table_rows.append(f"| **{profile.replace('-', ' ').title()}** | {desc} | `{total_count:,}` | {sources_html} | `{raw_link}` |")

        profiles_stats.append({
            "name": profile,
            "domains": total_count,
            "raw_link": raw_link,
            "sources": [{"provider": s["provider"], "url": s["url"], "count": s["count"]} for s in source_stats]
        })

    update_stats_json("profiles", profiles_stats)

    # Update README.md
    readme_path = "README.md"
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            readme_content = f.read()
        
        table_content = "<!-- PROFILES_TABLE_START -->\n"
        table_content += "| Profile | Description | Domains | Sources | Raw Link |\n"
        table_content += "|---------|-------------|---------|---------|----------|\n"
        table_content += "\n".join(profile_table_rows) + "\n"
        table_content += "<!-- PROFILES_TABLE_END -->"
        
        readme_content = re.sub(
            r"<!-- PROFILES_TABLE_START -->.*?<!-- PROFILES_TABLE_END -->",
            table_content,
            readme_content,
            flags=re.DOTALL
        )
        
        with open(readme_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(readme_content)

    print("\nDone.")

if __name__ == "__main__":
    main()
