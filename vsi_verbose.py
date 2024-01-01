
from jinja2 import Template
import re
from pprint import pprint

['vpls-north-cx-taxla-vod', 'bgp', 'up', 'Eth-Trunk3.1725', 'down', 'unblocked', '']

raw_result = """

 ***VSI Name               : 100
    Work Mode              : normal
    Administrator VSI      : no
    Isolate Spoken         : disable
    VSI Index              : 283
    PW Signaling           : ldp
    Member Discovery Style : static
    Bridge-domain Mode     : disable
    PW MAC Learn Style     : unqualify
    Encapsulation Type     : vlan
    MTU                    : 1500
    Diffserv Mode          : uniform
    Service Class          : --
    Color                  : --
    DomainId               : 255
    Domain Name            :
    Ignore AcState         : disable
    P2P VSI                : disable
    Multicast Fast Switch  : disable
    Create Time            : 355 days, 6 hours, 30 minutes, 55 seconds
    VSI State              : down
    Resource Status        : --
 
    VSI ID                 : 100

 ***VSI Name               : 1029
    Work Mode              : normal
    Administrator VSI      : no
    Isolate Spoken         : disable
    VSI Index              : 390
    PW Signaling           : ldp
    Member Discovery Style : --
    Bridge-domain Mode     : disable
    PW MAC Learn Style     : unqualify
    Encapsulation Type     : vlan
    MTU                    : 1500
    Diffserv Mode          : uniform
    Service Class          : --
    Color                  : --
    DomainId               : 255
    Domain Name            :
    Ignore AcState         : disable
    P2P VSI                : disable
    Multicast Fast Switch  : disable
    Create Time            : 96 days, 12 hours, 1 minutes, 21 seconds
    VSI State              : up
    Resource Status        : --

    VSI ID                 : 1029
   *Peer Router ID         : 203.135.19.44
    Negotiation-vc-id      : 1029
    Encapsulation Type     : vlan
    primary or secondary   : primary
    ignore-standby-state   : no
    VC Label               : 48189
    Peer Type              : dynamic
    Session                : up
    Tunnel ID              : 0x0000000001004c7489 
    Broadcast Tunnel ID    : --
    Broad BackupTunnel ID  : --
    CKey                   : 49154
    NKey                   : 83900868
    Stp Enable             : 0
    PwIndex                : 48770
    Control Word           : disable
    BFD for PW             : unavailable
 
    Interface Name         : GigabitEthernet1/0/18.1029
    State                  : up
    Ac Block State         : unblocked
    Access Port            : false
    Last Up Time           : 2023/08/09 22:31:29
    Total Up Time          : 96 days, 12 hours, 0 minutes, 15 seconds

  **PW Information:

   *Peer Ip Address        : 203.135.19.44
    PW State               : up
    Local VC Label         : 48189
    Remote VC Label        : 210496
    Remote Control Word    : disable
    PW Type                : label
    Local  VCCV            : alert lsp-ping bfd 
    Remote VCCV            : alert lsp-ping bfd 
    Tunnel ID              : 0x0000000001004c7489 
    Broadcast Tunnel ID    : --
    Broad BackupTunnel ID  : --
    Ckey                   : 49154
    Nkey                   : 83900868
    Main PW Token          : 0x0
    Slave PW Token         : 0x0
    Tnl Type               : ldp
    OutInterface           : Eth-Trunk27
    Backup OutInterface    : --
    Stp Enable             : 0
    Mac Flapping           : 0
    Monitor Group Name     : --
    PW Last Up Time        : 2023/11/08 14:13:10
    PW Total Up Time       : 96 days, 12 hours, 0 minutes, 13 seconds

 ***VSI Name               : 1032
    Work Mode              : normal
    Administrator VSI      : no
    Isolate Spoken         : disable
    VSI Index              : 223
    VSI Description        : HSI-RTR-ZTE-DSLAM-HAZRO
    PW Signaling           : ldp
    Member Discovery Style : static
    Bridge-domain Mode     : disable
    PW MAC Learn Style     : unqualify
    Encapsulation Type     : vlan
    MTU                    : 1500
    Diffserv Mode          : uniform
    Service Class          : --
    Color                  : --
    DomainId               : 255
    Domain Name            :
    Ignore AcState         : disable
    P2P VSI                : disable
    Multicast Fast Switch  : disable
    Create Time            : 355 days, 6 hours, 30 minutes, 55 seconds
    VSI State              : down
    Resource Status        : --

    VSI ID                 : 1032
 
    Interface Name         : Eth-Trunk27.1032
    State                  : up
    Ac Block State         : unblocked
    Access Port            : false
    Last Up Time           : 2022/12/24 03:11:02
    Total Up Time          : 355 days, 5 hours, 43 minutes, 39 seconds

 ***VSI Name               : 1037
    Work Mode              : normal
    Administrator VSI      : no
    Isolate Spoken         : disable
    VSI Index              : 228
    PW Signaling           : ldp
    Member Discovery Style : static
    Bridge-domain Mode     : disable
    PW MAC Learn Style     : unqualify
    Encapsulation Type     : vlan
    MTU                    : 1500
    Diffserv Mode          : uniform
    Service Class          : --
    Color                  : --
    DomainId               : 255
    Domain Name            :
    Ignore AcState         : disable
    P2P VSI                : disable
    Multicast Fast Switch  : disable
    Create Time            : 355 days, 6 hours, 30 minutes, 55 seconds
    VSI State              : down
    Resource Status        : --

    VSI ID                 : 1037
 
    Interface Name         : Eth-Trunk27.1037
    State                  : up
    Ac Block State         : unblocked
    Access Port            : false
    Last Up Time           : 2022/12/24 03:11:02
    Total Up Time          : 355 days, 5 hours, 43 minutes, 39 seconds

 ***VSI Name               : 1048
    Work Mode              : normal
    Administrator VSI      : no
    Isolate Spoken         : disable
    VSI Index              : 242
    PW Signaling           : ldp
    Member Discovery Style : static
    Bridge-domain Mode     : disable
    PW MAC Learn Style     : unqualify
    Encapsulation Type     : vlan
    MTU                    : 1500
    Diffserv Mode          : uniform
    Service Class          : --
    Color                  : --
    DomainId               : 255
    Domain Name            :
    Ignore AcState         : disable
    P2P VSI                : disable
    Multicast Fast Switch  : disable
    Create Time            : 355 days, 6 hours, 30 minutes, 55 seconds
    VSI State              : down
    Resource Status        : --

    VSI ID                 : 1048
 
    Interface Name         : Eth-Trunk27.1048
    State                  : up
    Ac Block State         : unblocked
    Access Port            : false
    Last Up Time           : 2022/12/24 03:11:02
    Total Up Time          : 355 days, 5 hours, 43 minutes, 39 seconds

 ***VSI Name               : 1056
    Work Mode              : normal
    Administrator VSI      : no
    Isolate Spoken         : disable
    VSI Index              : 225
    VSI Description        : HSI-RTR-ZTE-DSLAM-ATTOCK
    PW Signaling           : ldp
    Member Discovery Style : static
    Bridge-domain Mode     : disable
    PW MAC Learn Style     : unqualify
    Encapsulation Type     : vlan
    MTU                    : 1500
    Diffserv Mode          : uniform
    Service Class          : --
    Color                  : --
    DomainId               : 255
    Domain Name            :
    Ignore AcState         : disable
    P2P VSI                : disable
    Multicast Fast Switch  : disable
    Create Time            : 355 days, 6 hours, 30 minutes, 55 seconds
    VSI State              : down
    Resource Status        : --

    VSI ID                 : 1056
 
    Interface Name         : Eth-Trunk27.1056
    State                  : up
    Ac Block State         : unblocked
    Access Port            : false
    Last Up Time           : 2022/12/24 03:11:02
    Total Up Time          : 355 days, 5 hours, 43 minutes, 39 seconds
 
 ***VSI Name               : 1074
    Work Mode              : normal
    Administrator VSI      : no
    Isolate Spoken         : disable
    VSI Index              : 229
    VSI Description        : HSI-RTR-ZTE-DSLAM-KOTSARANG
    PW Signaling           : ldp
    Member Discovery Style : static
    Bridge-domain Mode     : disable
    PW MAC Learn Style     : unqualify
    Encapsulation Type     : vlan
    MTU                    : 1500
    Diffserv Mode          : uniform
    Service Class          : --
    Color                  : --
    DomainId               : 255
    Domain Name            :
    Ignore AcState         : disable
    P2P VSI                : disable
    Multicast Fast Switch  : disable
    Create Time            : 355 days, 6 hours, 30 minutes, 55 seconds
    VSI State              : down
    Resource Status        : --

    VSI ID                 : 1074
 
    Interface Name         : Eth-Trunk27.1074
    State                  : up
    Ac Block State         : unblocked
    Access Port            : false
    Last Up Time           : 2022/12/24 03:11:02
    Total Up Time          : 355 days, 5 hours, 43 minutes, 39 seconds

 ***VSI Name               : 1080
    Work Mode              : normal
    Administrator VSI      : no
    Isolate Spoken         : disable
    VSI Index              : 232
    PW Signaling           : ldp
    Member Discovery Style : static
    Bridge-domain Mode     : disable
    PW MAC Learn Style     : unqualify
    Encapsulation Type     : vlan
    MTU                    : 1500
    Diffserv Mode          : uniform
    Service Class          : --
    Color                  : --
    DomainId               : 255
    Domain Name            :
    Ignore AcState         : disable
    P2P VSI                : disable
    Multicast Fast Switch  : disable
    Create Time            : 355 days, 6 hours, 30 minutes, 55 seconds
    VSI State              : down
    Resource Status        : --

    VSI ID                 : 1080
 
    Interface Name         : Eth-Trunk27.1080
    State                  : up
    Ac Block State         : unblocked
    Access Port            : false
    Last Up Time           : 2022/12/24 03:11:02
    Total Up Time          : 355 days, 5 hours, 43 minutes, 39 seconds

 ***VSI Name               : 11
    Work Mode              : normal
    Administrator VSI      : no
    Isolate Spoken         : disable
    VSI Index              : 347
    PW Signaling           : ldp
    Member Discovery Style : --
    Bridge-domain Mode     : disable
    PW MAC Learn Style     : unqualify
    Encapsulation Type     : vlan
    MTU                    : 1500
    Diffserv Mode          : uniform
    Service Class          : --
    Color                  : --
    DomainId               : 255
    Domain Name            :
    Ignore AcState         : disable
    P2P VSI                : disable
    Multicast Fast Switch  : disable
    Create Time            : 355 days, 6 hours, 30 minutes, 55 seconds
    VSI State              : down
    Resource Status        : --

    VSI ID                 : 11
   *Peer Router ID         : 203.135.19.46
    Negotiation-vc-id      : 11
    Encapsulation Type     : vlan
    primary or secondary   : primary
    ignore-standby-state   : no
    VC Label               : 48086
    Peer Type              : dynamic
    Session                : up
    Tunnel ID              : 0x0000000001004c748b 
    Broadcast Tunnel ID    : --
    Broad BackupTunnel ID  : --
    CKey                   : 13
    NKey                   : 16781294
    Stp Enable             : 0
    PwIndex                : 13
    Control Word           : disable
    BFD for PW             : unavailable
 
    Interface Name         : Eth-Trunk20.11
    State                  : down
    Ac Block State         : unblocked
    Access Port            : false
    Last Up Time           : 2023/07/23 21:17:51
    Total Up Time          : 339 days, 22 hours, 42 minutes, 33 seconds
    Interface Name         : GigabitEthernet1/0/18.11
    State                  : down
    Ac Block State         : unblocked
    Access Port            : false
    Last Up Time           : 2023/07/23 20:30:22
    Total Up Time          : 0 days, 0 hours, 0 minutes, 11 seconds

 ***VSI Name               : 110
    Work Mode              : normal
    Administrator VSI      : no
    Isolate Spoken         : disable
    VSI Index              : 307
    PW Signaling           : ldp
    Member Discovery Style : --
    Bridge-domain Mode     : disable
    PW MAC Learn Style     : unqualify
    Encapsulation Type     : vlan
    MTU                    : 1500
    Diffserv Mode          : uniform
    Service Class          : --
    Color                  : --
    DomainId               : 255
    Domain Name            :
    Ignore AcState         : disable
    P2P VSI                : disable
    Multicast Fast Switch  : disable
    Create Time            : 355 days, 6 hours, 30 minutes, 55 seconds
    VSI State              : down
    Resource Status        : --

    VSI ID                 : 110
 
    Interface Name         : Eth-Trunk27.110
    State                  : up
    Ac Block State         : unblocked
    Access Port            : false
    Last Up Time           : 2022/12/24 03:11:02
    Total Up Time          : 355 days, 5 hours, 43 minutes, 39 seconds

 ***VSI Name               : 1122
    Work Mode              : normal
    Administrator VSI      : no
    Isolate Spoken         : disable
    VSI Index              : 162
    PW Signaling           : ldp
    Member Discovery Style : static
    Bridge-domain Mode     : disable
    PW MAC Learn Style     : unqualify
    Encapsulation Type     : vlan
    MTU                    : 1500
    Diffserv Mode          : uniform
    Service Class          : --
    Color                  : --
    DomainId               : 255
    Domain Name            :
    Ignore AcState         : disable
    P2P VSI                : disable
    Multicast Fast Switch  : disable
    Create Time            : 355 days, 6 hours, 30 minutes, 55 seconds
    VSI State              : down
    Resource Status        : --

    VSI ID                 : 1122
 
    Interface Name         : Eth-Trunk27.1122
    State                  : up
    Ac Block State         : unblocked
    Access Port            : false
    Last Up Time           : 2022/12/24 03:11:02
    Total Up Time          : 355 days, 5 hours, 43 minutes, 39 seconds
    Interface Name         : GigabitEthernet1/1/2.1122
    State                  : down
    Ac Block State         : unblocked
    Access Port            : false
    Last Up Time           : 2022/11/24 03:38:09
    Total Up Time          : 99 days, 8 hours, 57 minutes, 36 seconds

 ***VSI Name               : 1124
    Work Mode              : normal
    Administrator VSI      : no
    Isolate Spoken         : disable
    VSI Index              : 276
    PW Signaling           : ldp
    Member Discovery Style : static
    Bridge-domain Mode     : disable
    PW MAC Learn Style     : unqualify
    Encapsulation Type     : vlan
    MTU                    : 1500
    Diffserv Mode          : uniform
    Service Class          : --
    Color                  : --
    DomainId               : 255
    Domain Name            :
    Ignore AcState         : disable
    P2P VSI                : disable
    Multicast Fast Switch  : disable
    Create Time            : 355 days, 6 hours, 30 minutes, 55 seconds
    VSI State              : down
    Resource Status        : --

    VSI ID                 : 1124
 
    Interface Name         : Eth-Trunk27.1124
    State                  : up
    Ac Block State         : unblocked
    Access Port            : false
    Last Up Time           : 2022/12/24 03:11:02
    Total Up Time          : 355 days, 5 hours, 43 minutes, 39 seconds

 ***VSI Name               : 1149
    Work Mode              : normal
    Administrator VSI      : no
    Isolate Spoken         : disable
    VSI Index              : 258
    PW Signaling           : ldp
    Member Discovery Style : static
    Bridge-domain Mode     : disable
    PW MAC Learn Style     : unqualify
    Encapsulation Type     : vlan
    MTU                    : 1500
    Diffserv Mode          : uniform
    Service Class          : --
    Color                  : --
    DomainId               : 255
    Domain Name            :
    Ignore AcState         : disable
    P2P VSI                : disable
    Multicast Fast Switch  : disable
    Create Time            : 355 days, 6 hours, 30 minutes, 55 seconds
    VSI State              : down
    Resource Status        : --

    VSI ID                 : 1149
 
    Interface Name         : Eth-Trunk27.1149
    State                  : up
    Ac Block State         : unblocked
    Access Port            : false
    Last Up Time           : 2022/12/24 03:11:02
    Total Up Time          : 355 days, 5 hours, 43 minutes, 39 seconds

 ***VSI Name               : 1157
    Work Mode              : normal
    Administrator VSI      : no
    Isolate Spoken         : disable
    VSI Index              : 261
    PW Signaling           : ldp
    Member Discovery Style : static
    Bridge-domain Mode     : disable
    PW MAC Learn Style     : unqualify
    Encapsulation Type     : vlan
    MTU                    : 1500
    Diffserv Mode          : uniform
    Service Class          : --
    Color                  : --
    DomainId               : 255
    Domain Name            :
    Ignore AcState         : disable
    P2P VSI                : disable
    Multicast Fast Switch  : disable
    Create Time            : 355 days, 6 hours, 30 minutes, 55 seconds
    VSI State              : down
    Resource Status        : --

    VSI ID                 : 1157
 
    Interface Name         : Eth-Trunk27.1157
    State                  : up
    Ac Block State         : unblocked
    Access Port            : false
    Last Up Time           : 2022/12/24 03:11:02
    Total Up Time          : 355 days, 5 hours, 43 minutes, 39 seconds

 ***VSI Name               : 1304
    Work Mode              : normal
    Administrator VSI      : no
    Isolate Spoken         : disable
    VSI Index              : 266
    PW Signaling           : ldp
    Member Discovery Style : static
    Bridge-domain Mode     : disable
    PW MAC Learn Style     : unqualify
    Encapsulation Type     : vlan
    MTU                    : 1500
    Diffserv Mode          : uniform
    Service Class          : --
    Color                  : --
    DomainId               : 255
    Domain Name            :
    Ignore AcState         : disable
    P2P VSI                : disable
    Multicast Fast Switch  : disable
    Create Time            : 355 days, 6 hours, 30 minutes, 55 seconds
    VSI State              : down
    Resource Status        : --

    VSI ID                 : 1304
 
    Interface Name         : Eth-Trunk27.1304
    State                  : up
    Ac Block State         : unblocked
    Access Port            : false
    Last Up Time           : 2022/12/24 03:11:02
    Total Up Time          : 355 days, 5 hours, 43 minutes, 39 seconds

 ***VSI Name               : 1503
    Work Mode              : normal
    Administrator VSI      : no
    Isolate Spoken         : disable
    VSI Index              : 222
    PW Signaling           : ldp
    Member Discovery Style : static
    Bridge-domain Mode     : disable
    PW MAC Learn Style     : unqualify
    Encapsulation Type     : vlan
    MTU                    : 1500
    Diffserv Mode          : uniform
    Service Class          : --
    Color                  : --
    DomainId               : 255
    Domain Name            :
    Ignore AcState         : disable
    P2P VSI                : disable
    Multicast Fast Switch  : disable
    Create Time            : 355 days, 6 hours, 30 minutes, 55 seconds
    VSI State              : down
    Resource Status        : --

    VSI ID                 : 1503
 
    Interface Name         : Eth-Trunk27.1503
    State                  : up
    Ac Block State         : unblocked
    Access Port            : false
    Last Up Time           : 2022/12/24 03:11:02
    Total Up Time          : 355 days, 5 hours, 43 minutes, 39 seconds
    Interface Name         : GigabitEthernet1/1/2.1503
    State                  : down
    Ac Block State         : unblocked
    Access Port            : false
    Last Up Time           : 2022/11/24 03:38:09
    Total Up Time          : 99 days, 8 hours, 57 minutes, 36 seconds

"""

