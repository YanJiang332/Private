import os
from tkinter import Tk, filedialog
import re
from textfsm import TextFSM
import datetime
from pprint import pprint
import codecs
from sqlalchemy.orm import sessionmaker
from sqlite3_orm_create_table_device_info import Router, Interface, L2vc, Arp, Lldp, Bgp, Vsi, Vsi_peer, engine
import json

Session = sessionmaker(bind=engine)
session = Session()


def check_expiration():
    expiration_date = datetime.datetime(2024, 7, 1)

    current_date = datetime.datetime.now()

    if current_date > expiration_date:
        print("不能继续执行。")
        return False
    else:
        return True


def get_device_info(file_data):
    """
    从文件内容中获取设备名称和设备IP地址
    """
    device_name = ""
    device_ip = ""
    for line in file_data.split("\n"):
        if line.startswith("sysname"):
            device_name = line.split()[1]
        if line.startswith("router id") or line.startswith("mpls lsr-id"):
            device_ip = line.split()[2]
            break
    # print(device_name)
    return device_name, device_ip


def find_matching_paragraphs(content, device_name, search):
    # paragraphs = re.split(rf'<{device_name}>', content)
    if device_name:
        pattern = rf'<{re.escape(device_name)}>'
        # print(pattern)
        paragraphs = re.split(pattern, content)
        # print(paragraphs)
        for paragraph in paragraphs:
            if search in paragraph:
                # print(paragraph)

                return paragraph
    return None

def get_table_data_port(paragraph):
    """
    从文件内容中获取表格数据
    """

    if paragraph is not None:
        entries = paragraph.split("***")
        table_data = []
        for entry in entries:
            if not entry.strip():
                continue
            data = {"VSI Name": "N/A", "PW Signaling": "N/A", "VSI State": "N/A",
                    "VSI ID": "N/A", "Interface Name": [], "Interface State": [], "Ac Block State": []}
            lines = entry.split("\n")
            # print(lines)
            for line in lines:
                parts = line.split(" : ")
                if len(parts) == 2:
                    field_name = parts[0].strip()
                    field_value = parts[1].strip()
                    if field_name == "VSI Name":
                        data["VSI Name"] = field_value
                    elif field_name == "PW Signaling":
                        data["PW Signaling"] = field_value
                    elif field_name == "VSI State":
                        data["VSI State"] = field_value
                    elif field_name == "VSI ID":
                        data["VSI ID"] = field_value
                    elif field_name == "Interface Name":
                        data["Interface Name"].append(field_value)
                    elif field_name == "State":
                        data["Interface State"].append(field_value)
                    elif field_name == "Ac Block State":
                        data["Ac Block State"].append(field_value)
        #     table_data.append(data)
        # return table_data

            # 分别处理 Peer Ip Address 和 PW Last Up Time，将其拆分为多个字段
            for i in range(max(len(data["Interface Name"]), len(data["Interface State"]), len(data["Ac Block State"]))):
                new_data = data.copy()
                new_data["Interface Name"] = data["Interface Name"][i] if i < len(
                    data["Interface Name"]) else ""
                new_data["Interface State"] = data["Interface State"][i] if i < len(
                    data["Interface State"]) else ""
                new_data["Ac Block State"] = data["Ac Block State"][i] if i < len(
                    data["Ac Block State"]) else ""
                table_data.append(new_data)
        return table_data


def get_table_data_l2vc(paragraph):
    """
    从文件内容中获取表格数据
    """
    if paragraph is not None:
        # print(paragraph)
        entries = paragraph.split("*")
        table_data = []
        for entry in entries:
            if 'Client Interface' in entry:
                # pprint(entry)
                data = {"Interface": "N/A", "AC status": "N/A", "VC State": "N/A",
                        "VC ID": "N/A", "VC Type": "N/A", "session state": "N/A", "Destination": "N/A", "link state": "N/A"}
                lines = entry.split("\n")
                for line in lines:
                    parts = line.split(" : ")
                    # print(parts)
                    if len(parts) == 2:
                        field_name = parts[0].strip()
                        field_value = re.sub(r'\s', '', parts[1].strip())
                        if field_name == "Client Interface":
                            data["Interface"] = field_value
                        elif field_name == "AC status":
                            data["AC status"] = field_value
                        elif field_name in ["VC state", "VC State"]:
                            data["VC State"] = field_value
                        elif field_name == "VC ID":
                            data["VC ID"] = field_value
                        elif field_name == "VC Type":
                            data["VC Type"] = field_value
                        elif field_name == "session state":
                            data["session state"] = field_value
                        elif field_name == "Destination":
                            data["Destination"] = field_value
                        elif field_name == "link state":
                            data["link state"] = field_value
                table_data.append(data)
        # pprint(table_data)
        return table_data
    else:
        return []

