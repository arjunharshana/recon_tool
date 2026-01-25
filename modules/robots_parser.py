from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup
from colorama import Fore


def parse_robots(url):
    print(Fore.CYAN + f"[*] Analyzing robots.txt for: {url}")

    # construct the robots.txt URL
    if url.endswith("/"):
        robots_url = url + "robots.txt"
    else:
        robots_url = url + "/robots.txt"

    try:
        # fetch the robots.txt file
        response = requests.get(robots_url, timeout=10)
        content_type = response.headers.get("Content-Type", "").lower()

        if response.status_code == 200 and "text/plain" in content_type:
            print(Fore.GREEN + "[+] robots.txt found!")
            print(Fore.YELLOW + "\n[robots.txt content]:\n")
            print(Fore.WHITE + response.text)

            # parse the robots.txt content
            rp = RobotFileParser()
            rp.parse(response.text.splitlines())

            keywords = ["admin", "backup", "config", "dev", "test", "api", "secret"]

            # display disallowed paths
            disallowed_paths = []

            if rp.default_entry:
                for rule in rp.default_entry.rulelines():
                    if not rule.allowance:
                        path = rule.path
                        disallowed_paths.append(path)

                    if any(keyword in rule.path.lower() for keyword in keywords):
                        print(
                            Fore.MAGENTA
                            + f"[!] Suspicious path found in robots.txt: {rule.path}"
                        )
                    else:
                        continue

            if not disallowed_paths:
                print(Fore.YELLOW + "[*] No disallowed paths found in robots.txt.")

            return disallowed_paths
        elif "text/html" in content_type:
            print(
                Fore.RED
                + "[-] robots.txt appears to be HTML content, possible misconfiguration."
            )
            soup = BeautifulSoup(response.text, "html.parser")
            leaked_paths = set()

            tags = soup.find_all(["a", "link", "script", "img"])

            for tag in tags:
                path = tag.get("href") or tag.get("src")
                if path and path.startswith("/"):
                    leaked_paths.add(path)

            unique_leaked_paths = sorted(list(leaked_paths))
            if unique_leaked_paths:
                for path in unique_leaked_paths:
                    print(Fore.WHITE + f"    > Leaked Path: {path}")
            else:
                print(Fore.YELLOW + "[*] No leaked paths found in HTML content.")

            return unique_leaked_paths

        else:
            print(
                Fore.RED + "[-] Source not found (HTTP Status Code: "
                f"{response.status_code})"
            )

    except requests.RequestException as e:
        print(Fore.RED + f"[!] Error fetching robots.txt: {e}")
        return []