raw_result2 = raw_result.split('***')


# pprint(raw_result2)
for raw_result in raw_result2:
    if not raw_result.strip():
        continue

    data = {}
    raw_result1 = raw_result.split('\n')
    current_interface = None
    interfaces = []
    current_peer = None
    peer_ip_address = []
    for line in raw_result1:
        if ':' in line:
            key, value = map(str.strip, line.split(':', 1))
    
            if key == 'VSI Name':
                data.update({'VSI Name': value})
            elif key == 'PW Signaling':
                data.update({'PW Signaling': value})
            elif key == 'VSI State':
                data.update({'VSI State': value})
            elif key == 'VSI ID':
                data.update({'VSI ID': value})  


            elif key == 'Interface Name':
                if current_interface is not None:
                    interfaces.append(current_interface)
                current_interface = {'Interface Name': value}
            elif key == 'State':
                current_interface.update({'State': value})
            elif key == 'Ac Block State':
                current_interface.update({'Ac Block State': value})
            elif key == 'Last Up Time':
                current_interface.update({'Last Up Time': value})
 
            elif key == '*Peer Ip Address':
                if current_peer is not None:
                    peer_ip_address.append(current_peer)
                current_peer = {'*Peer Ip Address': value}
            elif key == 'PW State':
                current_peer.update({'PW State': value})  



    # Add the last interface
    if current_interface is not None:
        interfaces.append(current_interface)

    if current_peer is not None:
        peer_ip_address.append(current_peer)
    # print(interfaces)  
    data.update({'peer_ip': peer_ip_address})  
    data.update({'interfaces': interfaces})
    pprint(data)
    # x = data.get('peer_ip')
    y = [interface_dict.get('*Peer Ip Address') for interface_dict in data.get('peer_ip')]
    print(y)
    print(len(data['peer_ip']))


