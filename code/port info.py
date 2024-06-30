
from textfsm import TextFSM
from pprint import pprint


raw_result = """
GigabitEthernet0/2/5 current state : UP (ifindex: 10)
Line protocol current state : UP 
Last line protocol up time : 2023-08-27 06:12:59+03:00
Link quality grade : GOOD
Description: To-UMOJA_INNERCORE_ATC-NBI0938-ATN910C-CSG-01-GE0/2/5
Route Port,The Maximum Transmit Unit(L3) is 1500 bytes, The Maximum Receive Unit(L2) is 9700 bytes 
Internet Address is 10.251.238.140/31
IP Sending Frames' Format is PKTFMT_ETHNT_2, Hardware address is 8889-2f48-a095
The Vendor PN is RTXM228-462
The Vendor Name is WTD
The Vendor Private Information is NA, Transceiver Identifier: SFP+
Port BW: 10G, Transceiver max BW: 10G, Transceiver Mode: SingleMode
WaveLength: 1330.00nm, Transmission Distance: 10km, Transceiver Type:BiDi
Rx Power:  -6.36dBm, Working range: [-14.400,  0.499]dBm
Tx Power:  -2.23dBm, Working range: [-8.498,  0.499]dBm
Loopback:none, LAN full-duplex mode, Pause Flowcontrol:Receive Enable and Send Disable
Last physical up time   : 2023-08-27 06:12:59+03:00
Last physical down time : 2023-08-27 06:12:48+03:00
Current system time: 2023-11-22 16:57:42+03:00
Statistics last cleared:never
    Last 300 seconds input rate: 1274642 bits/sec, 1016 packets/sec
    Last 300 seconds output rate: 914495418 bits/sec, 165600 packets/sec
    Input peak rate 302351112 bits/sec, Record time: 2023-09-19 22:20:26+03:00
    Output peak rate 1855012474 bits/sec, Record time: 2023-11-03 22:08:54+03:00
    Input: 34936765982979 bytes, 130496944382 packets
    Output: 671608254191369 bytes, 942009683952 packets
    Input:
      Unicast: 130449003438 packets, Multicast: 45477123 packets
      Broadcast: 2463821 packets, JumboOctets: 2190630202 packets
      CRC: 0 packets, Symbol: 0 packets
      Overrun: 0 packets, InRangeLength: 0 packets
      LongPacket: 0 packets, Jabber: 0 packets, Alignment: 0 packets
      Fragment: 0 packets, Undersized Frame: 0 packets
      RxPause: 0 packets
    Output:
      Unicast: 941950663821 packets, Multicast: 48948208 packets
      Broadcast: 10071928 packets, JumboOctets: 7010088676 packets
      Lost: 0 packets, Overflow: 0 packets, Underrun: 0 packets
      System: 0 packets, Overruns: 0 packets
      TxPause: 0 packets
    Local fault: normal, Remote fault: normal.
    Last 300 seconds input utility rate:  0.01%
    Last 300 seconds output utility rate: 9.14%
"""

raw_result1 = raw_result.split('\n\n+')
# print(raw_result1)


# # 使用模板解析文本
with open(f'./template/display_interface.template') as f:
    template = TextFSM(f)
    # print(template)
    for raw_result in raw_result1:
        # print(raw_result)     
        # if f"Transceiver Mode" in raw_result:
            print(raw_result)
            show_vlan_dict = template.ParseText(raw_result)
            pprint(show_vlan_dict)