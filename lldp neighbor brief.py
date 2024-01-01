

from textfsm import TextFSM
from pprint import pprint


raw_result = """
display lldp neighbor brief
Local Intf                     Neighbor Dev         Neighbor Intf        Exptime (sec)
--------------------------------------------------------------------------------------
100GE1/0/0                     ISB-IBA2-P01-N9K     100GE2/1/2                     110
100GE1/0/1                     ISB-IBA1-AGG01-N4X16 100GE1/0/1                      91
100GE7/0/0                     ISB-IBA1-P01-N9K     100GE1/1/2                     112
100GE7/0/1                     ISB-IBA1-CDN-CE68    100GE2/0/1                     108
50|100GE3/0/0                  ISB-IBA1-CDN-CE68    100GE1/0/2                     113
50|100GE3/0/6                  HWI-ISB-IBA1-NPE-N4X16-1 50|100GE5/0/2                   99
50|100GE3/1/0                  ISB-IBA1-AGG01-N4X16 50|100GE3/1/0                   93
50|100GE3/1/4                  FE1.PTCL-ISB3        eth-1/1/49                     119
50|100GE3/1/6                  HWI-MDN-CNTR-NPE-N4X16-1 50|100GE15/0/2                 108
50|100GE4/0/0                  ISB-IBA1-CE6865E-OTT-DATA-02 100GE1/0/1                     114
50|100GE4/0/2                  FE1.PTCL-ISB3        eth-1/1/50                     119
50|100GE4/0/6                  HWI-ISB-CANT-NPE-N4X16-2 50|100GE2/1/0                  116
50|100GE4/1/0                  ISB-IBA2-P01-N9K     100GE1/0/9                      95
50|100GE4/1/4                  ISB-IBA1-P01-N9K     100GE3/0/7                     112
50|100GE4/1/6                  ISB-IBA2-P01-N9K     100GE4/0/0                     118
GigabitEthernet1/1/5           ISB-IBA1-AGG-M2F01   GigabitEthernet0/3/2           117
GigabitEthernet1/1/6           ISB-MRGL-NPE-N4X8-1  GigabitEthernet1/0/15          105
GigabitEthernet1/1/8           GKN-GKN-NPE-N4X8-1   GigabitEthernet8/1/22          114
GigabitEthernet1/1/9           HWI-KHT-KDA-UPE-N4X8-1 GigabitEthernet1/0/2           115
GigabitEthernet1/1/12          ISB-IBA2-PS-S9312-2  XGigabitEthernet8/0/13         114
GigabitEthernet1/1/13          ISB-PE-NE40E-X8A-A2  GigabitEthernet5/1/7           111
GigabitEthernet1/1/14          ISB-IBA1-CDN-CE68    10GE2/0/32                     107
GigabitEthernet1/1/15          ISB-PE-NE40E-X8A-A2  GigabitEthernet5/1/5           107
GigabitEthernet1/1/16          ISB-PE-NE40E-X8A-A2  GigabitEthernet5/1/6           102
GigabitEthernet1/1/17          ISB-IBA2-PS-S9312-2  XGigabitEthernet9/0/10         108
GigabitEthernet5/0/0           ISB-P-NE40E-X16-A2   GigabitEthernet7/0/1           104
GigabitEthernet5/0/1           ISB-IBA2-PS-S9312-2  XGigabitEthernet9/0/11         117
GigabitEthernet5/0/2           ISB-IBA2-PS-S9312-2  XGigabitEthernet9/0/3          101
GigabitEthernet5/0/4           ISB-PE-NE40E-X8A-A2  GigabitEthernet3/0/7            92
GigabitEthernet5/0/5           ISB-PE-NE40E-X8A-A2  GigabitEthernet1/0/7           103
GigabitEthernet5/0/7           ISB-IBA2-PS-S9312-2  XGigabitEthernet9/0/2          109
GigabitEthernet5/0/9           ISB-PE-NE40E-X8A-A2  GigabitEthernet5/0/1            99
GigabitEthernet5/0/10          ISB-IBA2-PS-S9312-2  XGigabitEthernet8/0/15          98
GigabitEthernet5/0/11          ITR001-IBA-1         xgei-1/4/0/10                   93
GigabitEthernet5/0/11          ISB-IuB-S9306-A3     XGigabitEthernet2/0/5          114
GigabitEthernet5/0/12          HWI-PSH-CITY-NPE-N4X16-2 GigabitEthernet1/1/23          101
GigabitEthernet5/0/13          HWI-PSH-CITY-NPE-N4X16-2 GigabitEthernet7/0/23          116
GigabitEthernet5/0/14          ISB-PE-NE40E-X8A-A2  GigabitEthernet5/1/8            99
GigabitEthernet5/0/16          ISB-PE-NE40E-X8A-A2  GigabitEthernet5/1/9            99
GigabitEthernet5/0/17          HWI-KHT-KDA-UPE-N4X8-1 GigabitEthernet1/1/15          117
GigabitEthernet5/0/18          ISB-IBA2-PS-S9312-2  XGigabitEthernet8/0/14         110
GigabitEthernet5/0/23          HWI-ISB-IBA1-NPE-N4X16-1 GigabitEthernet9/0/11          109
GigabitEthernet5/1/0           HWI-KHT-KDA-UPE-N4X8-1 GigabitEthernet8/0/23          109
GigabitEthernet5/1/1           ITR068-IBA1-DC       xgei-1/22/0/1                   98
GigabitEthernet5/1/4           HWI-ISB-IBA1-NPE-N4X16-1 GigabitEthernet9/0/13          109
GigabitEthernet5/1/6           HWI-ISB-IBA1-NPE-N4X16-1 GigabitEthernet9/1/11          109
GigabitEthernet5/1/9           HWI-PSH-CITY-NPE-N4X16-2 GigabitEthernet1/0/20          107
GigabitEthernet5/1/10          HWI-PSH-CITY-NPE-N4X16-2 GigabitEthernet1/0/21          110
GigabitEthernet5/1/11          HWI-PSH-CITY-NPE-N4X16-2 GigabitEthernet1/0/22           98
GigabitEthernet5/1/14          HWI-ISB-IBA1-NPE-N4X16-1 GigabitEthernet7/1/12           91
GigabitEthernet5/1/17          GKN-GKN-NPE-N4X8-1   GigabitEthernet1/0/23           91
GigabitEthernet5/1/18          HWI-ISB-IBA1-NPE-N4X16-1 GigabitEthernet9/1/9           109
GigabitEthernet5/1/19          HWI-ISB-IBA1-NPE-N4X16-1 GigabitEthernet7/0/23           91
GigabitEthernet5/1/21          HWI-ISB-IBA1-NPE-N4X16-1 GigabitEthernet7/1/17           91
GigabitEthernet5/1/23          HWI-ISB-IBA1-NPE-N4X16-1 GigabitEthernet15/0/17          99
GigabitEthernet6/0/0           ISB-IBA2-PS-S9312-2  XGigabitEthernet8/0/4           98
GigabitEthernet6/0/1           ISB-IBA2-PS-S9312-2  XGigabitEthernet8/0/5           98
GigabitEthernet6/0/2           ISB-IBA2-PS-S9312-2  XGigabitEthernet8/0/12          98
GigabitEthernet6/0/4           HWI-ISB-IBA1-NPE-N4X16-1 GigabitEthernet9/1/3           109
GigabitEthernet6/0/6           ISB-IBA2-PS-S9312-2  XGigabitEthernet9/0/15         110
GigabitEthernet6/0/8           HWI-ISB-IBA1-NPE-N4X16-1 GigabitEthernet9/1/1           109
GigabitEthernet6/0/9           HWI-ISB-IBA1-NPE-N4X16-1 GigabitEthernet7/0/16           91
GigabitEthernet6/0/10          ISB-IBA1-S5332-OTT-MGMT-02 XGigabitEthernet0/0/3           94
GigabitEthernet6/0/11          GKN-GKN-NPE-N4X8-1   GigabitEthernet8/1/5           110
GigabitEthernet6/1/3           HWI-ISB-IBA1-NPE-N4X16-1 GigabitEthernet15/0/11          99
GigabitEthernet6/1/4           HWI-ABT-CNTR-NPE-N4X16-1 GigabitEthernet16/0/6          100
GigabitEthernet6/1/6           ITR068-IBA1-DC       xgei-1/22/0/3                  115
GigabitEthernet6/1/8           HWI-PSH-CITY-NPE-N4X16-2 GigabitEthernet7/0/19          116
GigabitEthernet6/1/9           HWI-PSH-CITY-NPE-N4X16-2 GigabitEthernet7/0/20          116
GigabitEthernet6/1/10          HWI-PSH-CITY-NPE-N4X16-2 GigabitEthernet7/0/21          113
GigabitEthernet6/1/11          HWI-PSH-CITY-NPE-N4X16-2 GigabitEthernet7/0/22          111
GigabitEthernet7/1/5           ISB-IBA1-AGG-M2F01   GigabitEthernet0/3/3           118
GigabitEthernet7/1/7           HWI-KHT-KDA-UPE-N4X8-1 GigabitEthernet8/1/1           114
GigabitEthernet7/1/15          ISB-PE-NE40E-X8A-A2  GigabitEthernet5/0/3            99
GigabitEthernet7/1/16          ISB-PE-NE40E-X8A-A2  GigabitEthernet5/1/4           112
GigabitEthernet7/1/18          ITR001-IBA-1         xgei-1/18/0/11                 116
GigabitEthernet7/1/18          ISB-PE-NE40E-X8A-A2  GigabitEthernet5/0/2           117
GigabitEthernet7/1/19          HWI-ABT-CNTR-NPE-N4X16-1 GigabitEthernet16/0/0          100
GigabitEthernet7/1/20          ISB-IBA2-PS-S9312-2  XGigabitEthernet9/0/7          118
"""

