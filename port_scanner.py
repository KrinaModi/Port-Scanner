import socket
import csv
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

import time

start_time = time.time()

open_ports = []
lock = Lock()

target = input("Enter target IP or domain: ")
start_port = int(input("Start Port: "))
end_port = int(input("End Port: "))

print(f"\nScanning {target}...\n")


def scan_port(port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.5)

            if sock.connect_ex((target, port)) == 0:
                try:
                    service = socket.getservbyport(port)
                except OSError:
                    service = "Unknown"

                with lock:
                    open_ports.append((port, service))

                print(f"Port {port:<5} OPEN ({service})")

    except Exception:
        pass


with ThreadPoolExecutor(max_workers=100) as executor:
    executor.map(scan_port, range(start_port, end_port + 1))

# Sort results
open_ports.sort()

# Save CSV report
with open("results.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Port", "Service"])
    writer.writerows(open_ports)

print("\n========== Scan Summary ==========")
print(f"Target       : {target}")
print(f"Ports Scanned: {end_port - start_port + 1}")
print(f"Open Ports   : {len(open_ports)}")
print("Report Saved : results.csv")
end_time = time.time()

print(f"Scan Time: {end_time - start_time:.2f} seconds")