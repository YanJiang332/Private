
from textfsm import TextFSM
from pprint import pprint


raw_result = """
display bgp peer
 
 BGP local router ID : 203.135.19.182
 Local AS number : 17557
 Total number of peers : 8                 Peers in established state : 7

  Peer                             V          AS  MsgRcvd  MsgSent  OutQ  Up/Down       State  PrefRcv
  59.103.248.154                   4       24435    12045    12682     0 0090h33m Established        1
  119.159.254.30                   4       65301    61148    61110     0 16:58:59 Established        1
  182.176.2.55                     4       64914   357914   584913     0 0168h59m Established        2
  182.176.4.151                    4       64914    84769   122227     0 0035h18m Established        2
  182.176.147.114                  4       65301    52045    52013     0 14:27:17 Established        1
  182.176.176.194                  4      137561        0        0     0 5630h33m        Idle        0
  203.135.19.250                   4       17557 80137122   376610     0 1870h12m Established   998822
  203.135.19.255                   4       17557 134469778   663500     0 3341h55m Established   998833
"""



with open(f'./template/display_bgp.template') as f:
    template = TextFSM(f)
    # # print(template)
    # show_vlan_dict = template.ParseText(raw_result)
    # pprint(show_vlan_dict)

    records = template.ParseText(raw_result)
    keys = template.header
    print(keys)
    results = [dict(zip(keys, record)) for record in records]
    print(results)