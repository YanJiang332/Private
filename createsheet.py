from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import pandas as pd
import datetime
import os
from sqlite3_orm_create_table_device_info import Router, Interface, L2vc, Arp, Lldp, Bgp, engine
# 连接到数据库
# engine = create_engine('sqlite:///sqlalchemy_sqlite3_device_info.db?check_same_thread=False')
Session = sessionmaker(bind=engine)
session = Session()

# 编写 SQL 查询语句
sql_query = text('''
    SELECT
        r.routername AS DeviceName,
        r.ip AS IP,
        r.routernamenew AS NewName,
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
data = [{'Router Name': router.routername,
         'Router IP': router.ip, 
         'BGP Peer': bgp.Peer,
         'BGP Status': bgp.Peer_status}
        for router, bgp in result]

print(data)

# # Create a DataFrame from the data
# bgp_df = pd.DataFrame(data)

# # 定义 Excel 文件的路径
# nowTime = datetime.datetime.now().strftime('%Y-%m-%d')
# folder_path = 'C:\\Users\\y84292119\\Desktop\\KENYA\\code\\ceshi'  
# excel_file = os.path.join(folder_path, f'Port_info {nowTime}.xlsx')

# # 打印 Excel 文件的路径（调试信息）
# print(f"Excel file path: {excel_file}")

# # 将结果写入 Excel 文件
# with pd.ExcelWriter(excel_file) as writer:
#     result_df.to_excel(writer, sheet_name='Port status', index=False)
#     bgp_df.to_excel(writer, sheet_name='bgp status', index=False)

# # 关闭数据库连接
# session.close()

# # 打印 DataFrame
# print(result_df)
