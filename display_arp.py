
from textfsm import TextFSM
from pprint import pprint

raw_result = """
display arp all 
IP ADDRESS      MAC ADDRESS     EXPIRE(M) TYPE        INTERFACE   VPN-INSTANCE 
                                          VLAN/CEVLAN 
------------------------------------------------------------------------------
192.168.0.1     346a-c26a-f736            I -         Eth0/0/0       __LOCAL_OAM_VPN__  
10.251.238.26   346a-c26a-f738            I -         GE0/2/17       
10.251.238.27   7817-be6e-5675  20        D-0         GE0/2/17       
10.251.194.101  346a-c26a-f748            I -         GE0/2/33       
10.251.194.100  e483-2672-20f9  12        D-0         GE0/2/33       
128.66.196.10   346a-c26a-f737            I -         GE0/2/16.4094  __dcn_vpn__        
128.66.196.10   346a-c26a-f738            I -         GE0/2/17.4094  __dcn_vpn__        
128.218.168.239 7817-be6e-5675  20        D-0         GE0/2/17.4094  __dcn_vpn__        
                                          4094/-      
128.66.196.10   346a-c26a-f739            I -         GE0/2/18.4094  __dcn_vpn__        
128.66.196.10   346a-c26a-f73a            I -         GE0/2/19.4094  __dcn_vpn__        
128.66.196.10   346a-c26a-f73b            I -         GE0/2/20.4094  __dcn_vpn__        
128.66.196.10   346a-c26a-f73c            I -         GE0/2/21.4094  __dcn_vpn__        
128.66.196.10   346a-c26a-f73d            I -         GE0/2/22.4094  __dcn_vpn__        
128.66.196.10   346a-c26a-f73e            I -         GE0/2/23.4094  __dcn_vpn__        
128.66.196.10   346a-c26a-f73f            I -         GE0/2/24.4094  __dcn_vpn__        
128.66.196.10   346a-c26a-f736            I -         GE0/2/25.4094  __dcn_vpn__        
10.251.196.52   346a-c26a-f741            I -         GE0/2/26.1500  
10.251.211.48   346a-c26a-f741            I -         GE0/2/26.1553  
128.66.196.10   346a-c26a-f736            I -         GE0/2/27.4094  __dcn_vpn__        
10.162.3.254    346a-c26a-f743            I -         GE0/2/28.1901  AIRTEL_LTE_OAM     
10.162.5.254    346a-c26a-f743            I -         GE0/2/28.1902  AIRTEL_LTE_S1_MME  
10.162.5.253    34ce-6932-ac2f  4         D-0         GE0/2/28.1902  AIRTEL_LTE_S1_MME  
                                          1902/-      
10.162.7.254    346a-c26a-f743            I -         GE0/2/28.1903  AIRTEL_LTE_S1_USER 
10.162.7.253    34ce-6932-ac2f  20        D-0         GE0/2/28.1903  AIRTEL_LTE_S1_USER 
                                          1903/-      
128.66.196.10   346a-c26a-f743            I -         GE0/2/28.4094  __dcn_vpn__        
128.66.196.10   346a-c26a-f744            I -         GE0/2/29.4094  __dcn_vpn__        
10.159.231.121  346a-c26a-f745            I -         GE0/2/30.2523  AIRTEL_2G_ABISoIP  
10.57.119.89    346a-c26a-f745            I -         GE0/2/30.4004  AIRTEL_DCN_OAM     
128.66.196.10   346a-c26a-f745            I -         GE0/2/30.4094  __dcn_vpn__        
128.66.196.10   346a-c26a-f746            I -         GE0/2/31.4094  __dcn_vpn__        
128.66.196.10   346a-c26a-f736            I -         GE0/2/32.4094  __dcn_vpn__        
128.66.196.10   346a-c26a-f748            I -         GE0/2/33.4094  __dcn_vpn__        
128.152.163.179 e483-2672-20f9  12        D-0         GE0/2/33.4094  __dcn_vpn__        
                                          4094/-      
10.162.213.177  346a-c26a-f743            I -         GE0/2/28.1804  AIRTEL_2G_ABISoIP  
10.162.213.180  34ce-6932-ac2f  4         D-0         GE0/2/28.1804  AIRTEL_2G_ABISoIP  
                                          1804/-      
10.159.229.89   346a-c26a-f743            I -         GE0/2/28.2455  AIRTEL_2G_ABISoIP  
10.159.229.92   34ce-6932-ac2f  20        D-0         GE0/2/28.2455  AIRTEL_2G_ABISoIP  
                                          2455/-      
10.159.234.41   346a-c26a-f743            I -         GE0/2/28.2831  AIRTEL_3G_IUB      
10.159.234.45   34ce-6932-ac2f  4         D-0         GE0/2/28.2831  AIRTEL_3G_IUB      
                                          2831/-      
10.162.48.209   346a-c26a-f745            I -         GE0/2/30.2376  AIRTEL_LTE_S1_MME  
10.162.48.217   346a-c26a-f745            I -         GE0/2/30.2377  AIRTEL_LTE_S1_USER 
10.162.48.225   346a-c26a-f745            I -         GE0/2/30.2378  AIRTEL_2G_ABISoIP  
10.57.127.225   346a-c26a-f746            I -         GE0/2/31.846   AIRTEL_DCN_OAM     
10.57.154.241   346a-c26a-f746            I -         GE0/2/31.846   AIRTEL_DCN_OAM     
10.57.154.242   0004-56d9-323a  3         D-0         GE0/2/31.846   AIRTEL_DCN_OAM     
                                           846/-      
10.57.154.247   58c1-7a47-1547  19        D-0         GE0/2/31.846   AIRTEL_DCN_OAM     
                                           846/-      
10.57.154.245   58c1-7a50-747d  15        D-0         GE0/2/31.846   AIRTEL_DCN_OAM     
                                           846/-      
10.57.154.248   58c1-7a49-b3fb  2         D-0         GE0/2/31.846   AIRTEL_DCN_OAM     
                                           846/-      
10.57.127.230   58c1-7a47-1a2d  6         D-0         GE0/2/31.846   AIRTEL_DCN_OAM     
                                           846/-      
10.57.154.244   0004-56e6-cabd  18        D-0         GE0/2/31.846   AIRTEL_DCN_OAM     
                                           846/-      
10.57.154.246   Incomplete      1         D-0         GE0/2/31.846   AIRTEL_DCN_OAM     
                                           846/-      
10.57.154.243   Incomplete      1         D-0         GE0/2/31.846   AIRTEL_DCN_OAM     
                                           846/-      
172.19.86.54    346a-c26a-f73f            I -         GE0/2/24.128   AIRTEL_DCN_OAM     
10.251.211.254  346a-c26a-f745            I -         GE0/2/30.3004  
10.57.143.65    346a-c26a-f736            I -         GE0/2/25.846   AIRTEL_DCN_OAM     
10.57.156.25    346a-c26a-f745            I -         GE0/2/30.846   AIRTEL_DCN_OAM     
10.251.194.207  346a-c26a-f736            I -         GE0/2/32.2222  
10.251.194.206  c833-e568-3cb3  5         D-0         GE0/2/32.2222  
                                          2222/-      
10.161.97.85    346a-c26a-f743            I -         GE0/2/28.1349  AIRTEL_LTE_S1_MME  
10.161.97.86    34ce-6932-ac2f  4         D-0         GE0/2/28.1349  AIRTEL_LTE_S1_MME  
                                          1349/-      
10.161.98.85    346a-c26a-f743            I -         GE0/2/28.1449  AIRTEL_LTE_S1_USER 
10.161.98.86    34ce-6932-ac2f  20        D-0         GE0/2/28.1449  AIRTEL_LTE_S1_USER 
                                          1449/-      
------------------------------------------------------------------------------
Total:62        Dynamic:20      Static:0     Interface:42   
"""

