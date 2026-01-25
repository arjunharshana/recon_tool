import requests
from bs4 import BeautifulSoup
from colorama import Fore
from urllib.parse import urljoin, urlparse


def crawl_target(url):
    print(Fore.CYAN + f"[*] Starting crawl for: {url}")
    print("-" * 50)

    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        interal_links = set()
        external_links = set()
        subdomains = set()

        target_domain = urlparse(url).netloc

        for tag in soup.find_all("a", href=True):
            link = tag["href"]
            full_link = urljoin(url, link)
            parsed_link = urlparse(full_link)

            if parsed_link.scheme not in ["http", "https"]:
                continue

            if target_domain in parsed_link.netloc:
                interal_links.add(full_link)

                if parsed_link.netloc != target_domain:
                    subdomains.add(parsed_link.netloc)
            else:
                external_links.add(full_link)

        print(Fore.GREEN + f"[+] Found {len(interal_links)} internal links.")
        print(Fore.GREEN + f"[+] Found {len(external_links)} external links.")

        if subdomains:
            print(Fore.RED + f"    > Subdomains Discovered: {len(subdomains)}")
            for sub in subdomains:
                print(Fore.RED + f"      - {sub}")

        return {
            "internal_links": list(interal_links),
            "external_links": list(external_links),
            "subdomains": list(subdomains),
        }

    except requests.RequestException as e:
        print(Fore.RED + f"[-] Error during crawl: {e}")
        return None
