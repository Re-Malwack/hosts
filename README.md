# Re-Malwack Hosts Repository

This repository hosts all the pre-compiled hosts and blocklist files used by Re-Malwack. It also provides direct raw links for non-root and custom adblocking applications like AdAway, Blokada, DNS66, NextDNS, and others.

## Main Project

The main module can be found here:
**[Re-Malwack](https://github.com/ZG089/Re-Malwack)**

## Repository Structure

```text
├── .github/          # GitHub Actions workflows for automated updates
├── blocklists/       # Specialized blocklist files (porn, gambling, fakenews, social, trackers)
├── hosts/            # Main profile host files (lite, balanced, default, aggressive)
├── scripts/          # Python update scripts to fetch and compile lists
├── sources/          # Source URLs for blocklists and tracker lists (shared with shell scripts)
└── README.md         # This documentation
```

## Hosts Profiles (For AdAway & Custom Ad-Blockers)

These are the main compiled profiles containing merged domains. Use the raw links below to import them into your ad-blocker application.

<!-- PROFILES_TABLE_START -->
| Profile | Description | Domains | Sources | Raw Link |
|---------|-------------|---------|---------|----------|
| **Lite** | Only basic ads and trackers. Very safe, minimal breakage. | `100,937` | <details><summary>View Sources</summary><ul><li><a href='https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts'>StevenBlack Unified hosts</a></li><li><a href='https://raw.githubusercontent.com/hagezi/dns-blocklists-legacy/main/hosts/light.txt'>Hagezi Light hosts</a></li><li><a href='https://raw.githubusercontent.com/r-a-y/mobile-hosts/refs/heads/master/AdguardMobileAds.txt'>Adguard Mobile Ads</a></li><li><a href='https://raw.githubusercontent.com/r-a-y/mobile-hosts/refs/heads/master/AdguardMobileSpyware.txt'>Adguard Mobile Spyware</a></li></ul></details> | `https://raw.githubusercontent.com/Re-Malwack/hosts/main/hosts/lite` |
| **Balanced** | Blocks ads, trackers, telemetry, and common annoyances. Recommended for most users. | `398,050` | <details><summary>View Sources</summary><ul><li><a href='https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts'>StevenBlack Unified hosts</a></li><li><a href='https://raw.githubusercontent.com/hagezi/dns-blocklists-legacy/main/hosts/multi.txt'>Hagezi Multi-Normal hosts</a></li><li><a href='https://badmojr.github.io/1Hosts/Lite/hosts.txt'>1Hosts Lite</a></li><li><a href='https://raw.githubusercontent.com/r-a-y/mobile-hosts/master/AdguardDNS.txt'>Adguard DNS</a></li><li><a href='https://raw.githubusercontent.com/r-a-y/mobile-hosts/refs/heads/master/AdguardMobileAds.txt'>Adguard Mobile Ads</a></li><li><a href='https://raw.githubusercontent.com/r-a-y/mobile-hosts/refs/heads/master/AdguardMobileSpyware.txt'>Adguard Mobile Spyware</a></li><li><a href='https://hosts.rem01gaming.dev/adblock'>Rem01Gaming AdBlock</a></li></ul></details> | `https://raw.githubusercontent.com/Re-Malwack/hosts/main/hosts/balanced` |
| **Default** | More aggressive blocking. Might break some referral links or minor site functionalities. | `567,396` | <details><summary>View Sources</summary><ul><li><a href='https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts'>StevenBlack Unified hosts</a></li><li><a href='https://raw.githubusercontent.com/hagezi/dns-blocklists-legacy/main/hosts/pro.txt'>Hagezi Pro</a></li><li><a href='https://badmojr.github.io/1Hosts/Lite/hosts.txt'>1Hosts Lite</a></li><li><a href='https://raw.githubusercontent.com/r-a-y/mobile-hosts/master/AdguardDNS.txt'>Adguard DNS</a></li><li><a href='https://raw.githubusercontent.com/r-a-y/mobile-hosts/refs/heads/master/AdguardMobileAds.txt'>Adguard Mobile Ads</a></li><li><a href='https://raw.githubusercontent.com/r-a-y/mobile-hosts/refs/heads/master/AdguardMobileSpyware.txt'>Adguard Mobile Spyware</a></li><li><a href='https://hosts.rem01gaming.dev/adblock'>Rem01Gaming AdBlock</a></li><li><a href='https://raw.githubusercontent.com/hagezi/dns-blocklists-legacy/main/hosts/native.tiktok.txt'>Hagezi TikTok Native</a></li><li><a href='https://blocklistproject.github.io/Lists/ads.txt'>BlocklistProject - Ads</a></li></ul></details> | `https://raw.githubusercontent.com/Re-Malwack/hosts/main/hosts/default` |
| **Aggressive** | Maximum protection. **Warning:** Will break sites, apps, and services. Only for advanced users who know how to whitelist. | `676,003` | <details><summary>View Sources</summary><ul><li><a href='https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts'>StevenBlack Unified hosts</a></li><li><a href='https://raw.githubusercontent.com/hagezi/dns-blocklists-legacy/main/hosts/pro.plus.txt'>Hagezi Pro</a></li><li><a href='https://badmojr.github.io/1Hosts/Lite/hosts.txt'>1Hosts Lite</a></li><li><a href='https://raw.githubusercontent.com/r-a-y/mobile-hosts/master/AdguardDNS.txt'>Adguard DNS</a></li><li><a href='https://raw.githubusercontent.com/r-a-y/mobile-hosts/refs/heads/master/AdguardMobileAds.txt'>Adguard Mobile Ads</a></li><li><a href='https://raw.githubusercontent.com/r-a-y/mobile-hosts/refs/heads/master/AdguardMobileSpyware.txt'>Adguard Mobile Spyware</a></li><li><a href='https://hosts.rem01gaming.dev/adblock'>Rem01Gaming AdBlock</a></li><li><a href='https://blocklistproject.github.io/Lists/ads.txt'>BlocklistProject - Ads</a></li><li><a href='https://blocklistproject.github.io/Lists/redirect.txt'>BlocklistProject - Malicious Redirects</a></li></ul></details> | `https://raw.githubusercontent.com/Re-Malwack/hosts/main/hosts/aggressive` |
<!-- PROFILES_TABLE_END -->

## Specialized Blocklists

These lists target specific categories and can be added alongside your main ad-blocker profiles.

<!-- BLOCKLISTS_TABLE_START -->
| Blocklist | Domains | Sources | Raw Link |
|-----------|---------|---------|----------|
| **Porn** | `115,804` | <details><summary>View Sources</summary><ul><li><a href='https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/porn-only/hosts'>StevenBlack Porn</a></li><li><a href='https://raw.githubusercontent.com/4skinSkywalker/Anti-Porn-HOSTS-File/refs/heads/master/HOSTS.txt'>Anti-Porn HOSTS</a></li></ul></details> | `https://raw.githubusercontent.com/Re-Malwack/hosts/main/blocklists/porn` |
| **Gambling** | `345,457` | <details><summary>View Sources</summary><ul><li><a href='https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/gambling-only/hosts'>StevenBlack Gambling</a></li><li><a href='https://blocklistproject.github.io/Lists/gambling.txt'>BlocklistProject Gambling</a></li></ul></details> | `https://raw.githubusercontent.com/Re-Malwack/hosts/main/blocklists/gambling` |
| **Fakenews** | `2,187` | <details><summary>View Sources</summary><ul><li><a href='https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/fakenews-only/hosts'>StevenBlack Fake News</a></li></ul></details> | `https://raw.githubusercontent.com/Re-Malwack/hosts/main/blocklists/fakenews` |
| **Social** | `3,222` | <details><summary>View Sources</summary><ul><li><a href='https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/social-only/hosts'>StevenBlack Social Media</a></li></ul></details> | `https://raw.githubusercontent.com/Re-Malwack/hosts/main/blocklists/social` |
| **Malware** | `2,656,321` | <details><summary>View Sources</summary><ul><li><a href='https://blocklistproject.github.io/Lists/malware.txt'>BlocklistProject - Malware</a></li></ul></details> | `https://raw.githubusercontent.com/Re-Malwack/hosts/main/blocklists/malware` |
| **Trackers** | `287,334` | <details><summary>View Sources</summary><ul><li><a href='https://raw.githubusercontent.com/r-a-y/mobile-hosts/refs/heads/master/AdguardTracking.txt'>Adguard Tracking</a></li><li><a href='https://blocklistproject.github.io/Lists/tracking.txt'>BlocklistProject Tracking</a></li></ul></details> | `https://raw.githubusercontent.com/Re-Malwack/hosts/main/blocklists/trackers` |
| **Trackers (Xiaomi)** | `287,334` | <details><summary>View Sources</summary><ul><li><a href='https://raw.githubusercontent.com/r-a-y/mobile-hosts/refs/heads/master/AdguardTracking.txt'>Adguard Tracking</a></li><li><a href='https://blocklistproject.github.io/Lists/tracking.txt'>BlocklistProject Tracking</a></li><li><a href='https://raw.githubusercontent.com/hagezi/dns-blocklists-legacy/main/hosts/native.xiaomi.txt'>Hagezi Native Xiaomi</a></li></ul></details> | `https://raw.githubusercontent.com/Re-Malwack/hosts/main/blocklists/trackers-xiaomi` |
| **Trackers (Samsung)** | `287,334` | <details><summary>View Sources</summary><ul><li><a href='https://raw.githubusercontent.com/r-a-y/mobile-hosts/refs/heads/master/AdguardTracking.txt'>Adguard Tracking</a></li><li><a href='https://blocklistproject.github.io/Lists/tracking.txt'>BlocklistProject Tracking</a></li><li><a href='https://raw.githubusercontent.com/hagezi/dns-blocklists-legacy/main/hosts/native.samsung.txt'>Hagezi Native Samsung</a></li></ul></details> | `https://raw.githubusercontent.com/Re-Malwack/hosts/main/blocklists/trackers-samsung` |
| **Trackers (Oppo Realme)** | `287,334` | <details><summary>View Sources</summary><ul><li><a href='https://raw.githubusercontent.com/r-a-y/mobile-hosts/refs/heads/master/AdguardTracking.txt'>Adguard Tracking</a></li><li><a href='https://blocklistproject.github.io/Lists/tracking.txt'>BlocklistProject Tracking</a></li><li><a href='https://raw.githubusercontent.com/hagezi/dns-blocklists-legacy/main/hosts/native.oppo-realme.txt'>Hagezi Native Oppo/Realme</a></li></ul></details> | `https://raw.githubusercontent.com/Re-Malwack/hosts/main/blocklists/trackers-oppo-realme` |
| **Trackers (Vivo)** | `287,334` | <details><summary>View Sources</summary><ul><li><a href='https://raw.githubusercontent.com/r-a-y/mobile-hosts/refs/heads/master/AdguardTracking.txt'>Adguard Tracking</a></li><li><a href='https://blocklistproject.github.io/Lists/tracking.txt'>BlocklistProject Tracking</a></li><li><a href='https://raw.githubusercontent.com/hagezi/dns-blocklists-legacy/main/hosts/native.vivo.txt'>Hagezi Native Vivo</a></li></ul></details> | `https://raw.githubusercontent.com/Re-Malwack/hosts/main/blocklists/trackers-vivo` |
| **Trackers (Huawei)** | `287,334` | <details><summary>View Sources</summary><ul><li><a href='https://raw.githubusercontent.com/r-a-y/mobile-hosts/refs/heads/master/AdguardTracking.txt'>Adguard Tracking</a></li><li><a href='https://blocklistproject.github.io/Lists/tracking.txt'>BlocklistProject Tracking</a></li><li><a href='https://raw.githubusercontent.com/hagezi/dns-blocklists-legacy/main/hosts/native.huawei.txt'>Hagezi Native Huawei</a></li></ul></details> | `https://raw.githubusercontent.com/Re-Malwack/hosts/main/blocklists/trackers-huawei` |
<!-- BLOCKLISTS_TABLE_END -->

> [!NOTE]  
> `.count` files are also available for each list by appending `.count` to the raw link (e.g. `https://raw.githubusercontent.com/Re-Malwack/hosts/main/hosts/lite.count`). These files contain a breakdown of domain counts per upstream source, which can be useful for stats tracking or parsing.

> [!NOTE]
> Thanks to every host source provider, full credits can be found in the main module repository.
