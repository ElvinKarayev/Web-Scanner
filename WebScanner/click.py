import requests
import time
import sys

def clickjacking_scan(domain):
    try:
        headers = requests.get("http://" + domain, timeout=5).headers

        if "X-Frame-Options" in headers:
            print(f"\n{domain} clickjacking zəifliyinə həssas deyil.")
        else:
            print(f"\n{domain} clickjacking zəifliyinə həssasdır.")

    except requests.Timeout:
        print("Istək sayısı limiti aşdı")

    except requests.RequestException as e:
        if isinstance(e, requests.ConnectionError) and isinstance(e.args[0], requests.packages.urllib3.exceptions.NewConnectionError):
            print("Xəta baş verdi: Domain tapılmadı. Xahiş olunurki mümkün bir domain daxil edin.")
        else:
            print("Xəta baş verdi: Bu domain tapılmadı.")

def loading_animation(seconds):
    for _ in range(seconds * 5):
        sys.stdout.write("\r" + "Gözləyin" + "." * ((_ % 3) + 1))
        sys.stdout.flush()
        time.sleep(0.4)

def loading_animation_start(seconds):
    chars = "/-\|"
    for _ in range(seconds * 5):
        sys.stdout.write("\r" + "Program başladılır. Zəhmət olmazsa gözləyin " + chars[_ % len(chars)])
        sys.stdout.flush()
        time.sleep(0.4)

def main():
    seconds = 3
    loading_animation_start(seconds)

    domain = input("\n[*] domaini daxil edin: ")
    domain = domain.strip()

    loading_animation(seconds)

    clickjacking_scan(domain)


if __name__ == "__main__":
    main()
