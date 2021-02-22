import socketio
from scapy.all import sniff, IP
import ipaddress
import json
import threading

from config import SOCKETIO_HOST, EXERCISE_ID, INTERFACES, ALLOW_PROTOCOLS, ALLOW_PORTS, PRIVACY_MODE, USER_ID


class SocketIOClient:
    def __init__(self, host, exercise_id):
        self.host = host
        self.exercise_id = exercise_id
        self.sio = socketio.Client()
        self.background_task = None

    def connect(self):
        self.sio.connect(f'{self.host}?exercise_id={self.exercise_id}&is_forwarder=true')

    def send_packet(self, data):
        self.sio.emit('packet', json.dumps({
            'exercise_id': self.exercise_id,
            'packet': data
        }))


class Scapy:
    def __init__(self, iface):
        self.iface = iface
        self.exists_packets = {}
        self.send_packet = None

    def start(self):
        sniff(iface=self.iface, prn=self.packet_callback)

    def packet_callback(self, packet):
        data = {}
        if not packet.haslayer(IP):
            return
        if len(self.exists_packets.values()) > 100:
            self.exists_packets = {}
        if bothIP := self.exists_packets.get(packet[IP].src + packet[IP].dst):
            if packet[IP].id in self.exists_packets:
                return
            self.exists_packets.append(packet[IP].id)
        else:
            self.exists_packets[bothIP] = [packet[IP].id]
        data['time'] = packet.time
        data['srcIP'] = packet[IP].src
        data['dstIP'] = packet[IP].dst
        if packet[IP].proto == 1:
            data['proto'] = 'icmp'
        elif packet[IP].proto in [6, 17]:
            data['proto'] = 'tcp' if packet[IP].proto == 6 else 'udp'
            try:
                data['srcPort'] = packet[IP].sport
                data['dstPort'] = packet[IP].dport
            except Exception as e:
                print(e)
                return
        if ipaddress.ip_address(data['srcIP']).is_global:
            data['srcIsGlobal'] = True
        if ipaddress.ip_address(data['dstIP']).is_global:
            data['dstIsGlobal'] = True
        if data.get('proto') in ALLOW_PROTOCOLS and (
                data.get('proto') == 'icmp' or
                data.get('srcPort') in ALLOW_PORTS or
                data.get('dstPort') in ALLOW_PORTS):
            try:
                if not PRIVACY_MODE:
                    self.send_packet(data)
                    return
                elif not (USER_ID and (data.get('srcIsGlobal') or data.get('dstIsGlobal'))):
                    return
                self.send_packet({
                    "userId": USER_ID,
                    "srcPort": data.get('srcPort'),
                    "dstPort": data.get('dstPort')
                })
            except Exception as e:
                print(e)


if __name__ == '__main__':
    sio_client = SocketIOClient(SOCKETIO_HOST, EXERCISE_ID)
    sio_client.connect()

    for iface in INTERFACES:
        scapy = Scapy(iface)
        scapy.send_packet = sio_client.send_packet
        thread = threading.Thread(target=scapy.start)
        try:
            thread.start()
        except Exception as e:
            print(e)
