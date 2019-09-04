import scapy
from scapy.all import *
from scapy.utils import PcapReader
import pandas as pd


def create_dict():
    # Ether
    pcap_dict = dict()
    #pcap_dict.setdefault("Ether_dst", list())  # mac目标地址(str)
    #pcap_dict.setdefault("Ether_src", list())  # mac源地址(str)

    # IP
    pcap_dict.setdefault("IP_ihl", list())  # ip报头长度(int)
    pcap_dict.setdefault("IP_tos", list())  # ip tos 服务类别
    pcap_dict.setdefault("IP_len", list())  # ip len 报文长度(int)
    pcap_dict.setdefault("IP_id", list())  # ip id 标识(int)，用于在IP层对数据包进行分段的时候，表示数据包
    pcap_dict.setdefault("IP_ttl", list())  # ip TTL 生存时间(int)
    pcap_dict.setdefault("IP_proto", list())  # ip 用户协议(int) 1---icmp,2---igmp,6---tcp,17---udp,89---ospf
    #pcap_dict.setdefault("IP_src", list())  # ip源地址(str)
    #pcap_dict.setdefault("IP_dst", list())  # ip目的地址(str)

    #UDP
    pcap_dict.setdefault("sport",list())        #udp 源端口(int)
    pcap_dict.setdefault("dport",list())        #udp 目的端口(int)
    #pcap_dict.setdefault("UDP_len",list())          #udp 报文长度(int)

    '''
    #TCP
    pcap_dict.setdefault("TCP_sport",list())        #tcp 源端口(int)
    pcap_dict.setdefault("TCP_sport",list())        #tcp 目的端口(int)
    pcap_dict.setdefault("TCP_seq",list())          #tcp 序号(int)
    pcap_dict.setdefault("TCP_ack",list())          #tcp 确认序号(int)
    pcap_dict.setdefault("TCP_dataofs",list())      #tcp 首部长度(int)
    pcap_dict.setdefault("TCP_flags",list())        #tcp 标志位(scapy.fields.FlagValue)
    pcap_dict.setdefault("TCP_window",list())       #tcp 窗口大小(int) 接收端希望接受的字节数

    #DNS
    pcap_dict.setdefault("DNS_id",list())           #dns id(int) 定义的随机数，服务器返回的ID与用户发送的一致
    '''
    return pcap_dict


#packets = rdpcap("./scpUp5.pcap")
packets = rdpcap("skype_file4.pcapng")

a=[]
#a.append(str(packets[0]))
#a.append(str(packets[1]))

print(a)
for pac in packets:
    a.append(str(pac))
print(a)
data = create_dict()

for pac in packets:
    if pac[Ether].type!=2048:
        continue
    #data["Ether_dst"].append(pac[Ether].dst)
    #data["Ether_src"].append(pac[Ether].src)

    data["IP_ihl"].append(pac[IP].ihl)
    data["IP_tos"].append(pac[IP].tos)
    data["IP_len"].append(pac[IP].len)
    data["IP_id"].append(pac[IP].id)
    data["IP_ttl"].append(pac[IP].ttl)
    data["IP_proto"].append(pac[IP].proto)
    #data["IP_src"].append(pac[IP].src)
    #data["IP_dst"].append(pac[IP].dst)

    if pac[IP].proto==6:
        data["sport"].append(pac[TCP].sport)
        data["dport"].append(pac[TCP].dport)
    if pac[IP].proto==17:
        data["sport"].append(pac[UDP].sport)
        data["dport"].append(pac[UDP].dport)

pcap_dataframe = pd.DataFrame(data)
pcap_dataframe.to_excel("1.xlsx")


