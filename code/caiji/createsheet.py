from sqlalchemy import create_engine, text, join 
from sqlalchemy.orm import sessionmaker
from pprint import pprint
from xlsxwriter import Workbook
import pandas as pd
import datetime
import os
from sqlite3_orm_create_table_device_info import Router, Interface, L2vc, Arp, Lldp, Bgp, Vsi, Vsi_peer, Vpn_instance, engine
from ipaddress import ip_network, ip_address

# 连接到数据库
# engine = create_engine('sqlite:///sqlalchemy_sqlite3_device_info.db?check_same_thread=False')
Session = sessionmaker(bind=engine)
session = Session()

# 
sql_query = text('''
    SELECT
        r.routername AS DeviceName,
        r.ip AS IP,
        -- r.routernamenew AS NewName,
        i.interface_name AS Interface,
        i.Physical_State AS Status,
        i.Protocol_State AS ProtocolStatus,
        n.Peer_Device AS NeighborDevice,
        n.Peer_Port AS NeighborInterface,
        i.Description AS Description,
        i.ip_address AS IpAddress,
        i.Current_BW AS Speed,
        i.Port_max_bw AS maxSpeed,
        i.Transceiver_Mode AS Mode,
        i.WaveLength AS Wavelength,
        i.Transmission_Distance AS Distance,
        i.Rx_Power AS RxPower,
        i.Tx_Power AS TxPower,
        i.Last_physical_down_time AS LastUpdate,
        i.Input_bandwidth AS InputBw,
        i.Output_bandwidth AS OutputBw
    FROM
        router r
    JOIN
        interface i ON r.id = i.router_id
    LEFT JOIN
        lldp n ON r.id = n.router_id AND i.interface_name = n.local_port
''')

# 提交会话中的任何更改
session.commit()

# 执行查询
result = session.execute(sql_query)
# for row in result:
#     print(row)

# 将结果转换为 DataFrame
result_df = pd.DataFrame(result.fetchall(), columns=result.keys())


# Query devices and BGP status
query = session.query(Router, Bgp).join(Bgp)
result = query.all()

# Create a list of dictionaries for the data
data_bgp = [{'Router Name': router.routername,
         'Router IP': router.ip, 
         'BGP Peer': bgp.Peer,
         'BGP Status': bgp.Peer_status}
        for router, bgp in result]

# print(data_bgp)

# Create a DataFrame from the data
bgp_df = pd.DataFrame(data_bgp)

query = session.query(Router, Arp).join(Arp)
result = query.all()
data_arp = [{'Router Name': router.routername,
         'Router IP': router.ip, 
         'IP_ADDRESS': arp.IP_ADDRESS,
         'MAC_ADDRESS': arp.MAC_ADDRESS,
         'EXPIRE': arp.EXPIRE,
         'TYPE': arp.TYPE,
         'INTERFACE': arp.INTERFACE,
         'VPN_INSTANCE': arp.VPN_INSTANCE}
        for router, arp in result]

# print(data_arp)
arp_df = pd.DataFrame(data_arp)


query = session.query(Router, L2vc).join(L2vc)
result = query.all()
data_l2vc = [{'Router Name': router.routername,
         'Router IP': router.ip, 
         'VC_ID': l2vc.VC_ID,
         'VC_Type': l2vc.VC_Type,
         'VC_State': l2vc.VC_State,
         'AC_status': l2vc.AC_status,
         'session_state': l2vc.session_state,
         'Destination': l2vc.Destination,
         'interface': l2vc.interface,                 
         'link_state': l2vc.link_state}
        for router, l2vc in result]

# print(data_l2vc)
l2vc_df = pd.DataFrame(data_l2vc)


query = session.query(Router, Lldp).join(Lldp)
result = query.all()
data_lldp = [{'Router Name': router.routername,
         'Router IP': router.ip, 
         'Local_Port': lldp.Local_Port,
         'Peer_Device': lldp.Peer_Device,               
         'Peer_Port': lldp.Peer_Port}
        for router, lldp in result]

# print(data_lldp)
lldp_df = pd.DataFrame(data_lldp)
lldp_df['Local_Port'].replace('', pd.NA, inplace=True)
lldp_df['Local_Port'] = lldp_df['Local_Port'].ffill()
pd.set_option('display.max_columns', None)
print(lldp_df.head(12))

# 创建新列，将 'Router Name' 和 'Local_Port' 组合
lldp_df['Combined'] = lldp_df['Router Name'] + '_' + lldp_df['Local_Port']

# 找到需要标红的行索引
duplicate_rows = lldp_df.duplicated(subset=['Combined'], keep=False)

# 将标红的行索引转换成布尔型 Series
red_rows = duplicate_rows.copy()