def get_table_data(paragraph):
    """
    从文件内容中获取表格数据
    """
    if paragraph is not None:
        entries = paragraph.split("***")
        table_data = []
        for entry in entries:
            # print(entry)
            if not entry.strip():
                continue
            data = {"VSI Name": "N/A", "PW Signaling": "N/A", "VSI State": "N/A",
                    "VSI ID": "N/A", "Peer Ip Address": [], "PW Last Up Time": []}
            lines = entry.split("\n")
            for line in lines:
                parts = line.split(" : ")
                if len(parts) == 2:
                    field_name = parts[0].strip()
                    field_value = parts[1].strip()
                    if field_name == "VSI Name":
                        data["VSI Name"] = field_value
                    elif field_name == "PW Signaling":
                        data["PW Signaling"] = field_value
                    elif field_name == "VSI State":
                        data["VSI State"] = field_value
                    elif field_name == "VSI ID":
                        data["VSI ID"] = field_value
                    elif field_name == "*Peer Ip Address":
                        data["Peer Ip Address"].append(field_value)
                    elif field_name == "PW Last Up Time":
                        data["PW Last Up Time"].append(field_value)
            # table_data.append(data)
        # return table_data

            # 分别处理 Peer Ip Address 和 PW Last Up Time，将其拆分为多个字段
            for i in range(max(len(data["Peer Ip Address"]), len(data["PW Last Up Time"]))):
                new_data = data.copy()
                new_data["Peer Ip Address"] = data["Peer Ip Address"][i] if i < len(
                    data["Peer Ip Address"]) else ""
                new_data["PW Last Up Time"] = data["PW Last Up Time"][i] if i < len(
                    data["PW Last Up Time"]) else ""
                table_data.append(new_data)
        # print(table_data)
        return table_data


def get_table_data_interface(paragraph):
    """
    从文件内容中获取表格数据
    """
    data_list_interface = []

    with open(f'../template/display_interface.template') as f:
        template = TextFSM(f)
        # print(template)
    if paragraph is None:
        return []
    parsed_data = re.split(r'\n\n+', paragraph)
    for entrys in parsed_data:
        # print(entrys)
        interface_data = template.ParseText(entrys)
        # print(interface_data)
    return interface_data


def get_table_data_info(raw_result):
    arp_info = []
    with open(f'../template/display_arp.template') as f:
        template = TextFSM(f)
        show_vlan_dict = template.ParseText(raw_result)
        arp_info.extend(show_vlan_dict)
    return arp_info


def get_table_lldp(raw_result):
    # parts = re.split(r'\n\n\n', raw_result)
    # if 'System name' in parts:
    #     print(parts)
    # parts = parts[1:]
    # data = {parts[i]: parts[i + 1] for i in range(0, len(parts), 2)}
    data_lldp = []
    try:
        with open(f'../template/display_lldp_neighbor.template', encoding='utf-8') as f:
            template = TextFSM(f)
            lldp = template.ParseText(raw_result)
            data_lldp.extend(lldp)
            # print(data_lldp)
            return data_lldp
    except Exception as e1:
        print(f"Error with template 1: {e1}")
    # try:
    #     with open(f'display_lldp_neighbor2.template', encoding='utf-8') as f2:
    #         template_2 = TextFSM(f2)
    #         lldp_2 = template_2.ParseText(raw_result)
    #         data_lldp.extend(lldp_2)
    #         print(data_lldp)
    #         return data_lldp
    # except Exception as e2:
    #     print(f"Error with template 2: {e2}")

    return data_lldp


def get_table_bgp(raw_result):
    # parts = re.split(r'\n\n\n', raw_result)
    # if 'System name' in parts:
    #     print(parts)
    # parts = parts[1:]
    # data = {parts[i]: parts[i + 1] for i in range(0, len(parts), 2)}
    data_bgp = []
    with open(f'../template/display_bgp.template') as f:
        template = TextFSM(f)
        bgp = template.ParseText(raw_result)
        data_bgp.extend(bgp)
    # print(data_lldp)
    return data_bgp


def get_all_files(script_path):
    # 当前工作目录下所有子文件夹的名称组成的列表
    # folders = [folder for folder in os.listdir(script_path) if os.path.isdir(os.path.join(script_path, folder))]
    files = []
    # for folder in folders:
    #     root_folder_path = os.path.join(script_path, folder)
    for folder_path, subfolders, filenames in os.walk(script_path):
        for filename in filenames:
            if filename.endswith((".txt", ".log")):
                files.append(os.path.join(folder_path, filename))
    return files


