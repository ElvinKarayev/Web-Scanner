import re
from datetime import datetime
import os

def analyze_logs(log_file_path):
    with open(log_file_path, 'r') as file:
        log_lines = file.readlines()

        sshd_pattern = re.compile(r'(\w{3} \d+ \d+:\d+:\d+) .*?sshd\(pam_unix\)\[\d+\]: authentication failure; logname= uid=0 euid=0 tty=NODEVssh ruser= rhost=(\S+).*?user=([^\s]+)')
        ftpd_pattern = re.compile(r'(\w{3} \d+ \d+:\d+:\d+) .*?ftpd\[\d+\]: connection from (\S+) \((\S+)\) at (\w{3} \w{3} \d+ \d+:\d+:\d+ \d+)')
        sudo_pattern = re.compile(r'(\w{3} \d{1,2} \d{2}:\d{2}:\d{2}) (\S+) sudo: (\S+) : TTY=(\S+) ; PWD=(\S+) ; USER=(\S+) ; COMMAND=(.+)')

        alerts = {
            'FTP': [],
            'SSH': [],
            'Sudo': [],
        }

        for line in log_lines:
            match_ftpd = ftpd_pattern.search(line)
            if match_ftpd:
                date_str, ip_address, host, connection_time = match_ftpd.groups()
                current_year = datetime.now().year
                date_obj = datetime.strptime(f"{date_str} {current_year}", "%b %d %H:%M:%S %Y")
                formatted_date = date_obj.strftime("%Y-%m-%d %H:%M:%S")
                alerts['FTP'].append(
                    f"ALERT: FTP Connection - Date: {formatted_date}, IP: {ip_address}, Host: {host}, Connection Time: {connection_time}")

            match_sshd = sshd_pattern.search(line)
            if match_sshd:
                date_str, ip_address, username = match_sshd.groups()
                current_year = datetime.now().year
                date_obj = datetime.strptime(f"{date_str} {current_year}", "%b %d %H:%M:%S %Y")
                formatted_date = date_obj.strftime("%Y-%m-%d %H:%M:%S")
                alerts['SSH'].append(
                    f"ALERT: SSH Authentication failure - Date: {formatted_date}, IP: {ip_address}, Username: {username}")

            match_sudo = sudo_pattern.search(line)
            if match_sudo:
                date_str,process_id, user, tty, pwd, username, command = match_sudo.groups()
                current_year = datetime.now().year
                date_obj = datetime.strptime(f"{date_str} {current_year}", "%b %d %H:%M:%S %Y")
                formatted_date = date_obj.strftime("%Y-%m-%d %H:%M:%S")
                alerts['Sudo'].append(
                    f"ALERT: Sudo Command detected - Date: {formatted_date}, User: {user}, Command: {command}")

    return alerts
def each_user_sudo(alerts,output_folder="output"):
    sudo_user_files={}
    for alert in alerts.get('Sudo', []):
        user = alert.split(",")[1].split(":")[1].strip()
        if user not in sudo_user_files:
            sudo_user_files[user] = open(os.path.join(output_folder, f"{user}_sudo.log"), 'w')
        sudo_user_files[user].write(alert + '\n')
    for file in sudo_user_files.values():
        file.close()

def write_to_file(alerts, output_folder="output"):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for alert_type, alert_list in alerts.items():
        output_file = os.path.join(output_folder, f"{alert_type.lower()}_alerts.log")
        with open(output_file, 'w') as file:
            for alert in alert_list:
                file.write(alert + '\n')