# 将 'Local_Port' 列中对应的重复行标红
lldp_df['Local_Port_Red'] = red_rows.map({True: 'red', False: ''})


query = session.query(Router, Vsi).join(Vsi)
result = query.all()
data_vsi = [{'Router Name': router.routername,
         'Router IP': router.ip, 
         'VSI_Name': vsi.VSI_Name,
         'PW_Signaling': vsi.PW_Signaling, 
         'VSI_State': vsi.VSI_State,
         'VSI_ID': vsi.VSI_ID,
         'Interface_Name': vsi.Interface_Name,
         'Interface_State': vsi.Interface_State,
         'Ac_Block_State': vsi.Ac_Block_State}
        for router, vsi in result]

# print(data_vsi)
vsi_df = pd.DataFrame(data_vsi)


query = session.query(Router, Vpn_instance).join(Vpn_instance)
result = query.all()
data_vpn = [{'Router Name': router.routername,
         'Router IP': router.ip, 
         'vpn_instance_name': vpn.vpn_instance_name,
         'interfaces': vpn.interfaces, 
         'route_distinguisher': vpn.route_distinguisher,
         'export_vpn_targets': vpn.export_vpn_targets,
         'import_vpn_targets': vpn.import_vpn_targets}
        for router, vpn in result]

# print(data_vpn)
vpn_df = pd.DataFrame(data_vpn)


query = session.query(Router, Vsi_peer).join(Vsi_peer)
result = query.all()
# print(result)
data_vsi_peer = [{'Router Name': router.routername,
                  'Router IP': router.ip, 
                  'VSI_Name': vsi.VSI_Name,
                  'PW_Signaling': vsi.PW_Signaling, 
                  'VSI_State': vsi.VSI_State,
                  'VSI_ID': vsi.VSI_ID,
                  'Peer_Ip_Address': vsi.Peer_Ip_Address,
                  'PW_Last_Up_Time': vsi.PW_Last_Up_Time}
                 for router, vsi in result]
# print(data_vsi_peer)
vsi_peer_df = pd.DataFrame(data_vsi_peer)   

query = session.query(Router, Interface).join(Interface)
result = query.all()
data_ip = [{'Router Name': router.routername,
                  'Router IP': router.ip, 
                  'IP Address': ip.ip_address,
                  'Subnet Mask': ip.ip_address.split('/')[1] if '/' in ip.ip_address else ''}
                 for router, ip in result if ip.ip_address]

private_networks = [
    ip_network("10.0.0.0/8"),
    ip_network("172.16.0.0/12"),
    ip_network("192.0.0.0/8")
]

ip_add = []
for item in data_ip:
    ip_network_obj = ip_network(item['IP Address'], strict=False)
    all_addresses = list(ip_network_obj)
    sorted_addresses = sorted(all_addresses)
    for address in sorted_addresses:
        if not any(ip_address(address) in private_net for private_net in private_networks):
            new_item = item.copy()
            new_item['IP'] = str(address)
            ip_add.append(new_item)
# print(ip_add)
ip_add_df = pd.DataFrame(ip_add) 

# # 定义 Excel 文件的路径
nowTime = datetime.datetime.now().strftime('%Y-%m-%d')
folder_path = 'C:\\Users\\YanJ\\Desktop\\code\\caiji'  
excel_file = os.path.join(folder_path, f'device_info {nowTime}.xlsx')

# 打印 Excel 文件的路径（调试信息）
print(f"Excel file path: {excel_file}")

# 将结果写入 Excel 文件
with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer:
    result_df.to_excel(writer, sheet_name='Port status', index=False)
    arp_df.to_excel(writer, sheet_name='arp status', index=False)
    l2vc_df.to_excel(writer, sheet_name='l2vc status', index=False)
    vsi_df.to_excel(writer, sheet_name='vsi port status', index=False)
    vsi_peer_df.to_excel(writer, sheet_name='vsi peer status', index=False)        
    lldp_df.drop(columns=['Combined', 'Local_Port_Red']).to_excel(writer, sheet_name='lldp status', index=False)
    bgp_df.to_excel(writer, sheet_name='bgp status', index=False)
    vpn_df.to_excel(writer, sheet_name='vpn_instance status', index=False)
    ip_add_df.to_excel(writer, sheet_name='ip address', index=False)

    worksheet = writer.sheets['lldp status']
    red_format = writer.book.add_format({'bg_color': '#FFC7CE'})
    # 标红 'Local_Port' 列
    for idx, color in enumerate(lldp_df['Local_Port_Red']):
        if color == 'red':
            worksheet.write(idx+1, 2, lldp_df['Local_Port'][idx], red_format)
        else:
            worksheet.write(idx+1, 2, lldp_df['Local_Port'][idx])

# 关闭数据库连接
session.close()

# # 打印 DataFrame
# print(result_df)
