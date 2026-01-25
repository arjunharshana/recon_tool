import argparse
import sys

from colorama import Fore, init

from modules.headers import check_headers
from modules.robots_parser import parse_robots

init(autoreset=True)


def print_banner():
    print(Fore.CYAN + "=" * 50)
    print(Fore.GREEN + "   AUTOMATED WEB RECON TOOL v1.0")
    print(Fore.CYAN + "=" * 50 + "\n")


def main():
    print_banner()

    # first we do argument parsing
    parser = argparse.ArgumentParser(description="Automated Web Recon Tool")
    parser.add_argument("url", help="Target URL for reconnaissance")

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    target_url = args.url

    # now we will validate the url
    if not target_url.startswith(("http://", "https://")):
        print(
            Fore.RED
            + "[!] Please provide a valid URL starting with http:// or https://"
        )
        sys.exit(1)

    print(Fore.YELLOW + f"[+] Starting reconnaissance on: {target_url}")
    print("-" * 50)

    # now here will come the module calls for web recon
    check_headers(target_url)
    print("-" * 50)
    parse_robots(target_url)

    print(Fore.YELLOW + f"[+] Reconnaissance completed on: {target_url}")


if __name__ == "__main__":
    main()