# arp_info = []

# with open(f'./template/display_arp.template') as f:
#     template = TextFSM(f)
#     # print(template)
#     show_vlan_dict = template.ParseText(raw_result)
#     arp_info.extend(show_vlan_dict)
# pprint(arp_info)


# # 创建一个字典用于存储源和目的的对应关系，按照接口进行分组
# interface_mapping = {}

# # 遍历ARP信息
# for entry in arp_info:
#     ip_address = entry[0]
#     mac_address = entry[1]
#     expire = entry[2]
#     arp_type = entry[3]
#     interface = entry[4].strip()
#     vpn_instance = entry[5].strip()

#     # 判断是源还是目的
#     source_dest_indicator = "I" if arp_type.startswith("I") else "D"

#     # 将源和目的的对应关系添加到字典中，按接口分组
#     if interface not in interface_mapping:
#         interface_mapping[interface] = {"sources": {}, "destinations": {}}

#     if source_dest_indicator == "I":
#         interface_mapping[interface]["sources"][ip_address] = {"vpn_instance": vpn_instance}
#     elif source_dest_indicator == "D":
#         interface_mapping[interface]["destinations"][ip_address] = {"vpn_instance": vpn_instance}

# # 生成ping测试命令
# for interface, mapping in interface_mapping.items():
#     for source_ip, source_info in mapping["sources"].items():
#         # 查找相应的目的
#         destinations = mapping["destinations"]
#         for dest_ip, dest_info in destinations.items():
#             # 检查是否有相应的源，如果有则生成ping命令
#             if source_ip == dest_ip:
#                 continue  # 源和目的IP相同，跳过
#             dest_command = f"ping -vpn-instance {source_info['vpn_instance']} -a {source_ip} {dest_ip}"
#             print(dest_command)






