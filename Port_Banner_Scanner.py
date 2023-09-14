import socket
import threading
import time
import re

target_host = input("Enter the target host: ")

while True:
    port_range = input("Enter the port range (e.g., 1-100): ")
    if re.match(r"^\d+-\d+$", port_range):
        start_port, end_port = map(int, port_range.split('-'))
        break
    else:
        print("Invalid port range format. Please use the format 'start_port-end_port'.")

num_threads = 10
total_ports = end_port - start_port + 1

def scan_port(host, port):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        result = client.connect_ex((host, port))
        if result == 0:
            banner = grab_banner(client)
            print(f"[{host}] Port {port} is open: {banner}")
        client.close()
    except (socket.timeout, ConnectionRefusedError):
        pass

def grab_banner(client):
    try:
        banner = client.recv(1024)
        return banner.decode().strip()
    except Exception:
        return "Banner not available"

def scan_host(host):
    for port in range(start_port, end_port + 1):
        scan_port(host, port)

def countdown_timer():
    remaining_ports = total_ports
    start_time = time.time()
    while remaining_ports > 0:
        time_elapsed = time.time() - start_time
        remaining_time = (time_elapsed / (total_ports - remaining_ports + 1)) * remaining_ports
        print(f"Estimated time remaining: {remaining_time:.2f} seconds", end="\r")
        remaining_ports -= 1
        time.sleep(1)

def main():
    countdown_thread = threading.Thread(target=countdown_timer)
    countdown_thread.daemon = True 
    countdown_thread.start()

    scan_host(target_host)
    print("\nScan completed.")

if __name__ == "__main__":
    main()
