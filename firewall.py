from netfilterqueue import NetfilterQueue
from scapy.all import *
import re

def is_http_packet(packet):
    try:
        http_payload = packet[Raw].load.decode(errors='ignore')
        return http_payload.startswith(('GET', 'POST', 'PUT', 'DELETE', 'HEAD'))
    except Exception:
        return False

def analyze_packet(pkt):
    scapy_pkt = IP(pkt.get_payload())
    
    if scapy_pkt.haslayer(TCP):
        if is_http_packet(scapy_pkt):
            print(f"HTTP packet detected on port:{scapy_pkt[TCP].dport}")
            pkt.drop()
            return

        elif scapy_pkt.haslayer(Raw):
            payload = scapy_pkt[Raw].load
            # Check for TLS Client Hello (TLS Handshake type 22 and various versions)
            tls_versions = [b'\x16\x03\x00', b'\x16\x03\x01', b'\x16\x03\x02', b'\x16\x03\x03', b'\x16\x03\x04']
            for version in tls_versions:
                if payload.startswith(version):
                    print(f"HTTPS packet detected on port:{scapy_pkt[TCP].dport}")
                    version_info = {
                        b'\x16\x03\x00': "SSL 3.0",
                        b'\x16\x03\x01': "TLS 1.0",
                        b'\x16\x03\x02': "TLS 1.1",
                        b'\x16\x03\x03': "TLS 1.2",
                        b'\x16\x03\x04': "TLS 1.3"
                    }
                    print(f"TLS Version: {version_info.get(version, 'Unknown')}")
                    pkt.accept()
                    return
    
    pkt.accept()

nfqueue = NetfilterQueue()
nfqueue.bind(1, analyze_packet)

try:
    print("Starting packet inspection")
    nfqueue.run()
except KeyboardInterrupt:
    print("Stopping packet inspection")

nfqueue.unbind()

