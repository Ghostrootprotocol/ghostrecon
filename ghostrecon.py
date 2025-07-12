#!/usr/bin/env python3
"""
GhostRecon: Automated Reconnaissance Tool
Uses: nmap, nikto, sublist3r, httprobe, ffuf
Outputs consolidated results in a timestamped directory
"""

import os
import subprocess
import datetime
import sys

def run_cmd(cmd, output_file):
    """
    Runs a shell command and writes stdout+stderr to output_file in output_dir.
    """
    print(f"[+] Running: {cmd}")
    out_path = os.path.join(output_dir, output_file)
    with open(out_path, "w") as f:
        subprocess.run(cmd, shell=True, stdout=f, stderr=subprocess.STDOUT)

def run_httprobe():
    """
    Filters live subdomains from subdomains.txt using httprobe.
    """
    subdomains_file = os.path.join(output_dir, "subdomains.txt")
    live_file = os.path.join(output_dir, "live_subdomains.txt")
    print("[+] Running httprobe on found subdomains...")
    with open(live_file, "w") as live_out:
        subprocess.run(f"cat {subdomains_file} | httprobe", shell=True, stdout=live_out, stderr=subprocess.STDOUT)

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <target domain or IP>")
        sys.exit(1)

    target = sys.argv[1]
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    global output_dir
    output_dir = f"recon_{target.replace('.', '_')}_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)

    # 1. Nmap scan
    run_cmd(f"nmap -sS -sV -sC -T4 {target}", "nmap.txt")

    # 2. Nikto scan
    run_cmd(f"nikto -h {target}", "nikto.txt")

    # 3. Subdomain enumeration with Sublist3r
    run_cmd(f"sublist3r -d {target} -o {os.path.join(output_dir, 'subdomains.txt')}", "sublist3r.log")

    # 4. Filter live subdomains with httprobe
    run_httprobe()

    # 5. Directory fuzzing on main target
    run_cmd(
        f"ffuf -u http://{target}/FUZZ -w /usr/share/wordlists/dirb/common.txt "
        f"-of json -o {os.path.join(output_dir, 'ffuf_main.json')}",
        "ffuf_main.log"
    )

    # 6. Fuzz live subdomains
    live_file = os.path.join(output_dir, "live_subdomains.txt")
    if os.path.exists(live_file):
        with open(live_file) as f:
            subs = [line.strip() for line in f if line.strip()]
        for sub in subs:
            domain = sub.replace('http://', '').replace('https://', '')
            json_name = f"ffuf_{domain}.json"
            log_name = f"ffuf_{domain}.log"
            cmd = (
                f"ffuf -u http://{domain}/FUZZ -w /usr/share/wordlists/dirb/common.txt "
                f"-of json -o {os.path.join(output_dir, json_name)}"
            )
            run_cmd(cmd, log_name)

    print(f"[+] Recon complete. Results in: {output_dir}")

if __name__ == '__main__':
    main()