from textfsm import TextFSM
from pprint import pprint

def parse_arp_info(raw_result):
    arp_info = []
    
    with open(f'./template/display_arp.template') as f:
        template = TextFSM(f)
        show_vlan_dict = template.ParseText(raw_result)
        arp_info.extend(show_vlan_dict)
    
    return arp_info

def generate_ping_commands(arp_info):
    # 创建一个字典用于存储源和目的的对应关系，按照接口进行分组
    interface_mapping = {}

    # 遍历ARP信息
    for entry in arp_info:
        ip_address = entry[0]
        mac_address = entry[1]
        expire = entry[2]
        arp_type = entry[3]
        interface = entry[4].strip()
        vpn_instance = entry[5].strip()

        # 判断是源还是目的
        source_dest_indicator = "I" if arp_type.startswith("I") else "D"

        # 将源和目的的对应关系添加到字典中，按接口分组
        if interface not in interface_mapping:
            interface_mapping[interface] = {"sources": {}, "destinations": {}}

        if source_dest_indicator == "I":
            interface_mapping[interface]["sources"][ip_address] = {"vpn_instance": vpn_instance}
        elif source_dest_indicator == "D":
            interface_mapping[interface]["destinations"][ip_address] = {"vpn_instance": vpn_instance}

    # 生成ping测试命令
    ping_commands = []
    for interface, mapping in interface_mapping.items():
        for source_ip, source_info in mapping["sources"].items():
            # 查找相应的目的
            destinations = mapping["destinations"]
            for dest_ip, dest_info in destinations.items():
                # 检查是否有相应的源，如果有则生成ping命令
                if source_ip == dest_ip:
                    continue  # 源和目的IP相同，跳过

                # 判断是否有 VPN 实例，决定是否包含 -vpn-instance
                vpn_instance_option = f"-vpn-instance {source_info['vpn_instance']}" if source_info['vpn_instance'] else ""
                
                ping_command = f"ping {vpn_instance_option} -a {source_ip} {dest_ip}"
                ping_commands.append(ping_command)

    return ping_commands

# # 使用示例
# raw_result = """
# # your raw result here
# """

arp_info = parse_arp_info(raw_result)
ping_commands = generate_ping_commands(arp_info)

# 打印生成的ping命令
pprint(arp_info)
pprint(ping_commands)