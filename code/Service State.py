import os
from tkinter import Tk, filedialog
import re
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.utils.dataframe import dataframe_to_rows
from textfsm import TextFSM
import datetime
from pprint import pprint
import codecs


import datetime

# 检查程序是否过期


def check_expiration():
    expiration_date = datetime.datetime(2024, 3, 1)

    # 获取当前日期
    current_date = datetime.datetime.now()

    # 如果当前日期在指定日期之后，禁止执行程序
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
            data = {"Device name": "", "Device ip": "", "VSI Name": "N/A", "PW Signaling": "N/A", "VSI State": "N/A",
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
                        data["Export"] = field_value
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
            # print(entry)
            if not entry.strip():
                continue
            data = {"Device name": "", "Device ip": "", "Interface": "N/A", "AC status": "N/A", "VC State": "N/A",
                    "VC ID": "N/A", "VC Type": "N/A", "session state": "N/A", "Destination": "N/A", "link state": "N/A"}
            lines = entry.split("\n")
            # print(lines)
            for line in lines:
                parts = line.split(" : ")
                if len(parts) == 2:
                    field_name = parts[0].strip()
                    field_value = parts[1].strip()
                    if field_name == "Client Interface":
                        data["Interface"] = field_value
                    elif field_name == "AC status":
                        data["AC status"] = field_value
                    elif field_name == "VC State":
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
            # print(table_data)
        return table_data


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
            data = {"Device name": "", "Device ip": "", "VSI Name": "N/A", "PW Signaling": "N/A", "VSI State": "N/A",
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
                        data["Export"] = field_value
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
    for device_name, data in paragraph.items():
        # print(device_name)
        if data is not None:
            with open(f'display_interface.template') as f:
                template = TextFSM(f)
                # print(template)
            parsed_data = re.split(r'\n\n+', data)
            for entrys in parsed_data:
                # print(entrys)
                interface_data = template.ParseText(entrys)
                # print(interface_data)
                # print(interface_data)
                for entry in interface_data:
                    data_list_interface.append([device_name] + entry)
    # pprint(data_list_interface)
    return data_list_interface

def get_table_data_info(raw_result):
    arp_info = []
    with open(f'display_arp.template') as f:
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
        with open(f'display_lldp_neighbor.template', encoding='utf-8') as f:        
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
    with open(f'display_bgp.template') as f:        
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
    data_list_interface = []  # 添加这一行
    data_list_peer = []
    data_list_port = []
    data_list_l2vc = []
    data_list_arp = []
    data_list_lldp = []
    data_list_bgp = []
    try:
        with codecs.open(filename, 'r', encoding='utf-16') as file:
            file_data = file.read()
            print(file_data)
    except UnicodeError:
        with codecs.open(filename, 'r', encoding='utf-8') as file:
            file_data = file.read()
            device_interface = {}
            device_interface_description = {}
            device_arp = {}
            device_name, device_ip = get_device_info(file_data)
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
            # print(paragraph_lldp)

            device_interface[device_name] = paragraph_interface
            # print(device_arp)

        if paragraph_vsi is not None:
            data_list_peer = get_table_data(paragraph_vsi)
            for data in data_list_peer:
                data["Device name"] = device_name
                data["Device ip"] = device_ip

        if paragraph_l2vc is not None:
            data_list_l2vc = get_table_data_l2vc(paragraph_l2vc)
            for data in data_list_l2vc:
                data["Device name"] = device_name
                data["Device ip"] = device_ip

        if paragraph_l2vc is not None:
            data_list_port = get_table_data_port(paragraph_vsi)
            for data in data_list_port:
                data["Device name"] = device_name
                data["Device ip"] = device_ip

        if paragraph_l2vc is not None:
            data_list_port = get_table_data_port(paragraph_vsi)
            for data in data_list_port:
                data["Device name"] = device_name
                data["Device ip"] = device_ip

        if paragraph_arp is not None:
            data_list_arp = get_table_data_info(paragraph_arp)
            # print(data_list_arp)
            for data in data_list_arp:                
                data.insert(0, device_name)
                data.insert(1, device_ip)

        data_list_interface = get_table_data_interface(device_interface)

        if paragraph_lldp is not None:
            data_list_lldp = get_table_lldp(paragraph_lldp)
            # print(data_list_arp)
            for data in data_list_lldp:
                data[1], data[2] = data[2], data[1]                
                data.insert(0, device_name)
                data.insert(1, device_ip) 

        if paragraph_arp is not None:
            data_list_bgp = get_table_bgp(paragraph_bgp)
            # print(data_list_arp)
            for data in data_list_bgp:                
                data.insert(0, device_name)
                data.insert(1, device_ip)

        # pprint(data_list_lldp)
        return data_list_peer, data_list_port, data_list_l2vc, data_list_interface, data_list_arp, data_list_lldp, data_list_bgp

def get_folder_path():
    root = Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory(title="Select Folder")
    return folder_path

def main():
    folder_path = get_folder_path()
    # script_path = '.'  # replace with your script path
    table_header_port = ["Device name", "Device ip", "VSI Name", "PW Signaling",
                         "VSI State", "VSI ID", "Interface Name", "Interface State", "Ac Block State"]
    table_data_port = []

    table_header_l2vc = ["Device name", "Device ip", "Interface", "AC status", "VC State",
                         "VC ID", "VC Type", "session state", "Destination", "link state"]
    table_data_l2vc = []

    table_header = ["Device name", "Device ip", "VSI Name", "PW Signaling",
                    "VSI State", "VSI ID", "Peer Ip Address", "PW Last Up Time"]
    table_data = []

    table_header_interface = ["Device name", "Interface", "Physical State",
                              "Protocol State", "Description", "ip_address", "Port_bw", "Port_max_bw", "Transceiver Mode", "WaveLength", "Transmission Distance",
                              "Rx Power", "Tx Power", "Last physical down time", "Input bandwidth", "Output bandwidth"]
    table_data_interface = []

    table_header_arp = ["Device name", "Device ip", "IP ADDRESS", "MAC ADDRESS",
                    "EXPIRE", "TYPE", "INTERFACE", "VPN-INSTANCE"]
    table_data_arp = []

    table_header_lldp = ["Device name", "Device ip", "Local_Port", "Peer_Device",
                    "Peer_Port"]
    table_data_lldp = []

    table_header_bgp = ["Device name", "Device ip", "peer", "version", "AS number",
                    "status"]
    table_data_bgp = []

    # script_path = os.getcwd()
    files = get_all_files(folder_path)
    # print(files)
    for filename in files:
        # print(filename)
        data_list_peer, data_list_port, data_list_l2vc, data_list_interface, data_list_arp, data_list_lldp, data_list_bgp = process_file(
            filename)
        # print(data_list_arp)
        if data_list_peer is not None:
            table_data.extend(data_list_peer)
        if data_list_port is not None:
            table_data_port.extend(data_list_port)
        if data_list_l2vc is not None:
            table_data_l2vc.extend(data_list_l2vc)
        if data_list_interface is not None:
            table_data_interface.extend(data_list_interface)
        if data_list_arp is not None:
            table_data_arp.extend(data_list_arp)
        if data_list_lldp is not None:
            table_data_lldp.extend(data_list_lldp)
        if data_list_bgp is not None:
            table_data_bgp.extend(data_list_bgp)            
    # pprint(table_data_interface)
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d')
    # print(nowTime)

    df1 = pd.DataFrame(table_data, columns=table_header)
    df2 = pd.DataFrame(table_data_port, columns=table_header_port)
    df3 = pd.DataFrame(table_data_l2vc, columns=table_header_l2vc)
    df4 = pd.DataFrame(table_data_interface, columns=table_header_interface)
    df5 = pd.DataFrame(table_data_arp, columns=table_header_arp)
    df6 = pd.DataFrame(table_data_lldp, columns=table_header_lldp)
    df7 = pd.DataFrame(table_data_bgp, columns=table_header_bgp)    
    # print(df6)

    excel_file = os.path.join(folder_path, f'VSI and L2vc State {nowTime}.xlsx')
    with pd.ExcelWriter(excel_file) as writer:
        df1.to_excel(writer, sheet_name='Vsi peer status', index=False)
        df2.to_excel(writer, sheet_name='Vsi Interface status', index=False)
        df3.to_excel(writer, sheet_name='L2vc status', index=False)
        df4.to_excel(writer, sheet_name='interface status', index=False)
        df5.to_excel(writer, sheet_name='arp status', index=False)
        df6.to_excel(writer, sheet_name='lldp status', index=False)
        df7.to_excel(writer, sheet_name='bgp status', index=False)

if __name__ == '__main__':
    if check_expiration():
        main()
