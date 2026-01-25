from urllib.robotparser import RobotFileParser

import requests
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

        # check if robots.txt exists
        if "html" in response.headers.get("Content-Type", "").lower():
            print(
                Fore.YELLOW
                + "[!] Warning: Server returned HTML instead of a plain text robots.txt"
            )
            return []

        if response.status_code == 200:
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

        else:
            print(
                Fore.RED + "[-] robots.txt not found (HTTP Status Code: "
                f"{response.status_code})"
            )

    except requests.RequestException as e:
        print(Fore.RED + f"[!] Error fetching robots.txt: {e}")
        return []
