from scapy.all import *
import requests
import json
import ipaddress

packets = {}

def select_DNS(pkt):
    pkt_time = pkt.sprintf('%sent.time%')
    try:
        dict = []
        # queries
        if DNSQR in pkt and pkt.dport == 53:
            domain = pkt.getlayer(DNS).qd.qname.decode() # .decode() gets rid of the b''
            print('Q - Time: ' + pkt_time + ' , source IP: ' + pkt[IP].src + ' , domain: ' + domain)
        # responses
        elif DNSRR in pkt and pkt.sport == 53:
            domain = pkt.getlayer(DNS).qd.qname.decode()
            print('R - Time: ' + pkt_time + ' , source IP: ' + pkt[IP].src + ' , domain: ' + domain)
    except:
        pass

def packet_callback(packet):
    data = {}
    if not packet.haslayer(IP):
        return
    if bothIP := packets.get(packet[IP].src + packet[IP].dst):
        if packet[IP].id in packets:
            return
        packets.append(packet[IP].id)
    else:
        packets[bothIP] = [packet[IP].id]
    data['time'] = packet.time
    data['srcIP'] = packet[IP].src
    data['dstIP'] = packet[IP].dst
    if packet[IP].proto == 1:
        data['proto'] = 'icmp'
    elif packet[IP].proto == 6:
        data['proto'] = 'tcp'
        data['srcPort'] = packet[IP].sport
        data['dstPort'] = packet[IP].dport
    elif packet[IP].proto == 17:
        data['proto'] = 'udp'
        data['srcPort'] = packet[IP].sport
        data['dstPort'] = packet[IP].dport
    if ipaddress.ip_address(data['srcIP']).is_global:
        data['srcIsGlobal'] = True
    if ipaddress.ip_address(data['dstIP']).is_global:
        data['dstIsGlobal'] = True
    if data.get('srcPort') in [80, 443] or data.get('dstPort') in [80, 443]:
        # packet.show()
        try:
            requests.post('http://localhost:5000/packet', json.dumps(data))
        except Exception as e:
            pass

sniff(iface='en0', prn=packet_callback)