def process_file(filename):
    data_dict = {}
    try:
        with codecs.open(filename, 'r', encoding='utf-8') as file:
            file_data = file.read()
            # print(file_data)
    except UnicodeError:
        with codecs.open(filename, 'r', encoding='utf-16') as file:
            file_data = file.read()
    device_interface = {}
    device_interface_description = {}
    device_arp = {}
    device_name, device_ip = get_device_info(file_data)
    print(device_name)
    new_device_name = device_name.replace('ATN910C-G-CSG01', 'ATN910D-A-CSG01').replace('ATN910B-CSG01', 'ATN910D-A-CSG01')
    data_dict.update({'device_name': f'{device_name}', 'device_ip': f'{device_ip}', 'new_device_name': f'{new_device_name}'})
    paragraph_vsi = find_matching_paragraphs(
        file_data, device_name, 'display vsi verbose')
    paragraph_l2vc = find_matching_paragraphs(
        file_data, device_name, 'display mpls l2vc brief')
    paragraph_interface = find_matching_paragraphs(
        file_data, device_name, 'display interface')
    paragraph_arp = find_matching_paragraphs(
        file_data, device_name, 'display arp all')
    paragraph_lldp = find_matching_paragraphs(
        file_data, device_name, 'display lldp neighbor')
    paragraph_bgp = find_matching_paragraphs(
        file_data, device_name, 'display bgp vpnv4 all peer')
    # print(paragraph_l2vc)

    data_list_peer = get_table_data(paragraph_vsi)

    data_list_port = get_table_data_port(paragraph_vsi)

    data_dict_l2vc = get_table_data_l2vc(paragraph_l2vc)
    # print(data_list_l2vc)
    # if data_list_l2vc is not None:
    #     data_dict_l2vc = [dict(zip(table_header_l2vc, item)) for item in data_list_l2vc]

    table_header_arp = ["IP ADDRESS", "MAC ADDRESS",
                        "EXPIRE", "TYPE", "INTERFACE", "VPN-INSTANCE"]
    data_list_arp = get_table_data_info(paragraph_arp)
    data_dict_arp = [dict(zip(table_header_arp, item))
                     for item in data_list_arp]

    table_header_interface = ["Interface", "Physical State",
                              "Protocol State", "Description", "ip_address", "Port_bw", "Port_max_bw", "Transceiver Mode", "WaveLength", "Transmission Distance",
                              "Rx Power", "Tx Power", "Last physical down time", "Input bandwidth", "Output bandwidth"]
    data_list_interface = get_table_data_interface(paragraph_interface)
    # print(data_list_interface)
    data_dict_interface = [dict(zip(table_header_interface, item))
                           for item in data_list_interface]

    table_header_lldp = ["Local_Port", "Peer_Port", "Peer_Device"]
    data_list_lldp = get_table_lldp(paragraph_lldp)
    data_dict_lldp = [dict(zip(table_header_lldp, item))
                      for item in data_list_lldp]
    # print(data_dict_lldp)

    table_header_bgp = ["peer", "version", "AS number", "status"]
    data_list_bgp = get_table_bgp(paragraph_bgp)
    data_dict_bgp = [dict(zip(table_header_bgp, item))
                     for item in data_list_bgp]

    data_dict.update({'Interfaces': f'{data_dict_interface}'})
    data_dict.update({'l2vc': f'{data_dict_l2vc}'})
    data_dict.update({'arp': f'{data_dict_arp}'})
    data_dict.update({'lldp': f'{data_dict_lldp}'})
    data_dict.update({'bgp': f'{data_dict_bgp}'})
    data_dict.update({'vsi': f'{data_list_port}'})
    data_dict.update({'vsi_peer': f'{data_list_peer}'})    
    pprint(data_dict['vsi_peer'])
    return data_dict


def get_folder_path():
    root = Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory(title="Select Folder")
    return folder_path


