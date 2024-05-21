import os
import subprocess

def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    if process.returncode != 0:
        raise Exception(f"Command failed with error: {err.decode().strip()}")
    return out.decode().strip()

def gather_subdomains(domain):
    # Use subfinder to gather subdomains
    subfinder_command = f"subfinder -d {domain} -all -o subfinder.txt"
    print(f"Running: {subfinder_command}")
    run_command(subfinder_command)

    # Use amass to gather subdomains
    amass_command = f"amass enum -d {domain} -o amass.txt"
    print(f"Running: {amass_command}")
    run_command(amass_command)

    # Combine and deduplicate subdomains
    combine_command = "cat subfinder.txt amass.txt | sort | uniq > subdomain.txt"
    print(f"Running: {combine_command}")
    run_command(combine_command)

def check_live_subdomains():
    # Use httpx to check live subdomains
    httpx_command = "httpx -l subdomain.txt -o live_sub.txt"
    print(f"Running: {httpx_command}")
    run_command(httpx_command)

def find_endpoints():
    # Use waybackurls to find endpoints
    wayback_command = "cat subfinder.txt | waybackurls > wayback.txt"
    print(f"Running: {wayback_command}")
    run_command(wayback_command)

def take_screenshots():
    # Use aquatone to take screenshots
    aquatone_command = "cat live_sub.txt | aquatone -out screenshot"
    print(f"Running: {aquatone_command}")
    run_command(aquatone_command)

if __name__ == "__main__":
    domain = input("Enter the domain to scan: ")
    gather_subdomains(domain)
    check_live_subdomains()
    find_endpoints()
    
    use_aquatone = input("Do you want to use Aquatone for taking screenshots? (yes/no): ").strip().lower()
    if use_aquatone == "yes":
        take_screenshots()
    else:
        print("Skipping Aquatone screenshots.")

    print("Reconnaissance process completed.")
