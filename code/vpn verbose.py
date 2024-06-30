from textfsm import TextFSM
from pprint import pprint
import re 

raw_result = """
<SNHZH-MC-CMNET-BRAS09-YXXGS/X16A>display ip vpn-instance verbose
 Total VPN-Instances configured      : 11
 Total IPv4 VPN-Instances configured : 11
 Total IPv6 VPN-Instances configured : 1

 VPN-Instance Name and ID : ChinaMobile_CMNET_SN_IMS, 1
  Interfaces : Eth-Trunk12.2900,
               Eth-Trunk18.2900,
               Eth-Trunk20.2900,
               Eth-Trunk22.2900,
               Eth-Trunk25.2900,
               Eth-Trunk29.2900,
               Eth-Trunk32.2900,
               Eth-Trunk39.4,
               Eth-Trunk40.2900,
               Eth-Trunk42.2900,
               Eth-Trunk43.2900,
               Eth-Trunk44.2900,
               Eth-Trunk51.2900,
               Eth-Trunk65.2900,
               Eth-Trunk67.2900,
               Eth-Trunk71.2900,
               Eth-Trunk76.2900,
               Eth-Trunk79.2900
 Address family ipv4
  Create date : 2023-03-29 03:18:49+08:00
  Up time : 375 days, 16 hours, 43 minutes and 08 seconds     
  Vrf Status : UP
  Route Distinguisher : 64650:10009160
  Export VPN Targets : 64650:10009160 64650:10000290
  Import VPN Targets : 64650:10009160 64650:10000290
  Label Policy : label per route
  The diffserv-mode Information is : uniform
  The ttl-mode Information is : pipe

 VPN-Instance Name and ID : ChinaMobile_CMNET_SN_PON_NMS, 2
  Interfaces : Eth-Trunk10.2,
               Eth-Trunk11.2,
               Eth-Trunk12.2,
               Eth-Trunk13.2,
               Eth-Trunk14.2,
               Eth-Trunk15.2,
               Eth-Trunk16.2,
               Eth-Trunk17.2,
               Eth-Trunk18.2,
               Eth-Trunk19.2,
               Eth-Trunk20.2,
               Eth-Trunk21.2,
               Eth-Trunk22.2,
               Eth-Trunk23.2,
               Eth-Trunk24.2,
               Eth-Trunk25.2,
               Eth-Trunk26.2,
               Eth-Trunk27.2,
               Eth-Trunk28.2,
               Eth-Trunk29.2,
               Eth-Trunk30.2,
               Eth-Trunk31.2,
               Eth-Trunk32.2,
               Eth-Trunk33.2,
               Eth-Trunk35.2,
               Eth-Trunk36.2,
               Eth-Trunk37.2,
               Eth-Trunk38.2,
               Eth-Trunk39.2,
               Eth-Trunk40.2,
               Eth-Trunk41.2,
               Eth-Trunk42.2,
               Eth-Trunk43.2,
               Eth-Trunk44.2,
               Eth-Trunk46.11,
               Eth-Trunk47.2,
               Eth-Trunk51.2,
               Eth-Trunk52.2,
               Eth-Trunk53.2,
               Eth-Trunk57.2,
               Eth-Trunk58.2,
               Eth-Trunk59.2,
               Eth-Trunk60.2,
               Eth-Trunk61.2,
               Eth-Trunk65.2,
               Eth-Trunk67.2,
               Eth-Trunk69.2,
               Eth-Trunk70.2,
               Eth-Trunk71.2,
               Eth-Trunk72.2,
               Eth-Trunk74.2,
               Eth-Trunk76.2,
               Eth-Trunk77.2,
               Eth-Trunk78.2,
               Eth-Trunk79.2,
               Eth-Trunk80.2,
               Eth-Trunk81.2,
               Eth-Trunk82.2,
               Eth-Trunk83.2,
               Eth-Trunk85.2,
               Eth-Trunk86.2,
               Eth-Trunk87.2,
               Eth-Trunk88.2,
               Eth-Trunk89.2,
               Eth-Trunk49.2,
               Eth-Trunk66.2,
               Eth-Trunk90.2
 Address family ipv4
  Create date : 2023-03-29 03:18:49+08:00
  Up time : 375 days, 16 hours, 43 minutes and 08 seconds     
  Vrf Status : UP
  Route Distinguisher : 64650:20009160
  Export VPN Targets : 64650:20009160 64650:100000082
  Import VPN Targets : 64650:20009160 64650:100000082
  Label Policy : label per route
  The diffserv-mode Information is : uniform
  The ttl-mode Information is : pipe
"""

# with open('./template/display_vpn_verbose.template') as f:
#     template = TextFSM(f)
#     parsed_data = template.ParseText(raw_result)
#     pprint(parsed_data)




# 使用空行分割VPN实例块
vpn_blocks = re.split(r'\n\s*\n', raw_result.strip())

# 定义捕获所需信息的正则表达式
vpn_instance_pattern = re.compile(r'^\s*VPN-Instance Name and ID\s*:\s*(\S+,\s\d+)')
interface_pattern = re.compile(r'^\s*Interfaces\s*:\s*(.+)')
additional_interface_pattern = re.compile(r'^\s+(\S+)')
route_distinguisher_pattern = re.compile(r'^\s*Route Distinguisher\s*:\s*(\d+:\d+)')
export_vpn_targets_pattern = re.compile(r'^\s*Export VPN Targets\s*:\s*(.+)')
import_vpn_targets_pattern = re.compile(r'^\s*Import VPN Targets\s*:\s*(.+)')

vpn_data = []

# 处理每个块并提取所需信息
for block in vpn_blocks:
    block = block.strip()
    if not block:
        continue
    
    # 检查块是否包含VPN实例信息
    if "VPN-Instance Name and ID" not in block:
        print("VPN instance information not found in block. Skipping...")
        continue
    
    vpn_instance_match = vpn_instance_pattern.search(block)
    if vpn_instance_match:
        vpn_instance_name = vpn_instance_match.group(1).strip()
    else:
        print("VPN instance pattern not matched!")
        continue
    
    interface_match = interface_pattern.search(block)
    if interface_match:
        interfaces = [interface_match.group(1).strip()]
        additional_interfaces = additional_interface_pattern.findall(block)
        interfaces.extend(additional_interfaces)
        interfaces = ', '.join(interfaces)
    else:
        interfaces = ''
    
    route_distinguisher_match = route_distinguisher_pattern.search(block)
    if route_distinguisher_match:
        route_distinguisher = route_distinguisher_match.group(1).strip()
    else:
        print("Route distinguisher pattern not matched!")
        continue
    
    export_vpn_targets_match = export_vpn_targets_pattern.search(block)
    if export_vpn_targets_match:
        export_vpn_targets = export_vpn_targets_match.group(1).strip()
    else:
        print("Export VPN targets pattern not matched!")
        continue
    
    import_vpn_targets_match = import_vpn_targets_pattern.search(block)
    if import_vpn_targets_match:
        import_vpn_targets = import_vpn_targets_match.group(1).strip()
    else:
        print("Import VPN targets pattern not matched!")
        continue
    
    vpn_data.append([
        vpn_instance_name,
        interfaces,
        route_distinguisher,
        export_vpn_targets,
        import_vpn_targets
    ])

pprint(vpn_data)