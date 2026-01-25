import requests
from colorama import Fore


def check_headers(url):
    print(Fore.CYAN + f"[*] Analyzing Security Headers for: {url}")

    # define the security headers to check
    security_headers = {
        "Content-Security-Policy": "Protects against XSS and injection attacks.",
        "X-Frame-Options": "Prevents Clickjacking (should be 'DENY' or 'SAMEORIGIN').",
        "Strict-Transport-Security": "Forces the use of HTTPS (HSTS).",
        "X-Content-Type-Options": "Prevents MIME-sniffing (should be 'nosniff').",
        "Referrer-Policy": "Controls how much referrer information is shared.",
        "Permissions-Policy": "Controls access to browser features and APIs.",
    }

    try:
        # fetch the headers from the target URL
        response = requests.get(url, timeout=10)
        headers = response.headers

        # tech stack fingerprinting
        print(Fore.YELLOW + "\n[*] Detected Technology:")
        tech_headers = [
            "Server",
            "X-Powered-By",
            "X-AspNet-Version",
            "X-Drupal-Cache",
            "Via",
            "X-Generator",
            "X-Cache",
        ]
        for tech_header in tech_headers:
            if tech_header in headers:
                print(
                    Fore.WHITE
                    + f"    > {tech_header}: "
                    + Fore.MAGENTA
                    + headers[tech_header]
                )
            else:
                print(Fore.WHITE + f"    > {tech_header}: " + Fore.RED + "Not Found")

        # check for security headers
        print(Fore.YELLOW + "\n[*] Security Headers Analysis:")
        missing_headers = []  # a list to keep track of missing headers

        for header, description in security_headers.items():
            if header in headers:
                print(
                    Fore.GREEN
                    + f"[+] {header} is present: {headers[header]} - {description}"
                )
            else:
                print(Fore.RED + f"[-] {header} is missing! - {description}")
                missing_headers.append(header)

        if missing_headers:
            print(
                Fore.YELLOW
                + f"[!] Missing security headers: {', '.join(missing_headers)}"
            )
        else:
            print(Fore.GREEN + "[+] All critical security headers are present.")

        # check for non-standard headers
        print(Fore.YELLOW + "\n[*] Non-Standard Headers:")
        custom_headers = False

        for h, v in headers.items():
            if (
                h.startswith("X-")
                and h not in security_headers
                and h not in tech_headers
            ):
                print(Fore.WHITE + f"    > {h}: " + Fore.CYAN + v)
                custom_headers = True
        if not custom_headers:
            print(Fore.GREEN + "    > No non-standard headers found.")

    except requests.RequestException as e:
        print(Fore.RED + f"[!] Error fetching headers: {e}")
