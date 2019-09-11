import scapy
from scapy.all import *
from scapy.utils import PcapReader
import pandas as pd


class PcapFeature:
    def __init__(self):
        self.packets = None
        self.pcap_dict = dict()
        self.list = []
        self.create_dict()

    def create_dict(self):
        # Ether
        # pcap_dict.setdefault("Ether_dst", list())  # mac目标地址(str)
        # pcap_dict.setdefault("Ether_src", list())  # mac源地址(str)

        # IP
        self.pcap_dict.setdefault("IP_ihl", list())  # ip报头长度(int)
        self.pcap_dict.setdefault("IP_tos", list())  # ip tos 服务类别
        self.pcap_dict.setdefault("IP_len", list())  # ip len 报文长度(int)
        self.pcap_dict.setdefault("IP_id", list())  # ip id 标识(int)，用于在IP层对数据包进行分段的时候，表示数据包
        self.pcap_dict.setdefault("IP_ttl", list())  # ip TTL 生存时间(int)
        self.pcap_dict.setdefault("IP_proto", list())  # ip 用户协议(int) 1---icmp,2---igmp,6---tcp,17---udp,89---ospf
        # pcap_dict.setdefault("IP_src", list())  # ip源地址(str)
        # pcap_dict.setdefault("IP_dst", list())  # ip目的地址(str)

        # UDP
        self.pcap_dict.setdefault("sport", list())  # udp 源端口(int)
        self.pcap_dict.setdefault("dport", list())  # udp 目的端口(int)
        # pcap_dict.setdefault("UDP_len",list())          #udp 报文长度(int)

    def read_packet(self, pcapfile, pktNum=100):
        self.packets = rdpcap(pcapfile)
        self.read_data(pktNum)

    #
    def read_data(self, pktNum=100):
        i = 0
        for pac in self.packets:
            try:
                if pac[Ether].type != 2048:
                    continue
                self.pcap_dict["IP_ihl"].append(pac[IP].ihl)
                self.pcap_dict["IP_tos"].append(pac[IP].tos)
                self.pcap_dict["IP_len"].append(pac[IP].len)
                self.pcap_dict["IP_id"].append(pac[IP].id)
                self.pcap_dict["IP_ttl"].append(pac[IP].ttl)
                self.pcap_dict["IP_proto"].append(pac[IP].proto)
                #self.pcap_dict["IP_src"].append(pac[IP].src)
                #self.pcap_dict["IP_dst"].append(pac[IP].dst)

                if pac[IP].proto == 6:
                    self.pcap_dict["sport"].append(pac[TCP].sport)
                    self.pcap_dict["dport"].append(pac[TCP].dport)
                elif pac[IP].proto == 17:
                    self.pcap_dict["sport"].append(pac[UDP].sport)
                    self.pcap_dict["dport"].append(pac[UDP].dport)
                else:
                    self.pcap_dict["sport"].append(0)
                    self.pcap_dict["dport"].append(0)

                i += 1
                if(i >= pktNum):
                    break
            except:
                continue

    def get_DataFrame(self):
        return pd.DataFrame(self.pcap_dict)


def test():
    pcap = PcapFeature()
    pcap.read_packets('./testData/email2a.pcap')
    pcap.read_packets('./testData/email2a.pcap')
    print(pcap.get_DataFrame())

# test()