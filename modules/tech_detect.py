import re

import requests
from bs4 import BeautifulSoup
from colorama import Fore


def detect_tech_stack(url):
    print(Fore.CYAN + f"\n[*] Identifying Technology Stack for: {url}")
    print("-" * 60)

    try:
        response = requests.get(url, timeout=10)

        soup = BeautifulSoup(response.text, "html.parser")
        html_lower = response.text.lower()
        headers = response.headers
        detected_tech = {}

        def add_tech(name, version=None):
            # Avoid overwriting existing version info
            if name not in detected_tech or (version and detected_tech[name] is None):
                detected_tech[name] = version

        # find cms platforms
        cms_signatures = {
            "WordPress": ["wp-content", "wp-includes"],
            "Joomla": ["index.php?option=com_", "templates/"],
            "Drupal": ["/sites/default/files/", "/misc/drupal.js"],
            "Shopify": ["cdn.shopify.com", "myshopify.com"],
        }

        for cms, sigs in cms_signatures.items():
            if any(s in html_lower for s in sigs):
                add_tech(cms)

        # find javascript frameworks and libraries
        version_patterns = {
            "jQuery": r"jquery[.\-/@]?v?([0-9]+\.[0-9]+(?:\.[0-9]+)?)",
            "React": r"react[.\-/@]?v?([0-9]+\.[0-9]+(?:\.[0-9]+)?)",
            "Angular": r"angular[.\-/@]?v?([0-9]+\.[0-9]+(?:\.[0-9]+)?)",
            "Vue": r"vue[.\-/@]?v?([0-9]+\.[0-9]+(?:\.[0-9]+)?)",
            "Bootstrap": r"bootstrap[.\-/@]?v?([0-9]+\.[0-9]+(?:\.[0-9]+)?)",
        }

        # html asset analysis
        asset_urls = []
        for tag in soup.find_all(["script", "link"]):
            src = tag.get("src") or tag.get("href")
            if src:
                asset_urls.append(src)

        for url_str in asset_urls:
            # check version patterns
            for lib, pattern in version_patterns.items():
                match = re.search(pattern, url_str, re.IGNORECASE)
                if match:
                    add_tech(lib, match.group(1))

            # check for wordpress version if found in asset url
            if "ver=" in url_str or "v=" in url_str:
                wp_match = re.search(r"[?&](?:ver|v)=([0-9.]+)", url_str)
                if wp_match and "wp-" in url_str:
                    add_tech("WordPress", wp_match.group(1))

        # meta generator tag
        meta_gen = soup.find("meta", attrs={"name": "generator"})
        if meta_gen:
            content = meta_gen.get("content", "")
            add_tech("Meta Generator", content)

        # results
        print(Fore.GREEN + "\n[+] Technologies Detected:")
        if detected_tech:
            for tech, version in detected_tech.items():
                if version:
                    print(Fore.WHITE + f"    - {tech}: {version}")
                else:
                    print(Fore.WHITE + f"    - {tech}")
        else:
            print(Fore.YELLOW + "    No technologies detected.")

        return detected_tech

    except Exception as e:
        print(Fore.RED + f"[-] Error: {e}")
        return {}
