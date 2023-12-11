import re
from datetime import datetime

def analyze_logs(log_file_path):
    with open(log_file_path, 'r') as file:
        log_lines = file.readlines()

    sshd_pattern = re.compile(r'(\w{3} \d+ \d+:\d+:\d+) .*?sshd\(pam_unix\)\[\d+\]: authentication failure; logname= uid=0 euid=0 tty=NODEVssh ruser= rhost=(\S+).*?user=(\S+)')
    ftpd_pattern = re.compile(r'(\w{3} \d+ \d+:\d+:\d+) .*?ftpd.*?(\d+\.\d+\.\d+\.\d+).*?Login failed')
    ftpd_pattern2 = re.compile(r'(\w{3} \d{1,2} \d{2}:\d{2}:\d{2}) .* ftpd\[\d+\]: connection from (\d+\.\d+\.\d+\.\d+) \((.*?)\) at \w{3} \w{3} \d{1,2} \d{2}:\d{2}:\d{2} \d{4}')


    ssh_alert = []
    ftp_alert = []
    for line in log_lines:
        match_sshd = sshd_pattern.search(line)
        if match_sshd:
            date_str, ip_address, username = match_sshd.groups()
            current_year = datetime.now().year
            date_obj = datetime.strptime(f"{date_str} {current_year}", "%b %d %H:%M:%S %Y")
            formatted_date = date_obj.strftime("%Y-%m-%d %H:%M:%S")
            ssh_alert.append(f"ALERT: SSH Authentication failure - Date: {formatted_date}, IP: {ip_address}, Username: {username}")

        # ftpd log analizi
        match_ftpd = ftpd_pattern.search(line)
        if match_ftpd:
            date_str, ip_address = match_ftpd.groups()
            current_year = datetime.now().year
            date_obj = datetime.strptime(f"{date_str} {current_year}", "%b %d %H:%M:%S %Y")
            formatted_date = date_obj.strftime("%Y-%m-%d %H:%M:%S")
            ftp_alert.append(f"ALERT: FTP Authentication failure - Date: {formatted_date}, IP: {ip_address}")
        else:
            match_ftpd=ftpd_pattern2.search(line)
            if match_ftpd:
                date_str, ip_address, domain_name = match_ftpd.groups()
                current_year = datetime.now().year
                date_obj = datetime.strptime(f"{date_str} {current_year}", "%b %d %H:%M:%S %Y")
                formatted_date = date_obj.strftime("%Y-%m-%d %H:%M:%S")
                ftp_alert.append(f"ALERT: FTP Connection - Date: {formatted_date}, IP: {ip_address}, Domain: {domain_name}")
    return (ssh_alert,ftp_alert)

def write_to_file(alerts, output_file):
    if alerts:
        with open(output_file, 'w') as file:
            for alert in alerts:
                file.write(alert + '\n')


