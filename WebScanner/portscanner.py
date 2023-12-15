import socket
import threading
import subprocess

def is_alive(target_host):
    try:
        result = subprocess.run(["ping", "-n", "4", target_host], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)#helelik windows ucundu bu deyisilmelidi linux ucun
        if "Sent = 4, Received = 4" in result.stdout:#buda hemcinin
            return True
    except:
        pass
    return False

def port_scan(target_host, start_port, end_port):
    open_ports = []

    def scan(port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((target_host, port))
            if result == 0:
                print(f"Port {port} açıqdır")
                open_ports.append(port)
            sock.close()
        except:
            pass

    if not is_alive(target_host):
        print("Hədəf Server Aktiv Deyil.")
        return

    threads = []
    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=scan, args=(port,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("Açıq portlar:", open_ports)

if __name__ == "__main__":
    target_host = input("Hədəf İp: ")
    start_port = int(input("Başlanğıc Portu Yaz: "))
    end_port = int(input("Bitiş Portu Yaz: "))

    port_scan(target_host, start_port, end_port)
