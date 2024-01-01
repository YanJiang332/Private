from textfsm import TextFSM
from pprint import pprint
import re

raw_result = """
display lldp neighbor
GigabitEthernet0/2/4 has 1 neighbor(s):

Neighbor index                     :1
Chassis type                       :macAddress
Chassis ID                         :f4de-afdf-167f
Port ID type                       :interfaceName
Port ID                            :GigabitEthernet0/2/4
Port description                   :tO NAIROBI_NGUMMO-NBI0076-ATN910B-CSG-01 0/2/18
System name                        :KE-NBI0895-HW-ATN910C-G-CSG01-NAIROBI_KEMRI
System description                 :Huawei Versatile Routing Platform Software
VRP (R) software, Version 8.191 (ATN 910C-G V300R006C00SPC300)
Copyright (C) 2012-2020 Huawei Technologies Co., Ltd.
HUAWEI ATN 910C-G

System capabilities supported      :bridge router
System capabilities enabled        :bridge router
Management address type            :ipv4
Management address                 :128.219.174.94
Expired time                       :94s

Port VLAN ID(PVID)                 :0
Port and Protocol VLAN ID(PPVID)   :unsupported         
VLAN name of VLAN                  :--
Protocol identity                  :--
Auto-negotiation supported         :Yes
Auto-negotiation enabled           :No
OperMau                            :speed (1000) /duplex (Full)
Link aggregation supported         :Yes
Link aggregation enabled           :No
Aggregation port ID                :0
Maximum frame Size                 :9700
Discovered time                    :2023-12-05 18:22:27+03:00

50|100GE8/0/4 has 0 neighbor(s)

GigabitEthernet0/2/19 has 1 neighbor:
Neighbor 1: 
ChassisIdSubtype: macAddress 
ChassisId: e483-26d8-b690 
PortIdSubtype: interfaceName 
PortId: GigabitEthernet0/2/4 
PortDesc: To NAIROBI_KIM_SOUTH_C-ATN910B-CSG-01 GE0/2/19 
SysName: KE-NBI0782-HW-ATN910C-G-CSG01-NAIROBI_RIDGEVIEW 
SysDesc: Huawei Versatile Routing Platform Software
VRP (R) software, Version 8.191 (ATN 910C-G V300R006C00SPC300)
Copyright (C) 2012-2020 Huawei Technologies Co., Ltd.
HUAWEI ATN 910C-G
 
SysCapSupported: bridge router  
SysCapEnabled: bridge router 
Management address: ipV4: 128.152.164.95  
Expired time: 114

50|100GE8/1/0 has 0 neighbor(s)

50|100GE8/1/2 has 0 neighbor(s)

50|100GE8/1/4 has 0 neighbor(s)
"""

def parse_data_with_template(template_path, raw_result):
    with open(template_path, encoding='UTF-8') as f:
        template = TextFSM(f)
        data = template.ParseText(raw_result)
    return data

def main():
    
    template_path = './template/display_lldp_neighbor.template'
    
    result = parse_data_with_template(template_path, raw_result)
    
    pprint(result)

if __name__ == '__main__':
    main()