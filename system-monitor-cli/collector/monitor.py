import psutil
import time
import json
from datetime import datetime


# =========================
# MÉTRICAS DEL SISTEMA
# =========================
def collect_metrics():
    cpu = psutil.cpu_percent(interval=None)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent

    net = psutil.net_io_counters()
    net_sent = net.bytes_sent
    net_recv = net.bytes_recv

    # Top 5 procesos por CPU
    processes = []
    for p in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            processes.append(p.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    top_processes = sorted(
        processes,
        key=lambda x: x['cpu_percent'] or 0,
        reverse=True
    )[:5]

    data = {
        "timestamp": datetime.now().isoformat(),
        "cpu": cpu,
        "ram": ram,
        "disk": disk,
        "network": {
            "bytes_sent": net_sent,
            "bytes_recv": net_recv
        },
        "top_processes": top_processes
    }

    return data


import os

# =========================
# LOGGING
# =========================
def write_log(data):
    os.makedirs("logs", exist_ok=True)
    with open("logs/system.log", "a") as file:
        file.write(json.dumps(data) + "\n")


# =========================
# LOOP PRINCIPAL
# =========================
def main():
    print("🟢 System Monitor started...")

    # warm-up CPU (importante para psutil)
    psutil.cpu_percent(interval=None)

    while True:
        try:
            data = collect_metrics()

            # Output legible en terminal
            print(
                f"[CPU {data['cpu']}% | RAM {data['ram']}% | DISK {data['disk']}%]"
            )

            write_log(data)

            time.sleep(3)

        except KeyboardInterrupt:
            print("\n🔴 Monitor stopped manually.")
            break

        except Exception as e:
            print(f"⚠️ Error: {e}")
            time.sleep(3)


# =========================
# ENTRY POINT
# =========================
if __name__ == "__main__":
    main()