def main():
    folder_path = get_folder_path()
    files = get_all_files(folder_path)
    for filename in files:
        data_dict = process_file(filename)
        # print(data_dict)
        router_device = Router(
            routername=data_dict['device_name'], ip=data_dict['device_ip'], routernamenew=data_dict['new_device_name'])
        session.add(router_device)

        interfaces_str = data_dict['Interfaces'].replace("'", "\"")
        print(interfaces_str)
        interfaces_list = json.loads(interfaces_str)
        # print(interfaces_list)

        for interface in interfaces_list:
            rx_power_str = ','.join(map(str, interface['Rx Power']))
            tx_power_str = ','.join(map(str, interface['Tx Power']))
            device_interface = Interface(
                router=router_device,
                interface_name=interface['Interface'],
                Physical_State=interface['Physical State'],
                Protocol_State=interface['Protocol State'],
                Description=interface['Description'],
                ip_address=interface['ip_address'],
                Current_BW=interface['Port_bw'],
                Port_max_bw=interface['Port_max_bw'],
                Transceiver_Mode=interface['Transceiver Mode'],
                WaveLength=interface['WaveLength'],
                Transmission_Distance=interface['Transmission Distance'],
                Rx_Power=rx_power_str,  # 使用转换后的字符串
                Tx_Power=tx_power_str,  # 使用转换后的字符串
                # Rx_Power=interface['Rx Power'],
                # Tx_Power=interface['Tx Power'],
                Last_physical_down_time=interface['Last physical down time'],
                Input_bandwidth=interface['Input bandwidth'],
                Output_bandwidth=interface['Output bandwidth']
            )
            session.add(device_interface)

        l2vc_str = data_dict['l2vc'].replace("'", "\"")
        # print(l2vc_str)
        l2vc_list = json.loads(l2vc_str)
        # print(l2vc_list)

        for l2vc in l2vc_list:
            device_l2vc = L2vc(
                router=router_device,
                interface=l2vc['Interface'],
                AC_status=l2vc['AC status'],
                VC_State=l2vc['VC State'],
                VC_ID=l2vc['VC ID'],
                VC_Type=l2vc['VC Type'],
                session_state=l2vc['session state'],
                Destination=l2vc['Destination'],
                link_state=l2vc['link state']
            )
            session.add(device_l2vc)

        arp_str = data_dict['arp'].replace("'", "\"")
        # print(arp_str)
        arp_list = json.loads(arp_str)
        # print(arp_list)

        for arp in arp_list:
            device_arp = Arp(
                router=router_device,
                IP_ADDRESS=arp['IP ADDRESS'],
                MAC_ADDRESS=arp['MAC ADDRESS'],
                EXPIRE=arp['EXPIRE'],
                TYPE=arp['TYPE'],
                INTERFACE=arp['INTERFACE'],
                VPN_INSTANCE=arp['VPN-INSTANCE']
            )
            session.add(device_arp)

        lldp_str = data_dict['lldp'].replace("'", "\"")
        # print(arp_str)
        lldp_list = json.loads(lldp_str)
        # print(arp_list)

        for lldp in lldp_list:
            device_lldp = Lldp(
                router=router_device,
                Local_Port=lldp['Local_Port'],
                Peer_Port=lldp['Peer_Port'],
                Peer_Device=lldp['Peer_Device']
            )
            session.add(device_lldp)

        bgp_str = data_dict['bgp'].replace("'", "\"")
        # print(arp_str)
        bgp_list = json.loads(bgp_str)
        # print(arp_list)

        for bgp in bgp_list:
            device_bgp = Bgp(
                router=router_device,
                Peer=bgp['peer'],
                Version=bgp['version'],
                AS_number=bgp['AS number'],
                Peer_status=bgp['status']
            )
            session.add(device_bgp)

        vsi_str = data_dict['vsi'].replace("'", "\"")
        vsi_list = json.loads(vsi_str)

        for vsi in vsi_list:
            device_vsi = Vsi(
                router=router_device,
                VSI_Name=vsi['VSI Name'],
                PW_Signaling=vsi['PW Signaling'],
                VSI_State=vsi['VSI State'],
                VSI_ID=vsi['VSI ID'],
                Interface_Name=vsi['Interface Name'],
                Interface_State=vsi['Interface State'],
                Ac_Block_State=vsi['Ac Block State']
            )
            session.add(device_vsi)

        vsi_peer_str = data_dict['vsi_peer'].replace("'", "\"")
        vsi_peer_list = json.loads(vsi_peer_str)

        for vsi_peer in vsi_peer_list:
            device_vsi_peer = Vsi_peer(
                router=router_device,
                VSI_Name=vsi_peer['VSI Name'],
                PW_Signaling=vsi_peer['PW Signaling'],
                VSI_State=vsi_peer['VSI State'],
                VSI_ID=vsi_peer['VSI ID'],
                Peer_Ip_Address=vsi_peer['Peer Ip Address'],
                PW_Last_Up_Time=vsi_peer['PW Last Up Time']
            )
            session.add(device_vsi_peer)

        session.commit()


if __name__ == '__main__':
    if check_expiration():
        main()