bottom_list = [['N/A', '50GE4/0/5'],
 ['N/A', '50GE4/1/3'],
 ['N/A', '50|100GE4/0/4'],
 ['N/A', '50|100GE4/0/6'],
 ['N/A', '50|100GE4/1/2'],
 ['Eth-Trunk4', '50|100GE3/0/2'],
 ['Eth-Trunk4', '50|100GE3/1/2'],
 ['Eth-Trunk10', '50|100GE3/1/4'],
 ['Eth-Trunk10', '50|100GE4/0/2'],
 ['Eth-Trunk12', 'GigabitEthernet1/1/0'],
 ['Eth-Trunk12', 'GigabitEthernet5/0/15'],
 ['Eth-Trunk12', 'GigabitEthernet5/1/12'],
 ['Eth-Trunk12', 'GigabitEthernet6/1/4'],
 ['Eth-Trunk12', 'GigabitEthernet7/1/19'],
 ['Eth-Trunk15', 'GigabitEthernet1/1/12'],
 ['Eth-Trunk15', 'GigabitEthernet1/1/17'],
 ['Eth-Trunk15', 'GigabitEthernet5/0/1'],
 ['Eth-Trunk15', 'GigabitEthernet5/0/2'],
 ['Eth-Trunk15', 'GigabitEthernet5/0/7'],
 ['Eth-Trunk15', 'GigabitEthernet5/0/18'],
 ['Eth-Trunk15', 'GigabitEthernet6/0/0'],
 ['Eth-Trunk15', 'GigabitEthernet6/0/1'],
 ['Eth-Trunk15', 'GigabitEthernet6/0/2'],
 ['Eth-Trunk15', 'GigabitEthernet7/1/20'],
 ['Eth-Trunk25', 'GigabitEthernet7/1/9'],
 ['Eth-Trunk26', 'GigabitEthernet1/1/8'],
 ['Eth-Trunk26', 'GigabitEthernet5/1/17'],
 ['Eth-Trunk26', 'GigabitEthernet6/0/11'],
 ['Eth-Trunk26', 'GigabitEthernet7/1/14'],
 ['N/A', 'Eth-Trunk29'],
 ['N/A', 'Eth-Trunk30'],
 ['Eth-Trunk32', 'GigabitEthernet6/0/10'],
 ['N/A', 'Eth-Trunk33'],
 ['Eth-Trunk34', 'GigabitEthernet5/1/1'],
 ['Eth-Trunk36', '50|100GE4/0/0'],
 ['N/A', 'Eth-Trunk40'],
 ['Eth-Trunk41', 'GigabitEthernet7/1/10'],
 ['N/A', 'Eth-Trunk45'],
 ['Eth-Trunk47', 'GigabitEthernet1/1/18'],
 ['Eth-Trunk47', 'GigabitEthernet1/1/22'],
 ['Eth-Trunk47', 'GigabitEthernet5/0/19'],
 ['Eth-Trunk47', 'GigabitEthernet7/1/2'],
 ['Eth-Trunk47', 'GigabitEthernet7/1/4'],
 ['Eth-Trunk47', 'GigabitEthernet7/1/22'],
 ['Eth-Trunk51', 'GigabitEthernet5/0/6'],
 ['Eth-Trunk51', 'GigabitEthernet6/0/3'],
 ['Eth-Trunk59', 'GigabitEthernet5/0/10'],
 ['Eth-Trunk59', 'GigabitEthernet6/0/6'],
 ['Eth-Trunk60', 'GigabitEthernet1/1/13'],
 ['Eth-Trunk60', 'GigabitEthernet1/1/15'],
 ['Eth-Trunk60', 'GigabitEthernet1/1/16'],
 ['Eth-Trunk60', 'GigabitEthernet5/0/4'],
 ['Eth-Trunk60', 'GigabitEthernet5/0/5'],
 ['Eth-Trunk60', 'GigabitEthernet5/0/9'],
 ['Eth-Trunk60', 'GigabitEthernet5/0/14'],
 ['Eth-Trunk60', 'GigabitEthernet5/0/16'],
 ['Eth-Trunk60', 'GigabitEthernet7/1/15'],
 ['Eth-Trunk60', 'GigabitEthernet7/1/16'],
 ['Eth-Trunk60', 'GigabitEthernet7/1/18'],
 ['Eth-Trunk61', 'GigabitEthernet1/1/10'],
 ['Eth-Trunk61', 'GigabitEthernet5/0/11'],
 ['N/A', 'Eth-Trunk66'],
 ['Eth-Trunk71', '50|100GE3/1/6'],
 ['Eth-Trunk73', 'GigabitEthernet5/0/23'],
 ['Eth-Trunk73', 'GigabitEthernet5/1/4'],
 ['Eth-Trunk73', 'GigabitEthernet6/0/4'],
 ['Eth-Trunk74', 'GigabitEthernet5/1/6'],
 ['Eth-Trunk74', 'GigabitEthernet5/1/14'],
 ['Eth-Trunk74', 'GigabitEthernet6/0/8'],
 ['Eth-Trunk75', 'GigabitEthernet5/0/3'],
 ['Eth-Trunk75', 'GigabitEthernet5/0/8'],
 ['Eth-Trunk75', 'GigabitEthernet6/0/5'],
 ['Eth-Trunk76', 'GigabitEthernet5/1/18'],
 ['Eth-Trunk76', 'GigabitEthernet5/1/19'],
 ['Eth-Trunk76', 'GigabitEthernet6/0/9'],
 ['Eth-Trunk78', 'GigabitEthernet5/1/21'],
 ['Eth-Trunk78', 'GigabitEthernet5/1/23'],
 ['Eth-Trunk78', 'GigabitEthernet6/1/3'],
 ['Eth-Trunk97', 'GigabitEthernet1/1/2'],
 ['Eth-Trunk97', 'GigabitEthernet7/1/6'],
 ['Eth-Trunk101', 'GigabitEthernet1/1/7'],
 ['Eth-Trunk101', 'GigabitEthernet5/0/20'],
 ['Eth-Trunk101', 'GigabitEthernet6/1/1'],
 ['Eth-Trunk101', 'GigabitEthernet6/1/5'],
 ['Eth-Trunk104', 'GigabitEthernet7/1/1'],
 ['Eth-Trunk104', 'GigabitEthernet7/1/3'],
 ['Eth-Trunk104', 'GigabitEthernet7/1/23'],
 ['Eth-Trunk105', 'GigabitEthernet1/1/19'],
 ['Eth-Trunk105', 'GigabitEthernet1/1/20'],
 ['Eth-Trunk105', 'GigabitEthernet1/1/21'],
 ['Eth-Trunk105', 'GigabitEthernet1/1/23'],
 ['N/A', 'Eth-Trunk111'],
 ['Eth-Trunk112', '100GE7/0/1'],
 ['Eth-Trunk112', '50|100GE3/0/0'],
 ['Eth-Trunk115', '100GE1/0/0'],
 ['Eth-Trunk115', '50|100GE4/1/0'],
 ['Eth-Trunk115', '50|100GE4/1/6'],
 ['Eth-Trunk120', '100GE7/0/0'],
 ['Eth-Trunk120', '50|100GE3/0/4'],
 ['Eth-Trunk120', '50|100GE4/1/4'],
 ['Eth-Trunk125', 'GigabitEthernet1/1/6'],
 ['Eth-Trunk125', 'GigabitEthernet6/1/6'],
 ['Eth-Trunk150', '100GE1/0/1'],
 ['Eth-Trunk150', '50|100GE3/1/0'],
 ['N/A', 'Eth-Trunk201'],
 ['Eth-Trunk203', '50|100GE3/0/6'],
 ['N/A', 'Eth-Trunk204'],
 ['Eth-Trunk205', 'GigabitEthernet5/0/12'],
 ['Eth-Trunk205', 'GigabitEthernet5/0/13'],
 ['Eth-Trunk205', 'GigabitEthernet5/1/9'],
 ['Eth-Trunk205', 'GigabitEthernet5/1/10'],
 ['Eth-Trunk205', 'GigabitEthernet5/1/11'],
 ['Eth-Trunk205', 'GigabitEthernet6/1/8'],
 ['Eth-Trunk205', 'GigabitEthernet6/1/9'],
 ['Eth-Trunk205', 'GigabitEthernet6/1/10'],
 ['Eth-Trunk205', 'GigabitEthernet6/1/11'],
 ['Eth-Trunk220', 'GigabitEthernet1/1/9'],
 ['Eth-Trunk220', 'GigabitEthernet5/0/17'],
 ['Eth-Trunk220', 'GigabitEthernet5/1/0'],
 ['Eth-Trunk220', 'GigabitEthernet7/1/7'],
 ['N/A', 'GigabitEthernet5/19/0']]



with open(f'./template/display_lldp_neighbor_brief.template') as f:
    template = TextFSM(f)
    # print(template)
    data = template.ParseText(raw_result)
    # pprint(data)
    top_dict = {item[0]: item[1:] for item in data}
    pprint(top_dict)

# sub_list_range = []
# for sub_list in data:
#     found = False  # 添加一个标记来跟踪是否找到匹配项
#     for item in bottom_list:
#         if item[1] in sub_list:
#             sub_list.insert(0, item[0])
#             found = True  # 如果找到匹配项，将标记设置为True
#             break  # 找到匹配项后就可以跳出循环
#     if not found:  # 如果没有找到匹配项，就在开头插入"N/A"
#         sub_list.insert(0, "N/A")
#     sub_list_range.append(sub_list)

# pprint(sub_list_range)  # 打印每个子列表
    
    
    

for item in bottom_list:
    if item[1] in top_dict:
        item.extend(top_dict[item[1]])
        item.insert(0, 'ME60-X16')
    else:
        pass

pprint(bottom_list)