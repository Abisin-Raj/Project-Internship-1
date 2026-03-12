import re
import pandas as pd
import matplotlib
matplotlib.use('Agg') # Using a non-interactive backend to avoid hanging!
import matplotlib.pyplot as plt
from collections import Counter
import os

# These are the files we need for the project
# Make sure they are in the same folder!
AUTH_LOG = 'auth.log'        # ssh logs
ACCESS_LOG = 'access.log'    # apache logs
BLACKLIST_FILE = 'blacklist.txt'
REPORT_FILE = 'security_report.md'

# Regex Patterns - Updated to be more flexible for "illegal user" and different IP formats
# SSH pattern: handles "Failed password for root" and "Failed password for illegal user test"
SSH_FAILED_PATTERN = r'(?P<timestamp>\w{3}\s+\d+\s+\d{2}:\d{2}:\d{2}).*Failed password for (?:illegal user |invalid user )?(?P<user>\S+) from (?P<ip>\S+)'
SSH_SUCCESS_PATTERN = r'(?P<timestamp>\w{3}\s+\d+\s+\d{2}:\d{2}:\d{2}).*Accepted password for (?P<user>\S+) from (?P<ip>\S+)'

# Apache pattern: handles standard IPs and placeholders like x.x.x.90
APACHE_PATTERN = r'(?P<ip>\S+) - - \[(?P<timestamp>.*?)\] "(?P<method>\w+) (?P<path>\S+) .*?" (?P<status>\d+) (?P<size>\d+)'

def load_blacklist():
    # loading the bad IPs from the file
    if os.path.exists(BLACKLIST_FILE):
        with open(BLACKLIST_FILE, 'r') as f:
            # removing whitespace just in case
            return [line.strip() for line in f if line.strip()]
    return []

def parse_auth_log():
    # this function reads the ssh log and finds failed/success logins
    data = []
    if os.path.exists(AUTH_LOG):
        with open(AUTH_LOG, 'r') as f:
            for line in f:
                failed_match = re.search(SSH_FAILED_PATTERN, line)
                if failed_match:
                    entry = failed_match.groupdict()
                    entry['type'] = 'SSH_FAILED'
                    data.append(entry)
                else:
                    success_match = re.search(SSH_SUCCESS_PATTERN, line)
                    if success_match:
                        entry = success_match.groupdict()
                        entry['type'] = 'SSH_SUCCESS'
                        data.append(entry)
    # converting to dataframe because its easier to use pandas
    return pd.DataFrame(data)

def parse_access_log():
    # same thing but for apache web logs
    data = []
    if os.path.exists(ACCESS_LOG):
        with open(ACCESS_LOG, 'r') as f:
            for line in f:
                match = re.search(APACHE_PATTERN, line)
                if match:
                    entry = match.groupdict()
                    entry['status'] = int(entry['status']) # must be int for checking status codes
                    data.append(entry)
    return pd.DataFrame(data)

def analyze_logs():
    print("--- Starting Log Analysis ---")
    print("Hold on, processing logs...") # user feedback lol
    
    blacklist = load_blacklist()
    auth_df = parse_auth_log()
    access_df = parse_access_log()
    
    incidents = [] # list to store all the bad stuff we find
    
    # 1. SSH Brute Force Detection
    # If an IP fails 5 times, its probably a bot or someone trying to guess passwords
    if not auth_df.empty:
        failed_attempts = auth_df[auth_df['type'] == 'SSH_FAILED']
        counts = failed_attempts['ip'].value_counts()
        for ip, count in counts.items():
            if count >= 5:
                incidents.append(f"[CRITICAL] SSH Brute-Force detected from {ip} ({count} failed attempts)")

    # 2. Apache Scanning Detection
    # Lookng for 404/403 errors. 3 or more is suspicious
    if not access_df.empty:
        scanners = access_df[access_df['status'].isin([404, 403])]
        counts = scanners['ip'].value_counts()
        for ip, count in counts.items():
            if count >= 3:
                incidents.append(f"[WARNING] Directory Scanning detected from {ip} ({count} error responses)")

    # 3. DoS Detection
    # Too many requests from one person
    if not access_df.empty:
        counts = access_df['ip'].value_counts()
        for ip, count in counts.items():
            if count >= 10: # threshold might be too low? maybe 100 for real server
                incidents.append(f"[CRITICAL] Potential DoS attack from {ip} ({count} requests)")

    # 4. Blacklist Check
    # Checking if any IP in our logs is in the blacklist.txt
    all_ips = set()
    if not auth_df.empty: all_ips.update(auth_df['ip'].unique())
    if not access_df.empty: all_ips.update(access_df['ip'].unique())
    
    for ip in all_ips:
        if ip in blacklist:
            incidents.append(f"[ALERT] Malicious IP detected from Blacklist: {ip}")

    # Generate the Report
    print("Creating the security report...")
    with open(REPORT_FILE, 'w') as f:
        f.write("# Intrusion Detection Security Report\n\n")
        f.write(f"Date of analysis: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("## Summary of Incidents found\n")
        if incidents:
            for incident in incidents:
                f.write(f"- {incident}\n")
        else:
            f.write("Everything looks okay! No major incidents detected.\n")
            
        f.write("\n## Statistics\n")
        if not auth_df.empty:
            f.write(f"- Total SSH failed attempts: {len(auth_df[auth_df['type'] == 'SSH_FAILED'])}\n")
        if not access_df.empty:
            f.write(f"- Total Apache requests processed: {len(access_df)}\n")

    print(f"Done! Report is at: {REPORT_FILE}")

    # Visualization - hope this works!
    if not access_df.empty:
        # 1. Bar chart by IP
        plt.figure(figsize=(12, 5))
        plt.subplot(1, 2, 1)
        access_df['ip'].value_counts().plot(kind='bar', color='skyblue')
        plt.title('Requests by IP')
        plt.xlabel('IP Address')
        plt.ylabel('Count')
        plt.xticks(rotation=45)

        # 2. Timeline (by time)
        # We need to convert timestamp to datetime first
        try:
            # Apache format: 24/Mar/2026:09:00:05 +0530
            access_df['dt'] = pd.to_datetime(access_df['timestamp'], format='%d/%b/%Y:%H:%M:%S %z')
            plt.subplot(1, 2, 2)
            access_df.set_index('dt').resample('1min').size().plot(kind='line', marker='o', color='green')
            plt.title('Requests over Time (1min intervals)')
            plt.xlabel('Time')
            plt.ylabel('Count')
        except Exception as e:
            print(f"Oops, couldn't plot timeline: {e}")

        plt.tight_layout()
        plt.savefig('request_analysis.png')
        plt.close() # Close to be safe
        print("Analysis visualization saved as: request_analysis.png")

if __name__ == "__main__":
    analyze_logs()
