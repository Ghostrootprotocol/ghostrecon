GhostRecon is an automated recon tool that uses Nmap, Nikto, Sublist3r, httprobe, and FFUF to gather information about a target. It is designed for ethical hackers and cybersecurity learners.

## Tools Used

- Nmap – Port scanning
- Nikto – Web vulnerability scanning
- Sublist3r – Subdomain enumeration
- httprobe – Check which subdomains are alive
- FFUF – Directory fuzzing

## Requirements

Make sure these tools are installed and available in your terminal:

- Python 3
- Nmap
- Nikto
- Sublist3r
- FFUF
- httprobe

## Installation

- git clone https://github.com/ghostrootprotocol/ghostrecon.git
- cd ghostrecon
- chmod +x ghostrecon.py

## Usage

python3 ghostrecon.py <target>

example: python3 ghostrecon.py target.com

## Output

All results will be saved in a folder named like this:

recon_example_com_20250712_143522/
- nmap.txt
- nikto.txt
- subdomains.txt
- live_subdomains.txt
- ffuf_main.json
- ffuf_main.log
- ffuf_subdomain.json
- ffuf_subdomain.log

P.S: This tool is for educational and authorized use only. Only to be use in permitted services.

## Made by ghostrootprotocol
