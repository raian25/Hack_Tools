from scapy.all import *

def nmap_detector(pkt):
    if pkt.haslayer(IP):
        ip_src = pkt[IP].src
        ip_dst = pkt[IP].dst

        if pkt.haslayer(TCP):
            tcp_flags = pkt[TCP].flags
            tcp_sport = pkt[TCP].sport
            tcp_dport = pkt[TCP].dport

            if tcp_flags == 2 and pkt[TCP].window == 1024:
                print(f"Nmap TCP SYN scan detected from {ip_src} to {ip_dst}")

            elif tcp_flags == 18 and pkt.haslayer(Raw):
                try:
                    payload = pkt[Raw].load.decode('utf-8')
                    if "Nmap" in payload and "Version:" in payload:
                        print(f"Nmap TCP version detection scan detected from {ip_src} to {ip_dst}")
                except UnicodeDecodeError:
                    pass

        elif pkt.haslayer(UDP):
            udp_sport = pkt[UDP].sport
            udp_dport = pkt[UDP].dport

            if pkt.haslayer(Raw):
                try:
                    payload = pkt[Raw].load.decode('utf-8')
                    if "Nmap" in payload and "UDP Scan" in payload:
                        print(f"Nmap UDP scan detected from {ip_src} to {ip_dst}")
                except UnicodeDecodeError:
                    pass

def main():
    print("Scan attempts will be listed bellow.")
    sniff(prn=nmap_detector, filter="tcp or udp", store=0)

if __name__ == "__main__":
    main()
