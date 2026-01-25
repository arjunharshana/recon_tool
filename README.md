# Automated Web Vulnerability Recon Tool 🛡️

A Python-based passive reconnaissance tool designed to automate the initial phases of web application security testing. This tool complements manual testing by quickly identifying technical stacks, security header gaps, and hidden directories.

## Features

- **Header Analysis**: Checks for missing security headers like CSP, X-Frame-Options, and HSTS.
- **Tech Stack Identification**: Detects CMS, frameworks, and server versions.
- **Crawler**: Extracts subdomains and internal/external links from the target.
- **Robots.txt Parser**: Scans for disallowed paths that might reveal sensitive directories.
<!-- - **Reporting**: Generates clean, actionable terminal output and saved reports. -->

## Prerequisites

- Python 3.9+
- VS Code

## Installation

1. ### **Clone the repository:**
   ```bash
   git clone https://github.com/arjunharshana/recon_tool.git
   cd recon_tool
   ```
2. ### **Environment Configuration**

   Open your terminal in the `recon_tool` folder and run:

   ```bash
   # Create the virtual env
   python -m venv venv

   # Activate the environment (use gitbash in terminal)
   source venv/Scripts/activate

   # Update pip
   python -m pip install --upgrade pip
   ```

3. ### **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. ### Run the script
   ```bash
   python main.py [target_url]
   ```
